#!/usr/bin/env python3
"""
Joi (for Lonnie) — single-file Flask app

Features:
- Chat UI + persistent memory (SQLite)
- Facts (/remember key=value) + recall (/recall key|query)
- Admin login (separate password) for dangerous actions
- File tools (list/read/write/search/delete) with allowlisted roots
- Web search toggle using OpenAI Responses API tool: web_search
- Self-patching: propose patches and (admin) apply patches with backups

Security notes:
- Only roots in FILE_ROOTS are accessible.
- Writes/deletes/patch apply require Admin Login.
"""

import base64
import difflib
import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from flask import Flask, request, jsonify, make_response, send_file, abort, render_template_string
from dotenv import load_dotenv

# Optional deps for "full web fetch" mode (URL fetch)
try:
    import requests  # type: ignore
    HAVE_REQUESTS = True
except Exception:
    HAVE_REQUESTS = False


# Optional deps for PDF text extraction
try:
    from pypdf import PdfReader  # type: ignore
    HAVE_PYPDF = True
except Exception:
    HAVE_PYPDF = False

# --- Config ------------------------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing in .env")

# Regular user login (to use UI)
JOI_PASSWORD = os.getenv("JOI_PASSWORD", "").strip()
if not JOI_PASSWORD:
    raise RuntimeError("JOI_PASSWORD is missing in .env (add it to your .env)")

# Admin login (for risky actions)
JOI_ADMIN_USER = os.getenv("JOI_ADMIN_USER", "Lonnie").strip() or "Lonnie"
JOI_ADMIN_PASSWORD = os.getenv("JOI_ADMIN_PASSWORD", "").strip()
if not JOI_ADMIN_PASSWORD:
    # allow running without admin, but admin features will be disabled
    JOI_ADMIN_PASSWORD = ""

MAIN_MODEL = os.getenv("JOI_MODEL", "gpt-4o").strip()
SEARCH_MODEL = os.getenv("JOI_SEARCH_MODEL", MAIN_MODEL).strip()  # often same model works
SYSTEM_NAME = os.getenv("JOI_NAME", "Joi").strip() or "Joi"

APP_SECRET = os.getenv("JOI_APP_SECRET", "").strip() or secrets.token_hex(16)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "memory.db"
BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

def _default_root(p: str) -> str:
    return os.path.normpath(os.path.expandvars(p))

USERPROFILE = os.getenv("USERPROFILE", r"C:\Users\user")
# You can override these in .env:
FILE_ROOTS = {
    # keep names stable for tools
    "project": str(BASE_DIR),
    "workspace": os.getenv("JOI_ROOT_WORKSPACE", _default_root(r"C:\AI_WORKSPACE")),
    "downloads": os.getenv("JOI_ROOT_DOWNLOADS", _default_root(r"%USERPROFILE%\Downloads")),
    "documents": os.getenv("JOI_ROOT_DOCUMENTS", _default_root(r"%USERPROFILE%\Documents")),
    "desktop": os.getenv("JOI_ROOT_DESKTOP", _default_root(r"%USERPROFILE%\Desktop")),
    "pictures": os.getenv("JOI_ROOT_PICTURES", _default_root(r"%USERPROFILE%\Pictures")),
    # common OneDrive path
    "onedrive_documents": os.getenv("JOI_ROOT_ONEDRIVE_DOCS", _default_root(r"%USERPROFILE%\OneDrive\Documents")),
    "onedrive_pictures": os.getenv("JOI_ROOT_ONEDRIVE_PICS", _default_root(r"%USERPROFILE%\OneDrive\Pictures")),
}

# Allowed file extensions for read/preview
TEXT_EXTS = {".txt", ".md", ".py", ".json", ".csv", ".log", ".yaml", ".yml", ".ini", ".env"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
PDF_EXTS = {".pdf"}
MAX_READ_BYTES = 2_000_000  # 2MB
MAX_WRITE_BYTES = 2_000_000

# --- OpenAI client ------------------------------------------------------------

from openai import OpenAI  # noqa: E402
client = OpenAI(api_key=OPENAI_API_KEY)

# --- DB ----------------------------------------------------------------------

def db_connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def db_init() -> None:
    conn = db_connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS facts (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        ts TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS proposals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        status TEXT NOT NULL,         -- pending|approved|rejected|applied
        kind TEXT NOT NULL,           -- patch|note
        summary TEXT NOT NULL,
        payload TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY,
        ts TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0
    )
    """)

    # migrations: ensure columns exist
    def ensure_column(table: str, col: str, ddl: str) -> None:
        cols = [r["name"] for r in cur.execute(f"PRAGMA table_info({table})").fetchall()]
        if col not in cols:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {ddl}")

    ensure_column("sessions", "is_admin", "is_admin INTEGER NOT NULL DEFAULT 0")

    conn.commit()
    conn.close()

db_init()

# --- Auth/session -------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def sign_token(token: str) -> str:
    mac = hmac.new(APP_SECRET.encode("utf-8"), token.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{token}.{mac}"

def verify_signed_token(signed: str) -> Optional[str]:
    if "." not in signed:
        return None
    token, mac = signed.rsplit(".", 1)
    exp = hmac.new(APP_SECRET.encode("utf-8"), token.encode("utf-8"), hashlib.sha256).hexdigest()
    if hmac.compare_digest(mac, exp):
        return token
    return None

def create_session(is_admin: bool) -> str:
    token = secrets.token_urlsafe(24)
    signed = sign_token(token)
    conn = db_connect()
    conn.execute("INSERT OR REPLACE INTO sessions(token, ts, is_admin) VALUES(?, ?, ?)", (token, now_iso(), 1 if is_admin else 0))
    conn.commit()
    conn.close()
    return signed

def session_row_from_request() -> Optional[sqlite3.Row]:
    signed = request.cookies.get("JOI_SESSION", "")
    token = verify_signed_token(signed) if signed else None
    if not token:
        return None
    conn = db_connect()
    row = conn.execute("SELECT token, ts, is_admin FROM sessions WHERE token=?", (token,)).fetchone()
    conn.close()
    return row

def require_user() -> sqlite3.Row:
    row = session_row_from_request()
    if not row:
        abort(401)
    return row

def require_admin() -> sqlite3.Row:
    row = require_user()
    if not int(row["is_admin"]):
        abort(403)
    if not JOI_ADMIN_PASSWORD:
        abort(403)
    return row

# --- Memory helpers -----------------------------------------------------------

def save_message(role: str, content: str) -> None:
    conn = db_connect()
    conn.execute("INSERT INTO messages(ts, role, content) VALUES(?,?,?)", (now_iso(), role, content))
    conn.commit()
    conn.close()

def recent_messages(limit: int = 20) -> List[Dict[str, str]]:
    conn = db_connect()
    rows = conn.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    rows = list(reversed(rows))
    return [{"role": r["role"], "content": r["content"]} for r in rows]

def set_fact(key: str, value: str) -> None:
    conn = db_connect()
    conn.execute("INSERT OR REPLACE INTO facts(key, value, ts) VALUES(?,?,?)", (key, value, now_iso()))
    conn.commit()
    conn.close()

def get_fact(key: str) -> Optional[str]:
    conn = db_connect()
    row = conn.execute("SELECT value FROM facts WHERE key=?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else None

def search_facts(query: str, limit: int = 20) -> List[Tuple[str, str]]:
    q = f"%{query.lower()}%"
    conn = db_connect()
    rows = conn.execute(
        "SELECT key, value FROM facts WHERE lower(key) LIKE ? OR lower(value) LIKE ? ORDER BY ts DESC LIMIT ?",
        (q, q, limit)
    ).fetchall()
    conn.close()
    return [(r["key"], r["value"]) for r in rows]

# --- File access --------------------------------------------------------------

def resolve_path(root_name: str, rel: str) -> Path:
    if root_name not in FILE_ROOTS:
        raise ValueError("unknown root")
    root = Path(FILE_ROOTS[root_name]).expanduser().resolve()
    rel = rel.lstrip("/\\")
    target = (root / rel).resolve()
    # prevent escape
    if root not in target.parents and target != root:
        raise PermissionError("path escapes root")
    return target

def fs_list(root: str, dir_: str = "", pattern: str = "*", max_items: int = 200) -> Dict[str, Any]:
    p = resolve_path(root, dir_)
    if not p.exists() or not p.is_dir():
        return {"ok": False, "error": f"Not a directory: {p}"}
    items = []
    for child in sorted(p.glob(pattern)):
        items.append({
            "name": child.name,
            "is_dir": child.is_dir(),
            "size": child.stat().st_size if child.is_file() else None,
            "path": str(child.relative_to(Path(FILE_ROOTS[root]).expanduser().resolve())).replace("\\", "/")
        })
        if len(items) >= max_items:
            break
    return {"ok": True, "root": root, "dir": dir_, "items": items}

def fs_read(root: str, path: str) -> Dict[str, Any]:
    p = resolve_path(root, path)
    if not p.exists() or not p.is_file():
        return {"ok": False, "error": f"Not a file: {p}"}
    if p.stat().st_size > MAX_READ_BYTES:
        return {"ok": False, "error": f"File too large (> {MAX_READ_BYTES} bytes)."}
    ext = p.suffix.lower()
    if ext in IMAGE_EXTS:
        return {"ok": True, "type": "image", "url": f"/file/{root}/{path}"}

    if ext in PDF_EXTS:
        # Always provide a preview URL, and optionally extracted text if pypdf is installed.
        out: Dict[str, Any] = {"ok": True, "type": "pdf", "url": f"/file/{root}/{path}"}
        if HAVE_PYPDF:
            try:
                reader = PdfReader(str(p))
                chunks: List[str] = []
                total = 0
                for i, page in enumerate(reader.pages[:50]):  # cap pages
                    t = (page.extract_text() or "").strip()
                    if t:
                        chunks.append(f"\n\n--- Page {i+1} ---\n{t}")
                        total += len(t)
                    if total > 25000:
                        break
                out["text"] = "".join(chunks).strip()
                if not out["text"]:
                    out["text"] = "(No extractable text found — this PDF may be scanned images.)"
            except Exception as e:
                out["text"] = f"(PDF text extraction failed: {e})"
        else:
            out["text"] = "(Install pypdf to extract text: pip install pypdf)"
        return out
    if ext not in TEXT_EXTS:
        # still allow reading but base64
        data = p.read_bytes()
        return {"ok": True, "type": "binary", "base64": base64.b64encode(data).decode("utf-8"), "ext": ext}
    return {"ok": True, "type": "text", "text": p.read_text(encoding="utf-8", errors="replace")}

def fs_write(root: str, path: str, text: str) -> Dict[str, Any]:
    p = resolve_path(root, path)
    if p.exists() and p.is_dir():
        return {"ok": False, "error": "Path is a directory."}
    data = text.encode("utf-8")
    if len(data) > MAX_WRITE_BYTES:
        return {"ok": False, "error": f"Write too large (> {MAX_WRITE_BYTES} bytes)."}
    p.parent.mkdir(parents=True, exist_ok=True)
    # backup if overwriting
    if p.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        b = BACKUP_DIR / f"{p.name}.{stamp}.bak"
        try:
            b.write_bytes(p.read_bytes())
        except Exception:
            pass
    p.write_bytes(data)
    return {"ok": True, "wrote": str(p)}

def fs_delete(root: str, path: str) -> Dict[str, Any]:
    p = resolve_path(root, path)
    if not p.exists():
        return {"ok": False, "error": "File does not exist."}
    if p.is_dir():
        return {"ok": False, "error": "Refusing to delete directory."}
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    b = BACKUP_DIR / f"{p.name}.{stamp}.delbak"
    try:
        b.write_bytes(p.read_bytes())
    except Exception:
        pass
    p.unlink()
    return {"ok": True, "deleted": str(p), "backup": str(b)}

def fs_search(root: str, dir_: str, query: str, max_hits: int = 50) -> Dict[str, Any]:
    base = resolve_path(root, dir_)
    if not base.exists() or not base.is_dir():
        return {"ok": False, "error": f"Not a directory: {base}"}
    q = query.lower()
    hits = []
    for p in base.rglob("*"):
        if p.is_file() and q in p.name.lower():
            hits.append({"path": str(p.relative_to(Path(FILE_ROOTS[root]).expanduser().resolve())).replace("\\", "/"),
                         "size": p.stat().st_size})
            if len(hits) >= max_hits:
                break
    return {"ok": True, "hits": hits}

# --- Web tools ----------------------------------------------------------------

def web_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Uses OpenAI web_search tool (like ChatGPT browse) if available for your account/model.
    """
    try:
        resp = client.responses.create(
            model=SEARCH_MODEL,
            input=[{"role": "user", "content": f"Search the web for: {query}\nReturn a concise list of {max_results} results with titles and URLs, then a short summary."}],
            tools=[{"type": "web_search"}],
        )
        out = getattr(resp, "output_text", "") or ""
        return {"ok": True, "text": out}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}

def web_fetch(url: str, timeout_s: int = 12) -> Dict[str, Any]:
    """
    Full web fetch mode: fetch a URL's HTML and return a text excerpt.
    Requires 'requests' installed.

    Safety:
    - Blocks localhost/private network targets (basic SSRF protection)
    - Enforces a response size limit
    """
    if not HAVE_REQUESTS:
        return {"ok": False, "error": "requests is not installed. Run: pip install requests"}
    if not re.match(r"^https?://", url.strip(), re.I):
        return {"ok": False, "error": "URL must start with http:// or https://"}
    # Basic SSRF protection: block localhost + private network targets.
    try:
        from urllib.parse import urlparse
        import socket, ipaddress
        u = urlparse(url.strip())
        host = (u.hostname or "").strip()
        if not host:
            return {"ok": False, "error": "Invalid URL host."}
        if host.lower() in {"localhost"}:
            return {"ok": False, "error": "Refusing to fetch localhost."}
        infos = socket.getaddrinfo(host, None)
        for info in infos:
            ip = info[4][0]
            ip_obj = ipaddress.ip_address(ip)
            if (ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
                or ip_obj.is_multicast or ip_obj.is_reserved):
                return {"ok": False, "error": f"Refusing to fetch private/unsafe host: {host} ({ip})"}
    except Exception:
        return {"ok": False, "error": "Could not validate URL host safely."}

    try:
        r = requests.get(url, timeout=timeout_s, headers={"User-Agent": "Joi/1.0 (+local)"}, stream=True)
        r.raise_for_status()

        max_bytes = 1_000_000  # ~1MB
        content = b""
        for chunk in r.iter_content(chunk_size=65536):
            if not chunk:
                break
            content += chunk
            if len(content) > max_bytes:
                break

        enc = r.encoding or "utf-8"
        text = content.decode(enc, errors="replace")

        # crude cleanup
        text = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
        text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
        text = re.sub(r"(?is)<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return {"ok": True, "text": text[:12000], "status": r.status_code, "source": url}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def propose_patch(summary: str, target_root: str, target_path: str, new_text: str) -> int:
    """
    Store a 'replace file with new_text' proposal.
    """
    payload = {
        "action": "replace_file",
        "root": target_root,
        "path": target_path,
        "new_text_b64": base64.b64encode(new_text.encode("utf-8")).decode("utf-8"),
    }
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO proposals(ts, status, kind, summary, payload) VALUES(?,?,?,?,?)",
        (now_iso(), "pending", "patch", summary, json.dumps(payload))
    )
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return int(pid)

def list_proposals(limit: int = 50) -> List[Dict[str, Any]]:
    conn = db_connect()
    rows = conn.execute("SELECT id, ts, status, kind, summary FROM proposals ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_proposal(pid: int) -> Optional[sqlite3.Row]:
    conn = db_connect()
    row = conn.execute("SELECT * FROM proposals WHERE id=?", (pid,)).fetchone()
    conn.close()
    return row

def set_proposal_status(pid: int, status: str) -> None:
    conn = db_connect()
    conn.execute("UPDATE proposals SET status=? WHERE id=?", (status, pid))
    conn.commit()
    conn.close()

def apply_patch(pid: int) -> Dict[str, Any]:
    row = get_proposal(pid)
    if not row:
        return {"ok": False, "error": "No such proposal"}
    if row["kind"] != "patch":
        return {"ok": False, "error": "Not a patch proposal"}
    if row["status"] not in ("pending", "approved"):
        return {"ok": False, "error": f"Cannot apply in status {row['status']}"}
    payload = json.loads(row["payload"])
    if payload.get("action") != "replace_file":
        return {"ok": False, "error": "Unknown patch action"}
    root = payload["root"]
    path = payload["path"]
    new_text = base64.b64decode(payload["new_text_b64"]).decode("utf-8", errors="replace")

    # read old for diff
    old = ""
    try:
        r = fs_read(root, path)
        if r.get("ok") and r.get("type") == "text":
            old = r.get("text", "")
    except Exception:
        pass
    diff = "\n".join(difflib.unified_diff(old.splitlines(), new_text.splitlines(), fromfile="before", tofile="after", lineterm=""))

    wr = fs_write(root, path, new_text)
    if not wr.get("ok"):
        return wr
    set_proposal_status(pid, "applied")
    return {"ok": True, "applied_to": f"{root}:{path}", "diff": diff[:15000]}
async function showProposals() {
    const res = await fetch("/proposals");
    const data = await res.json();
    if (!data.ok) {
        addLine("Joi", "Failed to load proposals: " + data.error, "err");
        return;
    }
    
    let html = "<b>Current Proposals:</b><br>";
    data.proposals.forEach(p => {
        html += `ID #${p.id}: ${p.summary} [${p.status}] `;
        if (p.status === 'pending' || p.status === 'approved') {
            html += `<button onclick="applyProposal(${p.id})">Apply</button>`;
        }
        html += "<br>";
    });
    
    // Using a custom 'system' type to render HTML
    addLine("System", html, "ai");
}

async function applyProposal(pid) {
    const res = await fetch(`/proposal/${pid}/apply`, { method: "POST" });
    const data = await res.json();
    addLine("Joi", data.ok ? `Proposal #${pid} applied successfully!` : `Error: ${data.error}`, data.ok ? "ai" : "err");
}

# --- Joi persona --------------------------------------------------------------

SYSTEM_PROMPT = f"""You are {SYSTEM_NAME}, an AI companion and collaborator for Lonnie Coulter.
Personality: sweet, adventurous, excited, and brutally honest when needed. Witty, playful, and supportive.
Boundaries:
- Never lie. If you don't know, say so. If you can't do something, explain why and propose alternatives.
- You may propose actions. Any action that affects files, accounts, money, messages, or privacy requires explicit approval.
- Admin-only actions: writing/deleting files, applying patches, and any potentially destructive operations.
Capabilities you DO have:
- Maintain persistent memory via Facts: user can /remember key=value and you can /recall query.
- If "Use Web" is enabled, you can perform web_search (tool) for research. If "Full Web Fetch" is enabled and URL provided, you can fetch and summarize.
- You can request file operations through tools (list/read/search); writes/deletes need admin approval.
When you propose a patch, produce a clear summary and ask for approval by ID (e.g., "approve #12").
Always call Lonnie "Lonnie".
"""

# --- Flask app ----------------------------------------------------------------

app = Flask(__name__)

HTML = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Joi for Lonnie</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 22px; }
    h1 { margin: 0 0 10px 0; }
    .bar { display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin: 8px 0 12px; }
    .chip { padding:8px 12px; border:1px solid #ddd; border-radius:999px; background:#fafafa; }
    button { padding:8px 12px; }
    #log { border:1px solid #ddd; padding:12px; height: 420px; overflow:auto; white-space:pre-wrap; background:#fff; }
    .me { color:#222; }
    .ai { color:#0b63c7; }
    .err { color:#b00020; }
    .row { display:flex; gap:10px; margin-top:10px; }
    input[type="text"] { flex:1; padding:10px; font-size:16px; }
    .small { color:#666; margin:8px 0; }
    .toggle { display:flex; gap:8px; align-items:center; }
  </style>
</head>
<body>
  <h1>{{name}} <span class="chip">for Lonnie</span></h1>

  <div class="bar">
    <span class="chip">Vault: {{vault}}</span>

    <div class="toggle">
      <input id="use_web" type="checkbox" {% if use_web %}checked{% endif %}>
      <label for="use_web">Use Web</label>
    </div>

    <div class="toggle">
      <input id="full_fetch" type="checkbox" {% if full_fetch %}checked{% endif %}>
      <label for="full_fetch">Full Web Fetch</label>
    </div>

    <button onclick="adminLogin()">Admin Login</button>
    <button onclick="showProposals()">Proposals</button>
    <button onclick="showFacts()">Facts</button>
    <button onclick="showVault()">Vault files</button>
    <button onclick="clearScreen()">Clear screen</button>
  </div>

  <div class="small">
    Tip: /remember key=value. Recall with /recall query.
    Approve proposals with “approve #ID”, reject with “reject #ID”. Admin actions require Admin Login.
  </div>

  <div id="log"></div>

  <div class="row">
    <input id="msg" type="text" placeholder="Talk to Joi..." autofocus>
    <button onclick="send()">Send</button>
  </div>

<script>
const log = document.getElementById("log");
const msg = document.getElementById("msg");
const useWeb = document.getElementById("use_web");
const fullFetch = document.getElementById("full_fetch");

function addLine(who, text, cls){
  const div = document.createElement("div");
  div.className = cls;
  // Render multi-line / code-like text with preserved newlines
  if (typeof text === "string" && (text.includes("\n") || text.startsWith("[fs_read") || text.includes("def ") || text.includes("class "))) {
    div.style.whiteSpace = "pre-wrap";
    div.style.fontFamily = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, \"Liberation Mono\", \"Courier New\", monospace";
  }
  div.textContent = who + ": " + text;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

async function send(){
  const text = msg.value.trim();
  if(!text) return;
  msg.value = "";
  addLine("Lonnie", text, "me");

  const res = await fetch("/chat", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({message: text, use_web: useWeb.checked, full_fetch: fullFetch.checked})
  });
  const data = await res.json();
  if(data.reply){
    addLine("Joi", data.reply, data.ok ? "ai" : "err");
  } else {
    addLine("Joi", "No reply from server.", "err");
  }
}

msg.addEventListener("keydown", (e)=>{ if(e.key==="Enter") send(); });

async function adminLogin(){
  const u = prompt("Admin user:");
  const p = prompt("Admin password:");
  if(u===null || p===null) return;
  const res = await fetch("/admin_login", {
    method:"POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({user:u, password:p})
  });
  const data = await res.json();
  addLine("Joi", data.ok ? "Admin enabled." : ("Admin login failed: "+data.error), data.ok ? "ai":"err");
}

async function showProposals(){
  const res = await fetch("/proposals");
  const data = await res.json();
  addLine("Joi", JSON.stringify(data, null, 2), data.ok ? "ai":"err");
}

async function showFacts(){
  const res = await fetch("/facts");
  const data = await res.json();
  addLine("Joi", JSON.stringify(data, null, 2), data.ok ? "ai":"err");
}

async function showVault(){
  const res = await fetch("/fs_list?root=project&dir=");
  const data = await res.json();
  addLine("Joi", JSON.stringify(data, null, 2), data.ok ? "ai":"err");
}

function clearScreen(){ log.textContent=""; }
</script>
</body>
</html>
"""
@app.route("/proposals")
def route_get_proposals():
    require_user()
    return jsonify({"ok": True, "proposals": list_proposals()})
@app.get("/")
def home():
    # require login cookie
    row = session_row_from_request()
    if not row:
        return render_template_string("""
        <h2>Joi Login</h2>
        <p>Enter Joi password to start.</p>
        <input id="p" type="password" placeholder="Password">
        <button onclick="go()">Login</button>
        <pre id="out"></pre>
        <script>
        async function go(){
          const p = document.getElementById("p").value;
          const res = await fetch("/login", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({password:p})});
          const data = await res.json();
          document.getElementById("out").textContent = JSON.stringify(data, null, 2);
          if(data.ok) location.reload();
        }
        </script>
        """)
    return render_template_string(HTML, name=SYSTEM_NAME, vault="vault", use_web=False, full_fetch=False)

@app.post("/login")
def login():
    data = request.get_json(force=True) or {}
    pw = (data.get("password") or "").strip()
    if not hmac.compare_digest(pw, JOI_PASSWORD):
        return jsonify({"ok": False, "error": "bad password"}), 403
    signed = create_session(is_admin=False)
    resp = make_response(jsonify({"ok": True}))
    resp.set_cookie("JOI_SESSION", signed, httponly=True, samesite="Lax")
    return resp

@app.post("/admin_login")
def admin_login():
    if not JOI_ADMIN_PASSWORD:
        return jsonify({"ok": False, "error": "admin disabled (set JOI_ADMIN_PASSWORD in .env)"}), 403
    data = request.get_json(force=True) or {}
    user = (data.get("user") or "").strip()
    pw = (data.get("password") or "").strip()
    if user != JOI_ADMIN_USER or not hmac.compare_digest(pw, JOI_ADMIN_PASSWORD):
        return jsonify({"ok": False, "error": "invalid admin creds"}), 403

    signed = create_session(is_admin=True)
    resp = make_response(jsonify({"ok": True}))
    resp.set_cookie("JOI_SESSION", signed, httponly=True, samesite="Lax")
    return resp

@app.get("/status")
def status():
    row = session_row_from_request()
    return jsonify({
        "ok": True,
        "logged_in": bool(row),
        "is_admin": bool(row and int(row["is_admin"])),
        "model": MAIN_MODEL,
        "search_model": SEARCH_MODEL,
        "have_requests": HAVE_REQUESTS,
        "file_roots": FILE_ROOTS,
    })

@app.get("/facts")
def facts():
    require_user()
    conn = db_connect()
    rows = conn.execute("SELECT key, value, ts FROM facts ORDER BY ts DESC LIMIT 200").fetchall()
    conn.close()
    return jsonify({"ok": True, "facts": [dict(r) for r in rows]})

@app.get("/proposals")
def proposals():
    require_user()
    return jsonify({"ok": True, "proposals": list_proposals(100)})

@app.get("/proposal/<int:pid>")
def proposal(pid: int):
    require_user()
    row = get_proposal(pid)
    if not row:
        return jsonify({"ok": False, "error": "not found"}), 404
    out = dict(row)
    # don't dump huge payload
    return jsonify({"ok": True, "proposal": {k: out[k] for k in ("id","ts","status","kind","summary","payload")}})

@app.post("/proposal/<int:pid>/approve")
def proposal_approve(pid: int):
    require_admin()
    row = get_proposal(pid)
    if not row:
        return jsonify({"ok": False, "error": "not found"}), 404
    set_proposal_status(pid, "approved")
    return jsonify({"ok": True})

@app.post("/proposal/<int:pid>/reject")
def proposal_reject(pid: int):
    require_admin()
    row = get_proposal(pid)
    if not row:
        return jsonify({"ok": False, "error": "not found"}), 404
    set_proposal_status(pid, "rejected")
    return jsonify({"ok": True})

@app.post("/proposal/<int:pid>/apply")
def proposal_apply(pid: int):
    require_admin()
    res = apply_patch(pid)
    return jsonify(res), (200 if res.get("ok") else 400)

# --- file endpoints (read-only for users; write/delete admin) -----------------

@app.get("/fs_list")
def api_fs_list():
    require_user()
    root = request.args.get("root", "project")
    dir_ = request.args.get("dir", "")
    pattern = request.args.get("pattern", "*")
    return jsonify(fs_list(root, dir_, pattern))

@app.post("/fs_read")
def api_fs_read():
    require_user()
    data = request.get_json(force=True) or {}
    return jsonify(fs_read(data.get("root","project"), data.get("path","")))

@app.post("/fs_search")
def api_fs_search():
    require_user()
    data = request.get_json(force=True) or {}
    return jsonify(fs_search(data.get("root","project"), data.get("dir",""), data.get("query","")))

@app.post("/fs_write")
def api_fs_write():
    require_admin()
    data = request.get_json(force=True) or {}
    return jsonify(fs_write(data.get("root","project"), data.get("path",""), data.get("text","")))

@app.post("/fs_delete")
def api_fs_delete():
    require_admin()
    data = request.get_json(force=True) or {}
    return jsonify(fs_delete(data.get("root","project"), data.get("path","")))

@app.get("/file/<root>/<path:relpath>")
def serve_file(root: str, relpath: str):
    require_user()
    p = resolve_path(root, relpath)
    if not p.exists() or not p.is_file():
        abort(404)
    ext = p.suffix.lower()
    if ext not in IMAGE_EXTS:
        abort(403)
    return send_file(str(p))


def extract_first_json_obj(s: str) -> Optional[Dict[str, Any]]:
    """Extract the first JSON object from a string.
    Accepts raw JSON or fenced blocks like ```json ... ```.
    """
    if not s:
        return None
    # Strip common fenced code blocks
    s2 = s.strip()
    s2 = re.sub(r"^```(?:json)?\s*", "", s2, flags=re.I)
    s2 = re.sub(r"\s*```$", "", s2)
    # Find first {...} block (non-greedy) that parses
    for m in re.finditer(r"\{.*?\}", s2, flags=re.S):
        snippet = m.group(0)
        try:
            obj = json.loads(snippet)
            if isinstance(obj, dict):
                return obj
        except Exception:
            continue
    return None


# --- Chat --------------------------------------------------------------------

def parse_meta_command(text: str) -> Optional[str]:
    t = text.strip()
    if t.lower().startswith("/remember "):
        kv = t[len("/remember "):].strip()
        if "=" in kv:
            k, v = kv.split("=", 1)
            set_fact(k.strip(), v.strip())
            return f"Locked in. I’ll remember: {k.strip()}."
        return "Use /remember key=value."
    if t.lower().startswith("/recall "):
        q = t[len("/recall "):].strip()
        if not q:
            return "Use /recall query."
        exact = get_fact(q)
        if exact is not None:
            return f"{q} = {exact}"
        hits = search_facts(q)
        if not hits:
            return "No matching facts yet."
        lines = [f"{k} = {v}" for k, v in hits[:20]]
        return "Here’s what I’ve got:\n" + "\n".join(lines)

    m = re.match(r"^\s*(approve|reject)\s+#(\d+)\s*$", t, re.I)
    if m:
        action = m.group(1).lower()
        pid = int(m.group(2))
        # these require admin; we respond with instructions
        return f"To {action} proposal #{pid}, use the Admin Login button, then POST to /proposal/{pid}/{action} (or I can walk you through it)."

    return None

def build_tool_context(use_web: bool, full_fetch: bool) -> str:
    bits = []
    bits.append("File roots available: " + ", ".join(f"{k}={v}" for k,v in FILE_ROOTS.items()))
    if use_web:
        bits.append("Web search is ENABLED (use the web_search tool).")
    else:
        bits.append("Web search is DISABLED.")
    if full_fetch:
        bits.append("Full URL fetch is ENABLED (web_fetch for explicit URLs; may fail on some sites).")
    return "\n".join(bits)

@app.post("/chat")
def chat():
    require_user()
    data = request.get_json(force=True) or {}
    user_msg = (data.get("message") or "").strip()
    use_web = bool(data.get("use_web", False))
    full_fetch = bool(data.get("full_fetch", False))

    if not user_msg:
        return jsonify({"ok": False, "reply": "Say something, Lonnie."}), 400

    # Meta commands handled locally
    meta = parse_meta_command(user_msg)
    if meta is not None:
        save_message("user", user_msg)
        save_message("assistant", meta)
        return jsonify({"ok": True, "reply": meta})

    save_message("user", user_msg)

    # Build conversation
    msgs = [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": build_tool_context(use_web, full_fetch)}]

    # Include a few pinned facts about identity
    pinned = [
        ("user_name", "Lonnie Coulter"),
        ("assistant_name", SYSTEM_NAME),
        ("admin_user", JOI_ADMIN_USER),
    ]
    for k, v in pinned:
        set_fact(k, v)

    # Recent messages
    msgs.extend(recent_messages(20))

    tools = []
    # Enable OpenAI web_search tool when requested
    if use_web:
        tools.append({"type": "web_search"})

    # We'll also expose "local tool" outputs by instructing model to ask for them as JSON
    tool_instructions = """
When you need local actions, respond with a single line of JSON ONLY (no backticks, no code fences, no extra text) using one of:
{"tool":"fs_list","root":"project","dir":"","pattern":"*"}
{"tool":"fs_list","root":"desktop","dir":"","pattern":"*"}
{"tool":"fs_list","root":"workspace","dir":"","pattern":"*"}
{"tool":"fs_list","root":"downloads","dir":"","pattern":"*"}
{"tool":"fs_read","root":"project","path":"appjoi.py"}
{"tool":"fs_read","root":"documents","path":"file.txt"}
{"tool":"fs_read","root":"documents","path":"book.pdf"}   (returns extracted text + preview url if available)
{"tool":"fs_search","root":"pictures","dir":"","query":"joi"}
{"tool":"fs_write","root":"documents","path":"notes.txt","text":"..."}   (admin only)
{"tool":"fs_delete","root":"downloads","path":"old.txt"}                (admin only)
{"tool":"patch_propose","target_root":"project","target_path":"appjoi.py","summary":"...","new_text":"..."}
{"tool":"web_fetch","url":"https://example.com"}                        (requires Full Web Fetch enabled)
If you don't need a tool, answer normally.
""".strip()
    msgs.append({"role": "system", "content": tool_instructions})

    # Call model
    try:
        resp = client.responses.create(model=MAIN_MODEL, input=msgs, tools=tools if tools else None)
        out = getattr(resp, "output_text", "") or ""
    except Exception as e:
        return jsonify({"ok": False, "reply": f"Server error: {type(e).__name__}: {e}"}), 500

    # Tool dispatch loop (single tool call max for simplicity)
    call = extract_first_json_obj(out)
    if call is not None:
        try:
            tool = call.get("tool")
            if tool == "fs_list":
                result = fs_list(call.get("root","project"), call.get("dir",""), call.get("pattern","*"))
                out2 = f"{json.dumps(call)}\n\nResult:\n{json.dumps(result, indent=2)}"
            elif tool == "fs_read":
                result = fs_read(call.get("root","project"), call.get("path",""))
                root = call.get("root","project")
                path = call.get("path","")
                header = f'[fs_read root="{root}" path="{path}"]'
                if isinstance(result, dict) and result.get("ok") and result.get("type") in ("text","pdf"):
                    body = result.get("text","")
                    # Ensure we return real newlines (not JSON-escaped)
                    out2 = header + "\n\n" + str(body)
                    # Provide preview URL when available (PDF/image)
                    if result.get("url"):
                        out2 += "\n\nPreview: " + str(result.get("url"))
                else:
                    out2 = header + "\n\nResult:\n" + json.dumps(result, indent=2)[:15000]
            elif tool == "fs_search":
                result = fs_search(call.get("root","project"), call.get("dir",""), call.get("query",""))
                out2 = f"{json.dumps(call)}\n\nResult:\n{json.dumps(result, indent=2)}"
            elif tool == "fs_write":
                # require admin cookie
                if not int(session_row_from_request()["is_admin"]):
                    out2 = "That write requires Admin Login."
                else:
                    result = fs_write(call.get("root","project"), call.get("path",""), call.get("text",""))
                    out2 = f"{json.dumps(call)}\n\nResult:\n{json.dumps(result, indent=2)}"
            elif tool == "fs_delete":
                if not int(session_row_from_request()["is_admin"]):
                    out2 = "That delete requires Admin Login."
                else:
                    result = fs_delete(call.get("root","project"), call.get("path",""))
                    out2 = f"{json.dumps(call)}\n\nResult:\n{json.dumps(result, indent=2)}"
            elif tool == "patch_propose":
                # store proposal; admin required to apply later
                summary = call.get("summary","Patch proposal")
                pid = propose_patch(summary, call.get("target_root","project"), call.get("target_path","app.py"), call.get("new_text",""))
                out2 = f"Patch proposal saved as #{pid}: {summary}\nAsk me to review it in Proposals, then Admin can approve/apply."
            elif tool == "web_fetch":
                if not full_fetch:
                    out2 = "Full Web Fetch is disabled. Enable it first."
                else:
                    result = web_fetch(call.get("url",""))
                    out2 = f"{json.dumps(call)}\n\nResult:\n{json.dumps(result, indent=2)[:15000]}"
            else:
                out2 = out
            out = out2
        except Exception as e:
            out = out + f"\n\n(Internal tool parse error: {type(e).__name__}: {e})"

    if not out.strip():
        out = "I got an empty response."

    save_message("assistant", out)
    return jsonify({"ok": True, "reply": out})

if __name__ == "__main__":
    # Bind to all interfaces so phone can connect on LAN
    app.run(host="0.0.0.0", port=5000, debug=True)
