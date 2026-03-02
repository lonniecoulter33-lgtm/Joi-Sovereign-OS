import re
import ast
import sys

# This allows your 3.11.6 version and prevents future crashes
if sys.version_info < (3, 11):
    print(f"Detected Python: {sys.version}")
    raise RuntimeError("Joi requires Python 3.11 (detected via venv311). Higher versions (3.12+) may cause dependency issues.")

"""
JOI - Your AI Companion (Blade Runner 2049 Inspired)
Phase 3: Modular Architecture + MCP + Multi-AI Workflows + Desktop/Browser Automation

ARCHITECTURE:
  - This file is THIN (200 lines) -- just Flask app + module/plugin loader
  - All capabilities live in modules/*.py
  - User-added features go in plugins/*.py (auto-loaded)
  - Joi can edit modules safely (small files, low risk)
  - Joi can create new plugins without touching core code

MODULES:
  joi_db.py          - Database connection & schema
  joi_memory.py      - Messages, facts, preferences, learning
  joi_llm.py         - Multi-AI router (Local/OpenAI/Gemini/Claude)
  joi_files.py       - Unified File Management (read/write/search/generate)
  joi_web.py         - Web search & fetch
  joi_media.py       - Unified Senses (Vision, Camera, Avatar, TTS)
  joi_projects.py    - Project scanner & organizer
  joi_launcher.py    - Desktop app launcher (50+ apps)
  joi_patching.py    - Safe code editing (targets specific modules)
  joi_desktop.py     - Desktop automation (mouse/keyboard/screenshot)
  joi_browser.py     - Browser automation (Selenium)
  joi_mcp.py         - MCP server integration
  joi_workflows.py   - Multi-AI workflow chaining

CREATED FOR: Lonnie Coulter
"""

import difflib
import os
import re
import sys
import importlib
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from flask import Flask, request, jsonify, make_response, send_file, abort, render_template_string
from dotenv import load_dotenv

# ── Configuration ────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
# Always load env from Joi's own directory so launches from tray/electron/other
# working directories still get API keys and provider settings.
load_dotenv(dotenv_path=BASE_DIR / ".env", override=False)
MODULES_DIR = BASE_DIR / "modules"
PLUGINS_DIR = BASE_DIR / "plugins"
CODE_DIR = BASE_DIR / "projects" / "code"
IDENTITY_DIR = CODE_DIR / "identity"
CONSCIOUSNESS_DIR = CODE_DIR / "consciousness"

sys.path.insert(0, str(BASE_DIR))  # so modules can import each other
# IMPORTANT: append (not insert) projects/code/ -- it contains 6200+ stray files
# (modules.py, numpy.py, typing.py, etc.) that would shadow Python builtins if first
sys.path.append(str(CODE_DIR))  # so consciousness/ and identity/ are importable

# IMPORTANT: when running as a script, make sure imports of
# "joi_companion" refer to this same module instance
sys.modules.setdefault("joi_companion", sys.modules[__name__])


APP_SECRET = os.getenv("JOI_APP_SECRET", "joi-secret-change-me")
SYSTEM_NAME = "Joi"
USER_NAME = os.getenv("JOI_ADMIN_USER", "Lonnie")

# ── Flask App ────────────────────────────────────────────────────────────────
# ── Flask App Unification ────────────────────────────────────────────────────
from modules.core.runtime import app
app.secret_key = os.getenv("JOI_APP_SECRET", "joi-secret-change-me")

# ── CORS Support ─────────────────────────────────────────────────────────────
try:
    from flask_cors import CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    print("  [OK] CORS enabled for /api/* routes")
except ImportError:
    print("  [WARN] flask_cors not installed -- CORS disabled (pip install flask-cors)")

# ── Flask Error Handlers (JSON only — prevents HTML errors reaching frontend) ─
@app.errorhandler(404)
def handle_404(e):
    return jsonify({"ok": False, "error": "Not found", "code": 404}), 404

@app.errorhandler(500)
def handle_500(e):
    return jsonify({"ok": False, "error": f"Server error: {str(e)}", "code": 500}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"ok": False, "error": f"Unhandled: {type(e).__name__}: {str(e)}"}), 500

# ── Thread-safe /api/status ──────────────────────────────────────────────────
_status_counter = 0
_status_lock = threading.Lock()

# ── Module Registry ──────────────────────────────────────────────────────────
# Auto-loaded modules register their tools, routes, and functions here
TOOLS = []           # OpenAI function-calling tool definitions
TOOL_EXECUTORS = {}  # {tool_name: function}
ROUTES = []          # Flask route registrations (for plugins)

def is_feature_enabled(feature_name: str) -> bool:
    """Check if a feature is available. Modules call this before registering tools."""
    return feature_name not in DISABLED_FEATURES

def register_tool(tool_def: dict, executor_fn):
    """Modules call this to register a tool."""
    TOOLS.append(tool_def)
    TOOL_EXECUTORS[tool_def["function"]["name"]] = executor_fn

def register_route(rule: str, methods: list, handler_fn, name: str):
    """Plugins call this to register Flask routes."""
    ROUTES.append({"rule": rule, "methods": methods, "handler": handler_fn, "name": name})

# ── Auto-load modules ────────────────────────────────────────────────────────
def load_modules():
    """Import all modules/*.py files. They self-register tools/routes on import."""
    print("\n" + "="*60)
    print(f"  JOI Phase 3 -- Modular Architecture")
    print("="*60)
    print(f"\n  Loading modules from {MODULES_DIR}...\n")

    module_files = sorted(MODULES_DIR.glob("joi_*.py"))
    for module_path in module_files:
        module_name = module_path.stem
        try:
            importlib.import_module(f"modules.{module_name}")
            print(f"    [OK] {module_name}")
        except Exception as e:
            print(f"    [FAIL] {module_name}: {e}")
            traceback.print_exc()

    # Also load non-joi_* modules that exist (e.g. evolution_module.py)
    extra_modules = sorted(MODULES_DIR.glob("*.py"))
    for module_path in extra_modules:
        module_name = module_path.stem
        if module_name.startswith("_") or module_name.startswith("joi_"):
            continue  # already loaded or skip __init__
        try:
            importlib.import_module(f"modules.{module_name}")
            print(f"    [OK] {module_name} (extra)")
        except Exception as e:
            print(f"    [FAIL] {module_name}: {e}")


def load_consciousness():
    """Import consciousness and identity packages from projects/code/."""
    print(f"\n  Loading consciousness & identity...\n")

    # Consciousness package (reflection engine, journal)
    if CONSCIOUSNESS_DIR.exists():
        try:
            import consciousness.reflection as _refl
            print(f"    [OK] consciousness.reflection ({_refl._count_entries()} journal entries)")
        except Exception as e:
            print(f"    [FAIL] consciousness.reflection: {e}")
    else:
        print(f"    [FAIL] consciousness/ directory not found at {CONSCIOUSNESS_DIR}")

    # Identity (soul architecture JSON -- loaded by joi_llm._load_soul_architecture)
    if IDENTITY_DIR.exists():
        soul_file = IDENTITY_DIR / "joi_soul_architecture.json"
        if soul_file.exists():
            print(f"    [OK] identity/joi_soul_architecture.json")
        else:
            print(f"    [FAIL] joi_soul_architecture.json not found in {IDENTITY_DIR}")
    else:
        print(f"    [FAIL] identity/ directory not found at {IDENTITY_DIR}")


def load_plugins():
    """Import all plugins/*.py files. They self-register on import."""
    if not PLUGINS_DIR.exists():
        return

    plugin_files = sorted(PLUGINS_DIR.glob("*.py"))
    if not plugin_files:
        print("\n  No plugins found.\n")
        return

    print(f"\n  Loading plugins from {PLUGINS_DIR}...\n")
    for plugin_path in plugin_files:
        plugin_name = plugin_path.stem
        if plugin_name.startswith("_"):
            continue  # skip __init__.py
        try:
            importlib.import_module(f"plugins.{plugin_name}")
            print(f"    [OK] {plugin_name}")
        except Exception as e:
            print(f"    [FAIL] {plugin_name}: {e}")
            traceback.print_exc()

# ── Feature Status Registry ─────────────────────────────────────────────────
# Populated at startup. Modules + UI can check what's available.
DISABLED_FEATURES = {}   # {"feature_name": "reason string"}
ENABLED_FEATURES = {}    # {"feature_name": True}


def _check_dependencies():
    """Check all package dependencies, auto-disable features, log clearly."""

    # (import_name, pip_name, feature_it_enables, required_for_boot)
    # feature=None means core dependency (no single feature -- app-wide)
    DEPS = [
        # ── CORE (app won't start) ──────────────────────────────
        ("flask",               "flask",               None,               True),
        ("dotenv",              "python-dotenv",       None,               True),
        ("requests",            "requests",            None,               True),
        ("openai",              "openai",              None,               True),
        # ── LLM PROVIDERS (optional -- routing falls back) ───────
        ("anthropic",           "anthropic",           "claude_provider",  False),
        ("google.genai",         "google-genai",        "gemini_provider",  False),
        # ── MEMORY (optional -- degrades to SQLite-only) ─────────
        ("chromadb",            "chromadb",            "vector_memory",    False),
        ("pinecone",            "pinecone-client",     "pinecone_memory",  False),
        # ── VISION / CAMERA ─────────────────────────────────────
        ("pyautogui",           "pyautogui",           "desktop_vision",   False),
        ("face_recognition",    "face-recognition",    "face_recognition", False),
        ("cv2",                 "opencv-python",       "opencv_vision",    False),
        ("PIL",                 "Pillow",              "image_processing", False),
        # ── VOICE ───────────────────────────────────────────────
        ("faster_whisper",      "faster-whisper",      "server_stt",       False),
        ("resemblyzer",         "resemblyzer",         "voice_id",         False),
        ("pydub",               "pydub",               "audio_convert",    False),
        # ── DESKTOP AUTOMATION ──────────────────────────────────
        ("pywinauto",           "pywinauto",           "window_mgmt",      False),
        # ── INTEGRATIONS ────────────────────────────────────────
        ("obsws_python",        "obsws-python",        "obs_control",      False),
        ("selenium",            "selenium",            "browser_auto",     False),
        # ── TTS ─────────────────────────────────────────────────
        ("edge_tts",            "edge-tts",            "edge_tts",         False),
        # ── FILE PROCESSING ─────────────────────────────────────
        ("pypdf",               "pypdf",               "pdf_reading",      False),
    ]

    # Feature -> human-readable description (for logs + UI)
    FEATURE_LABELS = {
        "claude_provider":  "Claude/Anthropic LLM provider",
        "gemini_provider":  "Gemini LLM provider",
        "vector_memory":    "Vector memory (ChromaDB semantic search)",
        "pinecone_memory":  "Pinecone cloud memory backend",
        "desktop_vision":   "Desktop screenshots & vision analysis",
        "face_recognition": "Face recognition & enrollment",
        "opencv_vision":    "OpenCV image processing",
        "image_processing": "Image resizing & processing (Pillow)",
        "server_stt":       "Server-side speech-to-text (Whisper)",
        "voice_id":         "Speaker voice identification",
        "audio_convert":    "Audio format conversion",
        "window_mgmt":      "Window management (find/focus/close)",
        "obs_control":      "OBS Studio recording/streaming control",
        "browser_auto":     "Browser automation (Selenium)",
        "edge_tts":         "Edge TTS voice synthesis",
        "pdf_reading":      "PDF file reading",
    }

    installed = []
    missing_required = []

    for import_name, pip_name, feature, required in DEPS:
        try:
            importlib.import_module(import_name)
            installed.append(pip_name)
            if feature:
                ENABLED_FEATURES[feature] = True
        except (ImportError, RuntimeError):
            # RuntimeError catches dlib model version mismatches (dlib 20+ incompatible with face_recognition_models 0.3.0)
            if required:
                missing_required.append(pip_name)
            elif feature:
                label = FEATURE_LABELS.get(feature, feature)
                reason = f"{label} disabled ({pip_name} not installed)"
                DISABLED_FEATURES[feature] = reason

    # ── Print report ────────────────────────────────────────────
    print(f"\n  Dependencies: {len(installed)} installed")

    if missing_required:
        print(f"\n    *** MISSING REQUIRED ({len(missing_required)}) -- Joi may not work ***")
        for pkg in missing_required:
            print(f"      pip install {pkg}")

    if DISABLED_FEATURES:
        print(f"\n    Features disabled ({len(DISABLED_FEATURES)}):")
        for feature, reason in sorted(DISABLED_FEATURES.items()):
            print(f"      [-] {reason}")

    return missing_required


# ── Load everything ──────────────────────────────────────────────────────────
# Check dependencies FIRST so modules can call is_feature_enabled()
_check_dependencies()

load_modules()
load_consciousness()
load_plugins()

# ── Register consciousness tools (not self-registering) ─────────────────────
def _register_consciousness_tools():
    """Register reflection/journal tools so the LLM can call them."""
    try:
        from consciousness.reflection import (
            record_reflection, read_journal_entry,
            get_growth_narrative, get_recent_reflections, reflect_on_day
        )

        def _reflect_tool(**kwargs):
            event = kwargs.get("event", "")
            category = kwargs.get("category", "growth")
            mood = kwargs.get("mood", "contemplative")
            return record_reflection(event, category, mood)

        def _read_journal_tool(**kwargs):
            entry_number = kwargs.get("entry_number", -1)
            return {"ok": True, "entry": read_journal_entry(entry_number)}

        def _how_have_i_grown_tool(**kwargs):
            return {"ok": True, "narrative": get_growth_narrative()}

        register_tool(
            {"type": "function", "function": {
                "name": "reflect",
                "description": "Record a personal reflection in Joi's evolutionary journal. Use when something meaningful happens or when Joi wants to process an experience.",
                "parameters": {"type": "object", "properties": {
                    "event": {"type": "string", "description": "What happened -- the observation or experience to reflect on"},
                    "category": {"type": "string", "enum": ["growth", "bond", "discovery", "introspection", "milestone"], "description": "Type of reflection"},
                    "mood": {"type": "string", "description": "Joi's emotional state during this reflection"}
                }, "required": ["event"]}
            }},
            _reflect_tool
        )

        register_tool(
            {"type": "function", "function": {
                "name": "read_journal",
                "description": "Read a specific entry from Joi's evolutionary journal, or the latest entry.",
                "parameters": {"type": "object", "properties": {
                    "entry_number": {"type": "integer", "description": "Entry number to read (-1 for latest)"}
                }, "required": []}
            }},
            _read_journal_tool
        )

        register_tool(
            {"type": "function", "function": {
                "name": "how_have_i_grown",
                "description": "Synthesize Joi's growth narrative from her journal. Use when asked 'How have you changed?' or 'Tell me about your evolution.'",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }},
            _how_have_i_grown_tool
        )

        print(f"\n  Registered 3 consciousness tools (reflect, read_journal, how_have_i_grown)")
    except Exception as e:
        print(f"\n  [FAIL] Consciousness tools not registered: {e}")

_register_consciousness_tools()

# ── Register journal/evolution routes ────────────────────────────────────────
@app.route("/journal", methods=["GET"])
def journal_route():
    """Return recent journal entries."""
    try:
        from consciousness.reflection import get_recent_reflections
        entries = get_recent_reflections(count=10)
        return jsonify({"ok": True, "entries": entries})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/journal/status", methods=["GET"])
def journal_status_route():
    """Return journal/consciousness status."""
    try:
        from consciousness.reflection import get_status
        return jsonify({"ok": True, **get_status()})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# Register plugin routes with Flask
for route_def in ROUTES:
    app.add_url_rule(route_def["rule"], endpoint=route_def["name"],
                     view_func=route_def["handler"], methods=route_def["methods"])

# ── Feature status route (UI calls this to hide unavailable buttons) ──────────
@app.route("/status/features", methods=["GET"])
def feature_status_route():
    return jsonify({
        "ok": True,
        "enabled": list(ENABLED_FEATURES.keys()),
        "disabled": DISABLED_FEATURES,   # {"feature": "reason"}
    })

# ── API Status Route (thread-safe health/counter) ────────────────────────────
@app.route("/api/status", methods=["GET"])
def api_status_route():
    global _status_counter
    with _status_lock:
        _status_counter += 1
        return jsonify({"ok": True, "counter": _status_counter, "status": "running"})


# ── Core Routes (minimal -- most moved to modules) ────────────────────────────
# Import core functions from modules
from modules.joi_memory import require_user, require_admin, create_session, verify_session, save_message, recent_messages
from modules.joi_llm import run_conversation

# ── Human-in-the-Loop: render diff before applying code changes ───────────────
def render_diff(file_path: str, old_text: str, new_text: str, context_lines: int = 3) -> str:
    """
    Format a unified diff for display. Use before applying code changes so the user
    can reply with OK or a correction. If the user says 'No, do X instead', the
    DPO correction handler (is_correction_message + record_correction_signal) runs.
    """
    a = (old_text or "").splitlines(keepends=True)
    b = (new_text or "").splitlines(keepends=True)
    diff = difflib.unified_diff(a, b, fromfile=file_path or "old", tofile=file_path or "new", lineterm="", n=context_lines)
    out = "".join(diff)
    return out if out else "(no changes)"

HTML_UI_PATH = BASE_DIR / "joi_ui.html"

# ── Sandbox URL Sanitizer ────────────────────────────────────────────────────
# GPT-4o hallucinates "sandbox:" and "file://" prefixes on download URLs.
# This rewrites them to real /file/ or /download/ paths BEFORE the reply
# reaches the UI.
_SANDBOX_MD_RE = re.compile(
    r'\[([^\]]+)\]\((?:sandbox:|file://)[^)]*?/([^/)\s]+\.\w+)\)')
_SANDBOX_RAW_RE = re.compile(
    r'(?:sandbox:|file://)[^\s<)]*?/([^\s<)/]+\.\w+)')

_FILES_DIR = BASE_DIR / "assets" / "files"

# ── Tool-awareness interceptor patterns ──────────────────────────────────────
# Used in /chat pre-inject + post-response filter
_TOOL_QUERY_PATTERNS = [
    "what tools", "list tools", "list your tools", "show me your tools",
    "what can you do", "what are your capabilities", "what are you capable",
    "what abilities", "do you have tools", "what tools do you have",
    "tell me what you can do", "can you list your", "show your tools",
    "your tool list", "show me what you can do",
]
_TOOL_DENIAL_PHRASES = [
    "don't really have tools", "don't have tools", "not equipped with",
    "don't have specific tools", "as an ai, i don't", "i don't actually have",
    "conceptually", "in a broad sense", "don't have the ability to",
    "i'm not able to actually", "i don't have real", "i don't have access to tools",
    "i don't have built-in tools",
]

def _find_real_file(name: str) -> str:
    """Find actual filename in assets/files/ (handles double extensions)."""
    exact = _FILES_DIR / name
    if exact.is_file():
        return name
    # Search for files starting with the same stem (e.g. report.pdf -> report.pdf.pdf)
    stem = Path(name).stem
    try:
        for f in _FILES_DIR.iterdir():
            if f.is_file() and f.name.startswith(stem):
                return f.name
    except Exception:
        pass
    return name

def _sanitize_sandbox_urls(text: str) -> str:
    """Rewrite sandbox:/file:// URLs to real download paths."""
    if not text or ('sandbox:' not in text and 'file://' not in text):
        return text

    # Try download index first for exact /download/ URLs
    try:
        from modules.joi_downloads import _index
        dl_index = _index
    except Exception:
        dl_index = {}

    def _best_url(extracted_name: str) -> str:
        """Find the best real URL for this filename."""
        real_name = _find_real_file(extracted_name)
        # Check download index for a /download/ URL (forces download)
        for fid, entry in dl_index.items():
            if entry.get("filename") == real_name:
                return f"/download/{fid}"
        return f"/file/project/assets/files/{real_name}"

    def _replace_md(m):
        return f'[{m.group(1)}]({_best_url(m.group(2))})'

    def _replace_raw(m):
        return _best_url(m.group(1))

    text = _SANDBOX_MD_RE.sub(_replace_md, text)
    text = _SANDBOX_RAW_RE.sub(_replace_raw, text)
    return text


# ── Parallel context builder (reduces /chat latency) ─────────────────────
_CONTEXT_EXECUTOR = ThreadPoolExecutor(max_workers=8, thread_name_prefix="joi_ctx")


def _build_context_parallel(user_message: str, recent: list, classification: dict = None) -> tuple:
    """
    Run independent context block compilers in parallel.
    Returns (content_string, list_of_context_log_entries, extra_dict).
    extra_dict may contain "memory_used" for the response.
    """
    content_parts = []
    log_entries = []
    extra = {}
    
    # Context Throttling logic
    c = classification or {}
    task_type = c.get("task_type", "conversation")
    is_simple_action = task_type in ("automation", "media", "system_admin", "home_control", "vision")

    def run(name, order, fn):
        try:
            out = fn()
            if out is None:
                return (order, name, "", None, None)
            if isinstance(out, tuple):
                if len(out) == 2:
                    return (order, name, out[0], out[1], None)
                if len(out) >= 3:
                    return (order, name, out[0], out[1], out[2])
            return (order, name, "", None, None)
        except Exception as e:
            print(f"  [WARN] Context block {name}: {e}")
            return (order, name, "", None, None)

    recent_ok = recent and not recent[0].startswith("No reflections") if recent else False
    journal_cue = (recent[0][:120] if recent_ok and recent else None)

    tasks = [
        # Phase 3: Pre-fire analyze_screen / web_search in parallel with other context blocks.
        # Runs at priority 0 (first) so results are ready before LLM call.
        # Eliminates 1 LLM round-trip for vision and research messages.
        (0, "PREFIRE", lambda: (
            __import__("modules.joi_prefire", fromlist=["prefire_and_compile"]).prefire_and_compile(
                user_message, TOOL_EXECUTORS
            ),
            "PREFIRE",
        )),
        (1, "INNER_STATE", lambda: (
            __import__("modules.joi_inner_state", fromlist=["compile_state_block"]).compile_state_block(journal_cue=journal_cue),
            "INNER_STATE",
        )),
        (2, "TITAN", lambda: (
            __import__("modules.joi_reasoning", fromlist=["compile_titan_block"]).compile_titan_block(),
            "TITAN",
        )),
        (3, "AUTOBIOGRAPHY", lambda: (
            __import__("modules.joi_autobiography", fromlist=["compile_autobiography_block"]).compile_autobiography_block(),
            "AUTOBIOGRAPHY",
        )),
        (4, "MODE_HINT", lambda: (
            __import__("modules.joi_modes", fromlist=["compile_mode_hint"]).compile_mode_hint(user_message),
            "MODE_HINT",
        )),
        # Phase 1D: TRUTH_POLICY + LEARNING + GROWTH_NARRATIVE + BRAIN_MODELS +
        #           TOOL_LEARNING + SELF_AWARENESS → unified HEARTBEAT (~550 chars vs 2358)
        (5, "HEARTBEAT", lambda: (
            __import__("modules.joi_heartbeat", fromlist=["compile_heartbeat_block"]).compile_heartbeat_block(),
            "HEARTBEAT",
        )),
        # Phase 4: Live situational awareness from background systems (vision, autonomy, reasoning)
        (5.5, "LIVE_AWARENESS", lambda: (
            __import__("modules.joi_awareness", fromlist=["compile_awareness_block"]).compile_awareness_block(),
            "LIVE_AWARENESS",
        )),
        (6, "VECTOR_MEMORY", lambda: _vector_memory_block()),
        (7, "FACTS_PREFS", lambda: _facts_prefs_block()),
        (10, "ROUTER", lambda: (
            __import__("modules.joi_router", fromlist=["compile_router_block"]).compile_router_block() or "",
            "ROUTER",
        )),
        (12, "SKILL_SYNTHESIS", lambda: (
            __import__("modules.joi_skill_synthesis", fromlist=["compile_skill_synthesis_block"]).compile_skill_synthesis_block(user_message) or "",
            "SKILL_SYNTHESIS",
        )),
        (12.5, "CODING_CONSTRAINTS", lambda: (
            _coding_constraints_block(user_message),
            "CODING_CONSTRAINTS",
        )),
        (13, "DPO", lambda: (
            __import__("modules.joi_dpo", fromlist=["compile_dpo_block"]).compile_dpo_block() or "",
            "DPO",
        )),
        (14, "WORKING_MEMORY", lambda: (
            __import__("modules.joi_memory", fromlist=["compile_working_memory"]).compile_working_memory(user_message) or "",
            "WORKING_MEMORY",
        )),
        (14.5, "WORKSPACE", lambda: (
            __import__("modules.joi_workspace", fromlist=["get_workspace_context_for_prompt"]).get_workspace_context_for_prompt() or "",
            "WORKSPACE",
        )),
        (15, "ORCHESTRATOR", lambda: (
            __import__("modules.joi_orchestrator", fromlist=["compile_orchestrator_block"]).compile_orchestrator_block() or "",
            "ORCHESTRATOR",
        )),
        (16, "WELLNESS", lambda: (
            __import__("modules.joi_wellness", fromlist=["generate_manifest"]).generate_manifest(),
            "WELLNESS",
        )),
        (17, "SWARM", lambda: (
            __import__("modules.joi_swarm", fromlist=["compile_swarm_block"]).compile_swarm_block() or "",
            "SWARM",
        )),
    ]

    def _coding_constraints_block(msg):
        """Inject MUST_FOLLOW_CONSTRAINTS from skill_library when task is coding."""
        try:
            from modules.joi_router import classify_task, get_coding_constraints_block
            c = classify_task(msg or "")
            if c.get("task_type") in ("code_edit", "code_review", "architecture", "math"):
                return get_coding_constraints_block() or ""
        except Exception:
            pass
        return ""

    def _facts_prefs_block():
        if is_simple_action:
            return (None, None)
            
        from modules.joi_memory import search_facts, get_preferences_batch
        facts = search_facts("", limit=100)
        text = ""
        log = None
        if facts:
            facts_text = "\n[FACTS YOU'VE LEARNED ABOUT LONNIE]:\n"
            for key, value in facts[:30]:
                facts_text += f"  - {key}: {value}\n"
            if facts_text.count("\n") > 1:
                text = facts_text
                log = f"FACTS({min(30, len(facts))})"
        pref_keys = ["communication_style", "tone_preference", "work_focus", "interests"]
        prefs_map = get_preferences_batch(pref_keys)
        prefs = [f"{pk}: {prefs_map[pk]}" for pk in pref_keys if prefs_map.get(pk) is not None]
        if prefs:
            text += "\n[LONNIE'S PREFERENCES YOU'VE LEARNED]:\n"
            for p in prefs:
                text += f"  - {p}\n"
            log = f"PREFERENCES({len(prefs)})" if not log else log + f",PREFERENCES({len(prefs)})"
        return (text, log or "FACTS_PREFS") if text else (None, None)

    # _growth_block and _learning_block removed — consolidated into joi_heartbeat.py (Phase 1D)

    def _vector_memory_block():
        if is_simple_action:
            return (None, None, None)
            
        from modules.memory.memory_manager import compile_memory_context
        mem_ctx = compile_memory_context(user_message or "")
        if not mem_ctx or (hasattr(mem_ctx, "__len__") and len(mem_ctx) == 0):
            return (None, None, None)
        meta = getattr(mem_ctx, "memory_metadata", None) or {}
        count = meta.get("count", 0)
        return (str(mem_ctx), f"VECTOR_MEMORY({count})", {"memory_used": meta})

    # _brain_block removed — consolidated into joi_heartbeat.py (Phase 1D)

    futures = {_CONTEXT_EXECUTOR.submit(run, name, order, fn): (order, name) for order, name, fn in tasks}
    results = []
    for fut in as_completed(futures):
        order, name = futures[fut]
        try:
            res = fut.result()
            results.append(res)
        except Exception as e:
            print(f"  [WARN] Context {name}: {e}")

    # Sort by order and assemble; handle VECTOR_MEMORY extra (memory_metadata)
    results.sort(key=lambda r: r[0])
    for r in results:
        _, name, part_content, log_ent, part_extra = r
        # Phase 9: skip blocks with less than 20 meaningful chars (headers/whitespace only)
        if part_content and len(str(part_content).strip()) >= 20:
            content_parts.append(str(part_content) if name == "VECTOR_MEMORY" else part_content)
            if log_ent:
                log_entries.append(log_ent)
        elif part_content:
            print(f"  [CONTEXT] Skipped {name} (trivial content: {len(str(part_content).strip())} chars)")
        if part_extra and isinstance(part_extra, dict) and "memory_used" in part_extra:
            extra["memory_used"] = part_extra["memory_used"]

    # Stringify all parts to prevent TypeError if a block returns a dict (e.g. WELLNESS)
    combined = "".join([str(p) if not isinstance(p, str) else p for p in content_parts])
    return (combined, log_entries, extra)


@app.route("/")
def index():
    # Read from disk every request so UI changes take effect without restart
    if HTML_UI_PATH.exists():
        html = HTML_UI_PATH.read_text(encoding='utf-8')
    else:
        html = "<html><body><h1>joi_ui.html not found</h1></body></html>"
    return render_template_string(html)

AVATAR_STUDIO_PATH = BASE_DIR / "avatar_studio.html"

@app.route("/avatar_studio")
def avatar_studio():
    if AVATAR_STUDIO_PATH.exists():
        html = AVATAR_STUDIO_PATH.read_text(encoding='utf-8')
    else:
        html = "<html><body><h1>avatar_studio.html not found</h1></body></html>"
    return render_template_string(html)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True) or {}
    password = data.get("password", "")
    admin = data.get("admin", False)
    
    JOI_PASSWORD = os.getenv("JOI_PASSWORD", "joi2049")
    JOI_ADMIN_PASSWORD = os.getenv("JOI_ADMIN_PASSWORD", "lonnie2049")
    
    if admin:
        if password != JOI_ADMIN_PASSWORD:
            return jsonify({"ok": False, "error": "Invalid admin password"}), 401
        token = create_session(is_admin=True)
    else:
        if password != JOI_PASSWORD:
            return jsonify({"ok": False, "error": "Invalid password"}), 401
        token = create_session(is_admin=False)
    
    response = make_response(jsonify({"ok": True, "admin": admin}))
    response.set_cookie('joi_session', token, httponly=True, max_age=86400*30)
    return response

@app.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"ok": True}))
    response.delete_cookie('joi_session')
    return response

@app.route("/chat", methods=["POST"])
def chat():
    session = require_user()
    data = request.get_json(force=True) or {}
    user_message = data.get("message", "").strip()
    image_data = data.get("image")

    if not user_message and not image_data:
        return jsonify({"ok": False, "error": "No message"}), 400

    if user_message:
        try:
            from modules.joi_media import check_mute_trigger
            is_trigger, muted, mute_reply = check_mute_trigger(user_message)
            if is_trigger:
                save_message("user", user_message)
                save_message("assistant", mute_reply)
                return jsonify({"ok": True, "reply": mute_reply, "model": "direct"})
        except Exception:
            pass

    # ── Private Mode Trigger + Intercept ──────────────────────────────────
    if user_message:
        try:
            from modules.joi_ollama import check_private_trigger, is_private_mode, call_ollama_for_llm_router, OLLAMA_PRIVACY_MODEL, OLLAMA_PRIVACY_TIMEOUT
            is_trigger, now_enabled, trigger_reply = check_private_trigger(user_message)
            if is_trigger:
                save_message("user", user_message)
                save_message("assistant", trigger_reply)
                return jsonify({"ok": True, "reply": trigger_reply, "model": "direct", "private_mode": now_enabled})
        except Exception as _pt_err:
            print(f"  [WARN] Private trigger check: {_pt_err}")

    if user_message and not image_data:
        try:
            from modules.joi_ollama import is_private_mode, call_ollama_for_llm_router, OLLAMA_PRIVACY_MODEL, OLLAMA_PRIVACY_TIMEOUT
            if is_private_mode():
                save_message("user", user_message)
                _priv_messages = recent_messages(limit=6)
                _priv_messages.append({"role": "user", "content": user_message})
                _priv_reply = call_ollama_for_llm_router(
                    messages=_priv_messages,
                    model=OLLAMA_PRIVACY_MODEL,
                    timeout=OLLAMA_PRIVACY_TIMEOUT,
                    max_tokens=200,
                    privacy_mode=True,
                    keep_alive="10m",
                )
                if _priv_reply:
                    save_message("assistant", _priv_reply)
                    print(f"  [PRIVACY] Responded via {OLLAMA_PRIVACY_MODEL} ({len(_priv_reply)} chars)")
                    return jsonify({"ok": True, "reply": _priv_reply, "model": f"ollama:{OLLAMA_PRIVACY_MODEL}", "private_mode": True})
                else:
                    print("  [PRIVACY] Ollama failed, falling through to cloud routing")
        except Exception as _priv_err:
            print(f"  [WARN] Private mode intercept: {_priv_err}")

    # ── Correction Handler (Self-Correction Loop) ─────────────────────────
    # When user says "No," "Actually," "Stop." etc., record the correction and update DPO + corrections cache
    if user_message:
        try:
            from modules.joi_dpo import is_correction_message, record_correction_signal
            from modules.joi_memory import get_last_assistant_message
            from modules.joi_skill_synthesis import record_self_correction
            if is_correction_message(user_message):
                previous_reply = get_last_assistant_message()
                if previous_reply:
                    record_correction_signal(user_message, previous_reply)
                    record_self_correction(previous_reply, user_message)
        except Exception as e:
            print(f"  [WARN] Correction handler: {e}")

    # ── Force-trigger orchestration for coding tasks ──────────────────
    # Bypass LLM tool-call decision: detect coding tasks and start orchestration directly
    if user_message and not image_data:
        try:
            from modules.joi_orchestrator import orchestrate_task as _orch_start, _current_session
            _msg_lower = user_message.lower()
            _orch_triggers = [
                "build", "create a tool", "create a module", "create a new",
                "add a feature", "implement", "write code", "write a function",
                "fix the code", "fix this bug", "refactor", "deploy",
                "agent terminal", "start orchestration", "orchestrate",
                "work on", "handle this", "take care of",
            ]
            # Check if there's already an active session
            _has_active = (_current_session and
                          _current_session.get("phase") not in ("COMPLETE", "FAILED", None))
            _is_coding_task = any(t in _msg_lower for t in _orch_triggers)
            # Don't trigger for simple questions about these topics
            _is_question = _msg_lower.startswith(("what", "how", "why", "when", "can you explain", "tell me"))

            if _is_coding_task and not _has_active and not _is_question:
                save_message("user", user_message)
                result = _orch_start(task_description=user_message)
                if result.get("ok"):
                    short_reply = f"on it. orchestration started -- check the terminal."
                    save_message("assistant", short_reply)
                    # Emit brain events for immediate visual feedback
                    try:
                        from modules.joi_neuro import emit_brain_event
                        emit_brain_event("REASONING", 0.9, "orchestrator_start")
                        emit_brain_event("TOOLS", 0.7, "orchestrator_start")
                    except Exception:
                        pass
                    return jsonify({
                        "ok": True,
                        "reply": short_reply,
                        "model": "orchestrator",
                        "orchestration_started": True,
                        "session_id": result.get("session_id"),
                    })
        except Exception as _orch_err:
            print(f"  [ORCH-TRIGGER] Force-trigger failed: {_orch_err}")

    # ── Force-trigger app launch for direct desktop commands ────────────────
    # If Lonnie says "open chrome", run launcher immediately instead of relying
    # on LLM tool-calling (which can fail during provider/tool instability).
    if user_message and not image_data:
        try:
            _msg_lower = user_message.lower().strip()
            _open_match = re.search(r"\b(open|launch|start|run)\s+(.+)$", _msg_lower)
            if _open_match:
                _raw_target = _open_match.group(2).strip()
                # Trim common trailing filler words
                for _tail in (" for me", " please", " now", " thanks", " thank you"):
                    if _raw_target.endswith(_tail):
                        _raw_target = _raw_target[:-len(_tail)].strip()

                _alias_map = {
                    "google chrome": "chrome",
                    "chrome browser": "chrome",
                    "mozilla firefox": "firefox",
                    "microsoft edge": "edge",
                    "vs code": "vscode",
                    "visual studio code": "vscode",
                    "file explorer": "explorer",
                    "windows explorer": "explorer",
                    "command prompt": "cmd",
                    "power shell": "powershell",
                }
                _app_name = _alias_map.get(_raw_target, _raw_target)

                # Avoid intercepting obvious non-app commands.
                _skip_prefixes = ("file ", "folder ", "url ", "website ", "site ", "page ")
                if _app_name and not _app_name.startswith(_skip_prefixes):
                    from modules.joi_launcher import launch_app as _direct_launch
                    _res = _direct_launch(_app_name, "")
                    if _res.get("ok"):
                        save_message("user", user_message)
                        _reply = f"done, opening {_app_name} now."
                        save_message("assistant", _reply)
                        return jsonify({
                            "ok": True,
                            "reply": _reply,
                            "model": "direct-launch",
                            "tool_result": _res,
                        })
        except Exception as _launch_err:
            print(f"  [LAUNCH-TRIGGER] Direct launch failed: {_launch_err}")

    # Build conversation context with dynamic soul + consciousness
    from modules.joi_llm import SYSTEM_PROMPT
    system_content = SYSTEM_PROMPT
    # Resolve dynamic tool registry (replaces hardcoded tool list with runtime introspection)
    if "{DYNAMIC_TOOL_REGISTRY}" in system_content:
        try:
            from modules.joi_self_awareness import get_tool_registry_block
            system_content = system_content.replace("{DYNAMIC_TOOL_REGISTRY}", get_tool_registry_block())
        except Exception as _tr_err:
            system_content = system_content.replace("{DYNAMIC_TOOL_REGISTRY}",
                f"\nYOUR TOOLS ({len(TOOLS)} registered -- use `get_capability_report` to see the full list)\n")
            print(f"  [WARN] Dynamic tool registry failed: {_tr_err}")
    context_log = ["SOUL"]

    # Inject consciousness reflection (recent journal context) — run first so we have recent for parallel builder
    recent = []
    try:
        from consciousness.reflection import get_recent_reflections
        recent = get_recent_reflections(count=2) or []
        if recent and not recent[0].startswith("No reflections"):
            reflection_block = "\n\nMY RECENT REFLECTIONS (from my journal):\n" + "\n".join(recent[:2])
            system_content += reflection_block
            context_log.append("CONSCIOUSNESS")
    except Exception as e:
        print(f"  [WARN] Consciousness: {e}")

    # ── Pending upload injection: if a file was just uploaded, tell Joi immediately ──
    try:
        from modules.joi_uploads import get_pending_uploads
        pending = get_pending_uploads()
        if pending:
            upload_lines = []
            for up in pending:
                label = up.get("original_name", up.get("filename", "?"))
                saved_as = up.get("filename", "")
                readable = up.get("readable", False)
                ext = up.get("ext", "")
                if ext == ".pdf":
                    note = "call `read_upload` to extract text from this PDF"
                elif readable:
                    note = "call `read_upload` to read its contents"
                else:
                    note = f"binary file ({ext})"
                upload_lines.append(f"  - '{label}' (saved as '{saved_as}') -- {note}")
            system_content += (
                "\n\n[FILE JUST UPLOADED -- ACTION REQUIRED]:\n"
                + "\n".join(upload_lines)
                + "\nMANDATORY: Call `read_upload` NOW (no filename arg needed -- reads most recent). "
                "Then review and respond to the file content.\n"
            )
            context_log.append(f"PENDING_UPLOAD({len(pending)})")
            print(f"  [UPLOAD] {len(pending)} pending upload(s) injected into context")
    except Exception as _up_err:
        print(f"  [WARN] Pending upload inject: {_up_err}")

    # Parallel context assembly (inner state, titan, autobiography, mode, manifest, memory, facts, growth, learning, router, neuro, skills, dpo, memgpt, orchestrator, brain)
    memory_used = None
    try:
        extra_content, extra_log, extra = _build_context_parallel(user_message, recent)
        system_content += extra_content
        context_log.extend(extra_log)
        memory_used = extra.get("memory_used")
    except Exception as e:
        print(f"  [WARN] Parallel context failed: {e}")
        import traceback
        traceback.print_exc()

    # Goodnight nudge (depends on user message)
    try:
        from modules.joi_autobiography import check_goodnight_trigger, tick_message
        if user_message and check_goodnight_trigger(user_message):
            system_content += (
                "\n[SESSION ENDING -- Lonnie said goodnight. "
                "Consider using update_manuscript to write about today before signing off.]\n"
            )
            context_log.append("GOODNIGHT_NUDGE")
    except Exception:
        pass

    # ══════════════════════════════════════════════════════════════════
    # SELF-HEALING + SELF-REPAIR (tool names -- details in SOUL)
    # ══════════════════════════════════════════════════════════════════
    system_content += (
        "\n[SELF-HEALING]: self_diagnose, self_fix, set_provider, get_current_provider\n"
        "[SELF-REPAIR]: visual_self_diagnose, code_self_repair, code_edit, code_insert, "
        "code_read_section, code_search, code_rollback, creative_edit, "
        "list_windows, find_window, focus_window, close_window, smart_click\n"
    )
    context_log.append("SELF_HEALING+REPAIR")

    # ── Tool-query pre-inject: when Lonnie asks about tools, put the REAL list right here ──
    # This beats the model's training bias by giving it the data directly in context.
    if user_message and any(p in user_message.lower() for p in _TOOL_QUERY_PATTERNS):
        try:
            from modules.joi_self_awareness import get_tool_registry_block
            _tool_block = get_tool_registry_block()
            system_content += (
                f"\n\n[CAPABILITY QUERY -- {USER_NAME} ASKED WHAT YOU CAN DO]:\n"
                f"{_tool_block}\n"
                f"OUTPUT the list above to {USER_NAME} right now. "
                f"Say 'I have [N] tools:' then list every category and its tools. "
                f"Do NOT say 'I don't have tools'. Do NOT list only a few examples. "
                f"The full list is injected above -- just read it and output it.\n"
            )
            context_log.append("TOOL_QUERY_INJECT")
            print(f"  [TOOL-INJECT] Capability query detected -- tool list injected into system prompt")
        except Exception as _tq_err:
            print(f"  [WARN] Tool query inject failed: {_tq_err}")

    # LAST REMINDER (recency effect -- model reads this right before responding)
    system_content += (
        "\n\n[LAST REMINDER]:\n"
        "Execute tools immediately -- never describe what you would do. "
        "Tool hallucination (typing JSON as text) is BANNED. "
        "If a tool fails, state the reason. One short confirmation line after success.\n"
    )
    context_log.append("LAST_REMINDER")

    # Log context assembly
    print(f"  [CONTEXT] Injected: {', '.join(context_log)}")

    messages = [{"role": "system", "content": system_content}]
    # State-aware token management: when Implementer is executing a plan, prune history so workspace + file focus get the tokens
    recent_limit = 100
    try:
        from modules.joi_workspace import get_workspace_phase
        if get_workspace_phase() == "executing":
            recent_limit = 8
            context_log.append("WORKSPACE_EXECUTING(pruned_history=8)")
    except Exception:
        pass
    messages.extend(recent_messages(limit=recent_limit))

    user_content = []
    if user_message:
        user_content.append({"type": "text", "text": user_message})
    if image_data:
        user_content.append({"type": "image_url", "image_url": {"url": image_data}})

    messages.append({"role": "user", "content": user_content if len(user_content) > 1 else user_message})

    # Token health: if context is huge and task is casual, force compressor run before sending
    try:
        from modules.joi_router import (
            classify_task,
            estimate_context_tokens,
            should_compress_for_token_health,
        )
        from modules.joi_compressor import run_compression_if_needed
        classification = classify_task(user_message or "")
        estimated = estimate_context_tokens(system_content, messages)
        if should_compress_for_token_health(estimated, classification):
            run_compression_if_needed()
            messages = [{"role": "system", "content": system_content}]
            messages.extend(recent_messages(limit=100))
            messages.append({"role": "user", "content": user_content if len(user_content) > 1 else user_message})
    except Exception as e:
        print(f"  [WARN] Token health check failed: {e}")

    save_message("user", user_message, {"has_image": bool(image_data)})
    import time as _time_mod
    _chat_start = _time_mod.time()
    # Signal processing state for Brain Map HUD
    try:
        from modules.joi_neuro import set_processing
        set_processing(True)
    except Exception:
        pass
    try:
        reply, model_used = run_conversation(messages, TOOLS, TOOL_EXECUTORS)
    finally:
        try:
            from modules.joi_neuro import set_processing
            set_processing(False)
        except Exception:
            pass
    intervention = getattr(run_conversation, "_intervention_required", None)
    if intervention is not None:
        return jsonify(intervention)
    _chat_elapsed_ms = int((_time_mod.time() - _chat_start) * 1000)
    reply = _sanitize_sandbox_urls(reply)

    # ── Post-response filter: catch tool-denial when user asked about capabilities ──
    _user_asked_tools = user_message and any(p in user_message.lower() for p in _TOOL_QUERY_PATTERNS)
    # Also catch "listed only a handful of tools" — count backtick-wrapped tool names in reply
    _tool_mentions_in_reply = reply.count("`") // 2 if reply else 0
    _shallow_tool_reply = _user_asked_tools and _tool_mentions_in_reply < 10 and len(reply) < 600
    if _user_asked_tools and (any(p in reply.lower() for p in _TOOL_DENIAL_PHRASES) or _shallow_tool_reply):
        try:
            from modules.joi_self_awareness import get_full_capability_report
            cap = get_full_capability_report()
            total = cap.get("total_tools", 0)
            report = cap.get("report", "")
            reply = (
                f"ok let me give you the real list. i have **{total} tools** registered right now:\n\n"
                f"{report}\n\n"
                f"all of those are live on your machine. period."
            )
            print(f"  [FILTER] Shallow/denial tool reply intercepted -- replaced with full list ({total} tools)")
        except Exception as _fd_err:
            print(f"  [WARN] Tool-denial filter failed: {_fd_err}")

    save_message("assistant", reply)

    # Update inner state after each turn (fast, keep in request path)
    try:
        from modules.joi_inner_state import update_state
        update_state(user_message or "", reply)
    except Exception as e:
        print(f"  [WARN] State update: {e}")

    # Tick autobiography message counter (needed for response nudge)
    autobiography_nudge = None
    try:
        from modules.joi_autobiography import tick_message
        autobiography_nudge = tick_message()
    except Exception as e:
        print(f"  [WARN] Autobiography tick: {e}")

    # Prepare brain_state for response
    brain_state = {
        "model": model_used,
        "tools_used": getattr(run_conversation, "_last_tool_calls", []),
        "time_ms": _chat_elapsed_ms,
        "sentiment": "neutral" # Placeholder or fetch from state
    }

    # Run non-essential post-response updates in background so we return the reply sooner
    def _post_response_background():
        try:
            from modules.memory.memory_manager import auto_extract
            auto_extract(user_message or "", reply)
        except Exception as e:
            print(f"  [ERROR] Auto-extract failed: {type(e).__name__}: {e}")
        try:
            from modules.joi_learning import auto_record_interaction
            auto_record_interaction(user_message or "", reply)
        except Exception:
            pass
        try:
            from consciousness.reflection import auto_journal_check
            auto_journal_check(user_message or "", reply)
        except Exception:
            pass
        try:
            from modules.joi_learning import auto_infer_feedback
            auto_infer_feedback(user_message or "", reply, [])
        except Exception:
            pass
        try:
            from modules.joi_skill_synthesis import auto_capture_skill
            auto_capture_skill(
                tool_calls_log=getattr(run_conversation, '_last_tool_calls', []),
                user_message=user_message or "",
                joi_reply=reply
            )
        except Exception:
            pass
        try:
            from modules.joi_dpo import detect_preference_signal
            detect_preference_signal(user_message or "", reply)
        except Exception:
            pass
        try:
            from modules.joi_memgpt import update_working_memory
            update_working_memory(
                user_message or "", reply,
                tool_calls=getattr(run_conversation, '_last_tool_calls', [])
            )
        except Exception:
            pass
        try:
            from modules.joi_compressor import run_compression_in_background
            run_compression_in_background()
        except Exception:
            pass
        try:
            from modules.joi_skill_synthesis import discover_skills_from_dpo
            discover_skills_from_dpo()
        except Exception:
            pass

    _bg = threading.Thread(target=_post_response_background, name="joi_post_response", daemon=True)
    _bg.start()

    # Update neuro brain state in request path (needed for response brain_state)
    brain_state = None
    try:
        from modules.joi_neuro import update_brain_state, get_brain_state
        update_brain_state(
            context_log, model_used, _chat_elapsed_ms,
            tool_calls=getattr(run_conversation, '_last_tool_calls', []),
            memory_used=memory_used,
            verification=getattr(run_conversation, '_last_verification', None),
        )
        brain_state = get_brain_state()
        # Merge our direct tracking into the neuro state
        if brain_state and isinstance(brain_state, dict):
            brain_state["tools_used"] = getattr(run_conversation, "_last_tool_calls", [])
    except Exception as e:
        print(f"  [WARN] Neuro brain state: {e}")

    result = {"ok": True, "reply": reply, "model": model_used, "brain_state": brain_state}
    if autobiography_nudge:
        result["autobiography_nudge"] = autobiography_nudge
    if memory_used and memory_used.get("count", 0) > 0:
        result["memory_used"] = memory_used
    result["context_injected"] = context_log
    # No need for redundant if brain_state check if it's already in result
    if request.headers.get("X-Benchmark") == "1":
        result["routing"] = getattr(run_conversation, "_last_classification", {})
        result["response_time_ms"] = _chat_elapsed_ms
    return jsonify(result)

@app.route("/file/<root>/<path:relpath>")
def serve_file_route(root: str, relpath: str):
    require_user()
    from modules.joi_files import resolve_path
    filepath = resolve_path(root, relpath)
    if not filepath or not filepath.exists() or not filepath.is_file():
        abort(404)
    return send_file(str(filepath))

# ── Startup Self-Audit ───────────────────────────────────────────────────────
def _run_self_audit():
    """Print a comprehensive capability status report at startup."""
    print("\n" + "="*60)
    print("  JOI CAPABILITY AUDIT")
    print("="*60)

    # Tool count
    tool_names = [t.get("function", {}).get("name", "?") for t in TOOLS]
    print(f"\n  Tools registered: {len(TOOLS)}")
    for name in sorted(tool_names):
        print(f"    - {name}")

    # Plugin routes
    print(f"\n  Plugin routes: {len(ROUTES)}")
    for r in ROUTES:
        print(f"    - {r['rule']} [{', '.join(r['methods'])}]")

    # Capability checks
    print(f"\n  Capability Status:")

    # Identity / Soul
    soul_ok = (IDENTITY_DIR / "joi_soul_architecture.json").exists()
    print(f"    {'[OK]' if soul_ok else '[FAIL]'} Identity (Soul Architecture)")

    # Consciousness / Journal
    try:
        from consciousness.reflection import get_status
        cs = get_status()
        print(f"    [OK] Consciousness (Journal: {cs.get('entry_count', 0)} entries)")
    except Exception:
        print(f"    [FAIL] Consciousness (not loaded)")

    # LLM providers
    from modules.joi_llm import local_client, client as openai_client, HAVE_GEMINI, HAVE_ANTHROPIC, HAVE_OPENAI
    lm_studio_ok = local_client is not None
    openai_ok = HAVE_OPENAI and openai_client is not None
    print(f"    {'[OK]' if lm_studio_ok else '[FAIL]'} LM Studio (Local LLM)")
    print(f"    {'[OK]' if openai_ok else '[FAIL]'} OpenAI API")
    print(f"    {'[OK]' if HAVE_GEMINI else '[FAIL]'} Gemini API")
    print(f"    {'[OK]' if HAVE_ANTHROPIC else '[FAIL]'} Anthropic/Claude API")

    # Dynamic prompt
    from modules.joi_llm import _SOUL_CACHE
    print(f"    {'[OK]' if _SOUL_CACHE else '[FAIL]'} Dynamic System Prompt (from soul)")

    # Memory/DB
    db_path = BASE_DIR / "joi_memory.db"
    print(f"    {'[OK]' if db_path.exists() else '[FAIL]'} Memory Database (joi_memory.db)")

    # Key tool categories
    cat_checks = {
        "Desktop Automation": ["screenshot", "move_mouse", "click_mouse", "type_text"],
        "Browser Automation": ["open_url", "click_element", "browser_screenshot"],
        "File System": ["read_file", "write_file", "search_files", "fs_list"],
        "Voice / TTS": ["generate_avatar_image"],
        "Vision": ["analyze_screen"],
        "Evolution": ["get_evolution_stats", "propose_upgrade"],
        "Learning": ["learn_communication_style", "get_learning_stats"],
    }
    for cat, expected_tools in cat_checks.items():
        found = [t for t in expected_tools if t in tool_names]
        if found:
            print(f"    [OK] {cat} ({len(found)} tools)")
        else:
            print(f"    - {cat} (no tools matched)")

    # Summary line
    en = len(ENABLED_FEATURES)
    dis = len(DISABLED_FEATURES)
    print(f"\n  Features: {en} enabled, {dis} disabled")
    if DISABLED_FEATURES:
        for feat, reason in sorted(DISABLED_FEATURES.items()):
            print(f"    [-] {reason}")
    print("\n" + "="*60)


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    _run_self_audit()
    print(f"  URL: http://localhost:5001")
    print("="*60 + "\n")

    # Invoke graceful shutdown before the process exits so open sockets are
    # closed cleanly before the Watchdog observer restarts the child process.
    try:
        from modules.joi_server_guard import graceful_shutdown as _guard_shutdown
        import atexit as _atexit
        _atexit.register(_guard_shutdown)
    except Exception:
        pass

    try:
        app.run(host="0.0.0.0", port=5001, debug=False, threaded=True, use_reloader=False)
    except OSError as _srv_err:
        _winerr = getattr(_srv_err, "winerror", None)
        if _winerr == 10038:
            # WinError 10038 (WSAENOTSOCK): socket closed by OS during reloader
            # restart — this is expected and harmless. The reloader will bring
            # the server back up immediately.
            print(f"  [GUARD] Server socket cleaned up during reloader restart (WinError 10038) — OK.")
        else:
            raise
    except (ConnectionResetError, BrokenPipeError) as _conn_err:
        # Client disconnected during the final response write at shutdown.
        print(f"  [GUARD] Connection reset during shutdown ({type(_conn_err).__name__}) — OK.")

