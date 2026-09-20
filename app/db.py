import os
import secrets
from datetime import datetime, timezone, timedelta

from .storage import conn, is_postgres, database_backend

SQLITE_SCHEMA = """
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
    ref_code TEXT,
    daily_streak INTEGER NOT NULL DEFAULT 0,
    last_daily_claim TEXT,
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

CREATE TABLE IF NOT EXISTS ownership_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    from_user_id INTEGER,
    to_user_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    reference_id TEXT,
    event_key TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    FOREIGN KEY(item_id) REFERENCES owned_items(id)
);

CREATE TABLE IF NOT EXISTS daily_mission_claims (
    telegram_id INTEGER NOT NULL,
    day TEXT NOT NULL,
    mission_key TEXT NOT NULL,
    claimed_at TEXT NOT NULL,
    PRIMARY KEY(telegram_id, day, mission_key),
    FOREIGN KEY(telegram_id) REFERENCES users(telegram_id)
);

CREATE TABLE IF NOT EXISTS daily_scout_targets (
    telegram_id INTEGER NOT NULL,
    day TEXT NOT NULL,
    character_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(telegram_id, day),
    FOREIGN KEY(telegram_id) REFERENCES users(telegram_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_users_ref_code
ON users(ref_code) WHERE ref_code IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_product_events_user_time
ON product_events(telegram_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_product_events_name_time
ON product_events(event_name, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_ownership_item
ON ownership_events(item_id, id ASC);
"""

POSTGRES_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    telegram_id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    referrer_id BIGINT,
    xp INTEGER NOT NULL DEFAULT 0,
    dust INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    first_paid_at TEXT,
    ref_code TEXT,
    daily_streak INTEGER NOT NULL DEFAULT 0,
    last_daily_claim TEXT,
    FOREIGN KEY(referrer_id) REFERENCES users(telegram_id)
);

CREATE TABLE IF NOT EXISTS purchases (
    id TEXT PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
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
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
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
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    reward_key TEXT NOT NULL,
    amount INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    UNIQUE(telegram_id, reward_key)
);

CREATE TABLE IF NOT EXISTS product_events (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    event_name TEXT NOT NULL,
    item_id BIGINT,
    character_id TEXT,
    source TEXT,
    metadata TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(telegram_id) REFERENCES users(telegram_id)
);

CREATE TABLE IF NOT EXISTS ownership_events (
    id BIGSERIAL PRIMARY KEY,
    item_id BIGINT NOT NULL,
    from_user_id BIGINT,
    to_user_id BIGINT NOT NULL,
    event_type TEXT NOT NULL,
    reference_id TEXT,
    event_key TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    FOREIGN KEY(item_id) REFERENCES owned_items(id)
);

CREATE TABLE IF NOT EXISTS daily_mission_claims (
    telegram_id BIGINT NOT NULL,
    day TEXT NOT NULL,
    mission_key TEXT NOT NULL,
    claimed_at TEXT NOT NULL,
    PRIMARY KEY(telegram_id, day, mission_key),
    FOREIGN KEY(telegram_id) REFERENCES users(telegram_id)
);

CREATE TABLE IF NOT EXISTS daily_scout_targets (
    telegram_id BIGINT NOT NULL,
    day TEXT NOT NULL,
    character_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(telegram_id, day),
    FOREIGN KEY(telegram_id) REFERENCES users(telegram_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_users_ref_code
ON users(ref_code) WHERE ref_code IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_product_events_user_time
ON product_events(telegram_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_product_events_name_time
ON product_events(event_name, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_ownership_item
ON ownership_events(item_id, id ASC);
"""

def init_db():
    with conn() as c:
        c.executescript(POSTGRES_SCHEMA if is_postgres() else SQLITE_SCHEMA)
        if is_postgres():
            c.execute("ALTER TABLE purchases ADD COLUMN IF NOT EXISTS pool_day TEXT")
            c.execute("ALTER TABLE purchases ADD COLUMN IF NOT EXISTS reservation_expires_at TEXT")
            c.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS ref_code TEXT")
            c.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS daily_streak INTEGER NOT NULL DEFAULT 0")
            c.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_daily_claim TEXT")
        else:
            cols = {r["name"] for r in c.execute("PRAGMA table_info(purchases)").fetchall()}
            if "pool_day" not in cols:
                c.execute("ALTER TABLE purchases ADD COLUMN pool_day TEXT")
            if "reservation_expires_at" not in cols:
                c.execute("ALTER TABLE purchases ADD COLUMN reservation_expires_at TEXT")
            user_cols = {r["name"] for r in c.execute("PRAGMA table_info(users)").fetchall()}
            if "ref_code" not in user_cols:
                c.execute("ALTER TABLE users ADD COLUMN ref_code TEXT")
            if "daily_streak" not in user_cols:
                c.execute("ALTER TABLE users ADD COLUMN daily_streak INTEGER NOT NULL DEFAULT 0")
            if "last_daily_claim" not in user_cols:
                c.execute("ALTER TABLE users ADD COLUMN last_daily_claim TEXT")
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_ref_code_runtime ON users(ref_code) WHERE ref_code IS NOT NULL")


def utcnow_dt():
    return datetime.now(timezone.utc)


def utcnow():
    return utcnow_dt().isoformat()


def _day_bounds(now=None):
    now = now or utcnow_dt()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start, end


def _pool_write_lock(c):
    if is_postgres():
        c.execute("SELECT pg_advisory_xact_lock(641061)")


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

    kinds = "('drop','test')" if include_test else "('drop')"
    opened = c.execute(
        f"""SELECT COUNT(*) AS n
            FROM owned_items oi
            JOIN purchases p ON p.id=oi.purchase_id
            WHERE oi.acquired_at>=? AND oi.acquired_at<? AND p.kind IN {kinds}""",
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
    if referrer_id == telegram_id:
        referrer_id = None
    with conn() as c:
        c.execute(
            """INSERT INTO users(telegram_id,username,first_name,referrer_id,created_at)
               VALUES (?,?,?,?,?) ON CONFLICT(telegram_id) DO NOTHING""",
            (telegram_id, username, first_name, referrer_id, utcnow())
        )
        c.execute(
            "UPDATE users SET username=?, first_name=? WHERE telegram_id=?",
            (username, first_name, telegram_id)
        )
        row = c.execute("SELECT ref_code FROM users WHERE telegram_id=?", (telegram_id,)).fetchone()
        if row and not row["ref_code"]:
            for _ in range(5):
                code = secrets.token_urlsafe(7).replace("-", "").replace("_", "")[:10]
                try:
                    c.execute("UPDATE users SET ref_code=? WHERE telegram_id=? AND ref_code IS NULL", (code, telegram_id))
                    break
                except Exception:
                    continue


def get_user(telegram_id: int):
    with conn() as c:
        return c.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,)).fetchone()


def get_user_by_ref_code(ref_code: str):
    code = (ref_code or "").strip()[:32]
    if not code:
        return None
    with conn() as c:
        return c.execute("SELECT * FROM users WHERE ref_code=?", (code,)).fetchone()


def reserve_purchase(pid: str, telegram_id: int, stars: int, base_supply: int, users_per_unlock: int, drops_per_unlock: int, max_supply: int, kind="drop", ttl_minutes=20):
    now = utcnow_dt()
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        _pool_write_lock(c)
        c.execute(
            "UPDATE purchases SET status='expired' WHERE status='pending' AND reservation_expires_at IS NOT NULL AND reservation_expires_at<=?",
            (now.isoformat(),)
        )
        active = c.execute(
            """SELECT id FROM purchases
               WHERE telegram_id=? AND status='pending'
                 AND reservation_expires_at IS NOT NULL AND reservation_expires_at>?
               ORDER BY created_at DESC LIMIT 1""",
            (telegram_id, now.isoformat())
        ).fetchone()
        if active:
            raise ValueError("active_reservation_exists")
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
    if is_postgres():
        row = c.execute(
            """INSERT INTO character_serials(character_id,last_serial) VALUES (?,1)
               ON CONFLICT(character_id)
               DO UPDATE SET last_serial=character_serials.last_serial+1
               RETURNING last_serial""",
            (character_id,)
        ).fetchone()
        return int(row["last_serial"])

    serial = c.execute("SELECT last_serial FROM character_serials WHERE character_id=?", (character_id,)).fetchone()
    next_serial = (serial["last_serial"] if serial else 0) + 1
    if serial:
        c.execute("UPDATE character_serials SET last_serial=? WHERE character_id=?", (next_serial, character_id))
    else:
        c.execute("INSERT INTO character_serials(character_id,last_serial) VALUES (?,?)", (character_id, next_serial))
    return next_serial


def _record_mint(c, item, now):
    c.execute(
        """INSERT INTO ownership_events(
               item_id,from_user_id,to_user_id,event_type,reference_id,event_key,created_at
           ) VALUES (?,?,?,?,?,?,?)
           ON CONFLICT(event_key) DO NOTHING""",
        (item["id"], None, item["telegram_id"], "mint", item["purchase_id"], f"mint:{item['id']}", now)
    )


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
        duplicate = bool(c.execute(
            "SELECT 1 FROM owned_items WHERE telegram_id=? AND character_id=? LIMIT 1",
            (p["telegram_id"], character_id)
        ).fetchone())
        c.execute(
            "INSERT INTO owned_items (telegram_id, character_id, serial_no, purchase_id, acquired_at) VALUES (?,?,?,?,?)",
            (p["telegram_id"], character_id, next_serial, pid, now)
        )
        c.execute(
            "UPDATE users SET xp=xp+10, first_paid_at=COALESCE(first_paid_at, ?), dust=dust+? WHERE telegram_id=?",
            (now, 1 if duplicate else 0, p["telegram_id"])
        )
        if duplicate:
            c.execute(
                """INSERT INTO rewards(telegram_id,reward_key,amount,created_at)
                   VALUES (?,?,?,?) ON CONFLICT(telegram_id,reward_key) DO NOTHING""",
                (p["telegram_id"], f"duplicate:{pid}", 1, now)
            )

        u = c.execute("SELECT referrer_id FROM users WHERE telegram_id=?", (p["telegram_id"],)).fetchone()
        if u and u["referrer_id"]:
            reward_key = f"paid_referral:{p['telegram_id']}"
            cur = c.execute(
                """INSERT INTO rewards(telegram_id,reward_key,amount,created_at)
                   VALUES (?,?,?,?) ON CONFLICT(telegram_id,reward_key) DO NOTHING""",
                (u["referrer_id"], reward_key, 1, now)
            )
            if cur.rowcount == 1:
                c.execute("UPDATE users SET xp=xp+50, dust=dust+1 WHERE telegram_id=?", (u["referrer_id"],))

        item = c.execute("SELECT * FROM owned_items WHERE purchase_id=?", (pid,)).fetchone()
        _record_mint(c, item, now)
        return item, True


def mark_test_and_mint(pid: str, telegram_id: int, character_id: str, base_supply: int, users_per_unlock: int, drops_per_unlock: int, max_supply: int):
    """Free QA mint. Exercises pool/draw/serial/collection/XP without Telegram payment or referral rewards."""
    now_dt = utcnow_dt()
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        _pool_write_lock(c)
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
        duplicate = bool(c.execute(
            "SELECT 1 FROM owned_items WHERE telegram_id=? AND character_id=? LIMIT 1",
            (telegram_id, character_id)
        ).fetchone())
        c.execute(
            "INSERT INTO owned_items (telegram_id, character_id, serial_no, purchase_id, acquired_at) VALUES (?,?,?,?,?)",
            (telegram_id, character_id, next_serial, pid, now)
        )
        c.execute("UPDATE users SET xp=xp+10, dust=dust+? WHERE telegram_id=?", (1 if duplicate else 0, telegram_id))
        if duplicate:
            c.execute(
                """INSERT INTO rewards(telegram_id,reward_key,amount,created_at)
                   VALUES (?,?,?,?) ON CONFLICT(telegram_id,reward_key) DO NOTHING""",
                (telegram_id, f"duplicate:{pid}", 1, now)
            )
        item = c.execute("SELECT * FROM owned_items WHERE purchase_id=?", (pid,)).fetchone()
        _record_mint(c, item, now)
        return item


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


MISSION_DEFS = {
    "hatch_one": {"title": "Hatch one creature", "goal": 1, "xp": 20, "dust": 1},
    "inspect_one": {"title": "Inspect a specimen", "goal": 1, "xp": 10, "dust": 0},
    "visit_market": {"title": "Visit the creature exchange", "goal": 1, "xp": 10, "dust": 1},
}

MILESTONE_REWARDS = {
    5: {"xp": 50, "dust": 2},
    10: {"xp": 100, "dust": 4},
    20: {"xp": 250, "dust": 8},
    30: {"xp": 500, "dust": 15},
}


def _today():
    return utcnow_dt().date()


def _mission_progress(c, telegram_id: int, key: str, start_iso: str, end_iso: str) -> int:
    if key == "hatch_one":
        return int(c.execute(
            "SELECT COUNT(*) AS n FROM owned_items WHERE telegram_id=? AND acquired_at>=? AND acquired_at<?",
            (telegram_id, start_iso, end_iso)
        ).fetchone()["n"])
    event_name = "specimen_open" if key == "inspect_one" else "market_open"
    return int(c.execute(
        """SELECT COUNT(*) AS n FROM product_events
           WHERE telegram_id=? AND event_name=? AND created_at>=? AND created_at<?""",
        (telegram_id, event_name, start_iso, end_iso)
    ).fetchone()["n"])


def retention_state(telegram_id: int):
    now = utcnow_dt()
    start, end = _day_bounds(now)
    start_iso, end_iso = start.isoformat(), end.isoformat()
    day = start.date().isoformat()
    yesterday = (start.date() - timedelta(days=1)).isoformat()

    with conn() as c:
        u = c.execute(
            "SELECT daily_streak,last_daily_claim,xp,dust FROM users WHERE telegram_id=?",
            (telegram_id,)
        ).fetchone()
        last = (u["last_daily_claim"] if u else None) or None
        current_streak = int((u["daily_streak"] if u else 0) or 0)
        next_streak = current_streak + 1 if last == yesterday else (current_streak if last == day else 1)
        daily_claimed = last == day
        daily_reward = {
            "xp": 15 + (50 if next_streak % 7 == 0 else 0),
            "dust": 1 + (2 if next_streak % 7 == 0 else 0),
        }

        claimed_rows = c.execute(
            "SELECT mission_key FROM daily_mission_claims WHERE telegram_id=? AND day=?",
            (telegram_id, day)
        ).fetchall()
        claimed = {r["mission_key"] for r in claimed_rows}
        missions = []
        for key, spec in MISSION_DEFS.items():
            progress = min(spec["goal"], _mission_progress(c, telegram_id, key, start_iso, end_iso))
            missions.append({
                "key": key,
                "title": spec["title"],
                "progress": progress,
                "goal": spec["goal"],
                "complete": progress >= spec["goal"],
                "claimed": key in claimed,
                "reward_xp": spec["xp"],
                "reward_dust": spec["dust"],
            })

        unique = int(c.execute(
            "SELECT COUNT(DISTINCT character_id) AS n FROM owned_items WHERE telegram_id=?",
            (telegram_id,)
        ).fetchone()["n"])
        reward_rows = c.execute(
            "SELECT reward_key FROM rewards WHERE telegram_id=? AND reward_key LIKE ?",
            (telegram_id, "collection:%")
        ).fetchall()
        reward_keys = {r["reward_key"] for r in reward_rows}
        milestones = []
        for threshold, reward in MILESTONE_REWARDS.items():
            milestones.append({
                "threshold": threshold,
                "reached": unique >= threshold,
                "claimed": f"collection:{threshold}" in reward_keys,
                "reward_xp": reward["xp"],
                "reward_dust": reward["dust"],
            })

        scout = c.execute(
            "SELECT character_id FROM daily_scout_targets WHERE telegram_id=? AND day=?",
            (telegram_id, day)
        ).fetchone()

        return {
            "day": day,
            "scout_target_id": scout["character_id"] if scout else None,
            "daily": {
                "streak": current_streak,
                "can_claim": not daily_claimed,
                "claimed": daily_claimed,
                "next_streak": next_streak,
                "reward_xp": daily_reward["xp"],
                "reward_dust": daily_reward["dust"],
            },
            "missions": missions,
            "milestones": milestones,
            "unique_species": unique,
        }


def claim_daily_reward(telegram_id: int):
    now = utcnow_dt()
    day = now.date().isoformat()
    yesterday = (now.date() - timedelta(days=1)).isoformat()
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        row_sql = "SELECT daily_streak,last_daily_claim FROM users WHERE telegram_id=?" + (" FOR UPDATE" if is_postgres() else "")
        u = c.execute(row_sql, (telegram_id,)).fetchone()
        if not u:
            raise ValueError("user_not_found")
        if u["last_daily_claim"] == day:
            raise ValueError("daily_already_claimed")
        streak = int(u["daily_streak"] or 0) + 1 if u["last_daily_claim"] == yesterday else 1
        xp = 15 + (50 if streak % 7 == 0 else 0)
        dust = 1 + (2 if streak % 7 == 0 else 0)
        now_iso = now.isoformat()
        c.execute(
            "UPDATE users SET daily_streak=?,last_daily_claim=?,xp=xp+?,dust=dust+? WHERE telegram_id=?",
            (streak, day, xp, dust, telegram_id)
        )
        c.execute(
            """INSERT INTO rewards(telegram_id,reward_key,amount,created_at)
               VALUES (?,?,?,?) ON CONFLICT(telegram_id,reward_key) DO NOTHING""",
            (telegram_id, f"daily:{day}", dust, now_iso)
        )
        return {"streak": streak, "xp": xp, "dust": dust}


def claim_daily_mission(telegram_id: int, mission_key: str):
    spec = MISSION_DEFS.get(mission_key)
    if not spec:
        raise ValueError("unknown_mission")
    now = utcnow_dt()
    start, end = _day_bounds(now)
    day = start.date().isoformat()
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        progress = _mission_progress(c, telegram_id, mission_key, start.isoformat(), end.isoformat())
        if progress < spec["goal"]:
            raise ValueError("mission_incomplete")
        exists = c.execute(
            "SELECT 1 FROM daily_mission_claims WHERE telegram_id=? AND day=? AND mission_key=?",
            (telegram_id, day, mission_key)
        ).fetchone()
        if exists:
            raise ValueError("mission_already_claimed")
        c.execute(
            "INSERT INTO daily_mission_claims(telegram_id,day,mission_key,claimed_at) VALUES (?,?,?,?)",
            (telegram_id, day, mission_key, now.isoformat())
        )
        c.execute(
            "UPDATE users SET xp=xp+?,dust=dust+? WHERE telegram_id=?",
            (spec["xp"], spec["dust"], telegram_id)
        )
        return {"mission_key": mission_key, "xp": spec["xp"], "dust": spec["dust"]}


def claim_collection_milestone(telegram_id: int, threshold: int):
    reward = MILESTONE_REWARDS.get(int(threshold))
    if not reward:
        raise ValueError("unknown_milestone")
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        unique = int(c.execute(
            "SELECT COUNT(DISTINCT character_id) AS n FROM owned_items WHERE telegram_id=?",
            (telegram_id,)
        ).fetchone()["n"])
        if unique < threshold:
            raise ValueError("milestone_incomplete")
        key = f"collection:{threshold}"
        exists = c.execute(
            "SELECT 1 FROM rewards WHERE telegram_id=? AND reward_key=?",
            (telegram_id, key)
        ).fetchone()
        if exists:
            raise ValueError("milestone_already_claimed")
        now = utcnow()
        c.execute(
            "INSERT INTO rewards(telegram_id,reward_key,amount,created_at) VALUES (?,?,?,?)",
            (telegram_id, key, reward["dust"], now)
        )
        c.execute(
            "UPDATE users SET xp=xp+?,dust=dust+? WHERE telegram_id=?",
            (reward["xp"], reward["dust"], telegram_id)
        )
        return {"threshold": threshold, "xp": reward["xp"], "dust": reward["dust"]}


def spend_research_scout(telegram_id: int, candidate_ids):
    import secrets as _secrets
    ids = [str(x) for x in candidate_ids if x]
    if not ids:
        raise ValueError("collection_complete")
    now = utcnow_dt()
    day = now.date().isoformat()
    with conn() as c:
        c.execute("BEGIN IMMEDIATE")
        row_sql = "SELECT dust FROM users WHERE telegram_id=?" + (" FOR UPDATE" if is_postgres() else "")
        u = c.execute(row_sql, (telegram_id,)).fetchone()
        if not u:
            raise ValueError("user_not_found")
        existing = c.execute(
            "SELECT character_id FROM daily_scout_targets WHERE telegram_id=? AND day=?",
            (telegram_id, day)
        ).fetchone()
        if existing:
            return {"character_id": existing["character_id"], "spent_dust": 0, "existing": True}
        if int(u["dust"] or 0) < 2:
            raise ValueError("not_enough_dust")
        character_id = _secrets.choice(ids)
        c.execute("UPDATE users SET dust=dust-2 WHERE telegram_id=?", (telegram_id,))
        c.execute(
            "INSERT INTO daily_scout_targets(telegram_id,day,character_id,created_at) VALUES (?,?,?,?)",
            (telegram_id, day, character_id, now.isoformat())
        )
        c.execute(
            """INSERT INTO rewards(telegram_id,reward_key,amount,created_at)
               VALUES (?,?,?,?) ON CONFLICT(telegram_id,reward_key) DO NOTHING""",
            (telegram_id, f"scout:{day}", -2, now.isoformat())
        )
        return {"character_id": character_id, "spent_dust": 2, "existing": False}
