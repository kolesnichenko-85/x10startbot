import hashlib, hmac, json, os, time
from urllib.parse import parse_qsl

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"
DEV_TELEGRAM_ID = int(os.getenv("DEV_TELEGRAM_ID", "777000001"))

def validate_init_data(init_data: str, max_age_seconds: int = 3600):
    if DEV_MODE and (not init_data or init_data == "dev"):
        return {"user": {"id": DEV_TELEGRAM_ID, "first_name": "Dev", "username": "dev_user"}, "start_param": None}
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not configured")
    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = pairs.pop("hash", None)
    if not received_hash:
        raise ValueError("missing hash")
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(pairs.items()))
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calculated_hash, received_hash):
        raise ValueError("bad hash")
    auth_date = int(pairs.get("auth_date", "0"))
    if auth_date and time.time() - auth_date > max_age_seconds:
        raise ValueError("stale auth")
    user = json.loads(pairs["user"]) if pairs.get("user") else None
    if not user:
        raise ValueError("missing user")
    return {"user": user, "start_param": pairs.get("start_param")}
