from __future__ import annotations
import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .joi_memory import require_admin, add_pending_op
from joi_registry import register_tool

BASE_DIR = Path(__file__).resolve().parents[1]

# Configure roots. You can extend these in .env
ROOTS = {
    "base": BASE_DIR,
    "projects": Path(os.getenv("JOI_PROJECTS_DIR", str(BASE_DIR / "projects"))),
    "assets": Path(os.getenv("JOI_ASSETS_DIR", str(BASE_DIR / "assets"))),
}

def resolve_path(root: str, relpath: str) -> Optional[Path]:
    if root not in ROOTS:
        return None
    root_path = ROOTS[root].resolve()
    p = (root_path / relpath).resolve()
    # prevent path traversal
    try:
        p.relative_to(root_path)
    except Exception:
        return None
    return p

def _tool_list_dir(args: Dict[str, Any]) -> Dict[str, Any]:
    root = args.get("root", "base")
    rel = args.get("path", "")
    p = resolve_path(root, rel)
    if not p or not p.exists() or not p.is_dir():
        return {"ok": False, "error": "Directory not found"}
    items=[]
    for child in sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
        items.append({"name": child.name, "is_dir": child.is_dir(), "size": child.stat().st_size if child.is_file() else None})
    return {"ok": True, "root": root, "path": rel, "items": items}

def _tool_read_file(args: Dict[str, Any]) -> Dict[str, Any]:
    root = args.get("root", "base")
    rel = args.get("path", "")
    p = resolve_path(root, rel)
    if not p or not p.exists() or not p.is_file():
        return {"ok": False, "error": "File not found"}
    # Size guard
    max_bytes = int(os.getenv("JOI_MAX_READ_BYTES", "200000"))
    data = p.read_bytes()
    if len(data) > max_bytes:
        return {"ok": False, "error": f"File too large ({len(data)} bytes). Limit is {max_bytes}."}
    try:
        text = data.decode("utf-8")
        return {"ok": True, "text": text}
    except UnicodeDecodeError:
        return {"ok": True, "base64": True, "bytes": len(data)}

def _tool_write_file(args: Dict[str, Any]) -> Dict[str, Any]:
    # Admin required for writes
    require_admin()
    root = args.get("root", "base")
    rel = args.get("path", "")
    content = args.get("content", "")
    confirm = bool(args.get("confirm", False))
    p = resolve_path(root, rel)
    if not p:
        return {"ok": False, "error": "Invalid path/root"}
    p.parent.mkdir(parents=True, exist_ok=True)
    op_id = add_pending_op("write_file", {"root": root, "path": rel, "bytes": len(content.encode("utf-8")), "preview": content[:2000]})
    if not confirm:
        return {"ok": True, "pending_op_id": op_id, "note": "Write staged. Re-run with confirm=true to apply."}
    p.write_text(content, encoding="utf-8")
    return {"ok": True, "wrote": str(p), "pending_op_id": op_id}

def _tool_delete_path(args: Dict[str, Any]) -> Dict[str, Any]:
    require_admin()
    root = args.get("root", "base")
    rel = args.get("path", "")
    confirm = bool(args.get("confirm", False))
    p = resolve_path(root, rel)
    if not p or not p.exists():
        return {"ok": False, "error": "Path not found"}
    op_id = add_pending_op("delete_path", {"root": root, "path": rel, "is_dir": p.is_dir()})
    if not confirm:
        return {"ok": True, "pending_op_id": op_id, "note": "Delete staged. Re-run with confirm=true to apply."}
    if p.is_dir():
        # only delete empty dirs for safety
        try:
            p.rmdir()
        except OSError:
            return {"ok": False, "error": "Directory not empty. Refusing to delete recursively."}
    else:
        p.unlink()
    return {"ok": True, "deleted": str(p), "pending_op_id": op_id}

# Register tools
register_tool({
    "type": "function",
    "function": {
        "name": "fs_list_dir",
        "description": "List directory contents under a safe root (base/projects/assets).",
        "parameters": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "enum": list(ROOTS.keys())},
                "path": {"type": "string", "description": "Relative path under the root"}
            },
            "required": ["root", "path"]
        }
    }
}, _tool_list_dir)

register_tool({
    "type": "function",
    "function": {
        "name": "fs_read_file",
        "description": "Read a text file under a safe root (returns text if UTF-8).",
        "parameters": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "enum": list(ROOTS.keys())},
                "path": {"type": "string"}
            },
            "required": ["root", "path"]
        }
    }
}, _tool_read_file)

register_tool({
    "type": "function",
    "function": {
        "name": "fs_write_file",
        "description": "Write a text file under a safe root. Admin only. Use confirm=true to actually write.",
        "parameters": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "enum": list(ROOTS.keys())},
                "path": {"type": "string"},
                "content": {"type": "string"},
                "confirm": {"type": "boolean"}
            },
            "required": ["root", "path", "content"]
        }
    }
}, _tool_write_file)

register_tool({
    "type": "function",
    "function": {
        "name": "fs_delete_path",
        "description": "Delete a file or empty directory under a safe root. Admin only. Use confirm=true to actually delete.",
        "parameters": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "enum": list(ROOTS.keys())},
                "path": {"type": "string"},
                "confirm": {"type": "boolean"}
            },
            "required": ["root", "path"]
        }
    }
}, _tool_delete_path)
