import os, httpx

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

async def tg(method: str, payload: dict):
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not configured")
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(f"{API}/{method}", json=payload)
        data = r.json()
        if not data.get("ok"):
            raise RuntimeError(f"Telegram API error: {data}")
        return data["result"]

async def create_drop_invoice(purchase_id: str, stars: int):
    return await tg("createInvoiceLink", {
        "title": "DROP1 Primal Hatch Egg",
        "description": "One guaranteed digital creature from DROP1 Primal Hatch.",
        "payload": f"drop:{purchase_id}",
        "currency": "XTR",
        "prices": [{"label": "Primal Hatch Egg", "amount": stars}]
    })

async def answer_precheckout(query_id: str, ok=True, error_message=None):
    payload = {"pre_checkout_query_id": query_id, "ok": ok}
    if error_message:
        payload["error_message"] = error_message
    return await tg("answerPreCheckoutQuery", payload)

async def send_message(chat_id: int, text: str, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return await tg("sendMessage", payload)

async def setup_bot(base_url: str, webhook_secret: str):
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN missing in Render environment")
    if not base_url:
        raise RuntimeError("BASE_URL missing in Render environment")
    if not webhook_secret:
        raise RuntimeError("WEBHOOK_SECRET missing in Render environment")

    me = await tg("getMe", {})
    print(f"Telegram token OK for @{me.get('username', 'unknown')}", flush=True)

    base_url = base_url.rstrip("/")
    launch_url = f"{base_url}/ios-canvas-22"
    webhook_url = f"{base_url}/telegram/webhook/{webhook_secret}"
    await tg("setWebhook", {
        "url": webhook_url,
        "allowed_updates": ["message", "pre_checkout_query"]
    })
    await tg("setChatMenuButton", {
        "menu_button": {
            "type": "web_app",
            "text": "Open DROP1",
            "web_app": {"url": launch_url}
        }
    })
    await tg("setMyCommands", {
        "commands": [
            {"command":"start","description":"Open DROP1"},
            {"command":"collection","description":"My collection"},
            {"command":"odds","description":"Drop rarity odds"},
            {"command":"leaderboard","description":"Leaderboard"},
            {"command":"support","description":"Support"}
        ]
    })
    print("Telegram webhook configured", flush=True)
    return True
