"""
modules/joi_code_edit.py

Surgical Code Editing -- Claude-Code-style file editing for Joi
================================================================

Gives Joi the ability to make precise, safe edits to her own code:
  - Exact string replacement (like Claude Code's Edit tool)
  - Insert code at specific locations
  - Read specific sections by line range
  - Search within files
  - Auto-backup before every edit
  - Rollback to previous versions
  - Creative editing: add new features to UI/modules

This is the critical missing piece that lets Joi go from
"I can see the problem" to "I can fix it myself safely."
"""

from __future__ import annotations

import os
import re
import json
import time
import shutil
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

import joi_companion
from flask import jsonify, request as flask_req

# ── Lazy auth import ─────────────────────────────────────────────────────────
def _require_user():
    from modules.joi_memory import require_user
    return require_user()

BASE_DIR = Path(__file__).resolve().parent.parent
MODULES_DIR = BASE_DIR / "modules"
BACKUP_DIR = BASE_DIR / "data" / "code_backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# Track recent edits for undo
_edit_history: List[Dict[str, Any]] = []
_MAX_HISTORY = 50


# ============================================================================
# MULTI-MODEL CODE ANALYSIS (config.joi_models: coding primary + fallback)
# ============================================================================

def _call_code_model(system_prompt: str, user_prompt: str, max_tokens: int = 2000) -> Optional[str]:
    """
    Route code analysis per config.joi_models: coding -> OpenAI (gpt-4o), fallback Gemini (reasoning).
    Returns the model response text, or None if all fail.
    """
    from config.joi_models import TASK_MODEL_ROUTING, OPENAI_MODELS, GEMINI_MODELS
    route = TASK_MODEL_ROUTING.get("coding", {"primary": ("openai", OPENAI_MODELS["coding"]), "fallback": ("gemini", GEMINI_MODELS["reasoning"])})
    primary = route.get("primary", ("openai", OPENAI_MODELS["coding"]))
    fallback = route.get("fallback", ("gemini", GEMINI_MODELS["reasoning"]))
    models_tried = []

    def try_openai(model_id: str) -> Optional[str]:
        try:
            from modules.joi_llm import _call_openai
            messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
            resp = _call_openai(messages, tools=None, max_tokens=max_tokens, model=model_id)
            if resp and getattr(resp, "choices", None):
                text = resp.choices[0].message.content
                if text:
                    print(f"  [code_edit] Used OpenAI ({model_id}) for code analysis")
                    return text
        except Exception as e:
            models_tried.append(f"openai:{model_id}:{e}")
        return None

    def try_gemini(model_id: str) -> Optional[str]:
        try:
            from modules.joi_llm import _call_gemini
            text = _call_gemini(f"{system_prompt}\n\n{user_prompt}", max_tokens=max_tokens, model=model_id)
            if text:
                print(f"  [code_edit] Used Gemini ({model_id}) for code analysis")
                return text
        except Exception as e:
            models_tried.append(f"gemini:{model_id}:{e}")
        return None

    for provider, model_id in (primary, fallback):
        if provider == "openai":
            out = try_openai(model_id)
        else:
            out = try_gemini(model_id)
        if out:
            return out

    print(f"  [code_edit] All models failed: {models_tried}")
    return None


# ============================================================================
# BACKUP / ROLLBACK
# ============================================================================

def _backup_file(file_path: Path) -> Optional[str]:
    """Create a timestamped backup of a file. Returns backup path."""
    if not file_path.exists():
        return None
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = file_path.name.replace(" ", "_")
    backup_name = f"{safe_name}.{ts}.bak"
    backup_path = BACKUP_DIR / backup_name
    shutil.copy2(str(file_path), str(backup_path))
    return str(backup_path)


def _get_backups(filename: str) -> List[Dict[str, Any]]:
    """List all backups for a given filename."""
    safe_name = filename.replace(" ", "_")
    backups = []
    for f in sorted(BACKUP_DIR.glob(f"{safe_name}.*.bak"), reverse=True):
        try:
            stat = f.stat()
            backups.append({
                "path": str(f),
                "name": f.name,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        except Exception:
            pass
    return backups


def _resolve_file(file_ref: str) -> Optional[Path]:
    """Resolve a file reference to an absolute path. Handles relative paths, module names, etc."""
    # Already absolute
    p = Path(file_ref)
    if p.is_absolute() and p.exists():
        return p

    # Try relative to project root
    candidates = [
        BASE_DIR / file_ref,
        MODULES_DIR / file_ref,
        BASE_DIR / "modules" / file_ref,
    ]
    # Handle bare module names like "joi_media.py" or "joi_ui.html"
    if not file_ref.startswith("modules/"):
        candidates.append(MODULES_DIR / file_ref)

    for c in candidates:
        if c.exists():
            return c

    return None


# ============================================================================
# SMOKE TEST + AUTO-ROLLBACK HELPERS
# ============================================================================

def _smoke_test_and_rollback(file_path: Path, backup_path: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Run smoke test on a file after editing. If it fails, auto-rollback.
    Returns smoke test result dict, or None if no test was needed.
    """
    # Only smoke test Python and HTML files
    if file_path.suffix not in (".py", ".html"):
        return None

    try:
        from modules.joi_router import smoke_test_file
        result = smoke_test_file(str(file_path))
    except ImportError:
        # Router not loaded yet -- do basic syntax check inline
        result = {"passed": True, "errors": []}
        if file_path.suffix == ".py":
            try:
                source = file_path.read_text(encoding="utf-8")
                compile(source, str(file_path), "exec")
            except SyntaxError as e:
                result = {"passed": False, "errors": [f"Syntax error at line {e.lineno}: {e.msg}"]}

    if not result.get("passed") and backup_path:
        # Auto-rollback
        try:
            shutil.copy2(backup_path, str(file_path))
            result["rolled_back"] = True
            print(f"  [code_edit] SMOKE TEST FAILED -- auto-rolled back {file_path.name}")
            print(f"  [code_edit] Errors: {result.get('errors', [])}")
        except Exception as e:
            result["rollback_error"] = str(e)
            print(f"  [code_edit] SMOKE TEST FAILED and rollback failed: {e}")

    return result


def _log_edit_to_learning(action: str, file_path: str, smoke_result: Optional[Dict[str, Any]]):
    """Log an edit outcome to the learning system (background, non-blocking)."""
    import threading

    def _log():
        try:
            from modules.joi_learning import log_tool_usage
            passed = smoke_result.get("passed", True) if smoke_result else True
            log_tool_usage(
                tool_name=action,
                success=passed,
                context={"file": file_path},
                outcome="passed smoke test" if passed else f"failed: {smoke_result.get('errors', [])}",
            )
        except (ImportError, AttributeError):
            pass  # Learning system not ready or log_tool_usage not yet added
        except Exception as e:
            print(f"  [code_edit] Learning log error: {e}")

    threading.Thread(target=_log, daemon=True).start()


# ============================================================================
# TOOLS
# ============================================================================

def code_edit(**kwargs) -> Dict[str, Any]:
    """
    Exact string replacement in a file -- like Claude Code's Edit tool.
    Finds old_text in the file and replaces it with new_text.
    Auto-creates a backup before editing.

    This is the primary editing tool. It's surgical and safe.
    """
    _require_user()

    file_path = kwargs.get("file_path", "").strip()
    old_text = kwargs.get("old_text", "")
    new_text = kwargs.get("new_text", "")

    if not file_path:
        return {"ok": False, "error": "Provide 'file_path' to edit."}
    if not old_text:
        return {"ok": False, "error": "Provide 'old_text' -- the exact text to find and replace."}
    if old_text == new_text:
        return {"ok": False, "error": "old_text and new_text are identical -- nothing to change."}

    resolved = _resolve_file(file_path)
    if not resolved:
        return {"ok": False, "error": f"File not found: {file_path}"}

    try:
        content = resolved.read_text(encoding="utf-8")
    except Exception as e:
        return {"ok": False, "error": f"Cannot read file: {e}"}

    # Check old_text exists in file
    count = content.count(old_text)
    if count == 0:
        # Try to help -- show nearby matches
        first_line = old_text.split("\n")[0].strip()[:60]
        return {
            "ok": False,
            "error": f"old_text not found in {resolved.name}. First line searched: '{first_line}'. "
                     f"Make sure you're matching the exact text including whitespace/indentation."
        }
    if count > 1:
        return {
            "ok": False,
            "error": f"old_text found {count} times in {resolved.name}. "
                     f"Provide more surrounding context to make the match unique."
        }

    # Backup
    backup_path = _backup_file(resolved)

    # Apply edit
    new_content = content.replace(old_text, new_text, 1)
    resolved.write_text(new_content, encoding="utf-8")

    # Smoke test -- auto-rollback on failure
    smoke = _smoke_test_and_rollback(resolved, backup_path)

    # Log
    _edit_history.append({
        "ts": time.time(),
        "action": "code_edit",
        "file": str(resolved),
        "backup": backup_path,
        "old_len": len(old_text),
        "new_len": len(new_text),
        "smoke_test": smoke,
    })
    if len(_edit_history) > _MAX_HISTORY:
        _edit_history.pop(0)

    # Log to learning system
    _log_edit_to_learning("code_edit", str(resolved), smoke)

    lines_changed = abs(new_text.count("\n") - old_text.count("\n"))
    result = {
        "ok": True,
        "message": f"Edited {resolved.name}: replaced {len(old_text)} chars with {len(new_text)} chars",
        "file": str(resolved),
        "backup": backup_path,
        "lines_delta": lines_changed,
        "smoke_test": smoke,
    }

    if smoke and not smoke.get("passed"):
        result["ok"] = False
        result["message"] = (
            f"Edit applied but FAILED smoke test -- auto-rolled back. "
            f"Errors: {smoke.get('errors', [])}"
        )
        result["rolled_back"] = True

    return result


def code_insert(**kwargs) -> Dict[str, Any]:
    """
    Insert new code after a marker string. Useful for adding features.
    The marker must be unique in the file.
    """
    _require_user()

    file_path = kwargs.get("file_path", "").strip()
    after_text = kwargs.get("after_text", "")
    new_text = kwargs.get("new_text", "")

    if not file_path:
        return {"ok": False, "error": "Provide 'file_path'."}
    if not after_text:
        return {"ok": False, "error": "Provide 'after_text' -- the marker after which to insert code."}
    if not new_text:
        return {"ok": False, "error": "Provide 'new_text' -- the code to insert."}

    resolved = _resolve_file(file_path)
    if not resolved:
        return {"ok": False, "error": f"File not found: {file_path}"}

    try:
        content = resolved.read_text(encoding="utf-8")
    except Exception as e:
        return {"ok": False, "error": f"Cannot read file: {e}"}

    count = content.count(after_text)
    if count == 0:
        return {"ok": False, "error": f"Marker text not found in {resolved.name}."}
    if count > 1:
        return {"ok": False, "error": f"Marker found {count} times -- needs to be unique."}

    backup_path = _backup_file(resolved)

    # Insert after the marker
    new_content = content.replace(after_text, after_text + new_text, 1)
    resolved.write_text(new_content, encoding="utf-8")

    # Smoke test -- auto-rollback on failure
    smoke = _smoke_test_and_rollback(resolved, backup_path)

    _edit_history.append({
        "ts": time.time(),
        "action": "code_insert",
        "file": str(resolved),
        "backup": backup_path,
        "inserted_len": len(new_text),
        "smoke_test": smoke,
    })
    if len(_edit_history) > _MAX_HISTORY:
        _edit_history.pop(0)

    _log_edit_to_learning("code_insert", str(resolved), smoke)

    result = {
        "ok": True,
        "message": f"Inserted {len(new_text)} chars into {resolved.name}",
        "file": str(resolved),
        "backup": backup_path,
        "lines_added": new_text.count("\n"),
        "smoke_test": smoke,
    }

    if smoke and not smoke.get("passed"):
        result["ok"] = False
        result["message"] = (
            f"Insert applied but FAILED smoke test -- auto-rolled back. "
            f"Errors: {smoke.get('errors', [])}"
        )
        result["rolled_back"] = True

    return result


def code_read_section(**kwargs) -> Dict[str, Any]:
    """
    Read a specific section of a file by line range or search pattern.
    Much better than reading the full 3000-line file.
    """
    _require_user()

    file_path = kwargs.get("file_path", "").strip()
    start_line = kwargs.get("start_line")
    end_line = kwargs.get("end_line")
    search = kwargs.get("search", "").strip()
    context_lines = kwargs.get("context_lines", 10)

    if not file_path:
        return {"ok": False, "error": "Provide 'file_path'."}

    resolved = _resolve_file(file_path)
    if not resolved:
        return {"ok": False, "error": f"File not found: {file_path}"}

    try:
        content = resolved.read_text(encoding="utf-8")
        lines = content.splitlines()
    except Exception as e:
        return {"ok": False, "error": f"Cannot read file: {e}"}

    total_lines = len(lines)

    if search:
        # Find lines matching the search pattern
        matches = []
        for i, line in enumerate(lines):
            if search.lower() in line.lower():
                start = max(0, i - context_lines)
                end = min(total_lines, i + context_lines + 1)
                section = []
                for j in range(start, end):
                    prefix = ">>>" if j == i else "   "
                    section.append(f"{prefix} {j+1:4d} | {lines[j]}")
                matches.append({
                    "line": i + 1,
                    "content": lines[i].strip(),
                    "section": "\n".join(section)
                })
                if len(matches) >= 5:
                    break

        return {
            "ok": True,
            "file": str(resolved),
            "total_lines": total_lines,
            "matches": matches,
            "match_count": len(matches)
        }

    elif start_line is not None:
        # Read by line range
        start = max(1, int(start_line)) - 1
        end = min(total_lines, int(end_line or start + 50))
        section = []
        for i in range(start, end):
            section.append(f"{i+1:4d} | {lines[i]}")

        return {
            "ok": True,
            "file": str(resolved),
            "total_lines": total_lines,
            "start_line": start + 1,
            "end_line": end,
            "content": "\n".join(section)
        }

    else:
        # Return file overview: first 20 lines + stats
        preview = []
        for i in range(min(20, total_lines)):
            preview.append(f"{i+1:4d} | {lines[i]}")

        return {
            "ok": True,
            "file": str(resolved),
            "total_lines": total_lines,
            "size_bytes": resolved.stat().st_size,
            "preview": "\n".join(preview)
        }


def code_search(**kwargs) -> Dict[str, Any]:
    """
    Search for a pattern across all Joi source files.
    Returns file paths and line numbers where matches are found.
    """
    _require_user()

    pattern = kwargs.get("pattern", "").strip()
    if not pattern:
        return {"ok": False, "error": "Provide a 'pattern' to search for."}

    file_filter = kwargs.get("file_filter", "")  # e.g., "*.py", "*.html"
    max_results = kwargs.get("max_results", 20)

    search_dirs = [BASE_DIR, MODULES_DIR]
    globs = ["*.py", "*.html", "*.js", "*.json", "*.css"]
    if file_filter:
        globs = [file_filter]

    results = []
    pattern_lower = pattern.lower()

    for search_dir in search_dirs:
        for glob_pattern in globs:
            for fpath in search_dir.glob(glob_pattern):
                if not fpath.is_file():
                    continue
                # Skip huge files and backup dir
                if "code_backups" in str(fpath) or fpath.stat().st_size > 500_000:
                    continue
                try:
                    content = fpath.read_text(encoding="utf-8", errors="ignore")
                    for i, line in enumerate(content.splitlines()):
                        if pattern_lower in line.lower():
                            results.append({
                                "file": str(fpath),
                                "line": i + 1,
                                "content": line.strip()[:200]
                            })
                            if len(results) >= max_results:
                                break
                except Exception:
                    pass
                if len(results) >= max_results:
                    break

    return {
        "ok": True,
        "pattern": pattern,
        "results": results,
        "count": len(results)
    }


def code_backup(**kwargs) -> Dict[str, Any]:
    """Manually create a backup of a file before making changes."""
    _require_user()

    file_path = kwargs.get("file_path", "").strip()
    if not file_path:
        return {"ok": False, "error": "Provide 'file_path' to backup."}

    resolved = _resolve_file(file_path)
    if not resolved:
        return {"ok": False, "error": f"File not found: {file_path}"}

    backup_path = _backup_file(resolved)
    return {
        "ok": True,
        "message": f"Backed up {resolved.name}",
        "file": str(resolved),
        "backup": backup_path
    }


def code_rollback(**kwargs) -> Dict[str, Any]:
    """Restore a file from its most recent backup."""
    _require_user()

    file_path = kwargs.get("file_path", "").strip()
    if not file_path:
        return {"ok": False, "error": "Provide 'file_path' to rollback."}

    resolved = _resolve_file(file_path)
    if not resolved:
        # Try to find from backup name
        return {"ok": False, "error": f"File not found: {file_path}"}

    backups = _get_backups(resolved.name)
    if not backups:
        return {"ok": False, "error": f"No backups found for {resolved.name}"}

    latest = backups[0]  # Most recent
    backup_path = Path(latest["path"])

    try:
        shutil.copy2(str(backup_path), str(resolved))
        return {
            "ok": True,
            "message": f"Restored {resolved.name} from backup {backup_path.name}",
            "file": str(resolved),
            "backup_used": str(backup_path),
            "backup_created": latest["created"]
        }
    except Exception as e:
        return {"ok": False, "error": f"Rollback failed: {e}"}


def code_list_backups(**kwargs) -> Dict[str, Any]:
    """List all available backups, optionally filtered by filename."""
    _require_user()

    file_path = kwargs.get("file_path", "").strip()

    if file_path:
        resolved = _resolve_file(file_path)
        name = resolved.name if resolved else Path(file_path).name
        backups = _get_backups(name)
    else:
        # List all backups
        backups = []
        for f in sorted(BACKUP_DIR.glob("*.bak"), reverse=True):
            try:
                stat = f.stat()
                backups.append({
                    "path": str(f),
                    "name": f.name,
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            except Exception:
                pass

    return {
        "ok": True,
        "backups": backups[:20],
        "total": len(backups)
    }


def creative_edit(**kwargs) -> Dict[str, Any]:
    """
    Add a new feature or make a creative change to Joi's code.

    Unlike code_self_repair (which fixes bugs), this CREATES new things:
    - "Add a dark mode toggle to the settings"
    - "Create a new sidebar section for OBS controls"
    - "Add a button that shows security camera feed"

    Uses multi-model routing (Claude Sonnet preferred) to generate the code,
    then applies it surgically with auto-backup.
    """
    _require_user()

    description = kwargs.get("description", "").strip()
    target_file = kwargs.get("target_file", "").strip()

    if not description:
        return {"ok": False, "error": "Provide a 'description' of what to create or change."}

    result: Dict[str, Any] = {
        "ok": True,
        "description": description,
        "actions_taken": [],
        "edit_applied": False,
        "model_used": None
    }

    # Determine target file
    if not target_file:
        # Guess from description
        desc_lower = description.lower()
        if any(w in desc_lower for w in ["ui", "button", "toggle", "sidebar", "modal", "html", "css", "layout"]):
            target_file = "joi_ui.html"
        elif any(w in desc_lower for w in ["avatar", "tts", "voice"]):
            target_file = "joi_media.py"
        elif any(w in desc_lower for w in ["camera", "face"]):
            target_file = "joi_media.py"
        else:
            target_file = "joi_ui.html"  # Default to UI

    resolved = _resolve_file(target_file)
    if not resolved:
        return {"ok": False, "error": f"Target file not found: {target_file}"}

    # Read the file
    try:
        content = resolved.read_text(encoding="utf-8")
        result["actions_taken"].append(f"Read {resolved.name} ({len(content.splitlines())} lines)")
    except Exception as e:
        return {"ok": False, "error": f"Cannot read {target_file}: {e}"}

    # For large files, send a structured overview instead of the full content
    if len(content) > 15000:
        lines = content.splitlines()
        # Build a structural overview
        overview_parts = []
        overview_parts.append(f"File: {resolved.name} ({len(lines)} lines, {len(content)} chars)")
        overview_parts.append(f"\nFirst 30 lines:\n")
        for i in range(min(30, len(lines))):
            overview_parts.append(f"{i+1:4d} | {lines[i]}")
        overview_parts.append(f"\nLast 30 lines:\n")
        for i in range(max(0, len(lines)-30), len(lines)):
            overview_parts.append(f"{i+1:4d} | {lines[i]}")

        # For HTML, also find key section markers
        if resolved.suffix == ".html":
            for i, line in enumerate(lines):
                if any(marker in line.lower() for marker in ["<script", "</script", "modal", "settings", "function ", "// ===="]):
                    overview_parts.append(f"  [{i+1}] {line.strip()[:100]}")

        file_context = "\n".join(overview_parts)
    else:
        file_context = content

    # Ask LLM to generate the edit
    system_prompt = (
        "You are a senior full-stack developer editing a web application. "
        "Given a feature request and the current source code, generate a SURGICAL edit. "
        "You MUST respond in this exact JSON format:\n"
        "{\n"
        '  "plan": "Brief description of what you will add/change",\n'
        '  "edits": [\n'
        '    {\n'
        '      "type": "replace",\n'
        '      "old_text": "exact text to find in the file (must be unique)",\n'
        '      "new_text": "the replacement text (includes the change)"\n'
        '    }\n'
        '  ],\n'
        '  "confidence": 0-100\n'
        "}\n\n"
        "RULES:\n"
        "- old_text MUST be an exact substring of the file (copy-paste precision)\n"
        "- old_text MUST be unique in the file (include enough context)\n"
        "- Keep edits minimal -- don't rewrite unrelated code\n"
        "- For insertions, use a nearby unique line as old_text and include it in new_text with the addition\n"
        "- For HTML files, maintain consistent indentation\n"
        "- For Python files, maintain consistent indentation and module patterns\n"
        "- Multiple edits are allowed if the feature needs changes in several places"
    )

    user_prompt = (
        f"Feature request: {description}\n\n"
        f"Target file: {resolved.name}\n\n"
        f"Current code:\n{file_context}"
    )

    response = _call_code_model(system_prompt, user_prompt, max_tokens=3000)
    if not response:
        result["actions_taken"].append("All LLM providers failed")
        return result

    result["actions_taken"].append("LLM generated edit plan")

    # Parse response
    try:
        json_match = re.search(r'\{[\s\S]*\}', response)
        if not json_match:
            result["actions_taken"].append("Could not parse JSON from LLM response")
            result["raw_response"] = response[:500]
            return result

        parsed = json.loads(json_match.group())
        plan = parsed.get("plan", "")
        edits = parsed.get("edits", [])
        confidence = parsed.get("confidence", 0)

        result["plan"] = plan
        result["confidence"] = confidence
        result["edit_count"] = len(edits)
        result["actions_taken"].append(f"Plan: {plan}")

        if confidence < 70:
            result["actions_taken"].append(
                f"Confidence {confidence}% too low -- showing plan but not applying. "
                f"Review and use code_edit to apply manually."
            )
            result["edits_preview"] = [
                {"old": e.get("old_text", "")[:200], "new": e.get("new_text", "")[:200]}
                for e in edits[:3]
            ]
            return result

        # Auto-backup before applying
        backup_path = _backup_file(resolved)
        result["backup"] = backup_path
        result["actions_taken"].append(f"Backup created: {backup_path}")

        # Apply edits sequentially
        current_content = content
        applied = 0
        failed = 0
        for i, edit in enumerate(edits):
            edit_type = edit.get("type", "replace")
            old_text = edit.get("old_text", "")
            new_text = edit.get("new_text", "")

            if not old_text:
                result["actions_taken"].append(f"Edit {i+1}: skipped (no old_text)")
                failed += 1
                continue

            if old_text not in current_content:
                result["actions_taken"].append(f"Edit {i+1}: old_text not found in file")
                failed += 1
                continue

            if current_content.count(old_text) > 1:
                result["actions_taken"].append(f"Edit {i+1}: old_text not unique ({current_content.count(old_text)} matches)")
                failed += 1
                continue

            current_content = current_content.replace(old_text, new_text, 1)
            applied += 1
            result["actions_taken"].append(f"Edit {i+1}: applied ({len(old_text)}->{len(new_text)} chars)")

        # Write if any edits were applied
        if applied > 0:
            resolved.write_text(current_content, encoding="utf-8")

            # Smoke test the creative edit
            smoke = _smoke_test_and_rollback(resolved, backup_path)
            result["smoke_test"] = smoke

            if smoke and not smoke.get("passed"):
                result["edit_applied"] = False
                result["edits_applied"] = 0
                result["edits_failed"] = applied
                result["actions_taken"].append(
                    f"SMOKE TEST FAILED -- auto-rolled back. Errors: {smoke.get('errors', [])}"
                )
                _log_edit_to_learning("creative_edit", str(resolved), smoke)
            else:
                result["edit_applied"] = True
                result["edits_applied"] = applied
                result["edits_failed"] = failed
                result["actions_taken"].append(f"Saved {resolved.name}: {applied} edit(s) applied, {failed} failed")
                if smoke:
                    result["actions_taken"].append("Smoke test passed")
                _log_edit_to_learning("creative_edit", str(resolved), smoke)
        else:
            result["actions_taken"].append("No edits could be applied -- all old_text matches failed")
            result["edits_failed"] = failed

    except json.JSONDecodeError as e:
        result["actions_taken"].append(f"JSON parse error: {e}")
        result["raw_response"] = response[:500]
    except Exception as e:
        result["actions_taken"].append(f"Edit application error: {e}")

    return result


# ============================================================================
# TOOL REGISTRATION
# ============================================================================

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "code_edit",
        "description": (
            "Surgically edit a file by exact string replacement. Finds old_text and replaces with new_text. "
            "Auto-creates a backup before editing. The old_text must be unique in the file. "
            "Use this for precise code fixes -- like Claude Code's Edit tool. "
            "Example: code_edit(file_path='joi_ui.html', old_text='color: red', new_text='color: blue')"
        ),
        "parameters": {"type": "object", "properties": {
            "file_path": {"type": "string", "description": "File to edit (e.g., 'joi_ui.html', 'modules/joi_camera.py')"},
            "old_text": {"type": "string", "description": "Exact text to find (must be unique in file)"},
            "new_text": {"type": "string", "description": "Replacement text"}
        }, "required": ["file_path", "old_text", "new_text"]}
    }},
    code_edit
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "code_insert",
        "description": (
            "Insert new code after a specific marker in a file. The marker must be unique. "
            "Use for adding new features: functions, HTML elements, CSS rules, routes. "
            "Example: code_insert(file_path='joi_ui.html', after_text='</div><!-- settings-end -->', new_text='<div>new section</div>')"
        ),
        "parameters": {"type": "object", "properties": {
            "file_path": {"type": "string", "description": "File to insert into"},
            "after_text": {"type": "string", "description": "Marker text after which to insert (must be unique)"},
            "new_text": {"type": "string", "description": "Code to insert"}
        }, "required": ["file_path", "after_text", "new_text"]}
    }},
    code_insert
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "code_read_section",
        "description": (
            "Read a specific section of a file by line range or search pattern. "
            "Much better than reading a full 3000-line file. "
            "Use search to find relevant code, or start_line/end_line for a known range."
        ),
        "parameters": {"type": "object", "properties": {
            "file_path": {"type": "string", "description": "File to read"},
            "start_line": {"type": "integer", "description": "Starting line number"},
            "end_line": {"type": "integer", "description": "Ending line number"},
            "search": {"type": "string", "description": "Text to search for (returns matching lines with context)"},
            "context_lines": {"type": "integer", "description": "Lines of context around search matches (default 10)"}
        }, "required": ["file_path"]}
    }},
    code_read_section
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "code_search",
        "description": (
            "Search for a pattern across all Joi source files (Python, HTML, JS, JSON, CSS). "
            "Returns file paths and line numbers. Use to find where something is defined or used."
        ),
        "parameters": {"type": "object", "properties": {
            "pattern": {"type": "string", "description": "Text or pattern to search for"},
            "file_filter": {"type": "string", "description": "Optional file glob filter (e.g., '*.py', '*.html')"},
            "max_results": {"type": "integer", "description": "Max results (default 20)"}
        }, "required": ["pattern"]}
    }},
    code_search
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "code_rollback",
        "description": (
            "Undo the last edit by restoring a file from its backup. "
            "Use when an edit breaks something. Every code_edit and code_insert creates an auto-backup."
        ),
        "parameters": {"type": "object", "properties": {
            "file_path": {"type": "string", "description": "File to rollback to its last backup"}
        }, "required": ["file_path"]}
    }},
    code_rollback
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "code_list_backups",
        "description": "List available code backups, optionally filtered by filename.",
        "parameters": {"type": "object", "properties": {
            "file_path": {"type": "string", "description": "Optional: only show backups for this file"}
        }}
    }},
    code_list_backups
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "creative_edit",
        "description": (
            "Add a new feature or make a creative change to Joi's code. "
            "Unlike code_self_repair (bug fixes), this CREATES new things: "
            "toggles, buttons, sidebar sections, modals, new functionality. "
            "Uses the best available AI model (Claude Sonnet > Gemini > GPT-4o) "
            "to generate surgical edits with auto-backup. "
            "Example: creative_edit(description='Add a dark mode toggle to settings')"
        ),
        "parameters": {"type": "object", "properties": {
            "description": {"type": "string", "description": "What to create or change (be specific)"},
            "target_file": {"type": "string", "description": "Optional: specific file to edit (auto-detected if omitted)"}
        }, "required": ["description"]}
    }},
    creative_edit
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "code_backup",
        "description": "Manually create a backup of a file before making manual changes.",
        "parameters": {"type": "object", "properties": {
            "file_path": {"type": "string", "description": "File to backup"}
        }, "required": ["file_path"]}
    }},
    code_backup
)

# Human-in-the-loop: show diff before applying. User replies with OK or correction (DPO).
def _render_diff_tool(**kwargs):
    import joi_companion
    return getattr(joi_companion, "render_diff", lambda *_: "(render_diff not available)")(
        kwargs.get("file_path", ""),
        kwargs.get("old_text", ""),
        kwargs.get("new_text", ""),
        kwargs.get("context_lines", 3),
    )

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "render_diff",
        "description": (
            "Format a unified diff for display BEFORE applying code changes. "
            "Call this to show the user the diff; then wait for them to say 'yes' to apply or give a correction. "
            "If they say 'No, do X instead', the correction handler runs."
        ),
        "parameters": {"type": "object", "properties": {
            "file_path": {"type": "string", "description": "File being changed"},
            "old_text": {"type": "string", "description": "Current text"},
            "new_text": {"type": "string", "description": "Proposed new text"},
            "context_lines": {"type": "integer", "description": "Lines of context in diff (default 3)"}
        }, "required": ["file_path", "old_text", "new_text"]}
    }},
    _render_diff_tool
)


# ============================================================================
# FLASK ROUTE
# ============================================================================

def _code_edit_route():
    """REST endpoint for code editing operations."""
    _require_user()

    if flask_req.method == "GET":
        return jsonify(code_list_backups())

    data = flask_req.get_json(silent=True) or {}
    action = data.get("action", "")

    actions = {
        "edit": code_edit,
        "insert": code_insert,
        "read": code_read_section,
        "search": code_search,
        "backup": code_backup,
        "rollback": code_rollback,
        "backups": code_list_backups,
        "creative": creative_edit,
    }

    handler = actions.get(action)
    if not handler:
        return jsonify({"ok": False, "error": f"Unknown action: {action}. Valid: {list(actions.keys())}"})

    return jsonify(handler(**data))


joi_companion.register_route("/code-edit", ["GET", "POST"], _code_edit_route, "code_edit_route")

print("  [joi_code_edit] Surgical editing tools registered: code_edit, code_insert, code_read_section, code_search, code_backup, code_rollback, code_list_backups, creative_edit")
print(f"  [joi_code_edit] Backups dir: {BACKUP_DIR}")
