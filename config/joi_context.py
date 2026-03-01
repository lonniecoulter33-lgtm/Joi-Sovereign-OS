"""
config/joi_context.py

Centralized Context Management Configuration
=============================================
All context window, trimming, summarization, and memory knobs in one place.
Toggle MAX_CONTEXT_TOKENS or SUMMARIZE_THRESHOLD_TOKENS here to control
Joi's memory behavior without touching module code.

Usage:
    from config.joi_context import MAX_CONTEXT_TOKENS, SUMMARIZE_THRESHOLD_TOKENS
"""

import os

# ── Token / Char Limits ─────────────────────────────────────────────────────
MAX_CONTEXT_TOKENS = int(os.getenv("JOI_MAX_CONTEXT_TOKENS", "32000"))
MAX_OUTPUT_TOKENS = int(os.getenv("JOI_MAX_OUTPUT_TOKENS", "8000"))
MAX_TOTAL_PROMPT_CHARS = int(os.getenv("JOI_MAX_TOTAL_PROMPT_CHARS", "128000"))

# ── Per-Message Caps ────────────────────────────────────────────────────────
MAX_MSG_CHARS = int(os.getenv("JOI_MAX_MSG_CHARS", "6000"))
MAX_SYSTEM_PROMPT_CHARS = int(os.getenv("JOI_MAX_SYSTEM_PROMPT_CHARS", "20000"))

# ── Surgical Trimming Priorities ────────────────────────────────────────────
# Lower number = higher priority (never deleted first)
PRIORITY_SYSTEM_PROMPT = 0       # NEVER delete
PRIORITY_PROJECT_MAP = 1         # NEVER delete
PRIORITY_CURRENT_SUBTASK = 2     # Keep for orchestrator context
PRIORITY_LAST_ERRORS = 3         # Keep last N error messages
PRIORITY_RECENT_USER = 4         # Keep last few user messages
PRIORITY_RECENT_ASSISTANT = 5    # Keep recent assistant replies
PRIORITY_TOOL_RESULTS = 6        # Tool call results
PRIORITY_MIDDLE_HISTORY = 10     # Summarize then discard

# Error log retention
KEEP_LAST_N_ERRORS = 3

# ── Summarization ───────────────────────────────────────────────────────────
# When estimated tokens exceed this threshold, summarize middle history
SUMMARIZE_THRESHOLD_TOKENS = int(os.getenv("JOI_SUMMARIZE_THRESHOLD", "30000"))
SUMMARY_MAX_TOKENS = 500         # Max tokens for the Memory Note
SUMMARY_MODEL = os.getenv("JOI_SUMMARY_MODEL", "o4-mini")

# ── File-Check Guard ────────────────────────────────────────────────────────
ENABLE_FILE_CHECK_GUARD = os.getenv("JOI_ENABLE_FILE_CHECK", "1").strip() not in ("0", "false", "no")

# ── Print on import ─────────────────────────────────────────────────────────
print(f"  [OK] joi_context config: MAX_CONTEXT_TOKENS={MAX_CONTEXT_TOKENS}, "
      f"SUMMARIZE_THRESHOLD={SUMMARIZE_THRESHOLD_TOKENS}, "
      f"SUMMARY_MODEL={SUMMARY_MODEL}, "
      f"FILE_CHECK_GUARD={'ON' if ENABLE_FILE_CHECK_GUARD else 'OFF'}")
