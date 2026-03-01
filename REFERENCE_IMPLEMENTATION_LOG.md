# Implementation Log — Session Reference

This file summarizes the work completed in this session for your reference. Save it wherever you like (e.g. `docs/` or project root).

---

## 1. Hard Stop & Human Intervention

**Goal:** When a plan step fails the sandbox 3 times, pause for human intervention instead of failing silently; support force-complete and correction-hint resume.

### Files changed

- **`modules/joi_workspace.py`**
  - Default workspace (in `_load_workspace()` and `clear_workspace()`) now includes: `phase`, `paused_reason`, `last_error`, `failed_step_index`, `failed_step_description`, `debug_log_path`, `correction_hint`.
  - **`set_paused_for_intervention(step_index, step_description, reason, last_error, stdout, stderr, code_snippet)`** — Sets `phase = 'PAUSED_FOR_INTERVENTION'`, writes a timestamped log under `data/debug_logs/`, updates workspace and status.
  - **`get_paused_state()`** — Returns the intervention payload for the UI (or `None`).
  - **`clear_paused()`** — Clears pause and related fields.
  - **`force_complete_step(step_index)`** — Marks the step complete and clears paused state.
  - **`set_correction_hint(hint)`** — Stores hint and clears paused so the next run can retry with it.
  - **`get_and_clear_correction_hint()`** — Returns and clears the stored hint.
  - **`manual_override` tool** — Registered on module load: `action` = `force_complete` (requires `step_index`) or `correction_hint` (requires `correction_hint` string).

- **`modules/joi_llm.py`**
  - On the **3rd consecutive sandbox failure** in `_run_plan_execution`: calls `set_paused_for_intervention(...)`, then returns `(msg, model, intervention_payload)`.
  - **`run_conversation`** sets `run_conversation._intervention_required = intervention` when that happens.
  - **Resume path:** If the user says "continue" / "resume" / "retry" and there are `pending_tasks`, it runs `_run_plan_execution(..., correction_hint=get_and_clear_correction_hint())`.
  - **`_run_plan_execution`** accepts optional `correction_hint` and injects it into the first step’s user message when resuming.

- **`joi_companion.py`**
  - After `run_conversation(...)`, if `run_conversation._intervention_required` is set, the handler returns **`jsonify(intervention)`** (e.g. `status`, `reason`, `last_error`, `failed_step_index`, `debug_log_path`) and skips normal reply handling.

### UI payload on intervention

```json
{
  "status": "intervention_required",
  "reason": "Execution failed after 3 retries",
  "last_error": "<stderr>",
  "failed_step_index": 0,
  "failed_step_description": "...",
  "debug_log_path": "<path to data/debug_logs/critical_failure_*.txt>"
}
```

### Flow (Tier 4)

| Step        | Component     | Action |
|------------|---------------|--------|
| Detection  | joi_tester    | 3rd consecutive `exit_code != 0` |
| Escalation | joi_workspace | `set_paused_for_intervention`; `phase = PAUSED_FOR_INTERVENTION` |
| Preservation | `data/debug_logs/` | Timestamped file with stdout, stderr, code snippet |
| Response   | joi_companion | Returns the intervention JSON above |
| Resolution | User          | Use `manual_override` (force_complete or correction_hint) or say "continue" to resume with hint |

---

## 2. JIT Tool Loading (Prompt bloat guard)

**Goal:** Load tools only when needed by task type; keep system prompt under ~500 tokens for casual turns.

### Files changed

- **`modules/joi_llm.py`**
  - Before tool selection: if `task_type == "conversation"` and `not needs_tools` and `not _actuation_intent`, **`tools = []`** and the selector is skipped.
  - Otherwise, existing `select_tools(...)` (and actuation extra groups) is used as before.

### Result

- **Casual** (conversation, no tools) → 0 tools, smaller prompt.
- **Coding / action** → Full tool selection (code_edit, filesystem, etc.) as before.

---

## 3. Conflict Resolver (System health audit)

**Goal:** Compare system prompts across modules for contradictions (e.g. "be concise" vs "be verbose").

### Files created

- **`scripts/check_system_health.py`**
  - Collects prompt text from `joi_llm.py` (runtime `_build_system_prompt()` or source excerpt) and from `joi_router.py` (planning prompt, MUST_FOLLOW/constraints, docstrings).
  - Calls a fast model (default `gpt-4o-mini`, overridable via `JOI_CONFLICT_CHECK_MODEL`) to compare for contradictions.
  - Writes **`data/conflict_report.txt`** and prints the report to stdout.

### How to run

```bash
python scripts/check_system_health.py
```

Requires `OPENAI_API_KEY` for the LLM step.

---

## 4. Project Tree Generator (Spatial awareness)

**Goal:** Give Joi a visual snapshot of the project (ASCII tree) for orientation, verification, and pruning; optional JOI_MAP.md for persistent layout.

### Files created

- **`modules/joi_tree.py`**
  - **`generate_project_tree(root_dir=None, max_depth=10, ignore_dirs=None, max_children=50)`** — Returns ASCII tree using `├──` and `└──`. Ignores `.git`, `__pycache__`, `.venv`, `venv`, `node_modules`, `sandbox`, etc.
  - **`update_joi_map(root_dir=None)`** — Writes the tree to **`JOI_MAP.md`** in the project root.
  - **Tool `project_tree`** — Params: `root` (default `"project"`), `save_to_joi_map` (default `False`), `max_depth` (default `10`). Registered with `joi_companion` on import.

### Files changed

- **`modules/joi_tool_selector.py`**
  - Added **`project_tree`** to **filesystem** and **code_edit** groups, with keywords (e.g. "tree", "structure", "layout", "project structure").

- **`modules/joi_llm.py`**
  - At the start of **`_run_plan_execution`**, the current project tree (max depth 8) is generated and **injected into the first step’s user message** so the Implementer always sees the layout.

### 3-tier usage

| Phase        | Usage | Result |
|-------------|--------|--------|
| Architect   | Re-orient | Tree injected at start of plan execution; can also call `project_tree`. |
| Implementer | Validation | Can call `project_tree` after creating files to confirm placement. |
| Reviewer    | Audit | Can call `project_tree` and compare to plan (e.g. missing/extra files). |

### JOI_MAP.md

- When **`project_tree`** is called with **`save_to_joi_map: true`**, the script updates **`JOI_MAP.md`** in the project root for persistent layout memory.

---

## Quick reference: key paths and symbols

| What | Where |
|------|--------|
| Pause state, debug logs dir | `modules/joi_workspace.py` — `DEBUG_LOGS_DIR`, `get_paused_state()`, `set_paused_for_intervention()` |
| Manual override tool | `modules/joi_workspace.py` — `manual_override` (force_complete / correction_hint) |
| 3-retry hard stop | `modules/joi_llm.py` — `_run_plan_execution` (sandbox failure branch) |
| Intervention response | `joi_companion.py` — `/chat` checks `run_conversation._intervention_required` |
| JIT tools (casual = 0 tools) | `modules/joi_llm.py` — block before TOOL GATING |
| Conflict report script | `scripts/check_system_health.py` → `data/conflict_report.txt` |
| Tree generator | `modules/joi_tree.py` — `generate_project_tree()`, `project_tree` tool, `update_joi_map()` |
| Tree in plan execution | `modules/joi_llm.py` — `_run_plan_execution` first-step context |

---

*Generated as a session reference. You can move or copy this file (e.g. to `docs/`) and edit as needed.*
