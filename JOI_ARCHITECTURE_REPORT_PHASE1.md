# JOI — Phase 1 Architecture Report

**Date:** 2026-02-14  
**Scope:** Repository analysis for LLM routing, agent system, fallbacks, and configuration.  
**Objective:** Map current behavior before implementing the new model policy and agent repairs.

---

## 1. How JOI Currently Works

### 1.1 Entry Points and Structure

| Component | Location | Role |
|-----------|----------|------|
| **Main app** | `joi_companion.py` | Flask app; loads modules from `modules/joi_*.py`, plugins from `plugins/`; registers TOOLS, ROUTES, TOOL_EXECUTORS. |
| **Chat endpoint** | `joi_companion.py` → `@app.route("/chat", methods=["POST"])` | Builds messages (soul, consciousness, inner state, Titan, etc.), calls `run_conversation()`, saves reply and runs post-chat hooks (learning, MemGPT, DPO, etc.). |
| **Module loader** | `load_modules()` in `joi_companion.py` | Iterates `MODULES_DIR.glob("joi_*.py")` and `importlib.import_module("modules.{name}")`; each module self-registers tools/routes on import. |
| **Plugin system** | `PLUGINS_DIR`, `register_route()` | Plugins register via `register_route(rule, methods, handler, name)`; routes applied in `load_plugins()`. |

- **Routing architecture:** Central `/chat` route; task classification and model choice happen inside `run_conversation()` (in `joi_llm.py`), which uses `joi_router` for classification and routing decisions. No separate API gateway; routing is in-process.

---

### 1.2 LLM Model Selection

- **Primary control:** `modules/joi_llm.py`.
  - **Env-driven:** `JOI_CHAT_PROVIDER` (default `"local"`), `JOI_LOCAL_BASE_URL`, `JOI_LOCAL_MODEL`, `OPENAI_TOOL_MODEL`, `GEMINI_MODEL`, `CLAUDE_MODEL`, `JOI_OPENAI_TOOL_MODEL`, `JOI_MODEL`, `JOI_VISION_MODEL`, etc.
  - **Runtime override:** `_RUNTIME_PROVIDER` and `_RUNTIME_MODEL` (from `set_provider` tool), persisted in `data/llm_provider.json`. Values: `auto | local | openai | gemini | claude`.
- **Flow in `run_conversation()`:**
  1. **Classification:** `joi_router.classify_task(user_msg)` → `task_type`, `complexity`, `risk`, `needs_tools`, `tier` (rule-based, no LLM).
  2. **Routing decision:** `joi_router.get_routing_decision(classification)` → `primary_model`, `verifier_model` from `_ROUTING_TABLE` keyed by `(task_type, tier)`. Table is **openai/gemini only** for primary; Claude only appears in comments and is explicitly skipped for auto-routing (“Claude reserved for Claude Code only”).
  3. **Provider override:** If `_RUNTIME_PROVIDER` is `claude` or `gemini`, a single call to `_call_claude` or `_call_gemini` is made (no tool loop for Claude/Gemini).
  4. **Default path (tools):** For tool-capable flow, `use_local` is derived from `_RUNTIME_PROVIDER` and `CHAT_PROVIDER`; then:
     - If local: `_call_local()`; on failure, switch to OpenAI.
     - Then `_call_openai()` with `OPENAI_TOOL_MODEL` (default `gpt-4o-mini`).
  5. **Fallback:** If both local and OpenAI fail, `joi_brain.brain.think()` is called (Gemini cascade); if that fails, return “Sorry Lonnie -- all models failed...”.
- **Model selection is deterministic** given the same classification and runtime provider: rule-based table + env/defaults. No random choice. Learning in `joi_brain` affects which Brain model is picked (score tiebreaker), not the main chat primary model.

---

### 1.3 Task Routing to Models

- **Router:** `modules/joi_router.py`.
  - **Classification:** `classify_task(message)` → `task_type` (e.g. `code_edit`, `writing`, `research`, `orchestration`, `conversation`), `complexity`, `risk`, `needs_tools`, `tier` (`fast` | `standard` | `critical`).
  - **Routing table:** `_ROUTING_TABLE`: keys `(task_type, tier)`; values `{"primary": "openai"|"claude"|"gemini", "verifier": ...}`. In practice the table uses **openai** as primary and **gemini** as verifier where verification is used; Claude is not in the table for auto-routing.
  - **Tool constraint:** If `needs_tools`, primary is forced to `openai` (only OpenAI does the tool loop in this codebase).
- **Verification (standard/critical):** After a text reply from the primary model, `_maybe_verify()` in `joi_llm.py` can call the verifier (Gemini or OpenAI) to get a second opinion; result can replace or annotate the reply. Implemented in `joi_router.verify_output()` which calls `_call_gemini` or `_call_openai` or `_call_claude`.

---

### 1.4 Fallbacks

- **Main chat (`joi_llm.run_conversation`):**
  - Local fails → use OpenAI.
  - OpenAI (and local) fail → try Brain (Gemini cascade) once; if that fails → return error message (no retry).
  - Bad tool JSON from local → retry once with OpenAI.
  - Tool gated (model asked for a tool not in selected set) → one fallback rerun with expanded tools.
- **Brain (`joi_brain.Brain.think`):**
  - `select_model()` picks by tier; on failure, `fallback=True` tries `DOWNGRADE_MAP` chain then `_get_all_fallbacks()` (other models in same tier and below).
  - No explicit “retry once then switch” at the top level; fallback is “try next model in list.”
- **joi_code_edit._call_code_model:** Claude → Gemini → GPT-4o; first success wins, no retry of same model.
- **Failures not uniformly handled:** Many `_call_*` paths only `print` and return `None`; caller may or may not try another provider. No central “retry once then fallback” policy.

---

### 1.5 Agent Roles and Definitions

- **Defined in:** `modules/joi_agents.py`.
  - **Architect:** Plans work; decomposes task into subtasks; outputs JSON with `subtasks[]`. Implemented by `call_architect()` which uses **Brain** (`brain.think(..., thinking_level=3)`) or, if Brain unavailable, direct `_call_gemini()`.
  - **Coder:** Produces surgical edits (old_text/new_text). Implemented by `call_coder()` which uses **Brain** (`thinking_level=2`) or, if Brain unavailable, direct `_call_openai(..., model="gpt-4o")`.
  - **Validator:** **Not an LLM.** Implemented by `call_validator()` — runs a shell command via `subprocess.run()` (syntax/import checks). `validate_python_file()` uses `ast.parse` + import-path check; no second LLM.
- **Orchestrator:** `modules/joi_orchestrator.py` — runs pipeline PLAN → (approval) → EXECUTE → VALIDATE → (approval) → APPLY. Calls `call_architect`, `call_coder`, `call_validator`/`validate_python_file`; state in `data/orchestrator_state.json`; SSE for terminal UI.

---

### 1.6 Spawning Agents / Sub-agents

- **Orchestration pipeline:** Started by `orchestrate_task()` (tool or force-trigger from `/chat`). Pipeline runs in a **background thread:** `threading.Thread(target=_run_pipeline, args=(task_description, project_path))`. So the **pipeline is real**, not stubbed; Architect and Coder are invoked sequentially in that thread; Validator is subprocess + AST.
- **“Agent terminal”:** The orchestrator exposes SSE (`/orchestrator/stream`) and a terminal-style UI; events like `agent_spawned`, `agent_thinking` are broadcast. There is no separate “sub-agent” process; Architect and Coder are function calls (Brain or direct LLM) in the same process.
- **Conclusion:** Agents are **real** (Architect/Coder/Validator run); they are **not** separate processes or async tasks — they run in one background thread, synchronously. No o3, no dedicated “supervisor” or “validator LLM” today; Validator is subprocess + static checks.

---

### 1.7 Coding Tasks and Validation

- **Coding tasks:** Routed via orchestration: Architect produces plan → Coder produces changes (JSON) → Validator runs test command / `validate_python_file` → user approval → apply. Code edits use `joi_code_edit` (e.g. `propose_patch`, `creative_edit`) and/or `joi_agents.preview_changes` / applicator in orchestrator.
- **Validation of outputs:**
  - **Chat:** Optional verification via `_maybe_verify()` → `joi_router.verify_output()` (second model).
  - **Orchestration:** Validator = subprocess + AST/import check; no LLM validator.
  - **Evolution:** `propose_upgrade` in `joi_evolution.py` validates Python syntax and imports before saving proposal; no LLM-based approval step.

---

### 1.8 API Keys and Environment Variables

- **Read in:** `joi_llm.py` at import time: `OPENAI_API_KEY`, `JOI_LOCAL_BASE_URL`, `JOI_LOCAL_MODEL`, `JOI_CHAT_PROVIDER`, `GEMINI_API_KEY`, `JOI_GEMINI_MODEL`, `ANTHROPIC_API_KEY`, `JOI_CLAUDE_MODEL`, `JOI_OPENAI_TOOL_MODEL`, `JOI_MODEL`, `JOI_VISION_MODEL`, `JOI_MAX_OUTPUT_TOKENS`, plus local context vars (`JOI_LOCAL_CTX`, etc.). `joi_companion.py` calls `load_dotenv()` at startup.
- **Validation at startup:** No single “validate all API keys” step. Each provider is initialized if key exists (e.g. `client = OpenAI(...)` if `OPENAI_API_KEY`); failures print and leave client as `None`. `joi_routes.provider_status()` does a live ping to each provider on demand.
- **Persistence:** Runtime provider selection in `data/llm_provider.json`; Brain uses `data/brain_stats.json`, `data/rpd_tracker.json`, `data/brain_learning.json`, `data/routing_overrides.json`.

---

## 2. File-by-File Control Summary

| Concern | Files |
|--------|--------|
| **LLM routing (main chat)** | `joi_llm.py` (`run_conversation`, provider override, local → openai → brain fallback) |
| **Task → model mapping** | `joi_router.py` (`classify_task`, `get_routing_decision`, `_ROUTING_TABLE`) |
| **Brain (tier-based model pick)** | `joi_brain.py` (`MODELS`, `Brain.select_model`, `Brain.think`, `_call_model`, downgrade/fallback) |
| **Agent logic** | `joi_agents.py` (Architect/Coder/Validator prompts and `call_*`); `joi_orchestrator.py` (pipeline and SSE) |
| **Fallback logic** | `joi_llm.py` (conversation fallback chain); `joi_brain.py` (Brain fallback chain); `joi_code_edit.py` (Claude→Gemini→GPT-4o) |
| **Hardcoded / env model names** | See next section. |
| **Verification (second model)** | `joi_router.verify_output`; `joi_llm._maybe_verify` |

---

## 3. Hardcoded and Unsupported Model References

- **joi_llm.py:**  
  - `GEMINI_MODEL = os.getenv("JOI_GEMINI_MODEL", "gemini-3-flash-preview")` — **unsupported** (Gemini 3 preview).  
  - `CLAUDE_MODEL`, `ANTHROPIC_API_KEY`, `_call_claude`, `HAVE_ANTHROPIC` — **Claude** (to be removed/disabled per policy).  
  - `LOCAL_MODEL` default `"mistral-7b"`, LM Studio — **local** (to be removed or kept as optional offline path only; not in approved list).  
  - `OPENAI_TOOL_MODEL` default `"gpt-4o-mini"`, `MAIN_MODEL`/`VISION_MODEL` default `"chatgpt-4o-latest"` — OpenAI names to align with approved list.
- **joi_brain.py:**  
  - `MODELS` dict: `gemini-3-pro`, `gemini-3-flash`, `gemini-2.5-pro`, `gemini-2-flash`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`, `gemma-3-27b`, `deepseek-r1-8b`, `mistral-7b`, `gpt-4o`. Many are **not** in the approved list (no gemini-3*, no gemma, no deepseek/mistral if we drop local).  
  - `DOWNGRADE_MAP` references same model keys.  
  - Last-resort fallback is `mistral-7b` (local).
- **joi_code_edit.py:**  
  - Claude first, then Gemini, then GPT-4o. Claude must be removed; Gemini/OpenAI model IDs must be from approved list.
- **joi_routes.py (provider_status):**  
  - Reports `claude` with model `"claude-haiku-3"`; LM Studio/local. To be updated or disabled for Claude/local.
- **joi_router.py:**  
  - Comments and availability checks reference Claude; routing table itself is already openai/gemini for auto.

---

## 4. Where Failures Are Not Handled / May Freeze

- **Blocking calls:**  
  - `/chat` is **synchronous:** it calls `run_conversation(...)` directly. No async, no queue. Long-running LLM calls (and tool loops) block the request thread until done. If a model hangs (e.g. network), the UI can freeze until timeout or failure.  
  - Orchestration runs in a **background thread**, so starting orchestration does not block `/chat`; but the pipeline itself runs blocking LLM calls inside that thread.
- **Timeouts:**  
  - OpenAI client and Anthropic/Gemini may use library defaults; no project-wide timeout is set in the reviewed code. `call_validator` uses `timeout=30` for subprocess.  
- **Retries:**  
  - OpenAI path in `joi_llm` has one retry on rate limit/too large (trim and retry). No generic “retry once then fallback” for other failures. Brain fallback tries other models but does not retry the same model.

---

## 5. Model Selection: Deterministic vs Random

- **Deterministic:**  
  - Classification is rule-based.  
  - Routing table lookup is deterministic.  
  - Brain’s `_pick_from_tier` uses learning score (and RPD); same inputs → same ordering → same model key.  
- **Not random:** No random selection of model anywhere in the reviewed flow.

---

## 6. Agent Spawning: Real vs Stubbed

- **Real:**  
  - Orchestration pipeline runs in a thread; `call_architect` and `call_coder` are invoked with real LLM calls (Brain or direct Gemini/OpenAI).  
  - `call_validator` runs real subprocess and file validation.  
- **Stubbed / not present:**  
  - No separate “supervisor” LLM (e.g. o3).  
  - No LLM-based “validator agent” — only subprocess + AST.  
  - No async or process-based sub-agents; all in one process, one pipeline thread.

---

## 7. Additional Notes

- **propose_upgrade (joi_evolution):** CLAUDE.md mentions a “propose_upgrade TypeError.” The function is `propose_upgrade(**params)` and is called from the tool executor with `**fn_args` and from Flask with `propose_upgrade(**data)`. A possible cause is `require_user()` (no request context when called from a tool) or a mismatch in params (e.g. tool schema vs what the function expects). Should be verified and fixed in Phase 4.  
- **Plugins:** Optional; e.g. `claude_code_delegate`, `system_monitor_dashboard`. Not required for core routing/agent behavior.  
- **Avatar / memory / UI:** As requested, these are out of scope for this report; no changes recommended here.

---

## 8. Summary Table

| Question | Answer |
|----------|--------|
| Where is LLM routing controlled? | `joi_llm.run_conversation` + `joi_router.classify_task` / `get_routing_decision`; Brain in `joi_brain.py` for fallback and agents. |
| Where are agent roles defined? | `joi_agents.py` (Architect/Coder/Validator); orchestrator in `joi_orchestrator.py`. |
| Where is fallback logic? | `joi_llm.py` (local→openai→brain); `joi_brain.py` (tier cascade + downgrade map); `joi_code_edit.py` (Claude→Gemini→GPT-4o). |
| Hardcoded models? | Yes: joi_llm (GEMINI_MODEL default, Claude, local), joi_brain (full MODELS dict), joi_code_edit (Claude first). |
| Unhandled failures / blocking? | `/chat` is blocking; no global timeouts; limited retries. |
| Model selection random? | No; deterministic. |
| Do agents really run? | Yes; pipeline runs in thread, Architect/Coder/Validator execute; no supervisor/validator LLM, no o3. |

---

**Next (Phase 2–7):** Implement new model policy (Gemini/OpenAI/o3 only), remove/disable Claude and LM Studio references, assign roles (Tier 1/2/3 and supervisor), repair agent hierarchy (supervisor + coder + validator LLMs), add robust fallback (retry → same-tier fallback → escalate → log), centralize config and keys, then implement in small patches with a clear change plan.
