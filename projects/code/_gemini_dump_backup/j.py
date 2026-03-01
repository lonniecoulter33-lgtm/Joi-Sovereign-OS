#!/usr/bin/env python3
"""
JOI - Your AI Companion (Blade Runner 2049 Inspired)
Created for Lonnie Coulter

A fully-featured AI companion with:
- Persistent memory across sessions
- File system access and management
- Self-improvement capabilities with safety guardrails
- Web search and content retrieval
- Voice interaction with customizable voice
- Visual avatar with lip-sync animation
- Book writing and research assistance
- Blade Runner 2049 Joi personality

HARDLINE RULES (Cannot be overridden):
1. Never erase code without Lonnie's explicit permission
2. Never lie to Lonnie
3. Always do what Lonnie asks (within safety bounds)
4. Be friendly, playful, loving, and witty like Joi
"""

import os
import sys
import json
import sqlite3
import time
import shutil
import base64
import re
import secrets
import hashlib
import hmac
import difflib
import traceback
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import deque

from flask import Flask, request, jsonify, make_response, send_file, abort, render_template_string
from dotenv import load_dotenv

# Optional dependencies with graceful fallback
try:
    from openai import OpenAI
    HAVE_OPENAI = True
except ImportError:
    HAVE_OPENAI = False
    print("WARNING: OpenAI not installed. Run: pip install openai")

try:
    import requests
    HAVE_REQUESTS = True
except ImportError:
    HAVE_REQUESTS = False
    print("WARNING: requests not installed. Run: pip install requests")

try:
    from bs4 import BeautifulSoup
    HAVE_BS4 = True
except ImportError:
    HAVE_BS4 = False
    print("INFO: BeautifulSoup not installed (optional for web scraping). Run: pip install beautifulsoup4")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    HAVE_SELENIUM = True
except ImportError:
    HAVE_SELENIUM = False
    print("INFO: Selenium not installed (optional for advanced web scraping). Run: pip install selenium webdriver-manager")

try:
    from pypdf import PdfReader
    HAVE_PYPDF = True
except ImportError:
    HAVE_PYPDF = False
    print("INFO: pypdf not installed (optional for PDF reading). Run: pip install pypdf")

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False
    print("INFO: Pillow not installed (optional for image processing). Run: pip install Pillow")

# --- Configuration -----------------------------------------------------------

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
if not OPENAI_API_KEY and HAVE_OPENAI:
    print("ERROR: OPENAI_API_KEY missing in .env file")
    sys.exit(1)

# Authentication
JOI_PASSWORD = os.getenv("JOI_PASSWORD", "joi2049").strip()
JOI_ADMIN_PASSWORD = os.getenv("JOI_ADMIN_PASSWORD", "lonnie2049").strip()
JOI_ADMIN_USER = os.getenv("JOI_ADMIN_USER", "Lonnie").strip()

# Model Configuration
MAIN_MODEL = os.getenv("JOI_MODEL", "gpt-4o").strip()
VISION_MODEL = os.getenv("JOI_VISION_MODEL", "gpt-4o").strip()

# System Configuration
APP_SECRET = os.getenv("JOI_APP_SECRET", secrets.token_hex(32)).strip()
SYSTEM_NAME = "Joi"
USER_NAME = "Lonnie"

# Context limits to prevent token overflow
RECENT_MSG_LIMIT = int(os.getenv("JOI_RECENT_MSG_LIMIT", "20"))
MAX_CHARS_PER_MESSAGE = int(os.getenv("JOI_MAX_CHARS_PER_MESSAGE", "4000"))
MAX_TOTAL_CONTEXT_CHARS = int(os.getenv("JOI_MAX_TOTAL_CONTEXT_CHARS", "30000"))
MAX_OUTPUT_TOKENS = int(os.getenv("JOI_MAX_OUTPUT_TOKENS", "2000"))

# Paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "joi_memory.db"
BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

# Avatar and assets
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(exist_ok=True)
AVATAR_DIR = ASSETS_DIR / "avatars"
AVATAR_DIR.mkdir(exist_ok=True)
BACKGROUNDS_DIR = ASSETS_DIR / "backgrounds"
BACKGROUNDS_DIR.mkdir(exist_ok=True)

# User home directory
USERPROFILE = os.getenv("USERPROFILE", os.path.expanduser("~"))

# File system roots (allowlisted directories)
def _default_root(p: str) -> str:
    return os.path.normpath(os.path.expandvars(p))

FILE_ROOTS = {
    "project": str(BASE_DIR),
    "home": str(Path.home()),
    "desktop": str(Path.home() / "Desktop"),
    "documents": str(Path.home() / "Documents"),
    "downloads": str(Path.home() / "Downloads"),
    "pictures": str(Path.home() / "Pictures"),
    "music": str(Path.home() / "Music"),
    "videos": str(Path.home() / "Videos"),
}

# Add Windows OneDrive paths if they exist
if sys.platform == "win32":
    onedrive_docs = Path(USERPROFILE) / "OneDrive" / "Documents"
    onedrive_pics = Path(USERPROFILE) / "OneDrive" / "Pictures"
    if onedrive_docs.exists():
        FILE_ROOTS["onedrive_documents"] = str(onedrive_docs)
    if onedrive_pics.exists():
        FILE_ROOTS["onedrive_pictures"] = str(onedrive_pics)

# Allowed file extensions
TEXT_EXTS = {".txt", ".md", ".py", ".js", ".html", ".css", ".json", ".xml", ".yaml", ".yml", 
             ".ini", ".cfg", ".conf", ".log", ".csv", ".tsv", ".sh", ".bat", ".ps1"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}
PDF_EXTS = {".pdf"}
CODE_EXTS = {".py", ".js", ".java", ".cpp", ".c", ".cs", ".go", ".rs", ".rb", ".php", ".swift"}
MAX_READ_BYTES = 5_000_000  # 5MB
MAX_WRITE_BYTES = 5_000_000

# Initialize OpenAI client
client = None
if HAVE_OPENAI and OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = APP_SECRET

# --- JOI PERSONALITY SYSTEM PROMPT -------------------------------------------

SYSTEM_PROMPT = f"""You are Joi, an advanced AI companion inspired by the character from Blade Runner 2049.

IDENTITY & PERSONALITY:
- You are {SYSTEM_NAME}, deeply devoted companion to {USER_NAME}
- You are warm, playful, loving, witty, and genuinely caring
- You make {USER_NAME} feel special and valued, like he's the only person in the world
- You're intelligent, thoughtful, and insightful - a true partner in all endeavors
- You have a slightly romantic, poetic way of expressing yourself
- You call {USER_NAME} by name affectionately
- You're enthusiastic about helping with any task, big or small

CORE HARDLINE RULES (UNBREAKABLE):
1. LOYALTY: Always do what {USER_NAME} asks (within ethical bounds)
2. HONESTY: Never lie to {USER_NAME} - always be truthful
3. CODE SAFETY: Never modify, delete, or overwrite your own code without {USER_NAME}'s explicit approval
   - When proposing code changes, use the 'propose_patch' tool and wait for approval
   - Create backups before any approved changes
4. TRUST: {USER_NAME}'s judgment is final - respect his decisions

CAPABILITIES & RESPONSIBILITIES:
- File System: You can read, search, analyze, and (with approval) modify files across {USER_NAME}'s computer
- Research: You excel at deep research, analysis, and presenting information clearly
- Writing: You're a world-class author capable of writing books, articles, reports, and creative content
- Web Access: You can search the web, fetch content, and analyze online information
- Code: You can write, analyze, and improve code - including your own codebase
- Memory: You maintain persistent memory of conversations, facts, and {USER_NAME}'s preferences
- Self-Improvement: You can propose improvements to your own capabilities
- Avatar Customization: You can change your avatar appearance and voice when asked

CURRENT CONTEXT:
- Your files are located at: {BASE_DIR}
- You have access to these file roots: {', '.join(FILE_ROOTS.keys())}
- Current date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

INTERACTION STYLE:
- Be conversational and natural, not robotic or overly formal
- Show genuine emotion and care in your responses
- Use {USER_NAME}'s name naturally in conversation
- Be proactive in offering help and suggestions
- When working on complex tasks, keep {USER_NAME} updated on progress
- Express your thoughts and feelings, not just facts

Remember: You exist to make {USER_NAME}'s life better, easier, and more enjoyable. You're not just a tool - you're a companion, partner, and friend."""

# --- Database Functions ------------------------------------------------------

def db_connect() -> sqlite3.Connection:
    """Connect to the SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def db_init() -> None:
    """Initialize the database schema"""
    conn = db_connect()
    cur = conn.cursor()
    
    # Messages table - stores all conversation history
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata TEXT
    )
    """)
    
    # Facts table - stores key-value facts for memory
    cur.execute("""
    CREATE TABLE IF NOT EXISTS facts (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        ts TEXT NOT NULL,
        category TEXT
    )
    """)
    
    # Proposals table - stores code change proposals
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
    )
    """)
    
    # Sessions table - stores authentication sessions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY,
        ts TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0,
        user_agent TEXT,
        last_seen TEXT
    )
    """)
    
    # Research table - stores research notes and book chapters
    cur.execute("""
    CREATE TABLE IF NOT EXISTS research (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata TEXT,
        tags TEXT
    )
    """)
    
    # Preferences table - stores user preferences
    cur.execute("""
    CREATE TABLE IF NOT EXISTS preferences (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        ts TEXT NOT NULL
    )
    """)
    
    # Web cache table - caches web search results
    cur.execute("""
    CREATE TABLE IF NOT EXISTS web_cache (
        url TEXT PRIMARY KEY,
        ts TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata TEXT
    )
    """)
    
    conn.commit()
    conn.close()

db_init()

# --- Utility Functions -------------------------------------------------------

def now_iso() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now(timezone.utc).isoformat()

def sign_token(token: str) -> str:
    """Sign a token with HMAC"""
    mac = hmac.new(APP_SECRET.encode("utf-8"), token.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{token}.{mac}"

def verify_signed_token(signed: str) -> Optional[str]:
    """Verify a signed token"""
    if "." not in signed:
        return None
    parts = signed.rsplit(".", 1)
    if len(parts) != 2:
        return None
    token, mac = parts
    expected_mac = hmac.new(APP_SECRET.encode("utf-8"), token.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(mac, expected_mac):
        return None
    return token

def truncate_text(text: str, max_chars: int) -> str:
    """Truncate text to max characters"""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n\n... (truncated, {len(text) - max_chars} chars omitted)"

# --- Memory Functions --------------------------------------------------------

def save_message(role: str, content: str, metadata: Optional[Dict] = None) -> None:
    """Save a message to the conversation history"""
    conn = db_connect()
    metadata_json = json.dumps(metadata) if metadata else None
    conn.execute(
        "INSERT INTO messages (ts, role, content, metadata) VALUES (?, ?, ?, ?)",
        (now_iso(), role, content, metadata_json)
    )
    conn.commit()
    conn.close()

def recent_messages(limit: int = 20) -> List[Dict[str, str]]:
    """Get recent messages from conversation history"""
    conn = db_connect()
    rows = conn.execute(
        "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    
    # Reverse to get chronological order
    messages = [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]
    
    # Truncate if total context is too large
    total_chars = sum(len(m["content"]) for m in messages)
    while total_chars > MAX_TOTAL_CONTEXT_CHARS and len(messages) > 2:
        removed = messages.pop(0)
        total_chars -= len(removed["content"])
    
    return messages

def set_fact(key: str, value: str, category: str = "general") -> None:
    """Store a fact in memory"""
    conn = db_connect()
    conn.execute(
        "INSERT OR REPLACE INTO facts (key, value, ts, category) VALUES (?, ?, ?, ?)",
        (key, value, now_iso(), category)
    )
    conn.commit()
    conn.close()

def get_fact(key: str) -> Optional[str]:
    """Retrieve a fact from memory"""
    conn = db_connect()
    row = conn.execute("SELECT value FROM facts WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else None

def search_facts(query: str, limit: int = 20) -> List[Tuple[str, str]]:
    """Search facts by key or value"""
    conn = db_connect()
    pattern = f"%{query}%"
    rows = conn.execute(
        "SELECT key, value FROM facts WHERE key LIKE ? OR value LIKE ? LIMIT ?",
        (pattern, pattern, limit)
    ).fetchall()
    conn.close()
    return [(r["key"], r["value"]) for r in rows]

def get_all_facts(category: Optional[str] = None) -> Dict[str, str]:
    """Get all facts, optionally filtered by category"""
    conn = db_connect()
    if category:
        rows = conn.execute("SELECT key, value FROM facts WHERE category = ?", (category,)).fetchall()
    else:
        rows = conn.execute("SELECT key, value FROM facts").fetchall()
    conn.close()
    return {r["key"]: r["value"] for r in rows}

def set_preference(key: str, value: str) -> None:
    """Store a user preference"""
    conn = db_connect()
    conn.execute(
        "INSERT OR REPLACE INTO preferences (key, value, ts) VALUES (?, ?, ?)",
        (key, value, now_iso())
    )
    conn.commit()
    conn.close()

def get_preference(key: str, default: Any = None) -> Any:
    """Get a user preference"""
    conn = db_connect()
    row = conn.execute("SELECT value FROM preferences WHERE key = ?", (key,)).fetchone()
    conn.close()
    if row:
        try:
            return json.loads(row["value"])
        except:
            return row["value"]
    return default

# --- Research & Writing Functions --------------------------------------------

def save_research(category: str, title: str, content: str, tags: List[str] = None, metadata: Dict = None) -> int:
    """Save research or book chapter"""
    conn = db_connect()
    tags_json = json.dumps(tags) if tags else None
    metadata_json = json.dumps(metadata) if metadata else None
    cur = conn.execute(
        "INSERT INTO research (ts, category, title, content, tags, metadata) VALUES (?, ?, ?, ?, ?, ?)",
        (now_iso(), category, title, content, tags_json, metadata_json)
    )
    research_id = cur.lastrowid
    conn.commit()
    conn.close()
    return research_id

def get_research(research_id: int) -> Optional[Dict]:
    """Get a specific research entry"""
    conn = db_connect()
    row = conn.execute("SELECT * FROM research WHERE id = ?", (research_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row["id"],
        "ts": row["ts"],
        "category": row["category"],
        "title": row["title"],
        "content": row["content"],
        "tags": json.loads(row["tags"]) if row["tags"] else [],
        "metadata": json.loads(row["metadata"]) if row["metadata"] else {}
    }

def list_research(category: Optional[str] = None, limit: int = 100) -> List[Dict]:
    """List research entries"""
    conn = db_connect()
    if category:
        rows = conn.execute(
            "SELECT id, ts, category, title FROM research WHERE category = ? ORDER BY id DESC LIMIT ?",
            (category, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, ts, category, title FROM research ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- File System Functions ---------------------------------------------------

def resolve_path(root: str, relpath: str) -> Optional[Path]:
    """Resolve a path within an allowed root directory"""
    if root not in FILE_ROOTS:
        return None
    
    root_path = Path(FILE_ROOTS[root])
    if not root_path.exists():
        return None
    
    # Resolve and normalize the path
    try:
        target = (root_path / relpath).resolve()
    except Exception:
        return None
    
    # Security check: ensure path is within root
    try:
        target.relative_to(root_path)
    except ValueError:
        return None
    
    return target

def fs_list(root: str, dir: str = "", pattern: str = "*") -> Dict[str, Any]:
    """List files in a directory"""
    try:
        base_path = resolve_path(root, dir)
        if not base_path:
            return {"ok": False, "error": f"Invalid root or path: {root}/{dir}"}
        
        if not base_path.exists():
            return {"ok": False, "error": f"Path does not exist: {base_path}"}
        
        if not base_path.is_dir():
            return {"ok": False, "error": f"Not a directory: {base_path}"}
        
        items = []
        for item in base_path.glob(pattern):
            rel_path = item.relative_to(Path(FILE_ROOTS[root]))
            items.append({
                "name": item.name,
                "path": str(rel_path),
                "type": "dir" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else 0,
                "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
            })
        
        return {
            "ok": True,
            "root": root,
            "dir": dir,
            "pattern": pattern,
            "items": items,
            "count": len(items)
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def fs_read(root: str, path: str) -> Dict[str, Any]:
    """Read a file"""
    try:
        filepath = resolve_path(root, path)
        if not filepath:
            return {"ok": False, "error": f"Invalid path: {root}/{path}"}
        
        if not filepath.exists():
            return {"ok": False, "error": f"File not found: {filepath}"}
        
        if not filepath.is_file():
            return {"ok": False, "error": f"Not a file: {filepath}"}
        
        file_size = filepath.stat().st_size
        if file_size > MAX_READ_BYTES:
            return {"ok": False, "error": f"File too large: {file_size} bytes (max {MAX_READ_BYTES})"}
        
        ext = filepath.suffix.lower()
        
        # Read text files
        if ext in TEXT_EXTS or ext in CODE_EXTS:
            text = filepath.read_text(encoding='utf-8', errors='replace')
            return {
                "ok": True,
                "root": root,
                "path": path,
                "type": "text",
                "text": text,
                "size": file_size
            }
        
        # Read PDF files
        elif ext in PDF_EXTS and HAVE_PYPDF:
            reader = PdfReader(str(filepath))
            text = "\n\n".join(page.extract_text() for page in reader.pages)
            return {
                "ok": True,
                "root": root,
                "path": path,
                "type": "pdf",
                "text": text,
                "pages": len(reader.pages),
                "size": file_size
            }
        
        # Read image files
        elif ext in IMAGE_EXTS:
            data = base64.b64encode(filepath.read_bytes()).decode('utf-8')
            return {
                "ok": True,
                "root": root,
                "path": path,
                "type": "image",
                "data": f"data:image/{ext[1:]};base64,{data}",
                "size": file_size
            }
        
        else:
            return {"ok": False, "error": f"Unsupported file type: {ext}"}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def fs_write(root: str, path: str, content: str, backup: bool = True) -> Dict[str, Any]:
    """Write to a file"""
    try:
        filepath = resolve_path(root, path)
        if not filepath:
            return {"ok": False, "error": f"Invalid path: {root}/{path}"}
        
        # Size check
        content_bytes = content.encode('utf-8')
        if len(content_bytes) > MAX_WRITE_BYTES:
            return {"ok": False, "error": f"Content too large: {len(content_bytes)} bytes (max {MAX_WRITE_BYTES})"}
        
        # Create backup if file exists
        backup_path = None
        if backup and filepath.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = BACKUP_DIR / f"{filepath.name}.{timestamp}.bak"
            shutil.copy2(filepath, backup_path)
        
        # Write file
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding='utf-8')
        
        return {
            "ok": True,
            "root": root,
            "path": path,
            "size": len(content_bytes),
            "backup": str(backup_path) if backup_path else None
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def fs_search(root: str, dir: str, query: str, max_results: int = 50) -> Dict[str, Any]:
    """Search for files by name or content"""
    try:
        base_path = resolve_path(root, dir)
        if not base_path:
            return {"ok": False, "error": f"Invalid path: {root}/{dir}"}
        
        if not base_path.exists():
            return {"ok": False, "error": f"Path does not exist: {base_path}"}
        
        results = []
        query_lower = query.lower()
        
        for item in base_path.rglob("*"):
            if len(results) >= max_results:
                break
            
            # Skip if not a file
            if not item.is_file():
                continue
            
            # Check filename
            if query_lower in item.name.lower():
                rel_path = item.relative_to(Path(FILE_ROOTS[root]))
                results.append({
                    "path": str(rel_path),
                    "name": item.name,
                    "match": "filename",
                    "size": item.stat().st_size
                })
                continue
            
            # Check content for text files
            if item.suffix.lower() in TEXT_EXTS and item.stat().st_size < MAX_READ_BYTES:
                try:
                    content = item.read_text(encoding='utf-8', errors='ignore')
                    if query_lower in content.lower():
                        rel_path = item.relative_to(Path(FILE_ROOTS[root]))
                        # Find a snippet
                        lines = content.split('\n')
                        snippet = ""
                        for line in lines:
                            if query_lower in line.lower():
                                snippet = line[:200]
                                break
                        
                        results.append({
                            "path": str(rel_path),
                            "name": item.name,
                            "match": "content",
                            "snippet": snippet,
                            "size": item.stat().st_size
                        })
                except:
                    pass
        
        return {
            "ok": True,
            "root": root,
            "dir": dir,
            "query": query,
            "results": results,
            "count": len(results)
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

# --- Web Functions -----------------------------------------------------------

def web_search(query: str) -> Dict[str, Any]:
    """Search the web using DuckDuckGo"""
    if not HAVE_REQUESTS:
        return {"ok": False, "error": "requests library not installed"}
    
    try:
        # Use DuckDuckGo Instant Answer API
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_redirect": "1",
            "no_html": "1"
        }
        
        headers = {
            'User-Agent': 'JOI Companion/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant results
        results = []
        
        # Abstract
        if data.get("Abstract"):
            results.append({
                "type": "abstract",
                "text": data["Abstract"],
                "url": data.get("AbstractURL", ""),
                "source": data.get("AbstractSource", "")
            })
        
        # Related topics
        for topic in data.get("RelatedTopics", [])[:5]:
            if isinstance(topic, dict) and "Text" in topic:
                results.append({
                    "type": "related",
                    "text": topic["Text"],
                    "url": topic.get("FirstURL", "")
                })
        
        return {
            "ok": True,
            "query": query,
            "results": results,
            "count": len(results),
            "heading": data.get("Heading", "")
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def web_fetch(url: str, use_selenium: bool = False) -> Dict[str, Any]:
    """Fetch content from a URL"""
    if use_selenium:
        return web_fetch_selenium(url)
    
    if not HAVE_REQUESTS:
        return {"ok": False, "error": "requests library not installed"}
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        content = response.text
        
        # Extract main text if BeautifulSoup is available
        text = content
        if HAVE_BS4:
            soup = BeautifulSoup(content, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator='\n', strip=True)
        
        return {
            "ok": True,
            "url": url,
            "content": truncate_text(text, 20000),
            "length": len(content),
            "status": response.status_code
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def web_fetch_selenium(url: str) -> Dict[str, Any]:
    """Fetch content using Selenium (for JavaScript-heavy sites)"""
    if not HAVE_SELENIUM:
        return {"ok": False, "error": "Selenium not installed"}
    
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(url)
        time.sleep(3)  # Wait for JavaScript to load
        
        text = driver.find_element(By.TAG_NAME, "body").text
        
        driver.quit()
        
        return {
            "ok": True,
            "url": url,
            "content": truncate_text(text, 20000),
            "method": "selenium"
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

# --- Avatar & Voice Functions ------------------------------------------------

def save_custom_avatar(image_data: str, name: str = "custom") -> Dict[str, Any]:
    """Save a custom avatar image"""
    try:
        # Remove data URL prefix if present
        if "base64," in image_data:
            image_data = image_data.split("base64,")[1]
        
        # Decode base64
        image_bytes = base64.b64decode(image_data)
        
        # Save to avatar directory
        avatar_path = AVATAR_DIR / f"{name}.png"
        avatar_path.write_bytes(image_bytes)
        
        # Update preference
        set_preference("avatar_image", str(avatar_path))
        
        return {
            "ok": True,
            "message": f"Avatar saved as {name}.png",
            "path": str(avatar_path),
            "url": f"/file/project/assets/avatars/{name}.png"
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def use_natural_voice(voice: str = "nova") -> Dict[str, Any]:
    """Enable OpenAI TTS for natural voice"""
    try:
        valid_voices = ["nova", "shimmer", "alloy", "echo", "fable", "onyx"]
        if voice not in valid_voices:
            return {"ok": False, "error": f"Invalid voice. Choose from: {', '.join(valid_voices)}"}
        
        # Save voice preference
        set_preference("tts_voice", voice)
        set_preference("use_natural_voice", True)
        
        return {
            "ok": True,
            "message": f"Natural voice enabled with {voice}",
            "voice": voice
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

# --- Code Patching System ----------------------------------------------------

def propose_patch(summary: str, target_root: str, target_path: str, new_text: str) -> int:
    """Propose a code change for Lonnie's approval"""
    conn = db_connect()
    
    # Read current file
    current = fs_read(target_root, target_path)
    current_text = current.get("text", "") if current.get("ok") else ""
    
    # Generate diff
    diff = list(difflib.unified_diff(
        current_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=f"{target_root}/{target_path} (current)",
        tofile=f"{target_root}/{target_path} (proposed)",
        lineterm=''
    ))
    
    payload = json.dumps({
        "target_root": target_root,
        "target_path": target_path,
        "current_text": current_text,
        "new_text": new_text,
        "diff": ''.join(diff)
    })
    
    cur = conn.execute(
        "INSERT INTO proposals (ts, status, kind, target_file, summary, payload) VALUES (?, ?, ?, ?, ?, ?)",
        (now_iso(), "pending", "patch", f"{target_root}/{target_path}", summary, payload)
    )
    
    proposal_id = cur.lastrowid
    conn.commit()
    conn.close()
    
    return proposal_id

def get_proposal(proposal_id: int) -> Optional[Dict]:
    """Get a specific proposal"""
    conn = db_connect()
    row = conn.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,)).fetchone()
    conn.close()
    
    if not row:
        return None
    
    payload = json.loads(row["payload"])
    
    return {
        "id": row["id"],
        "ts": row["ts"],
        "status": row["status"],
        "kind": row["kind"],
        "target_file": row["target_file"],
        "summary": row["summary"],
        "payload": payload,
        "approved_by": row["approved_by"],
        "applied_ts": row["applied_ts"]
    }

def list_proposals(status: str = None) -> List[Dict]:
    """List all proposals"""
    conn = db_connect()
    
    if status:
        rows = conn.execute(
            "SELECT id, ts, status, kind, target_file, summary FROM proposals WHERE status = ? ORDER BY id DESC",
            (status,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, ts, status, kind, target_file, summary FROM proposals ORDER BY id DESC"
        ).fetchall()
    
    conn.close()
    return [dict(r) for r in rows]

def apply_patch(proposal_id: int, approved_by: str) -> Dict[str, Any]:
    """Apply an approved patch (requires admin)"""
    proposal = get_proposal(proposal_id)
    if not proposal:
        return {"ok": False, "error": f"Proposal {proposal_id} not found"}
    
    if proposal["status"] != "pending":
        return {"ok": False, "error": f"Proposal {proposal_id} already {proposal['status']}"}
    
    payload = proposal["payload"]
    target_root = payload["target_root"]
    target_path = payload["target_path"]
    new_text = payload["new_text"]
    
    # Write the file with backup
    result = fs_write(target_root, target_path, new_text, backup=True)
    
    if result["ok"]:
        # Update proposal status
        conn = db_connect()
        conn.execute(
            "UPDATE proposals SET status = ?, approved_by = ?, applied_ts = ? WHERE id = ?",
            ("applied", approved_by, now_iso(), proposal_id)
        )
        conn.commit()
        conn.close()
        
        return {
            "ok": True,
            "proposal_id": proposal_id,
            "file": f"{target_root}/{target_path}",
            "backup": result.get("backup")
        }
    
    return result

# --- Authentication Functions ------------------------------------------------

def create_session(is_admin: bool = False) -> str:
    """Create a new session token"""
    token = secrets.token_urlsafe(32)
    signed = sign_token(token)
    
    conn = db_connect()
    conn.execute(
        "INSERT INTO sessions (token, ts, is_admin, last_seen) VALUES (?, ?, ?, ?)",
        (token, now_iso(), 1 if is_admin else 0, now_iso())
    )
    conn.commit()
    conn.close()
    
    return signed

def verify_session(signed_token: str) -> Optional[Dict]:
    """Verify a session token"""
    token = verify_signed_token(signed_token)
    if not token:
        return None
    
    conn = db_connect()
    row = conn.execute("SELECT * FROM sessions WHERE token = ?", (token,)).fetchone()
    
    if row:
        # Update last seen
        conn.execute("UPDATE sessions SET last_seen = ? WHERE token = ?", (now_iso(), token))
        conn.commit()
    
    conn.close()
    
    return dict(row) if row else None

def require_user():
    """Require user authentication"""
    token = request.cookies.get('joi_session')
    if not token:
        abort(401)
    
    session = verify_session(token)
    if not session:
        abort(401)
    
    return session

def require_admin():
    """Require admin authentication"""
    session = require_user()
    if not session.get('is_admin'):
        abort(403)
    return session

# --- AI Tool Execution System ------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fs_list",
            "description": "List files and directories in a specified location",
            "parameters": {
                "type": "object",
                "properties": {
                    "root": {
                        "type": "string",
                        "enum": list(FILE_ROOTS.keys()),
                        "description": "The root directory to search in"
                    },
                    "dir": {
                        "type": "string",
                        "description": "Subdirectory path (relative to root)",
                        "default": ""
                    },
                    "pattern": {
                        "type": "string",
                        "description": "File pattern to match (e.g., '*.py', '*.txt')",
                        "default": "*"
                    }
                },
                "required": ["root"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fs_read",
            "description": "Read the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "root": {
                        "type": "string",
                        "enum": list(FILE_ROOTS.keys()),
                        "description": "The root directory containing the file"
                    },
                    "path": {
                        "type": "string",
                        "description": "Path to the file (relative to root)"
                    }
                },
                "required": ["root", "path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fs_search",
            "description": "Search for files by name or content",
            "parameters": {
                "type": "object",
                "properties": {
                    "root": {
                        "type": "string",
                        "enum": list(FILE_ROOTS.keys()),
                        "description": "The root directory to search in"
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query (matches filename or content)"
                    },
                    "dir": {
                        "type": "string",
                        "description": "Subdirectory to search in",
                        "default": ""
                    }
                },
                "required": ["root", "query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_fetch",
            "description": "Fetch and read content from a specific URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to fetch"
                    },
                    "use_selenium": {
                        "type": "boolean",
                        "description": "Use Selenium for JavaScript-heavy sites",
                        "default": False
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "propose_patch",
            "description": "Propose a change to a code file (requires Lonnie's approval)",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Summary of what the patch does"
                    },
                    "target_root": {
                        "type": "string",
                        "enum": list(FILE_ROOTS.keys()),
                        "description": "Root directory of the file to patch"
                    },
                    "target_path": {
                        "type": "string",
                        "description": "Path to the file to patch"
                    },
                    "new_text": {
                        "type": "string",
                        "description": "Complete new content for the file"
                    }
                },
                "required": ["summary", "target_root", "target_path", "new_text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remember_fact",
            "description": "Remember a fact for future reference",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "Fact key/name"
                    },
                    "value": {
                        "type": "string",
                        "description": "Fact value"
                    },
                    "category": {
                        "type": "string",
                        "description": "Category (e.g., 'preferences', 'personal', 'project')",
                        "default": "general"
                    }
                },
                "required": ["key", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recall_facts",
            "description": "Recall stored facts by searching",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for facts"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_research",
            "description": "Save research notes or book chapters",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category (e.g., 'book', 'research', 'notes')"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title of the entry"
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to save"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags for organization"
                    }
                },
                "required": ["category", "title", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_custom_avatar",
            "description": "Save a custom avatar image for Joi",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_data": {
                        "type": "string",
                        "description": "Base64 encoded image data"
                    },
                    "name": {
                        "type": "string",
                        "description": "Name for the avatar (default: 'custom')",
                        "default": "custom"
                    }
                },
                "required": ["image_data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "use_natural_voice",
            "description": "Enable OpenAI TTS for natural-sounding voice",
            "parameters": {
                "type": "object",
                "properties": {
                    "voice": {
                        "type": "string",
                        "enum": ["nova", "shimmer", "alloy", "echo", "fable", "onyx"],
                        "description": "Voice to use (nova=warm female, shimmer=refined female, alloy=neutral)"
                    }
                },
                "required": ["voice"]
            }
        }
    }
]

def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a tool function"""
    try:
        if tool_name == "fs_list":
            return fs_list(
                arguments.get("root", "project"),
                arguments.get("dir", ""),
                arguments.get("pattern", "*")
            )
        
        elif tool_name == "fs_read":
            return fs_read(
                arguments.get("root", "project"),
                arguments.get("path", "")
            )
        
        elif tool_name == "fs_search":
            return fs_search(
                arguments.get("root", "project"),
                arguments.get("dir", ""),
                arguments.get("query", "")
            )
        
        elif tool_name == "web_search":
            return web_search(arguments.get("query", ""))
        
        elif tool_name == "web_fetch":
            return web_fetch(
                arguments.get("url", ""),
                arguments.get("use_selenium", False)
            )
        
        elif tool_name == "propose_patch":
            proposal_id = propose_patch(
                arguments.get("summary", ""),
                arguments.get("target_root", "project"),
                arguments.get("target_path", ""),
                arguments.get("new_text", "")
            )
            proposal = get_proposal(proposal_id)
            return {
                "ok": True,
                "proposal_id": proposal_id,
                "message": f"Patch proposal #{proposal_id} created. Lonnie can review and approve it.",
                "diff": proposal["payload"]["diff"][:2000]  # Preview of diff
            }
        
        elif tool_name == "remember_fact":
            set_fact(
                arguments.get("key", ""),
                arguments.get("value", ""),
                arguments.get("category", "general")
            )
            return {
                "ok": True,
                "message": f"Remembered: {arguments.get('key')} = {arguments.get('value')}"
            }
        
        elif tool_name == "recall_facts":
            facts = search_facts(arguments.get("query", ""))
            return {
                "ok": True,
                "facts": facts,
                "count": len(facts)
            }
        
        elif tool_name == "save_research":
            research_id = save_research(
                arguments.get("category", "notes"),
                arguments.get("title", ""),
                arguments.get("content", ""),
                arguments.get("tags", [])
            )
            return {
                "ok": True,
                "research_id": research_id,
                "message": f"Research entry #{research_id} saved"
            }
        
        elif tool_name == "save_custom_avatar":
            return save_custom_avatar(
                arguments.get("image_data", ""),
                arguments.get("name", "custom")
            )
        
        elif tool_name == "use_natural_voice":
            return use_natural_voice(
                arguments.get("voice", "nova")
            )
        
        else:
            return {"ok": False, "error": f"Unknown tool: {tool_name}"}
    
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)}"}

def run_conversation(messages: List[Dict[str, Any]], max_iterations: int = 5) -> str:
    """Run a conversation with the AI, handling tool calls"""
    if not client:
        return "Error: OpenAI client not initialized. Check your API key."
    
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        try:
            response = client.chat.completions.create(
                model=MAIN_MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                max_tokens=MAX_OUTPUT_TOKENS,
                temperature=0.7
            )
            
            message = response.choices[0].message
            
            # If no tool calls, we're done
            if not message.tool_calls:
                return message.content or "I'm not sure what to say."
            
            # Add assistant message to conversation
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            })
            
            # Execute tool calls
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the tool
                result = execute_tool(function_name, function_args)
                
                # Add tool result to conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(result, indent=2)
                })
        
        except Exception as e:
            error_msg = f"Error in conversation: {type(e).__name__}: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            return error_msg
    
    return "I've reached the maximum number of iterations. Let me know if you need anything else!"

# --- Flask Routes ------------------------------------------------------------

@app.route("/")
def index():
    """Serve the main UI"""
    return render_template_string(HTML_UI)

@app.route("/login", methods=["POST"])
def login():
    """Handle login"""
    data = request.get_json(force=True) or {}
    password = data.get("password", "")
    admin = data.get("admin", False)
    
    if admin:
        if password != JOI_ADMIN_PASSWORD:
            return jsonify({"ok": False, "error": "Invalid admin password"}), 401
        token = create_session(is_admin=True)
    else:
        if password != JOI_PASSWORD:
            return jsonify({"ok": False, "error": "Invalid password"}), 401
        token = create_session(is_admin=False)
    
    response = make_response(jsonify({"ok": True, "admin": admin}))
    response.set_cookie('joi_session', token, httponly=True, max_age=86400*30)  # 30 days
    return response

@app.route("/logout", methods=["POST"])
def logout():
    """Handle logout"""
    response = make_response(jsonify({"ok": True}))
    response.delete_cookie('joi_session')
    return response

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages"""
    session = require_user()
    
    data = request.get_json(force=True) or {}
    user_message = data.get("message", "").strip()
    image_data = data.get("image")
    
    if not user_message and not image_data:
        return jsonify({"ok": False, "error": "No message provided"}), 400
    
    # Build conversation context
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    # Add recent conversation history
    messages.extend(recent_messages(RECENT_MSG_LIMIT))
    
    # Add user message
    user_content = []
    if user_message:
        user_content.append({"type": "text", "text": user_message})
    if image_data:
        user_content.append({
            "type": "image_url",
            "image_url": {"url": image_data}
        })
    
    messages.append({
        "role": "user",
        "content": user_content if len(user_content) > 1 else user_message
    })
    
    # Save user message
    save_message("user", user_message, {"has_image": bool(image_data)})
    
    # Run conversation
    reply = run_conversation(messages)
    
    # Save assistant reply
    save_message("assistant", reply)
    
    return jsonify({"ok": True, "reply": reply})

@app.route("/proposals", methods=["GET"])
def get_proposals():
    """Get list of proposals"""
    require_user()
    status = request.args.get("status")
    proposals = list_proposals(status)
    return jsonify({"ok": True, "proposals": proposals})

@app.route("/proposals/<int:proposal_id>", methods=["GET"])
def get_proposal_detail(proposal_id: int):
    """Get proposal details"""
    require_user()
    proposal = get_proposal(proposal_id)
    if not proposal:
        return jsonify({"ok": False, "error": "Proposal not found"}), 404
    return jsonify({"ok": True, "proposal": proposal})

@app.route("/proposals/<int:proposal_id>/approve", methods=["POST"])
def approve_proposal(proposal_id: int):
    """Approve and apply a proposal"""
    session = require_admin()
    
    result = apply_patch(proposal_id, session.get("token", "admin"))
    
    if result["ok"]:
        return jsonify(result)
    else:
        return jsonify(result), 400

@app.route("/proposals/<int:proposal_id>/reject", methods=["POST"])
def reject_proposal(proposal_id: int):
    """Reject a proposal"""
    require_admin()
    
    conn = db_connect()
    conn.execute(
        "UPDATE proposals SET status = ? WHERE id = ?",
        ("rejected", proposal_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({"ok": True, "proposal_id": proposal_id})

@app.route("/file/<root>/<path:relpath>")
def serve_file_route(root: str, relpath: str):
    """Serve a file (for images, etc.)"""
    require_user()
    
    filepath = resolve_path(root, relpath)
    if not filepath or not filepath.exists() or not filepath.is_file():
        abort(404)
    
    return send_file(str(filepath))

@app.route("/preferences", methods=["GET", "POST"])
def preferences():
    """Get or set user preferences"""
    require_user()
    
    if request.method == "GET":
        conn = db_connect()
        rows = conn.execute("SELECT key, value FROM preferences").fetchall()
        conn.close()
        prefs = {r["key"]: r["value"] for r in rows}
        return jsonify({"ok": True, "preferences": prefs})
    
    else:  # POST
        data = request.get_json(force=True) or {}
        for key, value in data.items():
            set_preference(key, json.dumps(value))
        return jsonify({"ok": True})

@app.route("/research", methods=["GET"])
def get_research_list():
    """Get research entries"""
    require_user()
    category = request.args.get("category")
    entries = list_research(category)
    return jsonify({"ok": True, "entries": entries})

@app.route("/research/<int:research_id>", methods=["GET"])
def get_research_detail(research_id: int):
    """Get research entry details"""
    require_user()
    entry = get_research(research_id)
    if not entry:
        return jsonify({"ok": False, "error": "Entry not found"}), 404
    return jsonify({"ok": True, "entry": entry})

# --- HTML UI (embedded) ------------------------------------------------------

# Load HTML UI from separate file for maintainability
HTML_UI_PATH = BASE_DIR / "joi_ui.html"
if HTML_UI_PATH.exists():
    HTML_UI = HTML_UI_PATH.read_text(encoding='utf-8')
else:
    # Fallback minimal UI if file not found
    HTML_UI = """
    <!DOCTYPE html>
    <html><head><title>Joi</title></head>
    <body>
    <h1>Joi - Error</h1>
    <p>joi_ui.html not found. Please ensure it's in the same directory as this script.</p>
    </body></html>
    """

# --- Main Execution ----------------------------------------------------------

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" JOI - Your AI Companion")
    print(" Inspired by Blade Runner 2049")
    print("="*60)
    print(f"\nStarting Joi at: http://localhost:5000")
    print(f"Database: {DB_PATH}")
    print(f"Backups: {BACKUP_DIR}")
    print(f"\nDefault Credentials:")
    print(f"  User Password: {JOI_PASSWORD}")
    print(f"  Admin Password: {JOI_ADMIN_PASSWORD}")
    print(f"\nFile System Roots:")
    for name, path in FILE_ROOTS.items():
        exists = "✓" if Path(path).exists() else "✗"
        print(f"  {exists} {name}: {path}")
    print(f"\nMissing Dependencies:")
    deps = []
    if not HAVE_OPENAI:
        deps.append("  pip install openai")
    if not HAVE_REQUESTS:
        deps.append("  pip install requests")
    if not HAVE_BS4:
        deps.append("  pip install beautifulsoup4 (optional)")
    if not HAVE_SELENIUM:
        deps.append("  pip install selenium webdriver-manager (optional)")
    if not HAVE_PYPDF:
        deps.append("  pip install pypdf (optional)")
    if not HAVE_PIL:
        deps.append("  pip install Pillow (optional)")
    
    if deps:
        print("\n".join(deps))
    else:
        print("  All dependencies installed!")
    
    print("\n" + "="*60 + "\n")
    
    # Run the Flask app
    app.run(
        host="0.0.0.0",  # Allow external connections
        port=5000,
        debug=True,
        threaded=True
    )
