from __future__ import annotations
import difflib
import json
from pathlib import Path
from typing import Any, Dict

from .joi_memory import require_admin, add_pending_op
from joi_registry import register_tool

BASE_DIR = Path(__file__).resolve().parents[1]
MODULES_DIR = BASE_DIR / "modules"

def _safe_target(path: str) -> Path | None:
    p = (MODULES_DIR / path).resolve() if not path.startswith("modules/") else (BASE_DIR / path).resolve()
    try:
        p.relative_to(MODULES_DIR)
    except Exception:
        return None
    if not p.exists() or not p.is_file() or p.suffix != ".py":
        return None
    return p

def _tool_propose_patch(args: Dict[str, Any]) -> Dict[str, Any]:
    require_admin()
    target = args.get("target", "")
    new_content = args.get("content", "")
    p = _safe_target(target)
    if not p:
        return {"ok": False, "error": "Target must be an existing .py inside modules/."}
    old = p.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    new = new_content.splitlines(keepends=True)
    diff = "".join(difflib.unified_diff(old, new, fromfile=str(p), tofile=str(p), lineterm=""))
    op_id = add_pending_op("patch", {"target": str(p.relative_to(BASE_DIR)), "diff": diff, "bytes": len(new_content.encode("utf-8"))})
    return {"ok": True, "pending_op_id": op_id, "diff": diff[:8000], "note": "Patch staged. Apply with confirm=true using patch_apply."}

def _tool_apply_patch(args: Dict[str, Any]) -> Dict[str, Any]:
    require_admin()
    confirm = bool(args.get("confirm", False))
    target = args.get("target", "")
    diff_text = args.get("diff", "")
    p = _safe_target(target)
    if not p:
        return {"ok": False, "error": "Invalid target"}
    if not confirm:
        op_id = add_pending_op("patch_apply", {"target": str(p.relative_to(BASE_DIR)), "diff": diff_text[:200000]})
        return {"ok": True, "pending_op_id": op_id, "note": "Apply staged. Re-run with confirm=true to apply."}

    # naive apply: if diff not provided, refuse
    if not diff_text.strip():
        return {"ok": False, "error": "diff is required to apply patch"}
    # apply by replacing whole file not by hunks (simpler, safer for MVP)
    # Expect caller to pass full 'content' instead? We'll support that too.
    if "content" in args and args["content"]:
        p.write_text(args["content"], encoding="utf-8")
        return {"ok": True, "applied": str(p)}
    return {"ok": False, "error": "For MVP, provide full 'content' when confirm=true."}

register_tool({
    "type": "function",
    "function": {
        "name": "patch_propose",
        "description": "Stage a patch by providing full new content for a modules/*.py file. Admin only.",
        "parameters": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Relative path under modules/, e.g. joi_llm.py"},
                "content": {"type": "string", "description": "Full new file content"}
            },
            "required": ["target", "content"]
        }
    }
}, _tool_propose_patch)

register_tool({
    "type": "function",
    "function": {
        "name": "patch_apply",
        "description": "Apply a staged patch. For MVP, provide full content and confirm=true. Admin only.",
        "parameters": {
            "type": "object",
            "properties": {
                "target": {"type": "string"},
                "content": {"type": "string"},
                "diff": {"type": "string"},
                "confirm": {"type": "boolean"}
            },
            "required": ["target"]
        }
    }
}, _tool_apply_patch)
