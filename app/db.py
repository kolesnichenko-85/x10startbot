import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta

DB_PATH = os.getenv("DATABASE_PATH", "/data/drop1.db")

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    referrer_id INTEGER,
    xp INTEGER NOT NULL DEFAULT 0,
    dust INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    first_paid_at TEXT,
    FOREIGN KEY(referrer_id) REFERENCES users(telegram_id)
);

CREATE TABLE IF NOT EXISTS purchases (
    id TEXT PRIMARY KEY,
    telegram_id INTEGER NOT NULL,
    kind TEXT NOT NULL,
    stars INTEGER NOT NULL,
    status TEXT NOT NULL,
    telegram_charge_id TEXT UNIQUE,
    created_at TEXT NOT NULL,
    paid_at TEXT,
    pool_day TEXT,
    reservation_expires_at TEXT,
    FOREIGN KEY(telegram_id) REFERENCES users(telegram_id)
);

CREATE TABLE IF NOT EXISTS owned_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    character_id TEXT NOT NULL,
    serial_no INTEGER NOT NULL,
    purchase_id TEXT NOT NULL UNIQUE,
    acquired_at TEXT NOT NULL,
    FOREIGN KEY(telegram_id) REFERENCES users(telegram_id),
    FOREIGN KEY(purchase_id) REFERENCES purchases(id)
);

CREATE TABLE IF NOT EXISTS character_serials (
    character_id TEXT PRIMARY KEY,
    last_serial INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS rewards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    reward_key TEXT NOT NULL,
    amount INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    UNIQUE(telegram_id, reward_key)
);

CREATE TABLE IF NOT EXISTS product_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    event_name TEXT NOT NULL,
    item_id INTEGER,
    character_id TEXT,
    source TEXT,
    metadata TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(telegram_id) REFERENCES users(telegram_id)
);

CREATE INDEX IF NOT EXISTS idx_product_events_user_time
ON product_events(telegram_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_product_events_name_time
ON product_events(event_name, created_at DESC);
"""

@contextmanager
def conn():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    c = sqlite3.connect(DB_PATH, timeout=15)
    c.row_factory = sqlite3.Row
    try:
        yield c
        c.commit()
    finally:
        c.close()

def init_db():
    with conn() as c:
        c.executescript(SCHEMA)
        # Safe migration for databases created before the global pool feature.
        cols = {r["name"] for r in c.execute("PRAGMA table_info(purchases)").fetchall()}
        if "pool_day" not in cols:
            c.execute("ALTER TABLE purchases ADD COLUMN pool_day TEXT")
        if "reservation_expires_at" not in cols:
            c.execute("ALTER TABLE purchases ADD COLUMN reservation_expires_at TEXT")

def utcnow_dt():
    return datetime.now(timezone.utc)

def utcnow():
    return utcnow_dt().isoformat()

def _day_bounds(now=None):
    now = now or utcnow_dt()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end

def _pool_snapshot(c, base_supply: int, users_per_unlock: int, drops_per_unlock: int, max_supply: int, include_test: bool = True, now=None):
    now = now or utcnow_dt()
    start, end = _day_bounds(now)
    start_iso, end_iso = start.isoformat(), end.isoformat()
    day = start.date().isoformat()

    new_users = c.execute(
        "SELECT COUNT(*) AS n FROM users WHERE created_at>=? AND created_at<?",
        (start_iso, end_iso)
    ).fetchone()["n"]

    unlocked_steps = new_users // max(1, users_per_unlock)
    unlocked_bonus = unlocked_steps * max(0, drops_per_unlock)
    supply = min(max_supply, base_supply + unlocked_bonus)

    if include_test:
        opened = c.execute(
            """SELECT COUNT(*) AS n
               FROM owned_items oi
               JOIN purchases p ON p.id=oi.purchase_id
               WHERE oi.acquired_at>=? AND oi.acquired_at<? AND p.kind IN ('drop','test')""",
            (start_iso, end_iso)
        ).fetchone()["n"]
    else:
        opened = c.execute(
            """SELECT COUNT(*) AS n
               FROM owned_items oi
               JOIN purchases p ON p.id=oi.purchase_id
               WHERE oi.acquired_at>=? AND oi.acquired_at<? AND p.kind='drop'""",
            (start_iso, end_iso)
        ).fetchone()["n"]

    active_reserved = c.execute(
        """SELECT COUNT(*) AS n FROM purchases
           WHERE status='pending' AND pool_day=? AND reservation_expires_at>?""",
        (day, now.isoformat())
    ).fetchone()["n"]

    used_or_reserved = opened + active_reserved
    remaining = max(0, supply - used_or_reserved)

    if supply >= max_supply:
        to_next_unlock = 0
        next_unlock_drops = 0
    else:
        rem = new_users % max(1, users_per_unlock)
        to_next_unlock = max(1, users_per_unlock) - rem if rem else max(1, users_per_unlock)
        next_unlock_drops = min(max(0, drops_per_unlock), max_supply - supply)

    return {
        "day": day,
        "base_supply": base_supply,
        "supply": supply,
        "opened": opened,
        "reserved": active_reserved,
        "remaining": remaining,
        "new_collectors": new_users,
        "collectors_to_next_unlock": to_next_unlock,
        "next_unlock_drops": next_unlock_drops,
        "max_supply": max_supply,
        "reset_at": end.isoformat(),
    }

def daily_pool_status(base_supply: int, users_per_unlock: int, drops_per_unlock: int, max_supply: int, include_test: bool = True):
    with conn() as c:
        return _pool_snapshot(c, base_supply, users_per_unlock, drops_per_unlock, max_supply, include_test)

def upsert_user(telegram_id: int, username: str|None, first_name: str|None, referrer_id: int|None=None):
    with conn() as c:
        exists = c.execute("SELECT telegram_id, referrer_id FROM users WHERE telegram_id=?", (telegram_id,)).fetchone()
        if not exists:
            if referrer_id == telegram_id:
                referrer_id = None
            c.execute(
                "INSERT INTO users (telegram_id, username, first_name, referrer_id, created_at) VALUES (?,?,?,?,?)",
                (telegram_id, username, first_name, referrer_id, utcnow())
            )
        else:
            c.execute("UPDATE users SET username=?, first_name=? WHERE telegram_id=?",
                      (username, first_name, telegram_id))

def get_user(telegram_id: int):
    with conn() as c:
        return c.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,)).fetchone()

def reserve_purchase(pid: str, telegram_id: int, stars: int, base_supply: int, users_per_unlock: int, drops_per_unlock: int, max_supply: int, kind="drop", ttl_minutes=20):
    now = utcnow_dt()
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        pool = _pool_snapshot(c, base_supply, users_per_unlock, drops_per_unlock, max_supply, include_test=True, now=now)
        if pool["remaining"] <= 0:
            raise ValueError("daily_pool_sold_out")
        expires = now + timedelta(minutes=ttl_minutes)
        c.execute(
            """INSERT INTO purchases
               (id, telegram_id, kind, stars, status, created_at, pool_day, reservation_expires_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (pid, telegram_id, kind, stars, "pending", now.isoformat(), pool["day"], expires.isoformat())
        )
        return pool

def cancel_purchase(pid: str):
    with conn() as c:
        c.execute("UPDATE purchases SET status='cancelled' WHERE id=? AND status='pending'", (pid,))

def get_purchase(pid: str):
    with conn() as c:
        return c.execute("SELECT * FROM purchases WHERE id=?", (pid,)).fetchone()

def purchase_reservation_valid(p):
    if not p or p["status"] != "pending" or not p["reservation_expires_at"]:
        return False
    try:
        return datetime.fromisoformat(p["reservation_expires_at"]) > utcnow_dt()
    except Exception:
        return False

def _next_serial(c, character_id: str):
    serial = c.execute("SELECT last_serial FROM character_serials WHERE character_id=?", (character_id,)).fetchone()
    next_serial = (serial["last_serial"] if serial else 0) + 1
    if serial:
        c.execute("UPDATE character_serials SET last_serial=? WHERE character_id=?", (next_serial, character_id))
    else:
        c.execute("INSERT INTO character_serials(character_id,last_serial) VALUES (?,?)", (character_id,next_serial))
    return next_serial

def mark_paid_and_mint(pid: str, charge_id: str, character_id: str):
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        p = c.execute("SELECT * FROM purchases WHERE id=?", (pid,)).fetchone()
        if not p:
            raise ValueError("purchase_not_found")

        if p["status"] == "paid":
            item = c.execute("SELECT * FROM owned_items WHERE purchase_id=?", (pid,)).fetchone()
            return item, False
        if p["status"] != "pending":
            raise ValueError("purchase_not_pending")

        next_serial = _next_serial(c, character_id)
        now = utcnow()
        c.execute(
            "UPDATE purchases SET status='paid', telegram_charge_id=?, paid_at=? WHERE id=?",
            (charge_id, now, pid)
        )
        c.execute(
            "INSERT INTO owned_items (telegram_id, character_id, serial_no, purchase_id, acquired_at) VALUES (?,?,?,?,?)",
            (p["telegram_id"], character_id, next_serial, pid, now)
        )
        c.execute("UPDATE users SET xp=xp+10, first_paid_at=COALESCE(first_paid_at, ?) WHERE telegram_id=?",
                  (now, p["telegram_id"]))

        u = c.execute("SELECT referrer_id FROM users WHERE telegram_id=?", (p["telegram_id"],)).fetchone()
        if u and u["referrer_id"]:
            reward_key = f"paid_referral:{p['telegram_id']}"
            try:
                c.execute(
                    "INSERT INTO rewards(telegram_id,reward_key,amount,created_at) VALUES (?,?,?,?)",
                    (u["referrer_id"], reward_key, 1, now)
                )
                c.execute("UPDATE users SET xp=xp+50, dust=dust+1 WHERE telegram_id=?", (u["referrer_id"],))
            except sqlite3.IntegrityError:
                pass

        item = c.execute("SELECT * FROM owned_items WHERE purchase_id=?", (pid,)).fetchone()
        return item, True

def mark_test_and_mint(pid: str, telegram_id: int, character_id: str, base_supply: int, users_per_unlock: int, drops_per_unlock: int, max_supply: int):
    """Free QA mint. Exercises pool/draw/serial/collection/XP without Telegram payment or referral rewards."""
    now_dt = utcnow_dt()
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        pool = _pool_snapshot(c, base_supply, users_per_unlock, drops_per_unlock, max_supply, include_test=True, now=now_dt)
        if pool["remaining"] <= 0:
            raise ValueError("daily_pool_sold_out")
        now = now_dt.isoformat()
        next_serial = _next_serial(c, character_id)
        c.execute(
            """INSERT INTO purchases
               (id, telegram_id, kind, stars, status, telegram_charge_id, created_at, paid_at, pool_day)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (pid, telegram_id, "test", 0, "paid", f"test:{pid}", now, now, pool["day"])
        )
        c.execute(
            "INSERT INTO owned_items (telegram_id, character_id, serial_no, purchase_id, acquired_at) VALUES (?,?,?,?,?)",
            (telegram_id, character_id, next_serial, pid, now)
        )
        c.execute("UPDATE users SET xp=xp+10 WHERE telegram_id=?", (telegram_id,))
        return c.execute("SELECT * FROM owned_items WHERE purchase_id=?", (pid,)).fetchone()

def collection(telegram_id: int):
    with conn() as c:
        return c.execute(
            """SELECT oi.* FROM owned_items oi
               WHERE oi.telegram_id=? ORDER BY oi.id DESC""",
            (telegram_id,)
        ).fetchall()

def leaderboard(limit=50):
    with conn() as c:
        return c.execute(
            """SELECT telegram_id, username, first_name, xp, dust,
                      (SELECT COUNT(*) FROM owned_items oi WHERE oi.telegram_id=users.telegram_id) AS drops
               FROM users ORDER BY xp DESC, drops DESC, created_at ASC LIMIT ?""",
            (limit,)
        ).fetchall()


def track_event(telegram_id: int, event_name: str, item_id: int|None=None, character_id: str|None=None, source: str|None=None, metadata: str|None=None):
    name = (event_name or "").strip().lower()[:64]
    if not name:
        return
    with conn() as c:
        c.execute(
            """INSERT INTO product_events(telegram_id,event_name,item_id,character_id,source,metadata,created_at)
               VALUES (?,?,?,?,?,?,?)""",
            (telegram_id, name, item_id, character_id, (source or "")[:64] or None, (metadata or "")[:500] or None, utcnow())
        )

def product_event_counts(hours: int = 24):
    since = (utcnow_dt() - timedelta(hours=max(1, min(hours, 720)))).isoformat()
    with conn() as c:
        return c.execute(
            """SELECT event_name, COUNT(*) AS n
               FROM product_events WHERE created_at>=?
               GROUP BY event_name ORDER BY n DESC, event_name ASC""",
            (since,)
        ).fetchall()
