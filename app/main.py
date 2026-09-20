import os, uuid, secrets, hashlib
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

from .auth import validate_init_data
from .catalog import CATALOG
from .db import (
    init_db, upsert_user, get_user, get_user_by_ref_code, reserve_purchase, cancel_purchase, get_purchase,
    purchase_reservation_valid, mark_paid_and_mint, mark_test_and_mint, collection,
    leaderboard, daily_pool_status, track_event, retention_state,
    claim_daily_reward, claim_daily_mission, claim_collection_milestone,
    spend_research_scout
)
from .telegram import create_drop_invoice, answer_precheckout, send_message, setup_bot
from .market_api import router as market_router, init_market
from .storage import database_backend

DROP_PRICE_STARS = int(os.getenv("DROP_PRICE_STARS", "50"))
FREE_TEST_MODE = os.getenv("FREE_TEST_MODE", "false").lower() == "true"
BOT_USERNAME = os.getenv("BOT_USERNAME", "")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
SUPPORT_HANDLE = os.getenv("SUPPORT_HANDLE", "")

DAILY_POOL_BASE = int(os.getenv("DAILY_POOL_BASE", "200"))
DAILY_POOL_USERS_PER_UNLOCK = int(os.getenv("DAILY_POOL_USERS_PER_UNLOCK", "10"))
DAILY_POOL_DROPS_PER_UNLOCK = int(os.getenv("DAILY_POOL_DROPS_PER_UNLOCK", "3"))
DAILY_POOL_MAX = int(os.getenv("DAILY_POOL_MAX", "300"))
GENESIS_SUPPLY = int(os.getenv("GENESIS_SUPPLY", "100000"))

APP_VERSION = "0.12.0-release-candidate"

app = FastAPI(title="DROP1")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(market_router)

@app.middleware("http")
async def beta_no_cache(request: Request, call_next):
    response = await call_next(request)
    path = request.url.path
    volatile_js = path.endswith("/art.js") or path.endswith("/hatch_canvas_v22.js")
    if path == "/" or path.endswith(".html") or volatile_js:
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    elif path.startswith("/static/vendor/") or path.startswith("/static/models/"):
        response.headers["Cache-Control"] = "public, max-age=604800, immutable"
    elif path.startswith("/static/assets/"):
        response.headers["Cache-Control"] = "public, max-age=86400"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["X-DNS-Prefetch-Control"] = "off"
    return response

@app.on_event("startup")
async def startup():
    init_db()
    init_market()
    try:
        await setup_bot(os.getenv("BASE_URL", ""), WEBHOOK_SECRET)
    except Exception as e:
        print(f"Telegram setup skipped/failed: {e}")

def persistent_storage_ready():
    return database_backend() == "postgres" or not os.getenv("DATABASE_PATH", "/tmp/drop1.db").startswith("/tmp/")


def pool_status():
    return daily_pool_status(
        DAILY_POOL_BASE,
        DAILY_POOL_USERS_PER_UNLOCK,
        DAILY_POOL_DROPS_PER_UNLOCK,
        DAILY_POOL_MAX,
        include_test=True,
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
        return tid, payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def public_character(c):
    return {k: v for k, v in c.items() if k != "weight"}


def public_collector_label(telegram_id: int, ref_code: str | None = None) -> str:
    if ref_code:
        return f"Collector {str(ref_code)[:6].upper()}"
    digest = hashlib.sha256(f"drop1:{telegram_id}".encode()).hexdigest()[:6].upper()
    return f"Collector {digest}"

def choose_character():
    total = sum(c["weight"] for c in CATALOG)
    n = secrets.randbelow(total)
    cursor = 0
    for c in CATALOG:
        cursor += c["weight"]
        if n < cursor:
            return c
    return CATALOG[-1]

@app.head("/")
async def home_head():
    return HTMLResponse("", status_code=200)


@app.get("/")
async def home():
    return FileResponse("app/static/index.html", headers={"Cache-Control":"no-store, no-cache, must-revalidate, max-age=0","Pragma":"no-cache","Expires":"0"})

@app.get("/ios-canvas-22")
async def ios_canvas_22():
    return FileResponse("app/static/index.html", headers={
        "Cache-Control":"no-store, no-cache, must-revalidate, max-age=0",
        "Pragma":"no-cache",
        "Expires":"0",
        "X-DROP1-Build":"ios-canvas-22",
    })

@app.get("/health")
async def health():
    return {
        "ok": True,
        "bot_configured": bool(os.getenv("BOT_TOKEN")),
        "free_test_mode": FREE_TEST_MODE,
        "pool": pool_status(),
        "trade_market": True,
        "paid_resale": False,
        "version": APP_VERSION,
        "stage": "closed_beta",
        "storage": database_backend(),
        "persistent_storage": persistent_storage_ready(),
        "paid_launch_ready": bool(os.getenv("BOT_TOKEN")) and persistent_storage_ready() and not FREE_TEST_MODE,
        "launch_blockers": [
            blocker for blocker, blocked in [
                ("free_test_mode_enabled", FREE_TEST_MODE),
                ("persistent_storage_missing", not persistent_storage_ready()),
                ("bot_token_missing", not bool(os.getenv("BOT_TOKEN"))),
            ] if blocked
        ],
        "flagship_3d": True,
        "daily_expedition": True,
        "research_scout": True,
    }

@app.get("/odds", response_class=HTMLResponse)
async def odds_page():
    return """<!doctype html><html><meta name="viewport" content="width=device-width,initial-scale=1"><body style="font-family:-apple-system,Arial;max-width:680px;margin:40px auto;padding:0 18px;line-height:1.55"><h1>DROP1 — Primal Hatch Odds</h1><p>Every paid egg hatches exactly one digital creature.</p><ul><li>Common — 65.0%</li><li>Rare — 25.0%</li><li>Epic — 8.0%</li><li>Legendary — 1.8%</li><li>Mythic — 0.2%</li></ul><p>Creatures do not represent money, securities, or a promise of resale value. There is no cash-out.</p></body></html>"""

@app.get("/terms", response_class=HTMLResponse)
async def terms_page():
    support = SUPPORT_HANDLE or "the support contact shown in the bot"
    return f"""<!doctype html><html><meta name="viewport" content="width=device-width,initial-scale=1"><body style="font-family:-apple-system,Arial;max-width:680px;margin:40px auto;padding:0 18px;line-height:1.55"><h1>DROP1 Terms — MVP</h1><p>DROP1 sells digital creature hatches inside Telegram using Telegram Stars. Each purchase guarantees one digital creature. The creature received is randomly selected according to the published Primal Hatch odds.</p><p>DROP1 creatures have no guaranteed monetary value, no cash-out, and no promise of appreciation.</p><p>A beta creature-for-creature trade board may allow owners to voluntarily exchange creatures. DROP1 does not set or guarantee a market value. Paid user-to-user resale is not enabled in this MVP.</p><p>Daily DROP availability is limited by the currently unlocked global pool and may sell out before the daily reset.</p><p>Payments are fulfilled only after Telegram confirms a successful payment. For purchase support, contact {support}.</p></body></html>"""

@app.get("/privacy", response_class=HTMLResponse)
async def privacy_page():
    return """<!doctype html><html><meta name="viewport" content="width=device-width,initial-scale=1"><body style="font-family:-apple-system,Arial;max-width:680px;margin:40px auto;padding:0 18px;line-height:1.55"><h1>DROP1 Privacy — MVP</h1><p>The service stores the Telegram account identifier and basic Telegram profile data needed to operate the collection, purchases, referrals, XP, trade offers and support.</p><p>Payment identifiers are stored to reconcile purchases and handle refunds or disputes. Ownership-transfer history is stored to preserve creature provenance.</p></body></html>"""


@app.post("/api/events")
async def product_event(request: Request, x_telegram_init_data: str | None = Header(default=None)):
    tid, _ = auth_user(x_telegram_init_data)
    try:
        body = await request.json()
    except Exception:
        body = {}
    event_name = str(body.get("event") or "").strip().lower()
    allowed = {
        "app_open","hatch_click","hatch_complete","specimen_open","market_open",
        "listing_create","offer_create","share_click","physical_interest",
        "daily_claim","mission_claim","milestone_claim","research_scout"
    }
    if event_name not in allowed:
        raise HTTPException(status_code=400, detail="Unknown event")
    item_id = body.get("item_id")
    try:
        item_id = int(item_id) if item_id is not None else None
    except Exception:
        item_id = None
    track_event(
        tid,
        event_name,
        item_id=item_id,
        character_id=str(body.get("character_id") or "")[:32] or None,
        source=str(body.get("source") or "")[:64] or None,
        metadata=str(body.get("metadata") or "")[:500] or None,
    )
    return {"ok": True}

@app.get("/api/bootstrap")
async def bootstrap(x_telegram_init_data: str | None = Header(default=None)):
    tid, _ = auth_user(x_telegram_init_data)
    u = get_user(tid)
    items = []
    by_id = {c["id"]: c for c in CATALOG}
    for row in collection(tid):
        c = by_id[row["character_id"]]
        items.append({
            **public_character(c),
            "item_id": row["id"],
            "serial_no": row["serial_no"],
            "acquired_at": row["acquired_at"],
        })
    owned_species = {i["id"] for i in items}
    unique = len(owned_species)
    set_order = []
    set_map = {}
    for ch in CATALOG:
        name = ch.get("set") or "Primal Hatch"
        if name not in set_map:
            set_map[name] = {"name": name, "rarity": ch.get("rarity","common"), "total": 0, "owned": 0}
            set_order.append(name)
        set_map[name]["total"] += 1
        if ch["id"] in owned_species:
            set_map[name]["owned"] += 1
    season_sets = [set_map[name] for name in set_order]
    retention = retention_state(tid)
    if retention.get("scout_target_id"):
        target = by_id.get(retention["scout_target_id"])
        retention["scout_target"] = public_character(target) if target else None
    else:
        retention["scout_target"] = None
    return {
        "user": {
            "id": tid,
            "username": u["username"],
            "first_name": u["first_name"],
            "xp": u["xp"],
            "dust": u["dust"],
        },
        "price_stars": DROP_PRICE_STARS,
        "test_mode": FREE_TEST_MODE,
        "catalog_total": len(CATALOG),
        "catalog": [public_character(c) for c in CATALOG],
        "collection": items,
        "unique_count": unique,
        "season_sets": season_sets,
        "pool": pool_status(),
        "genesis_supply": GENESIS_SUPPLY,
        "trade_market_enabled": True,
        "paid_resale_enabled": False,
        "share_url": f"https://t.me/{BOT_USERNAME}?startapp=ref_{u['ref_code']}" if BOT_USERNAME and u and u["ref_code"] else "",
        "retention": retention,
    }

@app.post("/api/rewards/daily")
async def daily_reward_claim(x_telegram_init_data: str | None = Header(default=None)):
    tid, _ = auth_user(x_telegram_init_data)
    try:
        reward = claim_daily_reward(tid)
    except ValueError as e:
        code = str(e)
        if code == "daily_already_claimed":
            raise HTTPException(status_code=409, detail="Daily expedition reward already claimed")
        raise HTTPException(status_code=400, detail=code)
    track_event(tid, "daily_claim", source="expedition")
    return {"ok": True, "reward": reward, "retention": retention_state(tid)}


@app.post("/api/missions/{mission_key}/claim")
async def mission_claim(mission_key: str, x_telegram_init_data: str | None = Header(default=None)):
    tid, _ = auth_user(x_telegram_init_data)
    try:
        reward = claim_daily_mission(tid, mission_key)
    except ValueError as e:
        code = str(e)
        if code == "mission_incomplete":
            raise HTTPException(status_code=409, detail="Mission is not complete yet")
        if code == "mission_already_claimed":
            raise HTTPException(status_code=409, detail="Mission reward already claimed")
        raise HTTPException(status_code=400, detail=code)
    track_event(tid, "mission_claim", source=mission_key)
    return {"ok": True, "reward": reward, "retention": retention_state(tid)}


@app.post("/api/milestones/{threshold}/claim")
async def milestone_claim(threshold: int, x_telegram_init_data: str | None = Header(default=None)):
    tid, _ = auth_user(x_telegram_init_data)
    try:
        reward = claim_collection_milestone(tid, threshold)
    except ValueError as e:
        code = str(e)
        if code == "milestone_incomplete":
            raise HTTPException(status_code=409, detail="Collection milestone is not complete yet")
        if code == "milestone_already_claimed":
            raise HTTPException(status_code=409, detail="Milestone reward already claimed")
        raise HTTPException(status_code=400, detail=code)
    track_event(tid, "milestone_claim", source=f"species_{threshold}")
    return {"ok": True, "reward": reward, "retention": retention_state(tid)}


@app.post("/api/research/scout")
async def research_scout(x_telegram_init_data: str | None = Header(default=None)):
    tid, _ = auth_user(x_telegram_init_data)
    owned = {row["character_id"] for row in collection(tid)}
    missing = [c["id"] for c in CATALOG if c["id"] not in owned]
    try:
        result = spend_research_scout(tid, missing)
    except ValueError as e:
        code = str(e)
        if code == "not_enough_dust":
            raise HTTPException(status_code=409, detail="You need 2 Research Dust")
        if code == "collection_complete":
            raise HTTPException(status_code=409, detail="Your species collection is complete")
        raise HTTPException(status_code=400, detail=code)
    character = next((c for c in CATALOG if c["id"] == result["character_id"]), None)
    track_event(tid, "research_scout", character_id=result["character_id"], source="expedition")
    return {
        "ok": True,
        "target": public_character(character) if character else None,
        "spent_dust": result["spent_dust"],
        "existing": result["existing"],
        "retention": retention_state(tid),
    }


@app.get("/api/catalog")
async def catalog_api():
    return {"characters": [public_character(c) for c in CATALOG]}

@app.get("/api/leaderboard")
async def leaderboard_api():
    rows = leaderboard()
    return {
        "leaders": [
            {
                "rank": idx,
                "label": public_collector_label(int(row["telegram_id"]), row["ref_code"]),
                "xp": int(row["xp"]),
                "drops": int(row["drops"]),
            }
            for idx, row in enumerate(rows, start=1)
        ]
    }

@app.post("/api/test/drop")
async def test_drop(x_telegram_init_data: str | None = Header(default=None)):
    if not FREE_TEST_MODE:
        raise HTTPException(status_code=404)
    tid, _ = auth_user(x_telegram_init_data)
    pid = "test_" + uuid.uuid4().hex
    # Free QA rotates only through release-quality beta specimens. Paid drops
    # continue to use the full rarity-weighted catalog and published odds.
    preview_ids = ("c001","c002","c003","c004","c005","c006","c007","c008","c009","c010","r001","r002","r003","r004","r005","r006","r007","r008","e001","e002","e003","e004","e005","e006","l001","l002","l003","l004","m001","m002")
    owned_count = len(collection(tid))
    preview_id = preview_ids[owned_count % len(preview_ids)]
    character = next((c for c in CATALOG if c["id"] == preview_id), choose_character())
    try:
        item = mark_test_and_mint(
            pid, tid, character["id"],
            DAILY_POOL_BASE,
            DAILY_POOL_USERS_PER_UNLOCK,
            DAILY_POOL_DROPS_PER_UNLOCK,
            DAILY_POOL_MAX,
        )
    except ValueError as e:
        if str(e) == "daily_pool_sold_out":
            raise HTTPException(status_code=409, detail="Today's global DROP pool is sold out")
        raise
    return {
        "ok": True,
        "character": public_character(character),
        "item_id": item["id"],
        "serial_no": item["serial_no"],
        "pool": pool_status(),
    }

@app.post("/api/invoice/drop")
async def invoice_drop(x_telegram_init_data: str | None = Header(default=None)):
    if FREE_TEST_MODE:
        raise HTTPException(status_code=409, detail="Paid DROP disabled while free test mode is active")
    if not persistent_storage_ready():
        raise HTTPException(status_code=503, detail="Paid DROP is locked until persistent storage is connected")
    tid, _ = auth_user(x_telegram_init_data)
    pid = uuid.uuid4().hex
    try:
        reserve_purchase(
            pid, tid, DROP_PRICE_STARS,
            DAILY_POOL_BASE,
            DAILY_POOL_USERS_PER_UNLOCK,
            DAILY_POOL_DROPS_PER_UNLOCK,
            DAILY_POOL_MAX,
            kind="drop",
            ttl_minutes=10,
        )
    except ValueError as e:
        if str(e) == "daily_pool_sold_out":
            raise HTTPException(status_code=409, detail="Today's global DROP pool is sold out")
        if str(e) == "active_reservation_exists":
            raise HTTPException(status_code=409, detail="Finish or cancel your current hatch first")
        raise
    try:
        url = await create_drop_invoice(pid, DROP_PRICE_STARS)
    except Exception as e:
        cancel_purchase(pid)
        raise HTTPException(status_code=502, detail=str(e))
    return {"invoice_url": url, "purchase_id": pid, "pool": pool_status()}

@app.post("/api/purchases/{purchase_id}/cancel")
async def cancel_drop_reservation(purchase_id: str, x_telegram_init_data: str | None = Header(default=None)):
    tid, _ = auth_user(x_telegram_init_data)
    p = get_purchase(purchase_id)
    if not p or int(p["telegram_id"]) != tid:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if p["status"] == "paid":
        raise HTTPException(status_code=409, detail="Paid hatch cannot be cancelled")
    cancel_purchase(purchase_id)
    return {"ok": True, "pool": pool_status()}


@app.post("/telegram/webhook/{secret}")
async def telegram_webhook(secret: str, request: Request):
    if not WEBHOOK_SECRET or secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=404)

    update = await request.json()
    pcq = update.get("pre_checkout_query")
    if pcq:
        payload = pcq.get("invoice_payload", "")
        if not payload.startswith("drop:"):
            await answer_precheckout(pcq["id"], False, "Unknown product.")
            return {"ok": True}
        pid = payload.split(":", 1)[1]
        p = get_purchase(pid)
        payer_id = int((pcq.get("from") or {}).get("id", 0))
        valid = bool(
            p and p["status"] == "pending"
            and p["stars"] == pcq.get("total_amount")
            and p["telegram_id"] == payer_id
            and purchase_reservation_valid(p)
        )
        await answer_precheckout(
            pcq["id"], valid,
            None if valid else "This DROP reservation expired or is no longer available. Please open a new DROP.",
        )
        return {"ok": True}

    msg = update.get("message") or {}
    text = (msg.get("text") or "").strip()
    chat_id = (msg.get("chat") or {}).get("id")
    base = os.getenv("BASE_URL", "").rstrip("/")
    launch_url = f"{base}/ios-canvas-22" if base else ""

    if chat_id and text.startswith("/start"):
        markup = {"inline_keyboard": [[{"text": "Open DROP1", "web_app": {"url": launch_url}}]]} if launch_url else None
        await send_message(chat_id, "DROP1 is a digital creature-collection game. Every paid egg hatches one guaranteed creature.\nUse /odds for rarity probabilities, /terms for purchase terms and /support for help.", markup)
        return {"ok": True}
    if chat_id and text.startswith("/collection"):
        markup = {"inline_keyboard": [[{"text": "Open my collection", "web_app": {"url": launch_url}}]]} if launch_url else None
        await send_message(chat_id, "Your DROP1 creatures are inside the Mini App.", markup)
        return {"ok": True}
    if chat_id and text.startswith("/leaderboard"):
        rows = leaderboard(10)
        if rows:
            lines = ["🏆 DROP1 Leaderboard"]
            for idx, row in enumerate(rows, start=1):
                name = public_collector_label(int(row["telegram_id"]), row["ref_code"])
                lines.append(f"{idx}. {name} — {row['xp']} XP · {row['drops']} hatches")
            await send_message(chat_id, "\n".join(lines))
        else:
            await send_message(chat_id, "The leaderboard is empty. Be the first collector.")
        return {"ok": True}
    if chat_id and text.startswith("/odds"):
        await send_message(chat_id, "Primal Hatch odds:\nCommon 65% · Rare 25% · Epic 8% · Legendary 1.8% · Mythic 0.2%" + (f"\n{base}/odds" if base else ""))
        return {"ok": True}
    if chat_id and text.startswith("/terms"):
        await send_message(chat_id, f"{base}/terms" if base else "Terms will be available in the Mini App.")
        return {"ok": True}
    if chat_id and text.startswith("/support"):
        support = SUPPORT_HANDLE or "the project operator"
        await send_message(chat_id, f"Purchase support: {support}\nTelegram Support does not handle purchases made from this bot.")
        return {"ok": True}

    sp = msg.get("successful_payment")
    if sp:
        payload = sp.get("invoice_payload", "")
        if payload.startswith("drop:"):
            pid = payload.split(":", 1)[1]
            p = get_purchase(pid)
            payer_id = int((msg.get("from") or {}).get("id", 0))
            if p and p["status"] != "paid" and p["telegram_id"] == payer_id:
                character = choose_character()
                item, minted = mark_paid_and_mint(pid, sp["telegram_payment_charge_id"], character["id"])
                if minted:
                    rarity = character["rarity"].upper()
                    payer = get_user(int(p["telegram_id"]))
                    share_url = f"https://t.me/{BOT_USERNAME}?startapp=ref_{payer['ref_code']}" if BOT_USERNAME and payer and payer["ref_code"] else ""
                    markup = {"inline_keyboard": [[{"text": "Open collection", "web_app": {"url": launch_url}}]]} if launch_url else None
                    await send_message(
                        p["telegram_id"],
                        f"🥚 {rarity} HATCH!\n{character['emoji']} {character['name']} #{item['serial_no']:06d}\nPower {character['power']} · Luck {character['luck']}\n\nYour creature is now in your DROP1 collection." + (f"\nInvite link: {share_url}" if share_url else ""),
                        markup,
                    )
        return {"ok": True}

    return {"ok": True}
