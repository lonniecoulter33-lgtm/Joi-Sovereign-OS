"""
modules/joi_watchdog_feedback.py

Watchdog-Agent Feedback Channel.
=================================
Layer 4 — Auto-apply OK.

Records watchdog intervention events (rollbacks, circuit breakers) and
surfaces them to the coder agent on the next attempt — so the LLM knows
WHY a file was reverted and can make a smarter edit.

No Joi imports — standalone module that reads/writes data/watchdog_feedback.json.

Key functions:
  record_intervention(action, reason, affected_files, error_details, suggestion)
      → writes unacknowledged entry to watchdog_feedback.json

  get_feedback_for_files(file_paths) → List[dict]
      → returns all unacknowledged interventions for the given files

  get_retry_count_for_file(file_path) → int
      → total unacknowledged intervention count for the file (escalate at ≥ 3)

  format_feedback_for_prompt(feedback_list) → str
      → formats list as LLM-ready warning block

  acknowledge_feedback(file_paths)
      → marks entries acknowledged after a successful edit
"""

import json
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── Path ──────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
FEEDBACK_PATH = DATA_DIR / "watchdog_feedback.json"

_lock = threading.Lock()


# ── File I/O ──────────────────────────────────────────────────────────────────

def _load() -> List[Dict[str, Any]]:
    """Load all feedback entries from disk. Returns [] on any error."""
    try:
        if FEEDBACK_PATH.exists():
            with open(FEEDBACK_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def _save(entries: List[Dict[str, Any]]) -> None:
    """Persist feedback entries to disk. Keep last 500 entries to bound size."""
    try:
        with open(FEEDBACK_PATH, "w", encoding="utf-8") as f:
            json.dump(entries[-500:], f, indent=2, default=str)
    except Exception:
        pass


# ── Public API ────────────────────────────────────────────────────────────────

def record_intervention(
    action: str,
    reason: str,
    affected_files: List[str],
    error_details: str,
    suggestion: str,
) -> None:
    """
    Record a watchdog intervention event.

    Args:
        action:         What watchdog did ("rollback", "circuit_breaker", etc.)
        reason:         Why ("sanity_failed", "incremental_restore_failed", etc.)
        affected_files: List of file paths that were reverted
        error_details:  Raw error text (truncated to 500 chars)
        suggestion:     Human-readable hint for the coder agent
    """
    entry = {
        "timestamp":      time.time(),
        "action":         action,
        "reason":         reason,
        "affected_files": [str(p) for p in affected_files],
        "error_details":  str(error_details)[:500],
        "suggestion":     suggestion,
        "acknowledged":   False,
    }
    with _lock:
        entries = _load()
        entries.append(entry)
        _save(entries)

    # Emit to event bus (best-effort — don't let bus errors break watchdog)
    try:
        from modules.joi_task_events import get_event_bus, TaskEvent, TaskStatus
        bus = get_event_bus()
        bus.emit(TaskEvent(
            task_id=f"watchdog:{action}:{reason}",
            status=TaskStatus.FAILED,
            data={
                "action":         action,
                "reason":         reason,
                "affected_files": affected_files,
                "suggestion":     suggestion,
            },
        ))
    except Exception:
        pass


def get_feedback_for_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Return all unacknowledged interventions that affected any of the given files.
    Also returns entries with no affected_files (global interventions).
    """
    norm_paths = {str(Path(p).resolve()) for p in file_paths if p}
    norm_paths.update({str(p) for p in file_paths if p})  # also match as-given

    with _lock:
        entries = _load()

    result = []
    for entry in entries:
        if entry.get("acknowledged"):
            continue
        entry_files = entry.get("affected_files", [])
        if not entry_files:
            # Global intervention (circuit breaker with no specific files)
            result.append(entry)
            continue
        # Check if any affected file matches any requested file
        for ef in entry_files:
            ef_norm = str(Path(ef).resolve()) if Path(ef).exists() else ef
            if ef_norm in norm_paths or ef in norm_paths:
                result.append(entry)
                break

    return result


def get_retry_count_for_file(file_path: str) -> int:
    """
    Count unacknowledged interventions for a specific file.
    Escalate to human review when this reaches 3+.
    """
    return len(get_feedback_for_files([file_path]))


def format_feedback_for_prompt(feedback_list: List[Dict[str, Any]]) -> str:
    """
    Format a list of feedback entries as a block for injection into the coder prompt.
    Returns empty string if no feedback.
    """
    if not feedback_list:
        return ""

    lines = [
        "[WATCHDOG ALERT] This file has been automatically reverted by the safety watchdog.",
        "The following previous attempts failed and were rolled back:",
        "",
    ]
    for i, fb in enumerate(feedback_list, 1):
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fb.get("timestamp", 0)))
        lines.append(f"  [{i}] {ts} — Action: {fb.get('action')} | Reason: {fb.get('reason')}")
        if fb.get("error_details"):
            lines.append(f"       Error: {fb['error_details']}")
        if fb.get("suggestion"):
            lines.append(f"       Suggestion: {fb['suggestion']}")
        lines.append("")

    lines.append(
        "FIX REQUIRED: Address the issues above before making new changes. "
        "Break your edit into smaller, targeted steps."
    )
    return "\n".join(lines)


def acknowledge_feedback(file_paths: List[str]) -> int:
    """
    Mark all feedback entries for the given files as acknowledged.
    Called after a successful edit so old warnings don't accumulate.
    Returns count of entries acknowledged.
    """
    norm_paths = {str(Path(p).resolve()) for p in file_paths if p}
    norm_paths.update({str(p) for p in file_paths if p})

    with _lock:
        entries = _load()
        count = 0
        for entry in entries:
            if entry.get("acknowledged"):
                continue
            entry_files = entry.get("affected_files", [])
            for ef in entry_files:
                ef_norm = str(Path(ef).resolve()) if Path(ef).exists() else ef
                if ef_norm in norm_paths or ef in norm_paths:
                    entry["acknowledged"] = True
                    count += 1
                    break
        _save(entries)

    return count
