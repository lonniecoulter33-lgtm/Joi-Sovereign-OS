# Joi AI — Concrete Optimization Plan (Phase 2)

This document details **remaining** performance and efficiency improvements after the initial parallel context and background post-response work. All changes preserve core AI behavior, `brain_state`, and nudge mechanics.

---

## 1. Remaining Slow / Sequential Context Blocks

### 1.1 Facts & preferences (5 DB round-trips per request)

**Current:** `_facts_prefs_block()` in `joi_companion._build_context_parallel` does:
- 1× `search_facts("", limit=100)` → one connection + one query
- 4× `get_preference(pk)` for `communication_style`, `tone_preference`, `work_focus`, `interests` → four separate connections + four queries

**Change:** Batch preference reads into a single DB round-trip.

| Location | Change |
|----------|--------|
| `modules/joi_memory.py` | Add `get_preferences_batch(keys: List[str]) -> Dict[str, Any]` that runs a single `SELECT key, value FROM preferences WHERE key IN (?,?,?,?)` and returns `{key: parsed_value}`. |
| `joi_companion.py` → `_facts_prefs_block()` | Replace the loop of 4× `get_preference(pk)` with one `get_preferences_batch(pref_keys)`. |

**Expected gain:** ~3–4 fewer DB opens/queries per request; latency of facts/prefs block drops (especially on Windows where SQLite open is costlier). Roughly **5–20 ms** saved per request depending on environment.

---

### 1.2 Vector memory (2–3 vector queries per request)

**Current:** Per `/chat` request, in parallel workers:
- **VECTOR_MEMORY:** `compile_memory_context(user_message)` → `recall_memory(user_message, top_k=8)` (default namespace).
- **WORKING_MEMORY:** `compile_working_memory(user_message)` → `recall_memory(user_message, namespace="sessions", top_k=MAX_PAGED_IN)` (and expects a dict with `results`; `recall_memory` actually returns a list — see §4).
- **SKILL_SYNTHESIS:** `find_skills(user_message, top_k=3)` → `recall_memory(query, namespace="skills", top_k=top_k)` when vector path is used.

So we have **up to 3** separate vector store queries (default, `sessions`, `skills`) per request.

**Change (optional, medium effort):** Introduce a **single “context memory batch”** that runs all needed vector queries in one go and passes results to the blocks that need them.

| Location | Change |
|----------|--------|
| `joi_companion.py` or `modules/memory/memory_manager.py` | Add `recall_memory_multi(user_message: str, requests: List[Tuple[str, int, float]]) -> Dict[str, List]` where each request is `(namespace_or_none, top_k, threshold)`, and return `{namespace_key: list_of_results}`. Implement by calling existing `recall_memory` (or store.query) once per namespace. |
| `joi_companion._build_context_parallel` | At start of parallel phase, in the **main thread**, call `recall_memory_multi(user_message, [("default", 8, 0.25), ("sessions", MAX_PAGED_IN, 0.3), ("skills", 3, 0.0)])` once. Pass the returned dict (or relevant slices) into `_vector_memory_block`, `_working_memory_block`, and skill synthesis (or into shared closure). Each block then only does in-memory formatting, no vector I/O. |

**Alternative (simpler):** Keep current structure but ensure the three calls run in **parallel** (they already do via the context executor). The only extra win then is avoiding duplicate store connection overhead if the vector backend is not connection-pooled. Expected gain from batching: **~20–80 ms** if the vector backend is remote or slow; **~5–15 ms** if Chroma is local.

---

### 1.3 Skill synthesis (3 file reads + possible vector read)

**Current:** `compile_skill_synthesis_block(user_message)` calls:
- `_load_skill_library()` → read `SKILL_LIBRARY_PATH`
- `_load_goals()` → read `SKILL_GOALS_PATH`
- `_load_corrections()` → read corrections file
- Then `find_skills(user_message, top_k=3)` which may call `recall_memory(..., namespace="skills")` and again `_load_skill_library()` on hit.

**Change:** Add short-TTL in-memory caches for these file-backed structures so that within a time window (e.g. 30–60 s) the same request or multiple rapid requests reuse the same data.

| Location | Change |
|----------|--------|
| `modules/joi_skill_synthesis.py` | Add module-level cache: `_skill_library_cache = None`, `_skill_library_ts = 0`, `SKILL_CACHE_TTL = 45`. In `_load_skill_library()`, if `time.time() - _skill_library_ts < SKILL_CACHE_TTL` and cache is set, return cached dict. Otherwise read from disk and update cache and ts. Same pattern for `_load_goals()` and `_load_corrections()` with their own cache variables and TTL (or one shared TTL). Invalidate or bypass cache on write (e.g. in `_save_skill_library`, `_save_goals`). |

**Expected gain:** **5–15 ms** per request when skill block runs (avoids 3 file reads; second `_load_skill_library` in `find_skills` also served from cache).

---

### 1.4 Personality weights (file read every request)

**Current:** `compile_personality_weights_block()` calls `load_personality_weights()` which reads `WEIGHTS_PATH` on every request.

**Change:** Cache the parsed weights in memory with a short TTL; invalidate on write.

| Location | Change |
|----------|--------|
| `modules/joi_neuro.py` | Add `_personality_weights_cache = None`, `_personality_weights_ts = 0`, `WEIGHTS_CACHE_TTL = 60`. In `load_personality_weights()`, if cache is valid (age < TTL), return cache; else read file, update cache and ts, return. In `save_personality_weights()`, after writing, set `_personality_weights_cache = None` (or update to new value) so next read is fresh. |

**Expected gain:** **1–5 ms** per request.

---

## 2. Database Calls: Caching & Batching

### 2.1 Learning summary (already cached 60 s)

**Current:** `get_learning_summary()` in `joi_memory.py` is cached for 60 s.

**Optional:** Make TTL configurable via env, e.g. `JOI_LEARNING_SUMMARY_TTL=120`, and/or increase default to 120 s for lower DB load on busy sessions. No behavior change to AI or nudges.

---

### 2.2 get_brain_state

**Current:** Called once at end of `/chat` after `update_brain_state()`. It returns `_last_brain_state` when set, so no redundant computation.

**Change:** None. Already efficient.

---

### 2.3 Memory-related queries

**Current:** `recent_messages(limit=100)` is called once per `/chat` in the request path. No cache (correct; history changes every turn).

**Change:** None for `recent_messages`. For **facts + preferences**, use the batched `get_preferences_batch` as in §1.1; that is the main DB optimization.

---

### 2.4 DPO load

**Current:** `compile_dpo_block()` calls `_load_dpo()` (read `DPO_PATH` from disk). Runs inside the parallel context pool. `detect_preference_signal()` (background) also calls `_load_dpo()` and then `_save_dpo()`.

**Change:** Add a short-TTL cache for the DPO blob used by **prompt injection only** (so we don’t cache across a write in the same process).

| Location | Change |
|----------|--------|
| `modules/joi_dpo.py` | Add `_dpo_cache = None`, `_dpo_cache_ts = 0`, `DPO_CACHE_TTL = 45`. In `_load_dpo()`, if cache age < TTL, return cached dict; else read file, update cache, return. In `_save_dpo()`, after write, set `_dpo_cache = None` (or update to the new data). |

**Expected gain:** **1–5 ms** for the DPO context block when it runs.

---

## 3. Repeated / Redundant Computations

### 3.1 Router stats (file read every request)

**Current:** `compile_router_block()` calls `_load_routing_stats()` which reads `ROUTING_STATS_PATH` every time.

**Change:** Cache routing stats with a short TTL (e.g. 30 s). Stats change only when a decision is logged, so 30 s is safe.

| Location | Change |
|----------|--------|
| `modules/joi_router.py` | Add `_routing_stats_cache`, `_routing_stats_ts`, `ROUTING_STATS_CACHE_TTL = 30`. In `_load_routing_stats()`, if cache valid return it; else read file and cache. Where routing stats are **written** (e.g. after logging a decision), invalidate cache (set `_routing_stats_cache = None`) or update it. |

**Expected gain:** **1–3 ms** per request.

---

### 3.2 Learning data and patterns (2 file reads per request)

**Current:** `compile_learning_block()` calls `_load_learning_data()` and `_load_patterns()` — two file reads per request (inside parallel pool).

**Change:** Cache both with a short TTL; invalidate on write.

| Location | Change |
|----------|--------|
| `modules/joi_learning.py` | Add `_learning_data_cache`, `_learning_data_ts`, `_patterns_cache`, `_patterns_ts`, `LEARNING_CACHE_TTL = 45`. In `_load_learning_data()` and `_load_patterns()`, return cached value if age < TTL; else read and update cache. In `_save_learning_data()` and any pattern-save path, invalidate the corresponding cache. |

**Expected gain:** **2–8 ms** per request when learning block is built.

---

### 3.3 Working memory (MemGPT) load

**Current:** `compile_working_memory()` and `update_working_memory()` both call `_load_working_memory()`. The former runs in the context pool; the latter in the background thread. So in one turn we may read the same file twice (once for prompt, once for update).

**Change:** Cache `_load_working_memory()` with a very short TTL (e.g. 5–10 s) or “request-scoped” (e.g. cache for 2 s so the same request’s compile and the following background update can hit cache). Alternatively, in the background `update_working_memory`, pass the in-memory working-memory state from the compile step if it’s still available (more invasive). Simpler: add a 10 s TTL cache in `joi_memgpt._load_working_memory()` and invalidate in `_save_working_memory()`.

| Location | Change |
|----------|--------|
| `modules/joi_memgpt.py` | Add cache for `_load_working_memory()` with TTL 10 s; invalidate in `_save_working_memory()`. |

**Expected gain:** **1–3 ms** when both compile and update run in quick succession.

---

## 4. Cross-Module Call Efficiency

### 4.1 Routing, orchestrator, tools

**Verified:** 
- `classify_task` and `get_routing_decision` are each called **once** per request inside `run_conversation`.
- `select_tools` is called **once** per request; if the model requests a gated tool, **one** fallback rerun with expanded tools is done.
- Orchestrator is not invoked on every message; it’s triggered by keyword detection in `/chat` or by the model calling `orchestrate_task`.

**Change:** None. No over-calling.

---

### 4.2 MemGPT and memory_manager return shape

**Issue:** In `joi_memgpt.compile_working_memory()`, the code does:
`if results and results.get("ok") and results.get("results")` and then iterates `results["results"]`. But `memory_manager.recall_memory()` returns a **list** of dicts, not `{ "ok": True, "results": [...] }`. So the “PAGED-IN MEMORIES” block from MemGPT never gets added.

**Change (correctness, not performance):** In `joi_memgpt.compile_working_memory()`, treat `recall_memory`’s return as a list:
- `results = recall_memory(...)` → list
- Use `if results:` and iterate `results` directly (e.g. `for r in results[:MAX_PAGED_IN]`), using `r.get("text")`, `r.get("score")`, etc.

This fixes behavior and doesn’t change performance.

---

## 5. Lazy Loading, Parallelization, Background

### 5.1 Lazy loading

**Current:** Modules are loaded at startup via `load_modules()`. Tool executors are registered at import. No lazy loading of heavy modules (e.g. browser, vision) in the hot path beyond what’s already done by the tool registry.

**Optional:** For very heavy tools (e.g. Selenium, vision stacks), ensure the **executor** does a lazy import inside the tool function so that the process starts faster. Only do this where startup time is a problem; otherwise keep as-is.

---

### 5.2 Parallelization

**Current:** Context blocks are already parallelized in `_build_context_parallel` (ThreadPoolExecutor, 8 workers). Facts/prefs, vector memory, skill synthesis, personality weights, router, DPO, MemGPT, etc. all run in parallel.

**Remaining:** The only sequential part before the LLM call is: get `recent` (consciousness), then one parallel batch, then goodnight nudge + static blocks. No further parallelization needed for context.

---

### 5.3 Background processing

**Current:** Post-response updates (auto_extract, auto_record_interaction, auto_journal_check, auto_infer_feedback, auto_capture_skill, detect_preference_signal, update_working_memory) already run in a single daemon thread. `update_brain_state` and `get_brain_state` stay in the request path so the response can include `brain_state` and the UI stays correct.

**Change:** None. Keeping `brain_state` and nudge mechanics in the request path is required.

---

## 6. Keeping Responses Fast Without Changing Behavior

- **Do not** move `update_brain_state` or `get_brain_state` to background if the client expects `brain_state` in the same response.
- **Do not** change what is injected into the system prompt (same blocks, same semantics); only change how/when they are computed (cache, batch, parallel).
- **Do not** change nudge logic (e.g. `tick_message`, goodnight trigger, autobiography_nudge in the response).
- **Do not** change routing, tool selection, or verification logic; only optimize the data sources (DB batch, file caches, optional vector batching).

---

## 7. Optional Enhancements for High-Complexity Tasks

### 7.1 Quiet-Star pre-reasoning

**Current:** For **high** complexity, `generate_rationale()` in `joi_quietstar` calls Gemini Flash for a short reasoning pass before the main response, adding latency.

**Optional:** 
- Env flag: `JOI_QUIETSTAR_HIGH=0` to disable the Gemini call for high complexity and use the template-only rationale (like medium), reducing latency at the cost of slightly less “deep” pre-reasoning.
- Or: run the Quiet-Star rationale in a **non-blocking** way (e.g. fire-and-forget or store for next turn) so the first response is faster; this would require a design change (e.g. “thinking” shown on next message) and is not recommended if you want the same UX.

### 7.2 Verification tier

**Current:** For standard/critical tiers, a second model (e.g. Gemini) verifies the reply, adding a full extra LLM round-trip.

**Optional:** Env flag to disable verification for “standard” (e.g. `JOI_VERIFY_STANDARD=0`) so only “critical” is verified, reducing latency for medium-complexity tasks. Behavior change: medium tasks would no longer be verified; only high-risk/critical would.

---

## 8. Summary Table

| Item | Module(s) | Change | Expected gain |
|------|-----------|--------|----------------|
| Facts + prefs batch | joi_memory, joi_companion | `get_preferences_batch()`; use in `_facts_prefs_block` | 5–20 ms |
| Personality weights cache | joi_neuro | 60 s TTL in `load_personality_weights`; invalidate on save | 1–5 ms |
| Router stats cache | joi_router | 30 s TTL in `_load_routing_stats`; invalidate on write | 1–3 ms |
| Learning data/patterns cache | joi_learning | 45 s TTL for `_load_learning_data` and `_load_patterns` | 2–8 ms |
| Skill library/goals/corrections cache | joi_skill_synthesis | 45 s TTL for the three loaders; invalidate on write | 5–15 ms |
| DPO load cache | joi_dpo | 45 s TTL in `_load_dpo`; invalidate on save | 1–5 ms |
| Working memory cache | joi_memgpt | 10 s TTL in `_load_working_memory`; invalidate on save | 1–3 ms |
| MemGPT return shape fix | joi_memgpt | Treat `recall_memory` as list, not `{ok, results}` | Correctness |
| Vector memory batch (optional) | memory_manager / joi_companion | Single multi-namespace query; pass results to blocks | 20–80 ms (if vector slow) |
| Learning summary TTL (optional) | joi_memory | Env `JOI_LEARNING_SUMMARY_TTL` (e.g. 120) | Fewer DB hits |
| Quiet-Star high (optional) | joi_quietstar / env | `JOI_QUIETSTAR_HIGH=0` to skip Gemini for high complexity | 200–500 ms for high-complexity |
| Verify standard (optional) | joi_llm / env | `JOI_VERIFY_STANDARD=0` to skip verification for standard tier | 500 ms–2 s for medium-complexity |

**Total (without optional vector batching / Quiet-Star / verify):** on the order of **15–60 ms** saved per request from batching and file/DB caches, with no change to AI behavior, brain_state, or nudge mechanics.

Implementing the “Summary table” items in order (batch prefs → personality cache → router cache → learning cache → skill cache → DPO cache → working memory cache + MemGPT fix) gives the best effort/benefit ratio first.
