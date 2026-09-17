import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime, timezone

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

def utcnow():
    return datetime.now(timezone.utc).isoformat()

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

def create_purchase(pid: str, telegram_id: int, stars: int, kind="drop"):
    with conn() as c:
        c.execute(
            "INSERT INTO purchases (id, telegram_id, kind, stars, status, created_at) VALUES (?,?,?,?,?,?)",
            (pid, telegram_id, kind, stars, "pending", utcnow())
        )

def get_purchase(pid: str):
    with conn() as c:
        return c.execute("SELECT * FROM purchases WHERE id=?", (pid,)).fetchone()

def mark_paid_and_mint(pid: str, charge_id: str, character_id: str):
    with conn() as c:
        p = c.execute("SELECT * FROM purchases WHERE id=?", (pid,)).fetchone()
        if not p:
            raise ValueError("purchase_not_found")

        if p["status"] == "paid":
            item = c.execute("SELECT * FROM owned_items WHERE purchase_id=?", (pid,)).fetchone()
            return item, False

        serial = c.execute("SELECT last_serial FROM character_serials WHERE character_id=?", (character_id,)).fetchone()
        next_serial = (serial["last_serial"] if serial else 0) + 1
        if serial:
            c.execute("UPDATE character_serials SET last_serial=? WHERE character_id=?", (next_serial, character_id))
        else:
            c.execute("INSERT INTO character_serials(character_id,last_serial) VALUES (?,?)", (character_id,next_serial))

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
