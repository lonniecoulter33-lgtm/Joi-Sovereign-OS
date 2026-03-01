# Project Joi - Key Learnings

## Architecture
- Thin Flask orchestrator (`joi_companion.py`) + 24 self-registering modules in `modules/`
- Electron desktop shell (`main.js`) wrapping Flask on port 5001
- Tool executor in `joi_llm.py:465` calls tools with `**fn_args` (keyword expansion)
- Modules register tools via `joi_companion.register_tool(tool_def, executor_fn)`
- Plugins in `plugins/` auto-loaded by `load_plugins()` (needs `__init__.py`)
- Blueprint registration works from plugins via `joi_companion.app.register_blueprint()`

## Fixed Bugs (2026-02-06)
- `joi_evolution.py`: Changed 6 functions from `(params: Dict)` to `(**params)` - fixes TypeError
- `joi_market.py`: Restored `update_all_market_data()` loop body; removed orphaned dead code
- `joi_llm.py`: Added missing `"""` docstring delimiters around file header (lines 1-21)
- **Batch fix**: Changed 16 functions across 7 modules from `(params: Dict)` to `(**params)`:
  - `joi_diagnostics.py` (1), `joi_code_analyzer.py` (1), `joi_learning.py` (5),
  - `joi_file_output.py` (5), `joi_scheduler.py` (2), `joi_supervisor .py` (1), `joi_search.py` (1)
  - Also fixed all route handler call sites from `func(data)` to `func(**data)`
  - Also fixed cross-module call: supervisor's `run_system_diagnostic({})` → `run_system_diagnostic()`
- Activity logging hooks added to `joi_llm.py` (4 API providers) and `joi_filesystem.py` (3 file ops)
- See [bugs.md](bugs.md) for detailed tracking
- **Zero** `(params: Dict)` signatures remain in modules/

## Remaining Issues
- `.env` is tracked in git (`.gitignore` has `.env/` directory pattern, not `.env` file)
- `host="0.0.0.0"` in joi_companion.py exposes Flask to LAN
- `joi_supervisor .py` has trailing space in filename
- Overlapping file modules: `joi_filesystem.py`, `joi_file_output.py`, `joi_files.py`

## New Components (2026-02-06)
- `plugins/claude_code_delegate.py` - Claude Code CLI delegation (3 tools registered)
- `plugins/system_monitor_dashboard.py` - System monitor with Flask Blueprint at /monitor
- `templates/monitor_dashboard.html` - Dashboard UI with Chart.js
- `config/claude_code.json` - Delegation settings
- Dashboard URL: http://localhost:5001/monitor

## API Status
- CoinGecko: Working for XRP ("ripple" coin_id), returns price/history
- Finnhub/TwelveData: Configured via env vars, not independently verified

## Environment
- Use Python 3.12 venv: `venv312\Scripts\python.exe`
- Python 3.14 (system) has encoding issues with Unicode in print statements
- Always use `-X utf8` flag when testing via CLI
