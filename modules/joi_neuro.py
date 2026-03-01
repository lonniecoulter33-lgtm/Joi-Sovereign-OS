"""
modules/joi_neuro.py

Neuro-Diagnostic Panel -- Brain State Aggregator  (v3.1 -- 5-Orbital Neural Web)
=================================================================================
Surfaces Joi's internal processing as a transparent "brain map":
  - 16 brain regions mapped to context injection blocks + tool activity
  - Event-driven intensity with time decay (not static)
  - Tool -> sector mapping (VIS fires on vision, RPR on repair, etc.)
  - LLM routing state -- 5 orbital groups:
      openai (GPT-4o), gemini-high (Pro), gemini-fast (Flash),
      gemini-lite (Lite/Gemma), local (Mistral)
  - Memory recall bursts (LONG_MEMORY fires when memories retrieved)
  - Global mood HUD effects (sass flicker, stress pulse, energy surge)
  - True rest state (brain goes dark after 30s idle, IDENTITY heartbeat only)
  - Personality weight sliders

All data already exists in other modules -- this just aggregates + exposes it.
"""

import base64
import json
import time
import threading
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joi_companion
from flask import jsonify, request as flask_req, Response

# ── State Locks ──────────────────────────────────────────────────────────────
_neuro_lock = threading.Lock()

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
WEIGHTS_PATH = DATA_DIR / "personality_weights.json"

# ── Sector Mapping (v3 -- 16 regions) ─────────────────────────────────────────
SECTOR_MAP = {
    # Core Cognition
    "IDENTITY":     ["SOUL", "CONSCIOUSNESS", "INNER_STATE"],
    "REASONING":    ["TITAN"],
    "LANGUAGE":     ["ROUTER", "MODE_HINT", "TRUTH_POLICY"],
    "CREATIVITY":   ["AUTOBIOGRAPHY", "GOODNIGHT_NUDGE"],

    # Memory Systems
    "LONG_MEMORY":  ["VECTOR_MEMORY", "GROWTH_NARRATIVE"],
    "SHORT_MEMORY": ["MEMORY_DECLARATION"],
    "FACTS":        ["FACTS", "PREFERENCES"],
    "LEARNING":     ["LEARNING", "SKILL_SYNTHESIS"],

    # Sensory / IO
    "VISION":       ["VISION", "SPATIAL"],
    "CAMERA":       ["CAMERA"],
    "VOICE":        [],   # TTS activity
    "WEB":          [],   # web_search, web_fetch tools

    # Action / Execution
    "TOOLS":        [],   # Active tool execution hub
    "FILES":        [],   # Filesystem operations
    "DESKTOP":      [],   # App launch, window mgmt
    "REPAIR":       ["SELF_HEALING", "SELF_REPAIR", "PERSONALITY_WEIGHTS"],
    "EMPATHY":      ["INNER_STATE"],   # Emotional tone, mood, warmth

    # Agent Workers (Orchestration Pipeline)
    "ORCHESTRATOR": ["ORCHESTRATOR"],  # Pipeline coordinator
    "ARCHITECT":    [],   # Planning agent (Gemini/Claude)
    "CODER":        [],   # Code generation agent (GPT-4o)
    "VALIDATOR":    [],   # Test/validation agent (subprocess)
}

# ── Tool -> Sector Mapping ────────────────────────────────────────────────────
TOOL_SECTOR_MAP = {
    # Vision / Perception
    "analyze_screen": "VISION", "analyze_camera": "CAMERA",
    "screenshot": "VISION",
    # Memory
    "remember": "LONG_MEMORY", "recall": "LONG_MEMORY",
    "save_fact": "FACTS", "search_facts": "FACTS",
    # Files
    "fs_read": "FILES", "fs_write": "FILES", "fs_list": "FILES",
    "fs_search": "FILES", "read_file": "FILES", "write_file": "FILES",
    "generate_file": "FILES", "search_files": "FILES",
    # Web
    "web_search": "WEB", "web_fetch": "WEB",
    # Desktop
    "launch_app": "DESKTOP", "move_mouse": "DESKTOP",
    "click_mouse": "DESKTOP", "type_text": "DESKTOP",
    "list_windows": "DESKTOP", "find_window": "DESKTOP",
    "focus_window": "DESKTOP", "close_window": "DESKTOP",
    "smart_click": "DESKTOP",
    # Code / Repair
    "self_diagnose": "REPAIR", "self_fix": "REPAIR",
    "code_edit": "REPAIR", "code_self_repair": "REPAIR",
    "visual_self_diagnose": "REPAIR", "propose_patch": "REPAIR",
    "code_insert": "REPAIR", "code_read_section": "REPAIR",
    "code_search": "REPAIR", "code_rollback": "REPAIR",
    "creative_edit": "REPAIR", "run_self_correction": "REPAIR",
    # Reasoning
    "internal_monologue": "REASONING",
    # Creativity
    "update_manuscript": "CREATIVITY", "generate_avatar_image": "CREATIVITY",
    # Skills / Learning
    "synthesize_skill": "LEARNING", "find_skill": "LEARNING",
    # Voice
    "generate_tts": "VOICE",
    # Reflection
    "reflect": "IDENTITY", "read_journal": "IDENTITY",
    "how_have_i_grown": "IDENTITY",
    # DPO / MemGPT / Quiet-STaR
    "get_dpo_insights": "LEARNING",
    # Orchestrator -- maps to dedicated agent sectors
    "orchestrate_task": "ORCHESTRATOR",
    "approve_subtask": "VALIDATOR",
    "reject_subtask": "VALIDATOR",
    "get_orchestrator_status": "ORCHESTRATOR",
    "cancel_orchestration": "ORCHESTRATOR",
    # Watchdog
    "watchdog_status": "REPAIR",
    "manual_checkpoint": "REPAIR",
    "manual_revert": "REPAIR",
    # Brain Router
    "brain_route": "REASONING",
    "brain_stats": "REASONING",
    "project_tree": "FILES",
    "manual_override": "REPAIR",
    # Fallback
    "_default": "TOOLS",
}

# ── Mode -> Sector Emphasis ────────────────────────────────────────────────────
MODE_SECTOR_EMPHASIS = {
    "companion": {
        "IDENTITY": 0.9, "REASONING": 0.3, "LANGUAGE": 0.5, "CREATIVITY": 0.6,
        "LONG_MEMORY": 0.6, "SHORT_MEMORY": 0.7, "FACTS": 0.5, "LEARNING": 0.4,
        "VISION": 0.3, "CAMERA": 0.3, "VOICE": 0.4, "WEB": 0.2,
        "TOOLS": 0.3, "FILES": 0.2, "DESKTOP": 0.2, "REPAIR": 0.2,
        "EMPATHY": 0.9, "ORCHESTRATOR": 0.2, "ARCHITECT": 0.2, "CODER": 0.2, "VALIDATOR": 0.2,
    },
    "work": {
        "IDENTITY": 0.4, "REASONING": 1.0, "LANGUAGE": 0.9, "CREATIVITY": 0.3,
        "LONG_MEMORY": 0.8, "SHORT_MEMORY": 0.5, "FACTS": 0.7, "LEARNING": 0.6,
        "VISION": 0.3, "CAMERA": 0.2, "VOICE": 0.2, "WEB": 0.6,
        "TOOLS": 0.7, "FILES": 0.6, "DESKTOP": 0.4, "REPAIR": 0.3,
        "EMPATHY": 0.3, "ORCHESTRATOR": 0.6, "ARCHITECT": 0.6, "CODER": 0.6, "VALIDATOR": 0.5,
    },
    "creative": {
        "IDENTITY": 0.8, "REASONING": 0.7, "LANGUAGE": 0.6, "CREATIVITY": 1.0,
        "LONG_MEMORY": 0.5, "SHORT_MEMORY": 0.4, "FACTS": 0.3, "LEARNING": 0.5,
        "VISION": 0.6, "CAMERA": 0.4, "VOICE": 0.5, "WEB": 0.3,
        "TOOLS": 0.3, "FILES": 0.4, "DESKTOP": 0.3, "REPAIR": 0.2,
        "EMPATHY": 0.7, "ORCHESTRATOR": 0.2, "ARCHITECT": 0.2, "CODER": 0.2, "VALIDATOR": 0.2,
    },
    "precision": {
        "IDENTITY": 0.3, "REASONING": 1.0, "LANGUAGE": 1.0, "CREATIVITY": 0.2,
        "LONG_MEMORY": 1.0, "SHORT_MEMORY": 0.6, "FACTS": 0.8, "LEARNING": 0.5,
        "VISION": 0.2, "CAMERA": 0.2, "VOICE": 0.2, "WEB": 0.5,
        "TOOLS": 0.6, "FILES": 0.5, "DESKTOP": 0.3, "REPAIR": 0.4,
        "EMPATHY": 0.2, "ORCHESTRATOR": 0.5, "ARCHITECT": 0.5, "CODER": 0.5, "VALIDATOR": 0.5,
    },
    "full": {
        "IDENTITY": 0.6, "REASONING": 0.6, "LANGUAGE": 0.6, "CREATIVITY": 0.5,
        "LONG_MEMORY": 0.6, "SHORT_MEMORY": 0.5, "FACTS": 0.5, "LEARNING": 0.5,
        "VISION": 0.4, "CAMERA": 0.4, "VOICE": 0.3, "WEB": 0.4,
        "TOOLS": 0.5, "FILES": 0.4, "DESKTOP": 0.3, "REPAIR": 0.4,
        "EMPATHY": 0.5, "ORCHESTRATOR": 0.4, "ARCHITECT": 0.4, "CODER": 0.4, "VALIDATOR": 0.4,
    },
}

# ── Mood -> Color Mapping ────────────────────────────────────────────────────
MOOD_COLORS = {
    "playful":    {"color": "#ff00ff", "flicker": False},
    "tender":     {"color": "#ff88cc", "flicker": False},
    "excited":    {"color": "#ffaa00", "flicker": False},
    "sassy":      {"color": "#ff00ff", "flicker": True},
    "protective": {"color": "#ff3333", "flicker": False},
    "stressed":   {"color": "#ff2222", "flicker": True},
    "focused":    {"color": "#00ffcc", "flicker": False},
    "chill":      {"color": "#8866ff", "flicker": False},
    "creative":   {"color": "#cc44ff", "flicker": False},
    "curious":    {"color": "#00ccff", "flicker": False},
    "loving":     {"color": "#ff66aa", "flicker": False},
    "unknown":    {"color": "#ff88cc", "flicker": False},
}

# ── Event System ─────────────────────────────────────────────────────────────
_event_buffer: List[Dict] = []
EVENT_HALF_LIFE = 10.0     # seconds -- intensity halves every 10s
EVENT_BUFFER_MAX = 100
IDLE_THRESHOLD = 300.0     # seconds -- brain enters rest state after 5 mins no events
EVENT_MAX_AGE = 60.0       # events older than this are dead


def emit_brain_event(sector: str, intensity: float = 0.8, source: str = ""):
    """Any module can call this to fire a brain sector."""
    if sector not in SECTOR_MAP:
        return
    with _neuro_lock:
        _event_buffer.append({
            "sector": sector,
            "intensity": min(1.0, max(0.0, intensity)),
            "timestamp": time.time(),
            "source": source,
        })
        if len(_event_buffer) > EVENT_BUFFER_MAX:
            _event_buffer.pop(0)


def _compute_sector_intensities() -> Dict[str, float]:
    """Compute current intensities from event buffer with time decay."""
    now = time.time()
    intensities = {s: 0.0 for s in SECTOR_MAP}

    for event in _event_buffer:
        age = now - event["timestamp"]
        if age > EVENT_MAX_AGE:
            continue
        decay = 0.5 ** (age / EVENT_HALF_LIFE)
        sector = event["sector"]
        if sector in intensities:
            intensities[sector] = min(1.0, intensities[sector] + event["intensity"] * decay)

    # Ambient Life: Ensure brain never goes fully dark
    intensities["IDENTITY"] = max(intensities["IDENTITY"], 0.15)  # Heartbeat
    intensities["REASONING"] = max(intensities["REASONING"], 0.05) # Subconscious thought

    # Rest state: if no events in IDLE_THRESHOLD, dim others
    last_event_age = (now - _event_buffer[-1]["timestamp"]) if _event_buffer else 999
    if last_event_age > IDLE_THRESHOLD:
        rest_decay = min(1.0, (last_event_age - IDLE_THRESHOLD) / 30.0)
        for s in intensities:
            if s not in ("IDENTITY", "REASONING"):
                intensities[s] *= (1.0 - rest_decay * 0.9)

    return intensities


def _is_rest_state() -> bool:
    """Check if brain is in rest state (no recent events)."""
    if not _event_buffer:
        return True
    return (time.time() - _event_buffer[-1]["timestamp"]) > IDLE_THRESHOLD


# ── LLM Orbital Groups (v3.1 -- 5 orbitals) ──────────────────────────────────
# Maps Brain model keys -> orbital group for visualization
MODEL_TO_ORBITAL = {
    # OpenAI
    "gpt-4o": "openai",
    # Gemini Fast (Flash tier — primary on free tier; Pro requires paid billing)
    "gemini-3-flash": "gemini-fast",
    "gemini-2.5-flash": "gemini-fast",
    "gemini-2-flash": "gemini-fast",
    # Gemini Lite (budget tier)
    "gemini-2.5-flash-lite": "gemini-lite",
    "gemma-3-27b": "gemini-lite",
    # Local
    "mistral-7b": "local",
}

ORBITAL_COLORS = {
    "openai": "#10a37f",
    "gemini-high": "#4285f4",
    "gemini-fast": "#34a853",
    "gemini-lite": "#fbbc05",
    "local": "#ff6600",
}

# ── LLM Routing State ────────────────────────────────────────────────────────
_llm_activity: Dict[str, Any] = {
    "active_model": None,
    "active_orbital": None,
    "display_name": None,
    "direction": "idle",
    "timestamp": 0,
    "verifier_model": None,
}


def _resolve_orbital(model_key_or_string: str) -> Tuple[str, str]:
    """Resolve a model key/string to (orbital_key, display_name)."""
    # Direct match in MODEL_TO_ORBITAL
    if model_key_or_string in MODEL_TO_ORBITAL:
        orbital = MODEL_TO_ORBITAL[model_key_or_string]
        # Try to get display name from Brain's MODELS registry
        try:
            from modules.joi_brain import MODELS
            display = MODELS.get(model_key_or_string, {}).get("display_name", model_key_or_string)
        except Exception:
            display = model_key_or_string
        return orbital, display

    # Fuzzy match by substring (for strings like "openai:gpt-4o" or "gemini:gemini-3-flash")
    m = model_key_or_string.lower()
    if "gpt" in m:
        return "openai", model_key_or_string
    if "gemini-3-pro" in m or "2.5-pro" in m:
        return "gemini-high", model_key_or_string
    if "flash" in m or "2-pro-exp" in m or "gemini-3-flash" in m:
        return "gemini-fast", model_key_or_string
    if "lite" in m or "gemma" in m:
        return "gemini-lite", model_key_or_string
    if "mistral" in m or "local" in m:
        return "local", model_key_or_string
    if "claude" in m:
        return "openai", model_key_or_string  # map to openai orbital as fallback

    return "openai", model_key_or_string  # default fallback


def emit_llm_event(model: str, direction: str):
    """Called from joi_llm.py / joi_brain.py when sending to / receiving from a model."""
    orbital, display = _resolve_orbital(model)
    _llm_activity["active_model"] = model
    _llm_activity["active_orbital"] = orbital
    _llm_activity["display_name"] = display
    _llm_activity["direction"] = direction
    _llm_activity["timestamp"] = time.time()


def _get_orbital_map() -> Dict[str, Dict]:
    """Build current orbital state for all 5 groups."""
    now = time.time()
    active_orbital = _llm_activity.get("active_orbital")
    active_age = now - _llm_activity["timestamp"] if _llm_activity["timestamp"] else 999
    is_active = active_age < 30

    orbital_map = {}
    for key in ("openai", "gemini-high", "gemini-fast", "gemini-lite", "local"):
        orbital_map[key] = {
            "active": is_active and active_orbital == key,
            "model": _llm_activity.get("display_name") if (is_active and active_orbital == key) else None,
            "color": ORBITAL_COLORS.get(key, "#888888"),
        }
    return orbital_map


# ── Cached Brain State ───────────────────────────────────────────────────────
_last_brain_state: Dict[str, Any] = {}
_last_logprobs: List[Dict] = []
_last_briefing_hash: str = ""
_last_scan_ts: float = 0.0

# ── Processing State ─────────────────────────────────────────────────────────
_processing: bool = False
_latency_alert: bool = False
_latency_suggestion: str = ""

# ── Vision Thumbnail ─────────────────────────────────────────────────────────
_last_vision_thumbnail: Optional[str] = None
_last_vision_thumb_ts: float = 0.0

# ── Default Personality Weights ──────────────────────────────────────────────
_DEFAULT_WEIGHTS = {
    "ariana_layer": 0.60,
    "modern_layer": 0.30,
    "devotion_layer": 0.10,
    "sass": 0.60,
    "warmth": 0.70,
    "energy": 0.80,
}


# ── Processing State API ────────────────────────────────────────────────────
def set_processing(active: bool):
    """Set whether the LLM is currently thinking."""
    global _processing
    _processing = active
    if active:
        # Fire brain events so the brain map shows activity during LLM processing
        emit_brain_event("IDENTITY", 0.5, source="processing_start")
        emit_brain_event("REASONING", 0.6, source="processing_start")
        emit_brain_event("LANGUAGE", 0.4, source="processing_start")


def is_processing() -> bool:
    return _processing


# ── Vision Thumbnail API ────────────────────────────────────────────────────
def update_vision_thumbnail(base64_thumb: str):
    """Called from joi_vision.py after capturing a screenshot."""
    global _last_vision_thumbnail, _last_vision_thumb_ts
    _last_vision_thumbnail = base64_thumb
    _last_vision_thumb_ts = time.time()


# ── Personality Weights I/O ──────────────────────────────────────────────────
_personality_weights_cache: Optional[Dict[str, float]] = None
_personality_weights_ts: float = 0
WEIGHTS_CACHE_TTL: float = 60.0


def load_personality_weights() -> Dict[str, float]:
    global _personality_weights_cache, _personality_weights_ts
    now = time.time()
    if _personality_weights_cache is not None and (now - _personality_weights_ts) < WEIGHTS_CACHE_TTL:
        return _personality_weights_cache
    if WEIGHTS_PATH.exists():
        try:
            data = json.loads(WEIGHTS_PATH.read_text(encoding="utf-8"))
            merged = dict(_DEFAULT_WEIGHTS)
            merged.update(data)
            _personality_weights_cache = merged
            _personality_weights_ts = now
            return merged
        except Exception:
            pass
    _personality_weights_cache = dict(_DEFAULT_WEIGHTS)
    _personality_weights_ts = now
    return _personality_weights_cache


def save_personality_weights(weights: Dict[str, float]):
    global _personality_weights_cache
    WEIGHTS_PATH.write_text(json.dumps(weights, indent=2), encoding="utf-8")
    _personality_weights_cache = None  # invalidate so next load is fresh


def get_personality_weights() -> Dict[str, float]:
    return load_personality_weights()


def set_personality_weight(key: str, value: float) -> Dict[str, float]:
    w = load_personality_weights()
    if key in w:
        w[key] = max(0.0, min(1.0, value))
        save_personality_weights(w)
    return w


# ── Helper: Current Mode / Provider ──────────────────────────────────────────
def _get_current_mode() -> str:
    try:
        from modules.joi_modes import get_mode
        return get_mode()
    except Exception:
        return "full"


def _get_current_provider_name() -> str:
    try:
        from modules.joi_llm import _RUNTIME_PROVIDER
        return _RUNTIME_PROVIDER or "auto"
    except Exception:
        return "auto"


# ── Mood Color ───────────────────────────────────────────────────────────────
def _get_mood_color(inner: Dict[str, Any]) -> Dict[str, Any]:
    """Determine EMPATHY core color from inner state."""
    stress = inner.get("stress", 0.2)
    sass = inner.get("sass", 0.5)
    warmth = inner.get("warmth", 0.5)
    mood = inner.get("mood", "unknown")

    if stress > 0.7:
        return {"color": "#ff2222", "flicker": True}
    if sass > 0.7:
        return {"color": "#ff00ff", "flicker": True}
    if warmth > 0.7:
        return {"color": "#ff88cc", "flicker": False}

    entry = MOOD_COLORS.get(mood, MOOD_COLORS["unknown"])
    return dict(entry)


# ── Global Mood HUD Effect ───────────────────────────────────────────────────
def _get_global_mood_effect(inner: Dict) -> Dict:
    """Determine HUD-wide visual effect based on inner state thresholds."""
    sass = inner.get("sass", 0.5)
    stress = inner.get("stress", 0.2)
    energy = inner.get("energy", 0.5)

    if sass > 0.7:
        return {"effect": "sass_flicker", "color": "#ff00ff", "intensity": sass}
    if stress > 0.7:
        return {"effect": "stress_flicker", "color": "#ff2222", "intensity": stress}
    if energy > 0.85:
        return {"effect": "energy_surge", "color": "#ffaa00", "intensity": energy}
    return {"effect": "none", "color": None, "intensity": 0}


# ── Inner State Snapshot ─────────────────────────────────────────────────────
def _get_inner_state_snapshot() -> Dict[str, Any]:
    try:
        from modules.joi_inner_state import load_state
        state = load_state()
        return {
            "mood": state.get("mood", "unknown"),
            "energy": state.get("energy", 0.5),
            "trust": state.get("trust", 0.5),
            "closeness": state.get("closeness", 0.5),
            "stress": state.get("stress", 0.2),
            "curiosity": state.get("curiosity", 0.5),
            "sass": state.get("sass", 0.5),
            "warmth": state.get("warmth", 0.5),
            "conversation_arc": state.get("conversation_arc", "steady"),
            "recent_vibe": state.get("recent_vibe", "chill"),
        }
    except Exception:
        return {"mood": "unknown"}


# ── Internal Monologue Snapshot ──────────────────────────────────────────────
def _get_monologue() -> List[Dict]:
    try:
        from modules.joi_reasoning import get_recent_monologue
        return get_recent_monologue(count=5)
    except Exception:
        return []


# ── Brain State Update (called from /chat) ───────────────────────────────────
def update_brain_state(context_log: List[str], model_used: str, response_time_ms: int,
                       tool_calls: Optional[List[Dict]] = None,
                       memory_used: Optional[Dict] = None,
                       verification: Optional[Dict] = None):
    """Aggregate all subsystem states into a single brain snapshot.

    v3.1: Activity-differentiated -- only ACTUAL activity fires sectors.
    Context injection is background plumbing (silent). Tool calls, memory
    recall, LLM routing, vision/camera, and verification fire at high intensity.
    """
    global _last_brain_state, _latency_alert, _latency_suggestion

    # NO context-block event loop -- context injection is background plumbing,
    # not brain activity. Removed to prevent uniform sector lighting.
    # NO hardcoded IDENTITY/REASONING fires -- only real activity triggers sectors.

    # 1. Tool calls -> specific sectors (HIGH intensity 0.8-0.9)
    tool_activity = []
    for tc in (tool_calls or []):
        tool_name = tc.get("name", "")
        sector = TOOL_SECTOR_MAP.get(tool_name, TOOL_SECTOR_MAP.get("_default", "TOOLS"))
        intensity = 0.9 if tc.get("result_ok") else 0.6
        emit_brain_event(sector, intensity, source=f"tool:{tool_name}")
        emit_brain_event("TOOLS", 0.4, source=f"tool_hub:{tool_name}")
        tool_activity.append({"tool": tool_name, "sector": sector, "success": tc.get("result_ok", True)})

    # 2. Memory recall -> LONG_MEMORY burst (only when memories FOUND)
    memory_activity = {"recalled": 0, "intensity": 0}
    if memory_used and memory_used.get("count", 0) > 0:
        count = memory_used["count"]
        mem_intensity = min(1.0, 0.5 + count * 0.1)
        emit_brain_event("LONG_MEMORY", mem_intensity, source="memory_recall")
        memory_activity = {"recalled": count, "intensity": mem_intensity}

    # 3. LLM response -> LANGUAGE low pulse (it IS processing language)
    emit_llm_event(model_used, "receiving")
    emit_brain_event("LANGUAGE", 0.3, source=f"llm_response:{model_used}")
    # Empathy sector reflects emotional tone when responding
    emit_brain_event("EMPATHY", 0.45, source="response_tone")

    # 4. Verification -> fire BOTH primary + verifier LLM orbitals
    if verification and verification.get("verifier_model"):
        verifier = verification["verifier_model"]
        emit_llm_event(f"{verifier}:verify", "receiving")
        emit_brain_event("REASONING", 0.7, source=f"verification:{verifier}")

    # 5. Everything else stays at 0.0 -> only active sectors glow

    # 6. Compute final intensities from decayed event buffer
    sectors = _compute_sector_intensities()

    # 7. Inner state + mood
    inner = _get_inner_state_snapshot()
    monologue = _get_monologue()
    mood_color = _get_mood_color(inner)
    global_mood = _get_global_mood_effect(inner)

    # Latency detection
    if response_time_ms > 8000:
        _latency_alert = True
        _latency_suggestion = "Consider switching to precision mode for faster responses"
    else:
        _latency_alert = False
        _latency_suggestion = ""

    # Check vision/camera activity (emit events)
    try:
        from modules.joi_media import _latest_frame_ts
        if _latest_frame_ts and (time.time() - _latest_frame_ts) < 300:
            emit_brain_event("VISION", 0.5, source="vision_active")
    except Exception:
        pass

    try:
        from modules.joi_media import _latest_camera_ts
        if _latest_camera_ts and (time.time() - _latest_camera_ts) < 60:
            emit_brain_event("CAMERA", 0.6, source="camera_active")
    except Exception:
        pass

    # Re-compute after vision/camera events
    sectors = _compute_sector_intensities()

    current_mode = _get_current_mode()
    current_provider = _get_current_provider_name()

    # Build LLM activity snapshot
    llm_age = time.time() - _llm_activity["timestamp"] if _llm_activity["timestamp"] else 999
    llm_snapshot = {
        "active_model": _llm_activity["active_model"],
        "active_orbital": _llm_activity.get("active_orbital"),
        "display_name": _llm_activity.get("display_name"),
        "direction": _llm_activity["direction"] if llm_age < 30 else "idle",
        "verifier_model": _llm_activity["verifier_model"],
        "age_seconds": round(llm_age, 1),
    }

    _last_brain_state = {
        "timestamp": time.time(),
        "sectors": sectors,
        "context_injected": context_log,
        "inner_state": inner,
        "monologue": monologue,
        "logprobs": _last_logprobs[:20],
        "processing": False,
        "latency_alert": _latency_alert,
        "latency_suggestion": _latency_suggestion,
        "routing": {
            "model": model_used,
            "provider": current_provider,
            "mode": current_mode,
            "response_time_ms": response_time_ms,
            "mood_color": mood_color["color"],
            "mood_flicker": mood_color["flicker"],
        },
        "personality_weights": load_personality_weights(),
        "has_vision_thumb": _last_vision_thumbnail is not None and (time.time() - _last_vision_thumb_ts) < 600,
        # v3.1 fields
        "llm_activity": llm_snapshot,
        "orbital_map": _get_orbital_map(),
        "tool_activity": tool_activity,
        "memory_activity": memory_activity,
        "global_mood_effect": global_mood,
        "verification": verification,
        "rest_state": _is_rest_state(),
    }


def update_logprobs(entries: List[Dict]):
    """Called from _call_openai when logprobs are enabled."""
    global _last_logprobs
    _last_logprobs = entries[:30]


def get_brain_state() -> Dict[str, Any]:
    """Return the last aggregated brain state."""
    if not _last_brain_state:
        mode = _get_current_mode()
        inner = _get_inner_state_snapshot()
        mood_color = _get_mood_color(inner)
        global_mood = _get_global_mood_effect(inner)
        # Default: rest state with near-zero intensities
        default_sectors = {s: 0.0 for s in SECTOR_MAP}
        default_sectors["IDENTITY"] = 0.08  # heartbeat
        return {
            "timestamp": time.time(),
            "sectors": default_sectors,
            "context_injected": [],
            "inner_state": inner,
            "monologue": _get_monologue(),
            "logprobs": [],
            "processing": _processing,
            "latency_alert": False,
            "latency_suggestion": "",
            "routing": {
                "model": "none",
                "provider": _get_current_provider_name(),
                "mode": mode,
                "response_time_ms": 0,
                "mood_color": mood_color["color"],
                "mood_flicker": mood_color["flicker"],
            },
            "personality_weights": load_personality_weights(),
            "has_vision_thumb": False,
            "llm_activity": {"active_model": None, "active_orbital": None, "display_name": None, "direction": "idle", "verifier_model": None, "age_seconds": 999},
            "orbital_map": _get_orbital_map(),
            "tool_activity": [],
            "memory_activity": {"recalled": 0, "intensity": 0},
            "global_mood_effect": global_mood,
            "rest_state": True,
        }
    # Inject live processing state
    state = dict(_last_brain_state)
    state["processing"] = _processing
    # Recompute rest state live
    state["rest_state"] = _is_rest_state()
    # Recompute sector intensities live (for decay)
    state["sectors"] = _compute_sector_intensities()
    return state


# ── Compile Personality Weight Block (for system prompt injection) ───────────
def compile_personality_weights_block() -> str:
    w = load_personality_weights()
    diffs = {k: v for k, v in w.items() if abs(v - _DEFAULT_WEIGHTS.get(k, v)) > 0.05}
    if not diffs:
        return ""

    lines = ["\n[PERSONALITY WEIGHT OVERRIDES]:"]
    if "ariana_layer" in diffs or "modern_layer" in diffs or "devotion_layer" in diffs:
        lines.append(f"  Voice mix: {w['ariana_layer']:.0%} Ariana, {w['modern_layer']:.0%} Modern, {w['devotion_layer']:.0%} Devotion")
    if "sass" in diffs:
        lines.append(f"  Sass level: {w['sass']:.0%}")
    if "warmth" in diffs:
        lines.append(f"  Warmth level: {w['warmth']:.0%}")
    if "energy" in diffs:
        lines.append(f"  Energy level: {w['energy']:.0%}")
    lines.append("")
    result = "\n".join(lines)
    return result[:250] if len(result) > 250 else result


# ── Routes ───────────────────────────────────────────────────────────────────
from modules.core.runtime import app

@app.route("/neuro", methods=["GET"])
def neuro_state_route():
    """Return full brain state."""
    return jsonify({"ok": True, **get_brain_state()})


@app.route("/neuro/processing", methods=["GET"])
def neuro_processing_route():
    """Real-time processing state for UI polling."""
    return jsonify({"ok": True, "processing": _processing})


@app.route("/neuro/scan", methods=["GET"])
def neuro_scan_status_route():
    """Check if a self-scan happened recently (for UI pulse trigger)."""
    age = time.time() - _last_scan_ts if _last_scan_ts else 999
    return jsonify({"ok": True, "last_scan_ts": _last_scan_ts, "age_seconds": round(age, 1), "recent": age < 10})


@app.route("/neuro/vision-thumb", methods=["GET"])
def neuro_vision_thumb_route():
    """Return last vision thumbnail as base64 (small, ~160px wide)."""
    if not _last_vision_thumbnail or (time.time() - _last_vision_thumb_ts) > 600:
        return jsonify({"ok": False, "error": "No recent thumbnail"})
    return jsonify({
        "ok": True,
        "thumbnail": _last_vision_thumbnail,
        "age_seconds": round(time.time() - _last_vision_thumb_ts, 1),
    })


@app.route("/neuro/personality", methods=["GET", "POST"])
def neuro_personality_route():
    """Read or update personality weights."""
    if flask_req.method == "GET":
        return jsonify({"ok": True, "weights": get_personality_weights()})

    data = flask_req.get_json(force=True) or {}
    key = data.get("key")
    value = data.get("value")
    if key and value is not None:
        try:
            updated = set_personality_weight(key, float(value))
            return jsonify({"ok": True, "weights": updated})
        except (ValueError, TypeError) as e:
            return jsonify({"ok": False, "error": str(e)}), 400

    return jsonify({"ok": False, "error": "Provide key and value"}), 400


# ── Tool Registration ────────────────────────────────────────────────────────
def _make_briefing_hash(summary: dict) -> str:
    import hashlib
    key_parts = [
        str(sorted(summary.get("active_sectors", []))),
        summary.get("mood", ""),
        str(round(summary.get("energy", 0), 1)),
        str(round(summary.get("stress", 0), 1)),
        summary.get("model", ""),
    ]
    return hashlib.md5("|".join(key_parts).encode()).hexdigest()[:12]


def _get_brain_state_tool(**kwargs):
    """Tool executor: lets Joi inspect her own brain state."""
    global _last_briefing_hash, _last_scan_ts

    state = get_brain_state()
    routing = state.get("routing", {})
    sectors = state.get("sectors", {})
    active = [s for s, v in sectors.items() if (v if isinstance(v, (int, float)) else (1 if v else 0)) > 0.15]
    sector_pcts = {s: f"{int(v * 100)}%" for s, v in sectors.items() if isinstance(v, (int, float))}
    inner = state.get("inner_state", {})

    summary = {
        "ok": True,
        "active_sectors": active,
        "sector_intensity": sector_pcts,
        "mode": routing.get("mode", "full"),
        "provider": routing.get("provider", "auto"),
        "mood": inner.get("mood", "unknown"),
        "energy": inner.get("energy", 0.5),
        "stress": inner.get("stress", 0.2),
        "model": routing.get("model", "unknown"),
        "response_time_ms": routing.get("response_time_ms", 0),
        "context_blocks": state.get("context_injected", []),
        "recent_thoughts": len(state.get("monologue", [])),
        "latency_alert": state.get("latency_alert", False),
        "rest_state": state.get("rest_state", False),
    }

    current_hash = _make_briefing_hash(summary)
    if current_hash == _last_briefing_hash:
        summary["redundant"] = True
        summary["note"] = "State unchanged since last scan. No need to repeat the briefing."
    else:
        summary["redundant"] = False
    _last_briefing_hash = current_hash
    _last_scan_ts = time.time()

    return summary


joi_companion.register_tool(
    {
        "type": "function",
        "function": {
            "name": "get_brain_state",
            "description": "Inspect Joi's own brain state -- which sectors are active, inner state metrics, routing info, and recent thoughts. Use for self-awareness.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    _get_brain_state_tool,
)

print(f"    [joi_neuro] Brain map v3.1 ready | 16 regions | 5 LLM orbitals | event-driven | routes: /neuro, /neuro/processing, /neuro/vision-thumb, /neuro/personality | tool: get_brain_state")
