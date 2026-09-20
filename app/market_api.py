import hashlib
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Header, HTTPException, Request

from .auth import validate_init_data
from .catalog import CATALOG
from .db import upsert_user, get_user_by_ref_code
from .storage import conn, is_postgres, INTEGRITY_ERRORS

router = APIRouter()

SQLITE_MARKET_SCHEMA = """
CREATE TABLE IF NOT EXISTS market_listings (
    id TEXT PRIMARY KEY,
    item_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    mode TEXT NOT NULL DEFAULT 'trade',
    ask_stars INTEGER,
    want_character_id TEXT,
    want_rarity TEXT,
    note TEXT,
    fee_bps INTEGER,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    closed_at TEXT,
    FOREIGN KEY(item_id) REFERENCES owned_items(id),
    FOREIGN KEY(seller_id) REFERENCES users(telegram_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_market_one_active_listing_per_item
ON market_listings(item_id) WHERE status='active';

CREATE INDEX IF NOT EXISTS idx_market_active_created
ON market_listings(status, created_at DESC);

CREATE TABLE IF NOT EXISTS market_offers (
    id TEXT PRIMARY KEY,
    listing_id TEXT NOT NULL,
    offerer_id INTEGER NOT NULL,
    offered_item_id INTEGER,
    topup_stars INTEGER NOT NULL DEFAULT 0,
    note TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL,
    closed_at TEXT,
    FOREIGN KEY(listing_id) REFERENCES market_listings(id),
    FOREIGN KEY(offerer_id) REFERENCES users(telegram_id),
    FOREIGN KEY(offered_item_id) REFERENCES owned_items(id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_market_one_pending_offer_per_item
ON market_offers(offered_item_id) WHERE status='pending' AND offered_item_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_market_offer_listing
ON market_offers(listing_id, status, created_at DESC);
"""

POSTGRES_MARKET_SCHEMA = """
CREATE TABLE IF NOT EXISTS market_listings (
    id TEXT PRIMARY KEY,
    item_id BIGINT NOT NULL,
    seller_id BIGINT NOT NULL,
    mode TEXT NOT NULL DEFAULT 'trade',
    ask_stars INTEGER,
    want_character_id TEXT,
    want_rarity TEXT,
    note TEXT,
    fee_bps INTEGER,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    closed_at TEXT,
    FOREIGN KEY(item_id) REFERENCES owned_items(id),
    FOREIGN KEY(seller_id) REFERENCES users(telegram_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_market_one_active_listing_per_item
ON market_listings(item_id) WHERE status='active';

CREATE INDEX IF NOT EXISTS idx_market_active_created
ON market_listings(status, created_at DESC);

CREATE TABLE IF NOT EXISTS market_offers (
    id TEXT PRIMARY KEY,
    listing_id TEXT NOT NULL,
    offerer_id BIGINT NOT NULL,
    offered_item_id BIGINT,
    topup_stars INTEGER NOT NULL DEFAULT 0,
    note TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL,
    closed_at TEXT,
    FOREIGN KEY(listing_id) REFERENCES market_listings(id),
    FOREIGN KEY(offerer_id) REFERENCES users(telegram_id),
    FOREIGN KEY(offered_item_id) REFERENCES owned_items(id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_market_one_pending_offer_per_item
ON market_offers(offered_item_id) WHERE status='pending' AND offered_item_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_market_offer_listing
ON market_offers(listing_id, status, created_at DESC);
"""


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def init_market():
    with conn() as c:
        c.executescript(POSTGRES_MARKET_SCHEMA if is_postgres() else SQLITE_MARKET_SCHEMA)
        # Backfill mint provenance for legacy items. The operation is idempotent.
        if is_postgres():
            c.execute(
                """INSERT INTO ownership_events(
                       item_id, from_user_id, to_user_id, event_type, reference_id, event_key, created_at
                   )
                   SELECT id, NULL, telegram_id, 'mint', purchase_id, 'mint:' || id::text, acquired_at
                   FROM owned_items
                   ON CONFLICT(event_key) DO NOTHING"""
            )
        else:
            c.execute(
                """INSERT OR IGNORE INTO ownership_events(
                       item_id, from_user_id, to_user_id, event_type, reference_id, event_key, created_at
                   )
                   SELECT id, NULL, telegram_id, 'mint', purchase_id, 'mint:' || id, acquired_at
                   FROM owned_items"""
            )


def auth_user(init_data: str | None):
    try:
        payload = validate_init_data(init_data or "")
        u = payload["user"]
        start = payload.get("start_param")
        referrer_id = None
        if start and start.startswith("ref_"):
            code = start.split("_", 1)[1].strip()
            ref = get_user_by_ref_code(code)
            referrer_id = int(ref["telegram_id"]) if ref else None
        tid = int(u["id"])
        upsert_user(tid, u.get("username"), u.get("first_name"), referrer_id)
        return tid
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


def catalog_map():
    return {c["id"]: c for c in CATALOG}


def _owned_for_update(c, item_id: int):
    sql = "SELECT * FROM owned_items WHERE id=?" + (" FOR UPDATE" if is_postgres() else "")
    return c.execute(sql, (item_id,)).fetchone()


def _listing_for_update(c, listing_id: str):
    sql = "SELECT * FROM market_listings WHERE id=?" + (" FOR UPDATE" if is_postgres() else "")
    return c.execute(sql, (listing_id,)).fetchone()


def _offer_for_update(c, offer_id: str):
    sql = "SELECT * FROM market_offers WHERE id=?" + (" FOR UPDATE" if is_postgres() else "")
    return c.execute(sql, (offer_id,)).fetchone()


def _matches_listing(listing, offered_item) -> bool:
    if not listing or not offered_item:
        return False
    wanted_character = listing["want_character_id"]
    if wanted_character:
        return offered_item["character_id"] == wanted_character
    wanted_rarity = listing["want_rarity"]
    if wanted_rarity:
        ch = catalog_map().get(offered_item["character_id"])
        return bool(ch and ch.get("rarity") == wanted_rarity)
    return True


def collector_label(c, telegram_id: int) -> str:
    row = c.execute("SELECT ref_code FROM users WHERE telegram_id=?", (telegram_id,)).fetchone()
    code = row["ref_code"] if row and row["ref_code"] else None
    if code:
        return f"Collector {str(code)[:6].upper()}"
    digest = hashlib.sha256(f"drop1:{telegram_id}".encode()).hexdigest()[:6].upper()
    return f"Collector {digest}"


def public_item(row, cmap=None):
    cmap = cmap or catalog_map()
    c = cmap.get(row["character_id"], {})
    return {
        "item_id": row["id"],
        "character_id": row["character_id"],
        "name": c.get("name", row["character_id"]),
        "rarity": c.get("rarity", "unknown"),
        "emoji": c.get("emoji", "◉"),
        "power": c.get("power", 0),
        "luck": c.get("luck", 0),
        "set": c.get("set", ""),
        "serial_no": row["serial_no"],
        "acquired_at": row["acquired_at"],
    }


def _listing_payload(c, row, cmap, viewer_id=None):
    item = c.execute("SELECT * FROM owned_items WHERE id=?", (row["item_id"],)).fetchone()
    return {
        "id": row["id"],
        "mode": row["mode"],
        "ask_stars": row["ask_stars"],
        "want_character_id": row["want_character_id"],
        "want_rarity": row["want_rarity"],
        "note": row["note"],
        "status": row["status"],
        "created_at": row["created_at"],
        "seller": {
            "label": "You" if viewer_id == row["seller_id"] else collector_label(c, row["seller_id"]),
            "is_mine": bool(viewer_id == row["seller_id"]),
        },
        "item": public_item(item, cmap) if item else None,
    }


def _offer_payload(c, row, cmap, viewer_id=None):
    offered = c.execute(
        "SELECT * FROM owned_items WHERE id=?",
        (row["offered_item_id"],)
    ).fetchone() if row["offered_item_id"] else None
    return {
        "id": row["id"],
        "listing_id": row["listing_id"],
        "offerer": {
            "label": "You" if viewer_id == row["offerer_id"] else collector_label(c, row["offerer_id"]),
            "is_mine": bool(viewer_id == row["offerer_id"]),
        },
        "offered_item": public_item(offered, cmap) if offered else None,
        "topup_stars": row["topup_stars"],
        "note": row["note"],
        "status": row["status"],
        "created_at": row["created_at"],
    }


@router.get("/api/market")
async def market_feed(limit: int = 50, x_telegram_init_data: str | None = Header(default=None)):
    tid = auth_user(x_telegram_init_data)
    limit = max(1, min(100, limit))
    cmap = catalog_map()
    with conn() as c:
        rows = c.execute(
            "SELECT * FROM market_listings WHERE status='active' ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return {
            "listings": [_listing_payload(c, row, cmap, tid) for row in rows],
            "resale_enabled": False,
            "trade_enabled": True,
        }


@router.get("/api/market/my")
async def my_market(x_telegram_init_data: str | None = Header(default=None)):
    tid = auth_user(x_telegram_init_data)
    cmap = catalog_map()
    with conn() as c:
        listings = c.execute(
            "SELECT * FROM market_listings WHERE seller_id=? ORDER BY created_at DESC LIMIT 100",
            (tid,),
        ).fetchall()
        received = c.execute(
            """SELECT o.* FROM market_offers o
               JOIN market_listings l ON l.id=o.listing_id
               WHERE l.seller_id=? AND o.status='pending'
               ORDER BY o.created_at DESC LIMIT 100""",
            (tid,),
        ).fetchall()
        sent = c.execute(
            "SELECT * FROM market_offers WHERE offerer_id=? ORDER BY created_at DESC LIMIT 100",
            (tid,),
        ).fetchall()
        return {
            "listings": [_listing_payload(c, row, cmap, tid) for row in listings],
            "received_offers": [_offer_payload(c, row, cmap, tid) for row in received],
            "sent_offers": [_offer_payload(c, row, cmap, tid) for row in sent],
        }


@router.post("/api/market/listings")
async def create_listing(request: Request, x_telegram_init_data: str | None = Header(default=None)):
    tid = auth_user(x_telegram_init_data)
    body = await request.json()
    try:
        item_id = int(body.get("item_id"))
    except Exception:
        raise HTTPException(status_code=400, detail="item_id is required")

    mode = (body.get("mode") or "trade").strip().lower()
    if mode != "trade":
        raise HTTPException(status_code=409, detail="Paid resale is not enabled yet")

    want_character_id = (body.get("want_character_id") or "").strip() or None
    want_rarity = (body.get("want_rarity") or "").strip().lower() or None
    note = (body.get("note") or "").strip()[:180] or None
    if want_rarity and want_rarity not in {"common", "rare", "epic", "legendary", "mythic"}:
        raise HTTPException(status_code=400, detail="Unknown rarity")
    if want_character_id and want_character_id not in catalog_map():
        raise HTTPException(status_code=400, detail="Unknown character")
    if want_character_id:
        want_rarity = None

    listing_id = "lst_" + uuid.uuid4().hex
    now = utcnow()
    try:
        with conn() as c:
            c.execute("BEGIN IMMEDIATE")
            item = _owned_for_update(c, item_id)
            if not item or item["telegram_id"] != tid:
                raise HTTPException(status_code=404, detail="You do not own this creature")
            existing_offer = c.execute(
                "SELECT 1 FROM market_offers WHERE offered_item_id=? AND status='pending'",
                (item_id,),
            ).fetchone()
            if existing_offer:
                raise HTTPException(status_code=409, detail="This creature is already locked in an offer")
            c.execute(
                """INSERT INTO market_listings(
                       id,item_id,seller_id,mode,ask_stars,want_character_id,want_rarity,note,fee_bps,status,created_at
                   ) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (listing_id, item_id, tid, "trade", None, want_character_id, want_rarity, note, None, "active", now),
            )
    except INTEGRITY_ERRORS:
        raise HTTPException(status_code=409, detail="This creature is already listed")

    return {"ok": True, "listing_id": listing_id}


@router.post("/api/market/listings/{listing_id}/cancel")
async def cancel_listing(listing_id: str, x_telegram_init_data: str | None = Header(default=None)):
    tid = auth_user(x_telegram_init_data)
    now = utcnow()
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        row = _listing_for_update(c, listing_id)
        if not row or row["seller_id"] != tid:
            raise HTTPException(status_code=404, detail="Listing not found")
        if row["status"] != "active":
            raise HTTPException(status_code=409, detail="Listing is already closed")
        c.execute("UPDATE market_listings SET status='cancelled',closed_at=? WHERE id=?", (now, listing_id))
        c.execute("UPDATE market_offers SET status='cancelled',closed_at=? WHERE listing_id=? AND status='pending'", (now, listing_id))
    return {"ok": True}


@router.post("/api/market/listings/{listing_id}/offers")
async def create_offer(listing_id: str, request: Request, x_telegram_init_data: str | None = Header(default=None)):
    tid = auth_user(x_telegram_init_data)
    body = await request.json()
    try:
        offered_item_id = int(body.get("offered_item_id"))
    except Exception:
        raise HTTPException(status_code=400, detail="offered_item_id is required")
    note = (body.get("note") or "").strip()[:180] or None
    offer_id = "off_" + uuid.uuid4().hex
    now = utcnow()

    try:
        with conn() as c:
            c.execute("BEGIN IMMEDIATE")
            listing = _listing_for_update(c, listing_id)
            if not listing or listing["status"] != "active":
                raise HTTPException(status_code=404, detail="Listing is not active")
            if listing["seller_id"] == tid:
                raise HTTPException(status_code=409, detail="You cannot offer on your own listing")
            offered = _owned_for_update(c, offered_item_id)
            if not offered or offered["telegram_id"] != tid:
                raise HTTPException(status_code=404, detail="You do not own the offered creature")
            listed_elsewhere = c.execute(
                "SELECT 1 FROM market_listings WHERE item_id=? AND status='active'",
                (offered_item_id,),
            ).fetchone()
            if listed_elsewhere:
                raise HTTPException(status_code=409, detail="Offered creature is already listed")
            if not _matches_listing(listing, offered):
                wanted = listing["want_character_id"] or listing["want_rarity"] or "requested target"
                raise HTTPException(status_code=409, detail=f"This listing only accepts {wanted}")
            c.execute(
                """INSERT INTO market_offers(
                       id,listing_id,offerer_id,offered_item_id,topup_stars,note,status,created_at
                   ) VALUES (?,?,?,?,?,?,?,?)""",
                (offer_id, listing_id, tid, offered_item_id, 0, note, "pending", now),
            )
    except INTEGRITY_ERRORS:
        raise HTTPException(status_code=409, detail="This creature is already locked in another offer")

    return {"ok": True, "offer_id": offer_id}


@router.post("/api/market/offers/{offer_id}/reject")
async def reject_offer(offer_id: str, x_telegram_init_data: str | None = Header(default=None)):
    tid = auth_user(x_telegram_init_data)
    now = utcnow()
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        sql = """SELECT o.*, l.seller_id FROM market_offers o
                 JOIN market_listings l ON l.id=o.listing_id WHERE o.id=?""" + (" FOR UPDATE OF o" if is_postgres() else "")
        row = c.execute(sql, (offer_id,)).fetchone()
        if not row or row["seller_id"] != tid:
            raise HTTPException(status_code=404, detail="Offer not found")
        if row["status"] != "pending":
            raise HTTPException(status_code=409, detail="Offer is already closed")
        c.execute("UPDATE market_offers SET status='rejected',closed_at=? WHERE id=?", (now, offer_id))
    return {"ok": True}


@router.post("/api/market/offers/{offer_id}/withdraw")
async def withdraw_offer(offer_id: str, x_telegram_init_data: str | None = Header(default=None)):
    tid = auth_user(x_telegram_init_data)
    now = utcnow()
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        row = _offer_for_update(c, offer_id)
        if not row or row["offerer_id"] != tid:
            raise HTTPException(status_code=404, detail="Offer not found")
        if row["status"] != "pending":
            raise HTTPException(status_code=409, detail="Offer is already closed")
        c.execute("UPDATE market_offers SET status='withdrawn',closed_at=? WHERE id=?", (now, offer_id))
    return {"ok": True}


@router.post("/api/market/offers/{offer_id}/accept")
async def accept_offer(offer_id: str, x_telegram_init_data: str | None = Header(default=None)):
    seller_id = auth_user(x_telegram_init_data)
    now = utcnow()
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        offer_sql = "SELECT * FROM market_offers WHERE id=?" + (" FOR UPDATE" if is_postgres() else "")
        offer = c.execute(offer_sql, (offer_id,)).fetchone()
        if not offer or offer["status"] != "pending":
            raise HTTPException(status_code=404, detail="Offer is not active")
        listing_sql = "SELECT * FROM market_listings WHERE id=?" + (" FOR UPDATE" if is_postgres() else "")
        listing = c.execute(listing_sql, (offer["listing_id"],)).fetchone()
        if not listing or listing["status"] != "active" or listing["seller_id"] != seller_id:
            raise HTTPException(status_code=404, detail="Listing is not active")
        if listing["mode"] != "trade" or not offer["offered_item_id"]:
            raise HTTPException(status_code=409, detail="Unsupported offer type")

        item_sql = "SELECT * FROM owned_items WHERE id=?" + (" FOR UPDATE" if is_postgres() else "")
        seller_item = c.execute(item_sql, (listing["item_id"],)).fetchone()
        buyer_item = c.execute(item_sql, (offer["offered_item_id"],)).fetchone()
        if not seller_item or seller_item["telegram_id"] != seller_id:
            raise HTTPException(status_code=409, detail="Seller no longer owns the listed creature")
        if not buyer_item or buyer_item["telegram_id"] != offer["offerer_id"]:
            raise HTTPException(status_code=409, detail="Offerer no longer owns the offered creature")
        if not _matches_listing(listing, buyer_item):
            raise HTTPException(status_code=409, detail="Offered creature no longer matches this listing")

        c.execute("UPDATE owned_items SET telegram_id=? WHERE id=?", (offer["offerer_id"], seller_item["id"]))
        c.execute("UPDATE owned_items SET telegram_id=? WHERE id=?", (seller_id, buyer_item["id"]))

        c.execute(
            """INSERT INTO ownership_events(item_id,from_user_id,to_user_id,event_type,reference_id,event_key,created_at)
               VALUES (?,?,?,?,?,?,?)""",
            (seller_item["id"], seller_id, offer["offerer_id"], "trade", offer_id, f"trade:{offer_id}:{seller_item['id']}", now),
        )
        c.execute(
            """INSERT INTO ownership_events(item_id,from_user_id,to_user_id,event_type,reference_id,event_key,created_at)
               VALUES (?,?,?,?,?,?,?)""",
            (buyer_item["id"], offer["offerer_id"], seller_id, "trade", offer_id, f"trade:{offer_id}:{buyer_item['id']}", now),
        )

        c.execute("UPDATE market_offers SET status='accepted',closed_at=? WHERE id=?", (now, offer_id))
        c.execute(
            "UPDATE market_offers SET status='rejected',closed_at=? WHERE listing_id=? AND id<>? AND status='pending'",
            (now, listing["id"], offer_id)
        )
        c.execute("UPDATE market_listings SET status='completed',closed_at=? WHERE id=?", (now, listing["id"]))
        c.execute(
            "UPDATE market_listings SET status='cancelled',closed_at=? WHERE item_id=? AND status='active'",
            (now, buyer_item["id"])
        )

    return {"ok": True, "trade_id": offer_id}


@router.get("/api/items/{item_id}/provenance")
async def item_provenance(item_id: int):
    cmap = catalog_map()
    with conn() as c:
        item = c.execute("SELECT * FROM owned_items WHERE id=?", (item_id,)).fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Creature not found")
        events = c.execute(
            "SELECT event_type, created_at FROM ownership_events WHERE item_id=? ORDER BY id ASC",
            (item_id,),
        ).fetchall()
        history = [{"event_type": e["event_type"], "created_at": e["created_at"]} for e in events]
        return {
            "item": public_item(item, cmap),
            "minted_at": history[0]["created_at"] if history else item["acquired_at"],
            "trade_count": sum(1 for e in history if e["event_type"] == "trade"),
            "history": history,
        }
