# Joi AI — Performance Analysis & Optimizations

This document summarizes the performance review of the Joi AI system, findings, and the optimizations applied. All core features remain intact.

---

## 1. Request Flow Overview

**Primary path:** User message → `/chat` → context assembly → `run_conversation` (LLM + tools) → post-response updates → JSON response.

- **Context assembly:** 20+ blocks (consciousness, inner state, reasoning, autobiography, modes, diagnostics, vector memory, facts/preferences, growth, learning, router, neuro, skill synthesis, DPO, MemGPT, orchestrator, brain).
- **Post-response:** inner state update, autobiography tick, auto_extract, auto_record, auto_journal, auto_infer_feedback, auto_capture_skill, DPO signal, MemGPT update, neuro brain state.

---

## 2. Findings

### 2.1 Redundancy & Duplication

- **Consciousness / recent reflections:** Only one call to `get_recent_reflections` per request (used for consciousness block and for `journal_cue` in inner state). No duplicate.
- **Manifest (diagnostics):** `get_manifest()` is already cached; `get_manifest_summary()` is cheap after first load.
- **Facts/preferences:** Multiple DB calls in one block (`search_facts` + 4× `get_preference`). Kept as-is; parallelized with other blocks.

### 2.2 Slow / Heavy Paths

- **Context assembly:** All blocks were run **sequentially**. Each block does I/O (DB, files, vector store, or submodules). Total time was the sum of all block latencies.
- **Post-response:** Several updates ran **sequentially** after the LLM reply (auto_extract, learning, journal, DPO, MemGPT, etc.). They delayed the HTTP response even though the client only needs the reply and brain_state.
- **Learning summary:** `get_learning_summary()` ran on **every** request (DB query + processing). No cache.

### 2.3 Routing & Tool Effectiveness

- **Router:** Rule-based classification in `joi_router.classify_task` is fast (<1 ms). No change.
- **Tool selector:** `select_tools()` is in-memory and respects the 128-tool cap. When the model requests a gated tool, a single fallback rerun with expanded tools is done. Behavior is correct.
- **Quiet-Star:** For **high** complexity, an extra Gemini Flash call runs for pre-reasoning. This adds latency for complex tasks by design; no change.

### 2.4 Misrouting

- No misrouting identified. Orchestrator force-trigger for coding tasks and action-intent detection for play/open/launch are correct.

---

## 3. Optimizations Applied

### 3.1 Parallel Context Assembly (`joi_companion.py`)

- **What:** Independent context block compilers run in a **ThreadPoolExecutor** (8 workers) instead of sequentially.
- **Blocks parallelized:** Inner state, Titan, autobiography, mode hint, manifest summary, vector memory, facts/prefs, growth narrative, learning, router, personality weights, skill synthesis, DPO, working memory, orchestrator, brain models.
- **Order:** Consciousness still runs first (to get `recent` for inner state); then the parallel batch; then goodnight nudge (if any), memory declaration, self-healing, self-repair.
- **Effect:** Context assembly time is roughly **max(block times)** instead of **sum(block times)**, reducing latency before the LLM call.

### 3.2 Post-Response in Background Thread (`joi_companion.py`)

- **What:** Non-essential post-response work runs in a single **daemon thread** so the HTTP response can be sent sooner.
- **In background:** auto_extract, auto_record_interaction, auto_journal_check, auto_infer_feedback, auto_capture_skill, detect_preference_signal, update_working_memory.
- **Still in request path:** save_message, update_state, tick_message (for autobiography nudge), update_brain_state, get_brain_state (so the response includes `brain_state` and nudge).
- **Effect:** Shorter time to first byte for the client; learning/journal/DPO/MemGPT updates still run.

### 3.3 Learning Summary Cache (`modules/joi_memory.py`)

- **What:** `get_learning_summary()` result is cached in memory for **60 seconds**.
- **Effect:** Fewer DB hits on busy sessions; learning summary stays fresh enough for prompt injection.

---

## 4. Recommendations (Optional Future Work)

- **Index route:** `/` reads `joi_ui.html` from disk every time. Consider caching the HTML until file mtime changes.
- **Quiet-Star for high complexity:** If the extra Gemini call is too slow, consider making it optional via env (e.g. `JOI_QUIETSTAR_HIGH=0`) or skipping it for time-sensitive flows.
- **Facts/preferences:** A single DB round-trip (e.g. one query or a small batch) could replace `search_facts` + 4× `get_preference` for a small extra gain.
- **Manifest refresh:** If tools or routes change at runtime, call `refresh_manifest()` so the cached manifest and summary stay accurate.

---

## 5. What Was Not Changed

- Core features and behavior of routing, tool selection, orchestration trigger, and verification.
- Soul/identity, operational protocol, memory declaration, self-healing, self-repair blocks.
- LLM provider selection, tool loop, or fallback logic.
- Memory, learning, or consciousness behavior; only when/where they run (parallel or background) and caching of learning summary.

---

## 6. How to Verify

1. **Start server:** `python joi_companion.py`
2. **Send a few chat messages** and confirm replies and (if applicable) brain_state and autobiography nudge.
3. **Check logs** for `[CONTEXT] Injected: ...` to see which blocks were applied.
4. **Optional:** Add temporary timing logs around `_build_context_parallel` and the background thread to measure latency before/after.
