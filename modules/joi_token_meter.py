"""
modules/joi_token_meter.py

Soft Per-Task Token Budget Enforcement.
========================================
Layer 4 — Auto-apply OK.

Tracks estimated prompt tokens per task. At 80%: warning broadcast.
At 100%: pauses and saves progress — does NOT fail permanently.
Budget is per-task, not global. Estimates from prompt length (tiktoken optional).

No circular imports — does not import Joi modules at module level.

Key classes/functions:
  TaskBudget(task_id, task_type) — per-task budget tracker
  estimate_tokens(text)          — tiktoken if available, else len//4
  charge(task_id, prompt_text, response_text)
      → {ok, warning, paused, percent_used, tokens_used, budget}
  save_progress(task_id, completed_subtasks) — saves progress snapshot
  resume_with_more_budget(task_id, extra_budget) — extends budget
  get_task_budget(task_id)       — usage stats dict
  reset_task(task_id)            — clear on normal completion
"""

import json
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


# ── Budget Tiers by Task Type ─────────────────────────────────────────────────

BUDGETS_BY_TYPE: Dict[str, int] = {
    "simple_edit":   30_000,
    "new_file":      50_000,
    "multi_file":   100_000,
    "research":      75_000,
    "conversation": 200_000,
    "default":       50_000,
}

WARNING_THRESHOLD = 0.80   # broadcast warning at 80%
PAUSE_THRESHOLD   = 1.00   # pause (not fail) at 100%

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
PROGRESS_PATH = DATA_DIR / "token_meter_progress.json"

# ── Global Registry ───────────────────────────────────────────────────────────
_registry: Dict[str, Dict[str, Any]] = {}
_lock = threading.Lock()


# ── Token Estimation ──────────────────────────────────────────────────────────

def estimate_tokens(text: str) -> int:
    """
    Estimate token count for a text string.
    Uses tiktoken (cl100k_base) if available, otherwise falls back to len // 4.
    """
    if not text:
        return 0
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        # Fast fallback: ~4 chars/token average
        return max(1, len(text) // 4)


# ── TaskBudget Class ──────────────────────────────────────────────────────────

class TaskBudget:
    """
    Per-task token budget tracker.

    Usage:
        budget = TaskBudget("task-42", "new_file")
        result = budget.charge("task-42", prompt_text, response_text)
        if result["warning"]: broadcast_warning(...)
        if result["paused"]:  pause_and_save(...)
    """

    def __init__(self, task_id: str, task_type: str = "default"):
        self.task_id    = task_id
        self.task_type  = task_type
        self.budget     = BUDGETS_BY_TYPE.get(task_type, BUDGETS_BY_TYPE["default"])

        with _lock:
            if task_id not in _registry:
                _registry[task_id] = {
                    "task_id":     task_id,
                    "task_type":   task_type,
                    "budget":      self.budget,
                    "tokens_used": 0,
                    "warnings":    0,
                    "paused":      False,
                    "created_at":  time.time(),
                    "updated_at":  time.time(),
                }

    def charge(
        self,
        task_id: str,
        prompt_text: str,
        response_text: str,
    ) -> Dict[str, Any]:
        """
        Charge tokens for a prompt+response pair.

        Returns:
            {
              "ok":          bool   — True unless already paused
              "warning":     bool   — True if crossed 80% threshold this call
              "paused":      bool   — True if budget exhausted (caller should break loop)
              "percent_used": float — current usage %
              "tokens_used": int   — cumulative tokens
              "budget":      int   — total budget for this task
            }
        """
        tokens = estimate_tokens(prompt_text) + estimate_tokens(response_text)

        with _lock:
            entry = _registry.get(task_id)
            if entry is None:
                # Auto-create entry if task_id was registered externally
                entry = {
                    "task_id":     task_id,
                    "task_type":   self.task_type,
                    "budget":      self.budget,
                    "tokens_used": 0,
                    "warnings":    0,
                    "paused":      False,
                    "created_at":  time.time(),
                    "updated_at":  time.time(),
                }
                _registry[task_id] = entry

            if entry.get("paused"):
                return {
                    "ok":          False,
                    "warning":     False,
                    "paused":      True,
                    "percent_used": 1.0,
                    "tokens_used": entry["tokens_used"],
                    "budget":      entry["budget"],
                }

            entry["tokens_used"] += tokens
            entry["updated_at"] = time.time()

            budget       = entry["budget"]
            tokens_used  = entry["tokens_used"]
            percent      = tokens_used / budget if budget > 0 else 0.0

            warning = False
            paused  = False

            if percent >= PAUSE_THRESHOLD:
                entry["paused"] = True
                paused = True
            elif percent >= WARNING_THRESHOLD and entry["warnings"] == 0:
                entry["warnings"] += 1
                warning = True

        return {
            "ok":          not paused,
            "warning":     warning,
            "paused":      paused,
            "percent_used": percent,
            "tokens_used": tokens_used,
            "budget":      budget,
        }

    def is_paused(self) -> bool:
        with _lock:
            return _registry.get(self.task_id, {}).get("paused", False)


# ── Progress Saving ───────────────────────────────────────────────────────────

def save_progress(task_id: str, completed_subtasks: List[Dict[str, Any]]) -> None:
    """
    Save what was accomplished so far when a budget pause occurs.
    Stored in data/token_meter_progress.json for potential resume.
    """
    try:
        existing: Dict[str, Any] = {}
        if PROGRESS_PATH.exists():
            with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing[task_id] = {
            "task_id":            task_id,
            "saved_at":           time.time(),
            "completed_subtasks": completed_subtasks,
        }
        with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, default=str)
    except Exception:
        pass


def resume_with_more_budget(task_id: str, extra_budget: int = 50_000) -> Dict[str, Any]:
    """
    Extend the budget for a paused task so it can continue.
    Returns updated budget stats.
    """
    with _lock:
        entry = _registry.get(task_id)
        if entry is None:
            return {"ok": False, "error": f"Task {task_id} not found in meter registry"}
        entry["budget"]  += extra_budget
        entry["paused"]   = False
        entry["warnings"] = 0  # reset warning flag
        entry["updated_at"] = time.time()
        return {
            "ok":          True,
            "task_id":     task_id,
            "new_budget":  entry["budget"],
            "tokens_used": entry["tokens_used"],
            "percent_used": entry["tokens_used"] / entry["budget"],
        }


def get_task_budget(task_id: str) -> Dict[str, Any]:
    """Return current budget stats for a task."""
    with _lock:
        entry = _registry.get(task_id, {})
        if not entry:
            return {"ok": False, "error": f"Task {task_id} not in meter registry"}
        budget = entry.get("budget", 1)
        used   = entry.get("tokens_used", 0)
        return {
            "ok":          True,
            "task_id":     task_id,
            "task_type":   entry.get("task_type", "default"),
            "budget":      budget,
            "tokens_used": used,
            "percent_used": used / budget if budget else 0.0,
            "paused":      entry.get("paused", False),
            "warnings":    entry.get("warnings", 0),
        }


def reset_task(task_id: str) -> None:
    """Clear budget entry when a task completes normally."""
    with _lock:
        _registry.pop(task_id, None)
