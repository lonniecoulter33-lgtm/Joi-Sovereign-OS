# Agent Terminal — Architecture Map & Crash Analysis

This document maps how Agent Terminal (the multi-agent orchestration subsystem) is invoked, how tools and agents work, where results go, and the most likely crash points. Use it to fix issues without rewriting the system.

---

## 1. What Agent Terminal Is

**Agent Terminal** = the **Orchestrator pipeline** in `modules/joi_orchestrator.py`. It provides:

- **Self-repair**: multi-step code edits with Architect → Coder → Validator
- **Code-writing/debugging**: surgical edits via Coder, validated by subprocess/ast
- **Planner**: Architect decomposes tasks into ordered subtasks
- **Diagnostics**: pre/post watchdog checkpoints, sanity_check.py
- **Multi-agent controller**: single background thread runs PLAN → EXECUTE → APPLY with approval gates

Agents are **not** separate processes. They are:

| Agent      | Implementation                    | Location           |
|-----------|------------------------------------|--------------------|
| ARCHITECT | `call_architect()` → Brain/Gemini  | `joi_agents.py`    |
| CODER     | `call_coder()` → Brain/OpenAI      | `joi_agents.py`    |
| VALIDATOR | `call_validator()` → subprocess    | `joi_agents.py`    |
| Supervisor| `_run_pipeline()` in background   | `joi_orchestrator.py` |

**Self-healing:** On failure (plan or subtasks), the pipeline calls `_analyze_failure_and_propose_retry()` (Brain/LLM), gets a revised task description, and re-runs the pipeline with it. Capped at `MAX_RECOVERY_ATTEMPTS` (2), so up to 3 total runs (1 initial + 2 retries). Works for Joi’s own codebase and for separate projects when `project_path` is set.

---

## 2. How Agent Terminal Is Invoked

### 2.1 Chat force-trigger (bypasses LLM tool choice)

**File:** `joi_companion.py` (chat route)

- **Condition:** User message matches `_orch_triggers` (e.g. "agent terminal", "orchestrate", "work on", "handle this", "fix the code") AND no active session AND not a question (e.g. not starting with "what", "how").
- **Action:** Calls `orchestrate_task(task_description=user_message)` and returns immediately with `"on it. orchestration started -- check the terminal."`
- **Effect:** Pipeline runs in a **daemon background thread**. User sees reply before any plan exists.

### 2.2 Tool call (LLM chooses tool)

- **Router:** `joi_router.classify_task()` maps keywords (e.g. "agent terminal", "orchestrate", "multi-agent") to `task_type="orchestration"`, `needs_tools=True`.
- **Tool selection:** `joi_tool_selector` has group `"orchestrator"` at **priority 1**, so `orchestrate_task`, `approve_subtask`, `reject_subtask`, `get_orchestrator_status`, `cancel_orchestration` are always included when tools are sent.
- **Execution:** In `joi_llm.run_conversation()`, when the model returns a tool call for `orchestrate_task`, `TOOL_EXECUTORS["orchestrate_task"](**fn_args)` is called. That runs `orchestrate_task()` in `joi_orchestrator.py`, which creates a session and starts `_run_pipeline()` in a thread.

---

## 3. How Tools Are Registered

- **Companion registry:** `joi_companion.register_tool(tool_def, executor_fn)` appends to `TOOLS` and `TOOL_EXECUTORS`.
- **Orchestrator tools** are registered at import in `joi_orchestrator.py`: `orchestrate_task`, `approve_subtask`, `reject_subtask`, `get_orchestrator_status`, `cancel_orchestration`.
- **Tool gating:** `joi_tool_selector.select_tools()` can trim the list to ≤128 tools. Group `orchestrator` is priority 1, so these five are not trimmed. If the model requests a tool that wasn’t in the selected set, `get_expanded_tools()` is used and the conversation is rerun with an expanded set.

---

## 4. How LLM Routing Is Handled

### 4.1 Main chat path

- **Classification:** `joi_router.classify_task(message)` → `task_type`, `complexity`, `risk`, `needs_tools`, `tier`.
- **Routing:** `get_routing_decision(classification)` uses `config.joi_models.TASK_MODEL_ROUTING`. For `task_type=="orchestration"`, `_classification_to_config_task_key` returns `"supervisor"`; config has `"supervisor"` → primary OpenAI supervisor model, fallback Gemini.
- **Tool path:** When `needs_tools` is true (e.g. orchestration), the chat path uses **OpenAI** with tools (tool loop is OpenAI-only in current design). So orchestration requests get the tool list that includes `orchestrate_task`.

### 4.2 Architect / Coder (inside pipeline)

- **Architect:** `call_architect()` uses `joi_brain.brain.think(..., thinking_level=3 or 4)`. Brain picks model from config (e.g. Gemini for planning). No tool-calling; single completion.
- **Coder:** `call_coder()` uses `brain.think(..., thinking_level=2)` or direct `_call_openai()` with system/user messages. No tool-calling.

---

## 5. How Results Return to Joi

- **Session state:** In-memory `_current_session` plus persisted `data/orchestrator_state.json`. **Note:** `event_log` is not persisted (too large); on load, `event_log` is set to `[]`.
- **SSE:** `_broadcast(event)` pushes events to all clients connected to `GET /orchestrator/stream`. The Agent Terminal UI subscribes to this for real-time plan, diffs, approvals, and completion.
- **Final outcome:** `_broadcast({"type": "session_complete", "status": "complete"|"partial"|"failed", ...})`. Phase is set to `COMPLETE` or `FAILED` and state is saved.

---

## 6. Lifecycle of a Deployed “Agent” (Pipeline Run)

| Phase        | What happens |
|-------------|---------------|
| **Init**    | `orchestrate_task()` creates `_new_session()`, saves state, starts `threading.Thread(target=_run_pipeline, args=(task, project_path), daemon=True)`. |
| **Prompt build** | Architect: task + `_read_files(candidate_files)` + JOI_CONTEXT. Coder: subtask + target file content + optional error_feedback. |
| **Tool access** | Architect/Coder do **not** use Joi’s tool registry; they are direct LLM calls (Brain / Gemini / OpenAI). Validator uses `subprocess.run(test_command, timeout=30)`. |
| **Execution loop** | PLAN → (plan approval gate, 300s timeout) → for each subtask: Coder (up to MAX_RETRIES) → preview → Validator → subtask approval gate (300s) → APPLY via `_apply_changes()` (code_edit or direct write + backup). |
| **Failure conditions** | Architect returns `plan["error"]` → phase FAILED, session_complete. Coder retries 3x then subtask marked failed. Validator timeout 30s. Apply failure → rollback, subtask failed. Post-orchestration sanity failure → circuit breaker, all applied reverted. |
| **Shutdown** | Phase set to COMPLETE/FAILED, `_save_state()`, `_broadcast(session_complete)`. Thread exits. No join (daemon thread). |

---

## 7. Most Likely Crash Points

### 7.1 Pipeline thread crashes (no session_complete)

- **Root cause:** `_run_pipeline()` has **no top-level try/except**. Any uncaught exception (e.g. from `call_coder`, `call_architect`, `_apply_changes`, or Brain) kills the thread.
- **Effect:** Session stays in RUNNING/EXECUTE/APPLY; user never sees `session_complete`; SSE stops updating.

### 7.2 Routing / tool visibility

- If classification is wrong, `needs_tools` might be false and the model might get a reduced tool set or Gemini-only path (no tools). Then the model cannot call `orchestrate_task`.
- **Mitigation:** Orchestration keywords in `_TASK_PATTERNS["orchestration"]` and `orchestrator` group priority 1 keep tools in. Force-trigger in chat also starts orchestration without requiring a tool call.

### 7.3 Tool permission / executor mismatch

- If `orchestrate_task` were omitted by tool selector (e.g. bug or cap), the model could request it and hit “Unknown tool” or fallback rerun. Currently orchestrator is priority 1 so this is unlikely.

### 7.4 Async / threading

- Approval gates block the pipeline thread for up to 300s. If `approve_subtask` is called with wrong `subtask_id` type (e.g. string `"1"` vs int `1`), the event key in `_subtask_approvals` may not match and the gate never releases for that subtask (until timeout).
- **Mitigation:** Normalize `subtask_id` to int in `approve_subtask_fn` / `reject_subtask_fn` (already attempted; ensure consistency everywhere).

### 7.5 State persistence

- `event_log` not saved → after crash, recovered session has no event history. Acceptable for recovery; not a crash cause.
- State is saved after plan and after each subtask; if the process dies mid-write, file can be inconsistent (rare).

### 7.6 Supervisor / Brain

- If Brain or Gemini/OpenAI is down or returns malformed JSON, `call_architect` / `call_coder` can raise (e.g. KeyError on `result.get("text")`) or return error dict. Architect error is handled; Coder path can raise if code assumes `result` has certain keys.
- **Mitigation:** Defensive checks and top-level try/except in pipeline so any agent failure sets phase FAILED and broadcasts session_complete.

### 7.7 Recursion / loop traps

- Pipeline is sequential (no recursion). Tool loop in `run_conversation` has `max_iterations=5`. No obvious infinite loop in orchestrator.

### 7.8 Context overflow

- Architect receives multiple file contents (capped at 15 files, 50K chars each). Coder receives one file. Trimming in `_read_files` and in LLM layer (`_trim_messages_for_api`, `MAX_SYSTEM_PROMPT_CHARS`) reduces risk. If Brain or provider has a smaller limit, requests can fail; pipeline should treat that as a normal failure and report via session_complete.

### 7.9 propose_upgrade TypeError (evolution)

- `propose_upgrade(**params)` is called from the tool executor with `params` from the LLM. If `code` (or other required field) is `None` or not a string, `_validate_python_code(code)` can raise `TypeError`. Early validation/coercion of params prevents this.

---

## 8. Fix Order (from task spec)

- **A. Stability:** Top-level try/except in `_run_pipeline`; normalize/coerce params in `propose_upgrade`.
- **B. Routing:** Confirm orchestration → supervisor and tool set includes orchestrator tools (already in place; document or small guard).
- **C. Lifecycle:** On pipeline exception: set phase FAILED, save state, broadcast session_complete. Normalize `subtask_id` to int at approval entry points.
- **D. Diagnostics:** Log pipeline exceptions with traceback; optionally persist last N events for crash inspection.
- **E. Planning:** Keep subtask cap (e.g. 10); robust JSON extraction in Architect/Coder (already partially present).

This file is the single map for Agent Terminal; code changes should reference it and stay minimal and modular.
