import os, uuid, secrets
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

from .auth import validate_init_data
from .catalog import CATALOG
from .db import (
    init_db, upsert_user, get_user, reserve_purchase, cancel_purchase, get_purchase,
    purchase_reservation_valid, mark_paid_and_mint, mark_test_and_mint, collection,
    leaderboard, daily_pool_status
)
from .telegram import create_drop_invoice, answer_precheckout, send_message, setup_bot

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

app = FastAPI(title="DROP1")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def startup():
    init_db()
    try:
        await setup_bot(os.getenv("BASE_URL",""), WEBHOOK_SECRET)
    except Exception as e:
        print(f"Telegram setup skipped/failed: {e}")

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
            try:
                referrer_id = int(start.split("_",1)[1])
            except Exception:
                referrer_id = None
        upsert_user(int(u["id"]), u.get("username"), u.get("first_name"), referrer_id)
        return int(u["id"]), payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def public_character(c):
    return {k:v for k,v in c.items() if k != "weight"}

def choose_character():
    total = sum(c["weight"] for c in CATALOG)
    n = secrets.randbelow(total)
    cursor = 0
    for c in CATALOG:
        cursor += c["weight"]
        if n < cursor:
            return c
    return CATALOG[-1]

@app.get("/")
async def home():
    return FileResponse("app/static/index.html")

@app.get("/health")
async def health():
    return {
        "ok": True,
        "bot_configured": bool(os.getenv("BOT_TOKEN")),
        "free_test_mode": FREE_TEST_MODE,
        "pool": pool_status(),
    }

@app.get("/odds", response_class=HTMLResponse)
async def odds_page():
    return """<!doctype html><html><meta name="viewport" content="width=device-width,initial-scale=1"><body style="font-family:-apple-system,Arial;max-width:680px;margin:40px auto;padding:0 18px;line-height:1.55"><h1>DROP1 — Season 0 Odds</h1><p>Every paid DROP contains exactly one digital collectible.</p><ul><li>Common — 65.0%</li><li>Rare — 25.0%</li><li>Epic — 8.0%</li><li>Legendary — 1.8%</li><li>Mythic — 0.2%</li></ul><p>Collectibles do not represent money, securities, or a promise of resale value. There is no cash-out.</p></body></html>"""

@app.get("/terms", response_class=HTMLResponse)
async def terms_page():
    support = SUPPORT_HANDLE or "the support contact shown in the bot"
    return f"""<!doctype html><html><meta name="viewport" content="width=device-width,initial-scale=1"><body style="font-family:-apple-system,Arial;max-width:680px;margin:40px auto;padding:0 18px;line-height:1.55"><h1>DROP1 Terms — MVP</h1><p>DROP1 sells digital collectibles inside Telegram using Telegram Stars. Each purchase guarantees one digital collectible. The collectible received is randomly selected according to the published Season odds.</p><p>DROP1 collectibles have no guaranteed monetary value, no cash-out, and no promise of appreciation. A secondary-market resale feature is not part of this MVP.</p><p>Daily DROP availability is limited by the currently unlocked global pool and may sell out before the daily reset.</p><p>Payments are fulfilled only after Telegram confirms a successful payment. For purchase support, contact {support}.</p></body></html>"""

@app.get("/privacy", response_class=HTMLResponse)
async def privacy_page():
    return """<!doctype html><html><meta name="viewport" content="width=device-width,initial-scale=1"><body style="font-family:-apple-system,Arial;max-width:680px;margin:40px auto;padding:0 18px;line-height:1.55"><h1>DROP1 Privacy — MVP</h1><p>The service stores the Telegram account identifier and basic Telegram profile data needed to operate the collection, purchases, referrals, XP and support.</p><p>Payment identifiers are stored to reconcile purchases and handle refunds or disputes.</p></body></html>"""

@app.get("/api/bootstrap")
async def bootstrap(x_telegram_init_data: str | None = Header(default=None)):
    tid, _ = auth_user(x_telegram_init_data)
    u = get_user(tid)
    items = []
    by_id = {c["id"]: c for c in CATALOG}
    for row in collection(tid):
        c = by_id[row["character_id"]]
        items.append({**public_character(c), "serial_no": row["serial_no"], "acquired_at": row["acquired_at"]})
    unique = len(set(i["id"] for i in items))
    pool = pool_status()
    return {
        "user": {"id":tid,"username":u["username"],"first_name":u["first_name"],"xp":u["xp"],"dust":u["dust"]},
        "price_stars": DROP_PRICE_STARS,
        "test_mode": FREE_TEST_MODE,
        "catalog_total": len(CATALOG),
        "collection": items,
        "unique_count": unique,
        "pool": pool,
        "genesis_supply": GENESIS_SUPPLY,
        "share_url": f"https://t.me/{BOT_USERNAME}?startapp=ref_{tid}" if BOT_USERNAME else ""
    }

@app.get("/api/catalog")
async def catalog_api():
    return {"characters":[public_character(c) for c in CATALOG]}

@app.get("/api/leaderboard")
async def leaderboard_api():
    return {"leaders":[dict(r) for r in leaderboard()]}

@app.post("/api/test/drop")
async def test_drop(x_telegram_init_data: str | None = Header(default=None)):
    if not FREE_TEST_MODE:
        raise HTTPException(status_code=404)
    tid, _ = auth_user(x_telegram_init_data)
    pid = "test_" + uuid.uuid4().hex
    character = choose_character()
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
        "serial_no": item["serial_no"],
        "pool": pool_status(),
    }

@app.post("/api/invoice/drop")
async def invoice_drop(x_telegram_init_data: str | None = Header(default=None)):
    if FREE_TEST_MODE:
        raise HTTPException(status_code=409, detail="Paid DROP disabled while free test mode is active")
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
        )
    except ValueError as e:
        if str(e) == "daily_pool_sold_out":
            raise HTTPException(status_code=409, detail="Today's global DROP pool is sold out")
        raise
    try:
        url = await create_drop_invoice(pid, DROP_PRICE_STARS)
    except Exception as e:
        cancel_purchase(pid)
        raise HTTPException(status_code=502, detail=str(e))
    return {"invoice_url": url, "purchase_id": pid, "pool": pool_status()}

@app.post("/telegram/webhook/{secret}")
async def telegram_webhook(secret: str, request: Request):
    if not WEBHOOK_SECRET or secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=404)
    update = await request.json()
    pcq = update.get("pre_checkout_query")
    if pcq:
        payload = pcq.get("invoice_payload","")
        if not payload.startswith("drop:"):
            await answer_precheckout(pcq["id"], False, "Unknown product.")
            return {"ok": True}
        pid = payload.split(":",1)[1]
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
            None if valid else "This DROP reservation expired or is no longer available. Please open a new DROP."
        )
        return {"ok": True}

    msg = update.get("message") or {}
    text = (msg.get("text") or "").strip()
    chat_id = (msg.get("chat") or {}).get("id")
    base = os.getenv("BASE_URL","").rstrip("/")
    if chat_id and text.startswith("/start"):
        markup = {"inline_keyboard":[[{"text":"Open DROP1","web_app":{"url":base}}]]} if base else None
        await send_message(chat_id,"DROP1 is a digital collectible game. Every paid DROP contains one guaranteed collectible.\nUse /odds for rarity probabilities, /terms for purchase terms and /support for help.",markup)
        return {"ok": True}
    if chat_id and text.startswith("/collection"):
        markup = {"inline_keyboard":[[ {"text":"Open my collection","web_app":{"url":base}} ]]} if base else None
        await send_message(chat_id, "Your DROP1 collection is inside the Mini App.", markup)
        return {"ok": True}
    if chat_id and text.startswith("/leaderboard"):
        rows = leaderboard(10)
        if rows:
            lines = ["🏆 DROP1 Leaderboard"]
            for idx, row in enumerate(rows, start=1):
                name = row["username"] or row["first_name"] or f"user_{row['telegram_id']}"
                if row["username"]:
                    name = "@" + name
                lines.append(f"{idx}. {name} — {row['xp']} XP · {row['drops']} drops")
            await send_message(chat_id, "\n".join(lines))
        else:
            await send_message(chat_id, "The leaderboard is empty. Be the first collector.")
        return {"ok": True}
    if chat_id and text.startswith("/odds"):
        await send_message(chat_id,"Season 0 odds:\nCommon 65% · Rare 25% · Epic 8% · Legendary 1.8% · Mythic 0.2%" + (f"\n{base}/odds" if base else ""))
        return {"ok": True}
    if chat_id and text.startswith("/terms"):
        await send_message(chat_id, (f"{base}/terms" if base else "Terms will be available in the Mini App."))
        return {"ok": True}
    if chat_id and text.startswith("/support"):
        support = SUPPORT_HANDLE or "the project operator"
        await send_message(chat_id,f"Purchase support: {support}\nTelegram Support does not handle purchases made from this bot.")
        return {"ok": True}
    sp = msg.get("successful_payment")
    if sp:
        payload = sp.get("invoice_payload","")
        if payload.startswith("drop:"):
            pid = payload.split(":",1)[1]
            p = get_purchase(pid)
            payer_id = int((msg.get("from") or {}).get("id", 0))
            if p and p["status"] != "paid" and p["telegram_id"] == payer_id:
                character = choose_character()
                item, minted = mark_paid_and_mint(pid, sp["telegram_payment_charge_id"], character["id"])
                if minted:
                    rarity = character["rarity"].upper()
                    share_url = f"https://t.me/{BOT_USERNAME}?startapp=ref_{p['telegram_id']}" if BOT_USERNAME else ""
                    markup = {"inline_keyboard":[[{"text":"Open collection","web_app":{"url":base}}]]} if base else None
                    await send_message(p["telegram_id"],f"🎉 {rarity} DROP!\n{character['emoji']} {character['name']} #{item['serial_no']:06d}\nPower {character['power']} · Luck {character['luck']}\n\nYour collectible is now in your DROP1 collection." + (f"\nInvite link: {share_url}" if share_url else ""),markup)
        return {"ok": True}
    return {"ok": True}
