import time
from pathlib import Path
from flask import jsonify, request

import joi_companion
from modules.joi_memory import require_user
from modules.joi_filesystem import resolve_path

EXPORT_SUBDIR = "exports"  # will live under the "project" root


def _safe_filename(name: str, default_ext=".txt") -> str:
    name = (name or "").strip()
    keep = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_. ")
    name = "".join(c for c in name if c in keep).strip().replace(" ", "_")
    if not name:
        name = f"export_{int(time.time())}{default_ext}"
    # ensure it has an extension
    if "." not in name:
        name += default_ext
    return name


def save_text_file(filename: str, content: str):
    """Tool: save text content to project/exports and return a download URL."""
    require_user()
    filename = _safe_filename(filename, default_ext=".txt")

    out_path = resolve_path("project", f"{EXPORT_SUBDIR}/{filename}")
    if not out_path:
        return {"ok": False, "error": "Could not resolve export path"}

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content or "", encoding="utf-8")

    url = f"/file/project/{EXPORT_SUBDIR}/{filename}"
    return {"ok": True, "filename": filename, "url": url}


def save_binary_file(filename: str, data_b64: str):
    """Tool: save base64 content to project/exports and return a download URL."""
    import base64
    require_user()
    filename = _safe_filename(filename, default_ext=".bin")
    out_path = resolve_path("project", f"{EXPORT_SUBDIR}/{filename}")
    if not out_path:
        return {"ok": False, "error": "Could not resolve export path"}

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(data_b64.encode("utf-8")))

    url = f"/file/project/{EXPORT_SUBDIR}/{filename}"
    return {"ok": True, "filename": filename, "url": url}


# Optional API route (UI or manual curl)
def export_save_route():
    require_user()
    data = request.get_json(force=True) or {}
    filename = data.get("filename", "")
    content = data.get("content", "")
    return jsonify(save_text_file(filename, content))


# Register tools
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "save_text_file",
        "description": "Save text to a downloadable file under project/exports and return a download URL.",
        "parameters": {"type": "object", "properties": {
            "filename": {"type": "string", "description": "Example: notes.txt or script.py"},
            "content": {"type": "string", "description": "File contents"}
        }, "required": ["filename", "content"]}
    }},
    save_text_file
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "save_binary_file",
        "description": "Save base64 data to a downloadable file under project/exports and return a download URL.",
        "parameters": {"type": "object", "properties": {
            "filename": {"type": "string"},
            "data_b64": {"type": "string", "description": "Base64-encoded file bytes"}
        }, "required": ["filename", "data_b64"]}
    }},
    save_binary_file
)

# Register route
joi_companion.register_route("/exports/save", ["POST"], export_save_route, "export_save_route")
