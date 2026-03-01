# Agent Terminal Diagnostic Report

**Date:** 2026-02-15  
**Scope:** Joi's Agent Terminal (orchestrator pipeline) — can it write code, debug, and create new apps?

---

## Executive summary

| Capability            | Status | Notes |
|-----------------------|--------|--------|
| **Write code**        | ✅ Yes | Architect → Coder → surgical edits (old_text/new_text) → Validator → Apply via `code_edit` |
| **Debug**             | ✅ Yes | Validation runs test_command (e.g. ast.parse, pytest); error_feedback loop for Coder retries (up to 3) |
| **Create new apps**   | ⚠️ Partial | Only **edits to existing files**. New-file creation is **not** supported in the pipeline today |

**Verdict:** Agent Terminal can write and edit code and debug via validation/retries. It cannot create brand-new files/apps from scratch without a small enhancement (see below).

---

## 1. Diagnostic script results

Run: `python scripts/check_agent_terminal.py`

- **Module imports:** Failed under Python 3.14 (chromadb type inference). Use Python 3.11/3.12 for full live test. Static checks still ran.
- **Orchestrator tools:** All 5 present in source (orchestrate_task, approve_subtask, reject_subtask, get_orchestrator_status, cancel_orchestration).
- **Tool selector:** Orchestrator group priority 1, orchestrate_task included.
- **Router:** Orchestration classification present in source.
- **Brain:** No hardcoded `gemini-2-flash`; safe fallback chain in place.
- **Pipeline stability:** Top-level try/except in `_run_pipeline`; session_complete broadcast on crash.
- **Force-trigger:** Chat keywords ("agent terminal", etc.) and orchestrate_task present.
- **Crash log:** `data/orchestrator_crash.log` exists with **historical** KeyError for `gemini-2-flash`. Current `joi_brain.py` uses a safe fallback chain (no invalid key); those crashes were from an older build.

---

## 2. Errors and fixes

### 2.1 Resolved / already fixed

- **Brain KeyError `gemini-2-flash`:** Code now uses `MODELS.get(model_key) or MODELS.get("gemini-fallback") or ...` (no invalid key). Crash log is from before this fix.
- **propose_upgrade TypeError:** `joi_evolution.propose_upgrade` already coerces `code` and other params to `str` before `_validate_python_code(code)`, so LLM null/wrong types are handled.

### 2.2 Fix applied this run

- **Subtask ID type mismatch:** If the Architect returns `"id": 1` as string (JSON), the pipeline keys approval by `st_id` (string `"1"`) but `approve_subtask_fn` normalizes to `int(1)` and looks up `_subtask_approvals[1]` → no match, gate never releases. **Fix:** Normalize `st_id` to `int` at the start of each subtask loop so the approval gate key is always an integer.

### 2.3 Environment note

- **Python 3.14 + chromadb:** Companion import can fail (type inference). For Agent Terminal development and running the app, use **Python 3.11 or 3.12**.

---

## 3. Improvements (no major rewrites)

1. **Normalize subtask_id in pipeline** (done): Coerce `st.get("id")` to int when possible so approval gates match between pipeline and tool.
2. **New-file creation:** Currently `_apply_changes` and `code_edit` require an existing file and non-empty `old_text`. To support “create a new app”:
   - **Option A (minimal):** In `_apply_changes`, if the target path does not exist and there is a single change with `old_text == ""` and `new_text` non-empty, write `new_text` to the path (with backup dir or no backup for new files). Architect would emit a subtask with `files: ["path/to/new_file.py"]` and Coder would output one change with empty `old_text` and full file content.
   - **Option B:** Add a `code_write_file` (or similar) tool and have the Architect/Coder use it for “create file” subtasks. Slightly more structure, same idea.
3. **Diagnostic script:** When the only failure is `joi_companion` import (e.g. Python 3.14), consider reporting “PASS with env warning” if all static/orchestrator checks pass, so it’s clear the Agent Terminal code path is OK and the blocker is environment.
4. **Validator on Windows:** Python subtasks already use in-process `ast.parse` for syntax to avoid Windows path/encoding issues; non-Python validation still uses subprocess. No change needed unless you add more validators.

---

## 4. Suggested major changes (for your approval first)

- **New-file creation in pipeline:** As above (Option A or B). This is the one behavioral extension needed for “create new apps” without pre-creating empty files by hand.
- **Larger refactors (not recommended unless needed):** Moving agents to separate processes, replacing the approval gates with a different UX, or rewriting the pipeline from scratch — not suggested; current design is stable and documented in `AGENT_TERMINAL_ARCHITECTURE.md`.

---

## 5. Quick test checklist

After fixing the subtask_id normalization and using Python 3.11/3.12:

1. Start Joi: `python joi_companion.py`
2. In chat: “Use the agent terminal to add a comment at the top of `joi_companion.py`.”
3. Confirm: plan appears, subtask(s) run, diff shown, approval requested, then apply.
4. Optional: “Orchestrate: fix the typo in modules/joi_agents.py” (if you introduce a known typo) and confirm Coder + Validator + Apply flow.

---

## 6. File reference

| Component        | File |
|------------------|------|
| Pipeline         | `modules/joi_orchestrator.py` |
| Architect/Coder/Validator | `modules/joi_agents.py` |
| Brain (model routing) | `modules/joi_brain.py` |
| Code apply       | `modules/joi_code_edit.py` (`code_edit`), `joi_orchestrator._apply_changes` |
| Diagnostic script | `scripts/check_agent_terminal.py` |
| Architecture map | `AGENT_TERMINAL_ARCHITECTURE.md` |
