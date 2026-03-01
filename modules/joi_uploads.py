"""
File uploads -- allow UI to upload files to Joi.

POST /upload (multipart/form-data, field: "file")
Returns JSON: { ok, filename, url }
Saved under: assets/uploads/

Also provides:
- read_upload tool: lets Joi read uploaded text files
- list_uploads tool: lets Joi list recent uploads
- _pending_uploads list: tracks recent uploads so /chat can inject context
"""
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List

from flask import request, jsonify

import joi_companion
from modules.joi_memory import require_user

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "assets" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTS = {
    ".txt", ".md", ".json", ".csv",
    ".png", ".jpg", ".jpeg", ".webp", ".gif",
    ".pdf", ".docx", ".doc",
    ".py", ".js", ".html", ".css",
    ".zip"
}

# Text-readable extensions (non-binary)
TEXT_EXTS = {".txt", ".md", ".json", ".csv", ".py", ".js", ".html", ".css"}

# Track recent uploads so /chat can inject awareness (cleared after injection)
_pending_uploads: List[Dict[str, str]] = []
_MAX_PENDING = 5


def _safe_name(name: str) -> str:
    name = (name or "upload").strip()
    name = name.replace("\\", "/").split("/")[-1]
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    if not name:
        name = "upload"
    return name[:120]


def get_pending_uploads() -> List[Dict[str, str]]:
    """Return and clear pending uploads for /chat injection."""
    global _pending_uploads
    pending = list(_pending_uploads)
    _pending_uploads = []
    return pending


def upload_route():
    require_user()

    if "file" not in request.files:
        return jsonify({"ok": False, "error": "No file field named 'file'"}), 400

    f = request.files["file"]
    if not f or not f.filename:
        return jsonify({"ok": False, "error": "No file selected"}), 400

    filename = _safe_name(f.filename)
    ext = Path(filename).suffix.lower()

    if ext and ext not in ALLOWED_EXTS:
        return jsonify({"ok": False, "error": f"File type not allowed: {ext}"}), 400

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_name = f"{Path(filename).stem}_{stamp}{ext or ''}"
    out_path = UPLOAD_DIR / out_name

    f.save(str(out_path))

    # Track this upload so Joi knows about it
    _pending_uploads.append({
        "filename": out_name,
        "original_name": f.filename,
        "path": str(out_path),
        "ext": ext,
        "readable": ext in TEXT_EXTS,
    })
    # Cap pending list
    while len(_pending_uploads) > _MAX_PENDING:
        _pending_uploads.pop(0)

    url = f"/file/project/assets/uploads/{out_name}"
    return jsonify({"ok": True, "filename": out_name, "url": url})


# ── Tool: read_upload ────────────────────────────────────────────────────────

def read_upload(**kwargs) -> Dict[str, Any]:
    """Read the contents of an uploaded file by filename."""
    filename = kwargs.get("filename", "")
    if not filename:
        # If no filename given, try the most recent upload
        try:
            files = sorted(UPLOAD_DIR.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
            if files:
                filename = files[0].name
            else:
                return {"ok": False, "error": "No uploads found"}
        except Exception as e:
            return {"ok": False, "error": f"Could not list uploads: {e}"}

    # Sanitize
    filename = Path(filename).name  # strip any path traversal
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        # Try fuzzy match
        matches = [f for f in UPLOAD_DIR.iterdir() if filename.lower() in f.name.lower()]
        if matches:
            file_path = matches[0]
        else:
            return {"ok": False, "error": f"File not found: {filename}"}

    ext = file_path.suffix.lower()

    # PDF files -- extract text with pypdf
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(file_path))
            pages_text = []
            for i, page in enumerate(reader.pages):
                txt = page.extract_text() or ""
                if txt.strip():
                    pages_text.append(f"[Page {i+1}]\n{txt}")
            if not pages_text:
                return {
                    "ok": False,
                    "filename": file_path.name,
                    "error": "PDF has no extractable text (may be a scanned image — use analyze_screen on it instead)",
                }
            content = "\n\n".join(pages_text)
            truncated = len(content) > 20000
            if truncated:
                content = content[:20000] + "\n\n... [truncated]"
            return {
                "ok": True,
                "filename": file_path.name,
                "type": "pdf",
                "pages": len(reader.pages),
                "content": content,
                "truncated": truncated,
            }
        except ImportError:
            return {"ok": False, "error": "pypdf not installed -- cannot read PDF"}
        except Exception as e:
            return {"ok": False, "error": f"Could not read PDF: {e}"}

    # DOCX files -- extract text with python-docx
    if ext in (".docx", ".doc"):
        try:
            import docx as _docx
            doc = _docx.Document(str(file_path))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            if not paragraphs:
                return {"ok": False, "filename": file_path.name,
                        "error": "Word document appears to have no readable text"}
            content = "\n\n".join(paragraphs)
            truncated = len(content) > 20000
            if truncated:
                content = content[:20000] + "\n\n... [truncated]"
            return {
                "ok": True,
                "filename": file_path.name,
                "type": "docx",
                "paragraphs": len(paragraphs),
                "content": content,
                "truncated": truncated,
            }
        except ImportError:
            return {"ok": False, "error": "python-docx not installed -- cannot read Word files"}
        except Exception as e:
            return {"ok": False, "error": f"Could not read Word file: {e}"}

    # Other binary files (images, zip) -- return metadata only
    if ext not in TEXT_EXTS:
        size = file_path.stat().st_size
        return {
            "ok": True,
            "filename": file_path.name,
            "type": "binary",
            "size_bytes": size,
            "message": f"Binary file ({ext}), {size} bytes. Use analyze_screen or analyze_camera for images.",
        }

    # Text files -- read content
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        truncated = len(content) > 15000
        if truncated:
            content = content[:15000] + "\n\n... [truncated, file has more content]"
        return {
            "ok": True,
            "filename": file_path.name,
            "type": "text",
            "content": content,
            "truncated": truncated,
        }
    except Exception as e:
        return {"ok": False, "error": f"Could not read file: {e}"}


def list_uploads(**kwargs) -> Dict[str, Any]:
    """List recent uploaded files."""
    limit = int(kwargs.get("limit", 10))
    try:
        files = sorted(UPLOAD_DIR.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
        items = []
        for f in files[:limit]:
            ext = f.suffix.lower()
            items.append({
                "filename": f.name,
                "size_bytes": f.stat().st_size,
                "readable": ext in TEXT_EXTS,
                "ext": ext,
            })
        return {"ok": True, "files": items, "total": len(files)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ── Register ─────────────────────────────────────────────────────────────────

joi_companion.register_route("/upload", ["POST"], upload_route, "upload_route")

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "read_upload",
        "description": "Read the contents of an uploaded file. If no filename given, reads the most recent upload.",
        "parameters": {"type": "object", "properties": {
            "filename": {"type": "string", "description": "Name of the uploaded file (optional, defaults to most recent)"}
        }}
    }},
    read_upload,
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "list_uploads",
        "description": "List recently uploaded files with their names and sizes.",
        "parameters": {"type": "object", "properties": {
            "limit": {"type": "integer", "description": "Max files to return (default 10)"}
        }}
    }},
    list_uploads,
)

print("    [OK] joi_uploads (File Uploads: 2 tools, 1 route)")
