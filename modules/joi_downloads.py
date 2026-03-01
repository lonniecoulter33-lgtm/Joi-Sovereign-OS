"""
modules/joi_downloads.py

Central download registry.  Every module that produces a file calls
    register_download(filepath) -> "/download/<file_id>"
Flask serves GET /download/<file_id> with send_file.
"""
import json
import uuid
from pathlib import Path
from typing import Optional

import joi_companion
from flask import send_file, abort

_BASE = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = _BASE / "projects" / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = OUTPUTS_DIR / "_download_index.json"

# In-memory mirror (loaded once at import, flushed on every write)
_index: dict = {}   # {file_id: {"filename": str, "abspath": str}}

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp"}


def _load_index():
    global _index
    if INDEX_PATH.exists():
        try:
            _index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        except Exception:
            _index = {}
    else:
        _index = {}


def _save_index():
    INDEX_PATH.write_text(json.dumps(_index, indent=2), encoding="utf-8")


def register_download(filepath: Path) -> str:
    """
    Register a file for download.  Returns the URL "/download/<file_id>".
    The file can live anywhere on disk; the index stores the absolute path.
    """
    filepath = filepath.resolve()
    if not filepath.is_file():
        raise FileNotFoundError(f"Cannot register non-file: {filepath}")

    file_id = uuid.uuid4().hex[:12]
    _index[file_id] = {
        "filename": filepath.name,
        "abspath": str(filepath),
    }
    _save_index()
    return f"/download/{file_id}"


# ── Flask route ──────────────────────────────────────────────────────────────

def _serve_download(file_id: str):
    """GET /download/<file_id>"""
    entry = _index.get(file_id)
    if not entry:
        abort(404)

    fp = Path(entry["abspath"])

    # Block path traversal: must still be a real file
    if not fp.is_file():
        abort(404)

    # Extra guard: resolved path must not escape the drive (Windows)
    # and must match what was registered
    if str(fp.resolve()) != entry["abspath"]:
        print(f"  [downloads] path traversal blocked: {file_id}")
        abort(403)

    is_image = fp.suffix.lower() in IMAGE_EXTS
    return send_file(
        str(fp),
        as_attachment=not is_image,
        download_name=entry["filename"],
    )


# ── Startup ──────────────────────────────────────────────────────────────────
_load_index()
joi_companion.register_route(
    "/download/<file_id>", ["GET"], _serve_download, "serve_download"
)
print(f"  [joi_downloads] registry loaded ({len(_index)} files), route /download/<file_id> ready")
