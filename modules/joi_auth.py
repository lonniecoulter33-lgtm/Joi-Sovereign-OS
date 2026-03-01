
import os
import hmac
import hashlib
import secrets
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict
from flask import request, abort

APP_SECRET = os.getenv("JOI_APP_SECRET", "joi-secret-change-me")

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def sign_token(token: str) -> str:
    mac = hmac.new(APP_SECRET.encode("utf-8"), token.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{token}.{mac}"

def verify_signed_token(signed: str) -> Optional[str]:
    if "." not in signed: return None
    parts = signed.rsplit(".", 1)
    if len(parts) != 2: return None
    token, mac = parts
    expected_mac = hmac.new(APP_SECRET.encode("utf-8"), token.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(mac, expected_mac): return None
    return token

def create_session(is_admin: bool = False) -> str:
    from modules.joi_db import db_session
    token = secrets.token_urlsafe(32)
    signed = sign_token(token)
    with db_session() as conn:
        conn.execute("INSERT INTO sessions (token, ts, is_admin, last_seen) VALUES (?, ?, ?, ?)",
                     (token, _now_iso(), 1 if is_admin else 0, _now_iso()))
    return signed

def verify_session(signed_token: str) -> Optional[Dict]:
    from modules.joi_db import db_session
    token = verify_signed_token(signed_token)
    if not token: return None
    with db_session() as conn:
        row = conn.execute("SELECT * FROM sessions WHERE token = ?", (token,)).fetchone()
        if row:
            conn.execute("UPDATE sessions SET last_seen = ? WHERE token = ?", (_now_iso(), token))
    return dict(row) if row else None

def require_user():
    token = request.cookies.get('joi_session')
    if not token: abort(401)
    session = verify_session(token)
    if not session: abort(401)
    return session

def require_admin():
    session = require_user()
    if not session.get('is_admin'): abort(403)
    return session
