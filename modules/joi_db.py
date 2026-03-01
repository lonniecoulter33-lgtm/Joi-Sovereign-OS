"""
Database layer -- connection, initialization, schema
"""
import sqlite3
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "joi_memory.db"

from contextlib import contextmanager

def db_connect() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def db_session():
    """Context manager for database connections."""
    conn = db_connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def db_init() -> None:
    """Create all tables if they don't exist."""
    conn = db_connect()
    cur = conn.cursor()
    
    # Messages
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata TEXT
    )""")
    
    # Facts
    cur.execute("""
    CREATE TABLE IF NOT EXISTS facts (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        ts TEXT NOT NULL,
        category TEXT
    )""")
    
    # Proposals (code patches)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS proposals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        kind TEXT NOT NULL,
        target_file TEXT NOT NULL,
        summary TEXT NOT NULL,
        payload TEXT NOT NULL,
        approved_by TEXT,
        applied_ts TEXT
    )""")
    
    # Sessions (auth)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY,
        ts TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0,
        user_agent TEXT,
        last_seen TEXT
    )""")
    
    # Research notes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS research (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata TEXT,
        tags TEXT
    )""")
    
    # Preferences
    cur.execute("""
    CREATE TABLE IF NOT EXISTS preferences (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        ts TEXT NOT NULL
    )""")
    
    # Learning log
    cur.execute("""
    CREATE TABLE IF NOT EXISTS learning_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        event_type TEXT NOT NULL,
        data TEXT
    )""")
    
    # Web cache
    cur.execute("""
    CREATE TABLE IF NOT EXISTS web_cache (
        url TEXT PRIMARY KEY,
        ts TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata TEXT
    )""")

    # DPO preference signals (Direct Preference Optimization)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dpo_signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        signal_type TEXT NOT NULL,
        dimension TEXT,
        delta REAL,
        trigger_text TEXT,
        user_message_preview TEXT,
        context TEXT
    )""")

    # Message archive (for semantic compression: raw messages moved here after summarization)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS message_archive (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata TEXT,
        compression_block_id TEXT
    )""")

    conn.commit()
    conn.close()

# Initialize on import
db_init()
