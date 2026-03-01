"""
Code patching -- safe, targeted edits (targets specific modules, not monolith)
"""

import ast
import hashlib
import os
import tempfile
from contextlib import contextmanager
import json
import difflib
from pathlib import Path
from datetime import datetime, timezone

from modules.joi_db import db_connect
from modules.joi_files import fs_read, FILE_ROOTS, resolve_path

BASE_DIR = Path(__file__).resolve().parent.parent
BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def propose_patch(summary: str, target_root: str, target_path: str, new_text: str):
    """Propose a code change. Safer when targeting small modules instead of monolith."""
    conn = db_connect()
    current = fs_read(target_root, target_path)
    current_text = current.get("text", "") if current.get("ok") else ""
    diff = list(difflib.unified_diff(
        current_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
        fromfile=f"{target_root}/{target_path} (current)",
        tofile=f"{target_root}/{target_path} (proposed)", lineterm=''))
    payload = json.dumps({"target_root": target_root, "target_path": target_path,
                          "current_text": current_text, "new_text": new_text, "diff": ''.join(diff)})
    cur = conn.execute(
        "INSERT INTO proposals (ts, status, kind, target_file, summary, payload) VALUES (?, ?, ?, ?, ?, ?)",
        (now_iso(), "pending", "patch", f"{target_root}/{target_path}", summary, payload))
    conn.commit()
    conn.close()
    return cur.lastrowid

def propose_orchestration(task_description: str, project_path: str = "", project_id: str = ""):
    """Create an orchestration proposal. User reviews in Proposals tab; on approve, task is sent to Agent Terminal."""
    task_description = (task_description or "").strip()
    if not task_description:
        return None
    project_path = (project_path or str(BASE_DIR)).strip()
    payload = {
        "task_description": task_description,
        "project_path": project_path,
        "project_id": (project_id or "").strip(),
    }
    summary = task_description[:200] + ("..." if len(task_description) > 200 else "")
    target_file = project_path or "Agent Terminal"
    conn = db_connect()
    cur = conn.execute(
        "INSERT INTO proposals (ts, status, kind, target_file, summary, payload) VALUES (?, ?, ?, ?, ?, ?)",
        (now_iso(), "pending", "orchestration", target_file, summary, json.dumps(payload)),
    )
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid


def create_plugin(name: str, description: str, code: str):
    """Create a NEW plugin file (no risk to existing code)."""
    try:
        safe_name = name.replace(" ", "_").replace("-", "_").lower()
        if not safe_name.endswith(".py"):
            safe_name += ".py"
        plugin_path = BASE_DIR / "plugins" / safe_name
        if plugin_path.exists():
            return {"ok": False, "error": f"Plugin '{safe_name}' already exists"}
        plugin_path.write_text(code, encoding='utf-8')
        return {"ok": True, "message": f"Plugin '{safe_name}' created! Restart Joi to activate.",
                "path": str(plugin_path)}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def get_proposal(proposal_id: int):
    conn = db_connect()
    row = conn.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,)).fetchone()
    conn.close()
    if not row:
        return None
    payload = json.loads(row["payload"])
    return {"id": row["id"], "ts": row["ts"], "status": row["status"], "kind": row["kind"],
            "target_file": row["target_file"], "summary": row["summary"], "payload": payload,
            "approved_by": row["approved_by"], "applied_ts": row["applied_ts"]}

def list_proposals(status=None):
    conn = db_connect()
    if status:
        rows = conn.execute("SELECT id, ts, status, kind, target_file, summary FROM proposals WHERE status = ? ORDER BY id DESC",
                            (status,)).fetchall()
    else:
        rows = conn.execute("SELECT id, ts, status, kind, target_file, summary FROM proposals ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def _syntax_check_python(text: str, filename: str = "<patched>") -> None:
    # Raises SyntaxError if bad
    ast.parse(text, filename=filename)

@contextmanager
def _patch_lock(lock_path: Path):
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    # Simple cross-process lock using exclusive create
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode("utf-8"))
        os.close(fd)
        yield
    finally:
        try:
            lock_path.unlink(missing_ok=True)
        except Exception:
            pass

def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", dir=str(path.parent), suffix=".tmp") as tf:
        tf.write(text)
        tmp_name = tf.name
    os.replace(tmp_name, str(path))


def apply_patch(proposal_id: int, approved_by: str):
    proposal = get_proposal(proposal_id)
    if not proposal:
        return {"ok": False, "error": f"Proposal {proposal_id} not found"}
    if proposal["status"] != "pending":
        return {"ok": False, "error": f"Proposal already {proposal['status']}"}

    payload = proposal["payload"]
    filepath = resolve_path(payload["target_root"], payload["target_path"])
    if not filepath:
        return {"ok": False, "error": "Invalid target path"}

    lock_path = BACKUP_DIR / ".apply_patch.lock"
    with _patch_lock(lock_path):
        # Re-read file at time of apply (prevents “diff drift”)
        current = fs_read(payload["target_root"], payload["target_path"])
        current_text = current.get("text", "") if current.get("ok") else ""

        # Optional: refuse if file changed since proposal was created
        proposed_current = payload.get("current_text", "")
        if proposed_current and _sha256(proposed_current) != _sha256(current_text):
            return {
                "ok": False,
                "error": "Target file changed since proposal was created (refusing to apply). Re-propose patch.",
            }

        new_text = payload["new_text"]

        # Preflight: syntax check Python files
        if str(filepath).lower().endswith(".py"):
            try:
                _syntax_check_python(new_text, filename=str(filepath))
            except SyntaxError as e:
                # Mark proposal rejected/failed so it doesn’t keep resurfacing
                conn = db_connect()
                conn.execute(
                    "UPDATE proposals SET status = ?, approved_by = ?, applied_ts = ? WHERE id = ?",
                    ("failed", approved_by, now_iso(), proposal_id)
                )
                conn.commit()
                conn.close()
                return {"ok": False, "error": f"SyntaxError: {e.msg} at line {e.lineno}:{e.offset}"}

        backup_path = None
        try:
            # Backup current file
            if filepath.exists():
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = BACKUP_DIR / f"{filepath.name}.{ts}.bak"
                import shutil
                shutil.copy2(filepath, backup_path)

            # Atomic write
            _atomic_write_text(filepath, new_text)

            # Mark as applied
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
                "file": f"{payload['target_root']}/{payload['target_path']}",
                "backup": str(backup_path) if backup_path else None,
            }

        except Exception as e:
            # Rollback if we created a backup
            try:
                if backup_path and backup_path.exists():
                    import shutil
                    shutil.copy2(backup_path, filepath)
            except Exception:
                pass

            # Mark failed
            try:
                conn = db_connect()
                conn.execute(
                    "UPDATE proposals SET status = ?, approved_by = ?, applied_ts = ? WHERE id = ?",
                    ("failed", approved_by, now_iso(), proposal_id)
                )
                conn.commit()
                conn.close()
            except Exception:
                pass

            return {"ok": False, "error": f"Apply failed (rolled back if possible): {e}"}

# ── kwargs adapters (LLM tool calls pass **kwargs, not positional args) ──
def _propose_patch_wrapper(**kwargs):
    return propose_patch(
        summary=kwargs.get("summary", ""),
        target_root=kwargs.get("target_root", ""),
        target_path=kwargs.get("target_path", ""),
        new_text=kwargs.get("new_text", "")
    )

def _create_plugin_wrapper(**kwargs):
    return create_plugin(
        name=kwargs.get("name", ""),
        description=kwargs.get("description", ""),
        code=kwargs.get("code", "")
    )

# Register tools
import joi_companion
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "propose_patch",
        "description": "Propose a code change (requires Lonnie's approval). Target specific modules/*.py files, NOT the entire monolith.",
        "parameters": {"type": "object", "properties": {
            "summary": {"type": "string"},
            "target_root": {"type": "string", "enum": list(FILE_ROOTS.keys())},
            "target_path": {"type": "string", "description": "e.g. 'modules/joi_launcher.py' -- target SMALL files"},
            "new_text": {"type": "string"}
        }, "required": ["summary", "target_root", "target_path", "new_text"]}
    }},
    _propose_patch_wrapper
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "create_plugin",
        "description": "Create a NEW plugin file in plugins/ (no risk to existing code). Best for entirely new capabilities.",
        "parameters": {"type": "object", "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "code": {"type": "string"}
        }, "required": ["name", "description", "code"]}
    }},
    _create_plugin_wrapper
)


def _create_orchestration_proposal_wrapper(**kwargs):
    pid = propose_orchestration(
        task_description=kwargs.get("task_description", ""),
        project_path=kwargs.get("project_path", ""),
        project_id=kwargs.get("project_id", ""),
    )
    if pid is None:
        return {"ok": False, "error": "Missing or empty task_description"}
    return {
        "ok": True,
        "proposal_id": pid,
        "message": "Proposal created. Lonnie can review it in the Proposals tab and approve to run in Agent Terminal.",
    }


joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "create_orchestration_proposal",
        "description": "Create a coding/orchestration proposal for Lonnie to review. He reviews in the Proposals tab and approves to run in Agent Terminal. Use for build, create app, fix code, refactor, or any multi-step coding task.",
        "parameters": {"type": "object", "properties": {
            "task_description": {"type": "string", "description": "What to build, fix, or change"},
            "project_path": {"type": "string", "description": "Optional path to project folder (defaults to Joi root)"},
            "project_id": {"type": "string", "description": "Optional project ID if saving to a project"},
        }, "required": ["task_description"]}
    }},
    _create_orchestration_proposal_wrapper,
)

# Register routes
from flask import jsonify, request as flask_req
from modules.joi_memory import require_user, require_admin

def get_proposals():
    require_user()
    return jsonify({"ok": True, "proposals": list_proposals(flask_req.args.get("status"))})

def get_proposal_detail(proposal_id: int):
    require_user()
    p = get_proposal(proposal_id)
    if not p:
        return jsonify({"ok": False, "error": "Not found"}), 404
    return jsonify({"ok": True, "proposal": p})

def approve_proposal(proposal_id: int):
    session = require_admin()
    proposal = get_proposal(proposal_id)
    if not proposal:
        return jsonify({"ok": False, "error": "Proposal not found"}), 404
    if proposal["status"] != "pending":
        return jsonify({"ok": False, "error": f"Proposal already {proposal['status']}"}), 400

    if proposal["kind"] == "orchestration":
        # Send to Agent Terminal instead of applying a patch
        payload = proposal["payload"]
        task_description = payload.get("task_description", "")
        project_path = payload.get("project_path", str(BASE_DIR))
        if not task_description:
            return jsonify({"ok": False, "error": "Orchestration proposal has no task description"}), 400
        try:
            from modules.joi_orchestrator import orchestrate_task
            result = orchestrate_task(task_description=task_description, project_path=project_path)
        except Exception as e:
            conn = db_connect()
            conn.execute(
                "UPDATE proposals SET status = ?, applied_ts = ? WHERE id = ?",
                ("failed", now_iso(), proposal_id),
            )
            conn.commit()
            conn.close()
            return jsonify({"ok": False, "error": str(e)}), 500
        if not result.get("ok"):
            return jsonify(result), 400
        conn = db_connect()
        conn.execute(
            "UPDATE proposals SET status = ?, approved_by = ?, applied_ts = ? WHERE id = ?",
            ("sent_to_terminal", session.get("token", "admin"), now_iso(), proposal_id),
        )
        conn.commit()
        conn.close()
        return jsonify({
            "ok": True,
            "proposal_id": proposal_id,
            "message": "Sent to Agent Terminal. Check the Agent Terminal tab for progress.",
            "session_id": result.get("session_id"),
        })
    # Patch or other: apply as before
    result = apply_patch(proposal_id, session.get("token", "admin"))
    return jsonify(result) if result["ok"] else (jsonify(result), 400)

def reject_proposal(proposal_id: int):
    require_admin()
    conn = db_connect()
    conn.execute("UPDATE proposals SET status = ? WHERE id = ?", ("rejected", proposal_id))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "proposal_id": proposal_id})

joi_companion.register_route("/proposals", ["GET"], get_proposals, "get_proposals")
joi_companion.register_route("/proposals/<int:proposal_id>", ["GET"], get_proposal_detail, "get_proposal_detail")
joi_companion.register_route("/proposals/<int:proposal_id>/approve", ["POST"], approve_proposal, "approve_proposal")
joi_companion.register_route("/proposals/<int:proposal_id>/reject", ["POST"], reject_proposal, "reject_proposal")
