"""
modules/joi_exports.py

Binary file export tool. Text file saving is handled by joi_file_output.py.
"""
import base64
import time
from pathlib import Path
from flask import jsonify, request

import joi_companion
from modules.joi_memory import require_user
from modules.joi_files import resolve_path
from modules.joi_downloads import register_download

EXPORT_SUBDIR = "exports"


def _safe_filename(name: str, default_ext: str = ".bin") -> str:
    name = (name or "").strip()
    keep = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_. ")
    name = "".join(c for c in name if c in keep).strip().replace(" ", "_")
    if not name:
        name = f"export_{int(time.time())}{default_ext}"
    if "." not in name:
        name += default_ext
    return name


def save_binary_file(**kwargs) -> dict:
    """Tool: save base64-encoded bytes to project/exports and return a download URL."""
    require_user()
    filename = _safe_filename(kwargs.get("filename", ""), default_ext=".bin")
    data_b64 = kwargs.get("data_b64", "")
    if not data_b64:
        return {"ok": False, "error": "data_b64 is required"}

    out_path = resolve_path("project", f"{EXPORT_SUBDIR}/{filename}")
    if not out_path:
        return {"ok": False, "error": "Could not resolve export path"}

    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        out_path.write_bytes(base64.b64decode(data_b64.encode("utf-8")))
    except Exception as e:
        return {"ok": False, "error": f"Failed to decode/write file: {e}"}

    url = register_download(out_path)
    return {"ok": True, "filename": filename, "url": url}


# API route — delegates text saving to joi_file_output
def export_save_route():
    from modules.joi_auth import require_user
    require_user()
    from flask import request, jsonify
    data = request.get_json(force=True) or {}
    try:
        from modules.joi_files import save_text_file
        return jsonify(save_text_file(**data))
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


# Register tool
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "save_binary_file",
        "description": "Save base64-encoded binary data to a downloadable file. Returns 'url' -- present it as [filename](url).",
        "parameters": {"type": "object", "properties": {
            "filename": {"type": "string", "description": "e.g. image.png or archive.zip"},
            "data_b64": {"type": "string", "description": "Base64-encoded file bytes"},
        }, "required": ["filename", "data_b64"]},
    }},
    save_binary_file,
)

# Register route
joi_companion.register_route("/exports/save", ["POST"], export_save_route, "export_save_route")

print("  [OK] joi_exports -- save_binary_file (1 tool, 1 route)")
