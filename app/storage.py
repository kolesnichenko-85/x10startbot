import os
import re
import sqlite3
from contextlib import contextmanager

try:
    import psycopg
    from psycopg.rows import dict_row
    from psycopg import errors as pg_errors
except Exception:
    psycopg = None
    dict_row = None
    pg_errors = None

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
DB_PATH = os.getenv("DATABASE_PATH", "/data/drop1.db")
POSTGRES = DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://")


def is_postgres() -> bool:
    return POSTGRES


def _pg_sql(sql: str) -> str:
    s = sql.strip()
    if s.upper() == "BEGIN IMMEDIATE":
        return "BEGIN"
    # All app SQL uses qmark placeholders. No literal ? characters are used in statements.
    return sql.replace("?", "%s")


class DB:
    def __init__(self, raw, postgres: bool):
        self.raw = raw
        self.postgres = postgres

    def execute(self, sql, params=()):
        if self.postgres:
            return self.raw.execute(_pg_sql(sql), params)
        return self.raw.execute(sql, params)

    def executemany(self, sql, seq):
        if self.postgres:
            return self.raw.executemany(_pg_sql(sql), seq)
        return self.raw.executemany(sql, seq)

    def executescript(self, script: str):
        if not self.postgres:
            return self.raw.executescript(script)
        # DROP1 Postgres schema intentionally contains no procedural blocks;
        # semicolon splitting is therefore safe here.
        for stmt in script.split(";"):
            stmt = stmt.strip()
            if stmt:
                self.raw.execute(stmt)


if pg_errors:
    INTEGRITY_ERRORS = (sqlite3.IntegrityError, pg_errors.IntegrityError)
else:
    INTEGRITY_ERRORS = (sqlite3.IntegrityError,)


@contextmanager
def conn():
    if POSTGRES:
        if psycopg is None:
            raise RuntimeError("DATABASE_URL is Postgres but psycopg is not installed")
        c = psycopg.connect(DATABASE_URL, row_factory=dict_row, autocommit=False)
        db = DB(c, True)
        try:
            yield db
            c.commit()
        except Exception:
            c.rollback()
            raise
        finally:
            c.close()
        return

    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    c = sqlite3.connect(DB_PATH, timeout=20)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    db = DB(c, False)
    try:
        yield db
        c.commit()
    except Exception:
        c.rollback()
        raise
    finally:
        c.close()


def database_backend() -> str:
    return "postgres" if POSTGRES else "sqlite"
