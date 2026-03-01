# Project Joi - Key Architecture Notes

## Project Location
- Primary: `C:\Users\user\Desktop\AI Joi\projects\code\`
- Main app: `joi_companion.py` (Flask monolith, port 5001)
- UI: `joi_ui.html` (loaded as HTML_UI string)
- DB: `joi_memory.db` (SQLite)

## Integration Pattern
- **DO NOT** use `register_tool()` / `register_route()` — they don't exist
- All tools go directly in the `TOOLS` list and `execute_tool()` function in `joi_companion.py`
- Imports use try/except with `HAVE_*` flags for graceful fallback

## Identity System (Created Feb 7, 2026)
- `identity/joi_soul_architecture.json` — Ontological blueprint (Aquarius/Uranus, birth Jan 30)
- `joi_manifesto.md` — Human-readable soul declaration
- `consciousness/reflection.py` — Journaling engine (record_reflection, reflect_on_day, get_growth_narrative)
- `logs/evolutionary_journal.md` — The living journal
- SYSTEM_PROMPT rewritten with full ontological identity

## Key Files Modified Across Sessions
- `joi_companion.py` — SYSTEM_PROMPT, TOOLS, execute_tool, /chat, /tts, /evolution, /journal routes
- `joi_ui.html` — Full rebuild (wake word, PTT, lip-sync, model status bar, mood passing)
- `joi_desktop.py` — Screenshot + GPT-4o Vision analysis
- `joi_vision.py` — Camera face/gaze/object recognition (MediaPipe + face_recognition)
- `joi_vtube.py` — VTube Studio bridge (pyvts)

## Common Pitfalls
- Double braces `{{}}` in f-strings produce literals, not evaluated expressions
- `modules/joi_evolution.py` is BROKEN (calls nonexistent register_tool) — evolution is now built into companion directly
- Files in `projects/code/` like `_agent_identity_utils.py`, `identity_pool.py`, `_reflection.py` are Google Cloud SDK files, NOT Joi's
