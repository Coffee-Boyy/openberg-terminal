"""SQLite database layer for user-managed data."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "openberg.db"


def get_db() -> sqlite3.Connection:
    """Return a configured SQLite connection."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """Create all tables if they do not exist."""
    conn = get_db()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS watchlist (
                id    INTEGER PRIMARY KEY,
                ticker  TEXT UNIQUE NOT NULL,
                name   TEXT,
                added_at TIMESTAMP DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS portfolio (
                id         INTEGER PRIMARY KEY,
                ticker     TEXT NOT NULL,
                shares     REAL NOT NULL,
                avg_cost   REAL NOT NULL,
                current_price REAL DEFAULT 0,
                added_at   TIMESTAMP DEFAULT (datetime('now')),
                updated_at TIMESTAMP DEFAULT (datetime('now')),
                UNIQUE(ticker)
            );

            CREATE TABLE IF NOT EXISTS alerts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker      TEXT NOT NULL,
                alert_type  TEXT NOT NULL,
                threshold   REAL NOT NULL,
                triggered   INTEGER DEFAULT 0,
                created_at  TIMESTAMP DEFAULT (datetime('now')),
                resolved_at TIMESTAMP
            );
        """)
        conn.commit()
    finally:
        conn.close()


# Initialize tables at import time so the DB is always ready,
# regardless of whether the lifespan fires (e.g. under test clients).
init_db()
