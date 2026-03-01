"""
File uploads — allow UI to upload files to Joi.

POST /upload (multipart/form-data, field: "file")
Returns JSON: { ok, filename, url }
Saved under: assets/uploads/
"""
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

from flask import request, jsonify

import joi_companion
from modules.joi_memory import require_user

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "assets" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTS = {
    ".txt", ".md", ".json", ".csv",
    ".png", ".jpg", ".jpeg", ".webp", ".gif",
    ".pdf",
    ".py", ".js", ".html", ".css",
    ".zip"
}

def _safe_name(name: str) -> str:
    name = (name or "upload").strip()
    name = name.replace("\\", "/").split("/")[-1]
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    if not name:
        name = "upload"
    return name[:120]

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

    url = f"/file/project/assets/uploads/{out_name}"
    return jsonify({"ok": True, "filename": out_name, "url": url})

# Register route
joi_companion.register_route("/upload", ["POST"], upload_route, "upload_route")
