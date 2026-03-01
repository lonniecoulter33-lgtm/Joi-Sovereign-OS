# Project Joi - Bug Tracker

## BUG-1: TypeError in joi_evolution.py (CRITICAL)
**File:** `modules/joi_evolution.py`
**Symptom:** `TypeError: propose_upgrade() got an unexpected keyword argument 'capability'`
**Root cause:** Calling convention mismatch. `joi_llm.py:465` does `tool_executors[fn_name](**fn_args)` but all 6 evolution functions accept `(params: Dict)` instead of `**kwargs`.
**Affected functions:** propose_upgrade, apply_upgrade, monitor_ai_research, analyze_capabilities, list_proposals, get_evolution_stats
**Fix:** Change `params: Dict[str, Any]` to `**params` in all 6 function signatures. Internal `.get()` calls remain valid.

## BUG-2: update_all_market_data() is a no-op (HIGH)
**File:** `modules/joi_market.py:441-445`
**Symptom:** Function declares 4 local variables then implicitly returns None (no loop, no return).
**Root cause:** `create_price_alert()` definition at line 447 is NOT indented inside `update_all_market_data()` — it's a new top-level function that truncates the body. The actual update loop logic (lines 520-554) ended up as unreachable dead code after the `return` in `check_price_alerts()`.
**Impact:** Scheduled market updates silently fail (return None). XRP and all other watchlist data never gets cached to `market_data/` directory.
**Fix:** Move lines 520-554 back into `update_all_market_data()` body, properly indented.

## BUG-3: .env tracked in git
**File:** `.gitignore`
**Issue:** Pattern `.env/` matches directory, not the `.env` file. All API keys are in commit history.
**Fix:** Add `.env` (no trailing slash) to .gitignore, `git rm --cached .env`, rotate all keys.
