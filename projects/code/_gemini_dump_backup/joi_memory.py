import os
import sqlite3
import secrets
from datetime import datetime, timezone

from flask import request, has_request_context


# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "joi_memory.db")


# -------------------------
# DB helpers
# -------------------------
def _utc_ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def db_connect():
    # check_same_thread=False helps if Flask is threaded/reloader is on
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    """
    Create tables if missing. This will not modify existing schemas,
    but it WILL ensure required tables exist for the app to run.
    """
    con = db_connect()
    cur = con.cursor()

    # Messages (chat history)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            ts TEXT NOT NULL
        )
        """
    )

    # Sessions
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            ts TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0,
            user_agent TEXT,
            last_seen TEXT
        )
        """
    )

    # Pending ops for patching/self-edit proposals
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS pending_ops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            actor TEXT,
            kind TEXT NOT NULL,
            target TEXT,
            payload TEXT,
            status TEXT NOT NULL DEFAULT 'pending'
        )
        """
    )

    con.commit()
    con.close()


# Initialize on import
init_db()


# -------------------------
# Sessions
# -------------------------
def create_session(is_admin: bool = False, user_agent: str | None = None) -> str:
    token = secrets.token_urlsafe(32)
    ts = _utc_ts()

    con = db_connect()
    con.execute(
        """
        INSERT INTO sessions (token, ts, is_admin, user_agent, last_seen)
        VALUES (?, ?, ?, ?, ?)
        """,
        (token, ts, 1 if is_admin else 0, user_agent, ts),
    )
    con.commit()
    con.close()
    return token


def verify_session(token: str | None) -> dict | None:
    if not token:
        return None

    con = db_connect()
    cur = con.cursor()
    cur.execute(
        "SELECT token, is_admin, user_agent, last_seen FROM sessions WHERE token = ?",
        (token,),
    )
    row = cur.fetchone()
    if not row:
        con.close()
        return None

    now = _utc_ts()
    cur.execute("UPDATE sessions SET last_seen = ? WHERE token = ?", (now, token))
    con.commit()
    con.close()

    return {
        "token": row[0],
        "is_admin": bool(row[1]),
        "user_agent": row[2],
        "last_seen": row[3],
    }


def destroy_session(token: str | None):
    if not token:
        return
    con = db_connect()
    con.execute("DELETE FROM sessions WHERE token = ?", (token,))
    con.commit()
    con.close()


# -------------------------
# Request token extraction
# -------------------------
def _get_token_from_request() -> str | None:
    if not has_request_context():
        return None

    # Authorization: Bearer <token>
    auth = request.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        return auth.split(None, 1)[1].strip()

    # Custom header
    tok = request.headers.get("X-Session-Token")
    if tok:
        return tok.strip()

    # Cookies
    tok = (
        request.cookies.get("joi_session")
        or request.cookies.get("session")
        or request.cookies.get("token")
    )
    if tok:
        return tok.strip()

    # JSON body
    data = request.get_json(silent=True) or {}
    tok = data.get("token") or data.get("session") or data.get("session_token")
    if tok:
        return str(tok).strip()

    return None


def require_user(session: dict | None = None) -> dict | None:
    """
    Compatible with BOTH:
      session = require_user()
      session = require_user(existing_session)
    Returns a session dict or None.
    """
    if session is None:
        token = _get_token_from_request()
        session = verify_session(token)

    if not session:
        return None

    return session


def require_admin(session: dict | None = None) -> dict | None:
    session = require_user(session)
    if not session:
        return None
    if not session.get("is_admin"):
        return None
    return session


# -------------------------
# Chat memory
# -------------------------
def save_message(role: str, content: str):
    ts = _utc_ts()
    con = db_connect()
    con.execute(
        "INSERT INTO messages (role, content, ts) VALUES (?, ?, ?)",
        (role, content, ts),
    )
    con.commit()
    con.close()


def recent_messages(limit: int = 20) -> list[dict]:
    con = db_connect()
    cur = con.cursor()
    cur.execute(
        "SELECT role, content, ts FROM messages ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    con.close()

    rows.reverse()
    return [{"role": r[0], "content": r[1], "ts": r[2]} for r in rows]


# -------------------------
# Pending ops (patch proposals)
# -------------------------
def add_pending_op(kind: str, target: str | None = None, payload: str | None = None, actor: str | None = None) -> int:
    """
    Used by joi_patching.py to queue up file changes / ops for approval.
    """
    ts = _utc_ts()
    con = db_connect()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO pending_ops (ts, actor, kind, target, payload, status)
        VALUES (?, ?, ?, ?, ?, 'pending')
        """,
        (ts, actor, kind, target, payload),
    )
    con.commit()
    op_id = int(cur.lastrowid)
    con.close()
    return op_id


def list_pending_ops(status: str = "pending", limit: int = 50) -> list[dict]:
    con = db_connect()
    cur = con.cursor()
    cur.execute(
        """
        SELECT id, ts, actor, kind, target, payload, status
        FROM pending_ops
        WHERE status = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (status, limit),
    )
    rows = cur.fetchall()
    con.close()

    return [
        {
            "id": r[0],
            "ts": r[1],
            "actor": r[2],
            "kind": r[3],
            "target": r[4],
            "payload": r[5],
            "status": r[6],
        }
        for r in rows
    ]


def set_pending_op_status(op_id: int, status: str):
    con = db_connect()
    con.execute("UPDATE pending_ops SET status = ? WHERE id = ?", (status, op_id))
    con.commit()
    con.close()
