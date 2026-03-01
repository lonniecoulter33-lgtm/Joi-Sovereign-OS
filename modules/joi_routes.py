"""
Additional Flask routes -- research, preferences, history, provider status
"""
from flask import jsonify, request as flask_req
# from modules.joi_auth import require_user (moved to lazy)
from modules.joi_memory import get_preference, set_preference, get_conversation_history
from modules.joi_memory import save_research, get_research, list_research
import json

def get_history():
    from modules.joi_auth import require_user
    require_user()
    limit = int(flask_req.args.get("limit", "100"))
    return jsonify({"ok": True, "history": get_conversation_history(limit)})

def get_preferences():
    from modules.joi_auth import require_user
    require_user()
    from modules.joi_db import db_connect
    conn = db_connect()
    rows = conn.execute("SELECT key, value FROM preferences").fetchall()
    conn.close()
    return jsonify({"ok": True, "preferences": {r["key"]: r["value"] for r in rows}})

def set_preferences():
    from modules.joi_auth import require_user
    require_user()
    data = flask_req.get_json(force=True) or {}
    for k, v in data.items():
        set_preference(k, json.dumps(v))
    return jsonify({"ok": True})

def get_research_list():
    from modules.joi_auth import require_user
    require_user()
    return jsonify({"ok": True, "entries": list_research(flask_req.args.get("category"))})

def get_research_detail(research_id: int):
    from modules.joi_auth import require_user
    require_user()
    entry = get_research(research_id)
    if not entry:
        return jsonify({"ok": False, "error": "Not found"}), 404
    return jsonify({"ok": True, "entry": entry})

def provider_status():
    """Live health check of AI providers (config.joi_models: openai + gemini only)."""
    status = {}
    from modules.joi_llm import client, OPENAI_TOOL_MODEL, HAVE_GEMINI, GEMINI_MODEL, _gemini_client

    if client:
        try:
            client.chat.completions.create(model=OPENAI_TOOL_MODEL,
                messages=[{"role": "user", "content": "ping"}], max_tokens=3)
            status["openai"] = {"ok": True, "model": OPENAI_TOOL_MODEL}
        except Exception as e:
            status["openai"] = {"ok": False, "error": str(e)[:80]}
    else:
        status["openai"] = {"ok": False, "error": "No key"}

    if HAVE_GEMINI and _gemini_client:
        try:
            resp = _gemini_client.models.generate_content(
                model=GEMINI_MODEL, contents="ping",
                config={"max_output_tokens": 50})
            status["gemini"] = {"ok": bool(resp and resp.text), "model": GEMINI_MODEL}
        except Exception as e:
            status["gemini"] = {"ok": False, "error": str(e)[:80]}
    else:
        status["gemini"] = {"ok": False, "error": "No key or SDK"}

    return jsonify({"ok": True, "providers": status})

# Register routes
import joi_companion

joi_companion.register_route("/history", ["GET"], get_history, "get_history")
joi_companion.register_route("/preferences", ["GET"], get_preferences, "get_prefs")
joi_companion.register_route("/preferences", ["POST"], set_preferences, "set_prefs")
joi_companion.register_route("/research", ["GET"], get_research_list, "research_list")
joi_companion.register_route("/research/<int:research_id>", ["GET"], get_research_detail, "research_detail")
joi_companion.register_route("/status", ["GET"], provider_status, "provider_status")
