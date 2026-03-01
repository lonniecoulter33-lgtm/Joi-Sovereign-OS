"""
Kokoro-82M Local TTS Module
Replaces ElevenLabs with fully local neural speech synthesis.
No API key, no credits, no rate limits.

Model: hexgrad/Kokoro-82M (downloaded automatically on first use from HuggingFace)
Sample rate: 24 000 Hz  |  Output: WAV  |  Voices: 11 built-in
"""

import json
import time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = BASE_DIR / "assets" / "audio"
DATA_DIR  = BASE_DIR / "data"
SETTINGS_PATH = DATA_DIR / "kokoro_settings.json"

# ── Available Kokoro Voices ──────────────────────────────────────────────────
KOKORO_VOICES = {
    "af_heart":    {"label": "Heart",     "desc": "Warm, emotive female",          "lang": "a"},
    "af_bella":    {"label": "Bella",     "desc": "Bright, energetic female",      "lang": "a"},
    "af_nicole":   {"label": "Nicole",    "desc": "Smooth, professional female",   "lang": "a"},
    "af_sarah":    {"label": "Sarah",     "desc": "Clear, articulate female",      "lang": "a"},
    "af_sky":      {"label": "Sky",       "desc": "Airy, breathy female",          "lang": "a"},
    "am_adam":     {"label": "Adam",      "desc": "Deep, resonant male",           "lang": "a"},
    "am_michael":  {"label": "Michael",   "desc": "Natural, conversational male",  "lang": "a"},
    "bf_emma":     {"label": "Emma",      "desc": "Crisp British female",          "lang": "b"},
    "bf_isabella": {"label": "Isabella",  "desc": "Warm British female",           "lang": "b"},
    "bm_george":   {"label": "George",    "desc": "Distinguished British male",    "lang": "b"},
    "bm_lewis":    {"label": "Lewis",     "desc": "Rich British male",             "lang": "b"},
}

DEFAULT_SETTINGS = {
    "voice":         "af_heart",
    "speed":         1.0,
    "temperature":   0.5,
    "voice_prompt":  "Warm, expressive, clear",
    "active_preset": "default",
    "presets": {
        "default": {
            "label":        "Joi Default",
            "voice":        "af_heart",
            "speed":        1.0,
            "temperature":  0.5,
            "voice_prompt": "Warm, expressive, clear",
        }
    },
}

# ── Lazy pipeline cache (one pipeline per lang_code) ─────────────────────────
_pipelines: dict = {}
_have_kokoro: bool | None = None


def _load_settings() -> dict:
    if SETTINGS_PATH.exists():
        try:
            return json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    s = dict(DEFAULT_SETTINGS)
    s["presets"] = {k: dict(v) for k, v in DEFAULT_SETTINGS["presets"].items()}
    return s


def _save_settings(settings: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(settings, indent=2), encoding="utf-8")


def _get_pipeline(lang_code: str = "a"):
    global _have_kokoro
    if _have_kokoro is False:
        return None
    if lang_code in _pipelines:
        return _pipelines[lang_code]
    try:
        import warnings
        warnings.filterwarnings("ignore", message=".*dropout.*LSTM.*")
        warnings.filterwarnings("ignore", message=".*weight_norm is deprecated.*")
        
        from kokoro import KPipeline
        pipe = KPipeline(lang_code=lang_code)
        _pipelines[lang_code] = pipe
        _have_kokoro = True
        print(f"[kokoro] Pipeline ready (lang='{lang_code}')")
        return pipe
    except Exception as exc:
        print(f"[kokoro] Failed to load pipeline: {exc}")
        _have_kokoro = False
        return None


def kokoro_available() -> bool:
    """Return True if Kokoro is installed and importable."""
    global _have_kokoro
    if _have_kokoro is not None:
        return _have_kokoro
    try:
        import kokoro  # noqa: F401
        import soundfile  # noqa: F401
        _have_kokoro = True
        return True
    except ImportError:
        _have_kokoro = False
        return False


def generate_speech_kokoro(
    text: str,
    voice: str | None = None,
    speed: float | None = None,
    temperature: float | None = None,
) -> Path | None:
    """
    Generate speech using Kokoro-82M.

    Args:
        text:        Text to synthesise.
        voice:       Kokoro voice ID (e.g. 'af_heart').  Reads from saved settings if None.
        speed:       Speech speed multiplier (0.5–2.0).  Reads from saved settings if None.
        temperature: Naturalness variation (0.0–1.0).    Reads from saved settings if None.

    Returns:
        Path to generated WAV file, or None on failure.
    """
    try:
        import soundfile as sf
        import numpy as np
    except ImportError:
        print("[kokoro] soundfile / numpy not available — install with: pip install soundfile")
        return None

    settings = _load_settings()
    voice       = voice       if voice       is not None else settings.get("voice",       "af_heart")
    speed       = speed       if speed       is not None else float(settings.get("speed",       1.0))
    temperature = temperature if temperature is not None else float(settings.get("temperature", 0.5))

    # Determine language code from voice ID
    lang_code = KOKORO_VOICES.get(voice, {}).get("lang", "a")
    pipeline  = _get_pipeline(lang_code)
    if pipeline is None:
        return None

    try:
        # Temperature adds subtle speed micro-variation for more natural prosody.
        # Low temp = very consistent; High temp = more expressive.
        effective_speed = speed
        if temperature > 0.3:
            import random
            jitter_range  = (temperature - 0.3) * 0.08
            effective_speed = max(0.5, min(2.0, speed * (1.0 + random.uniform(-jitter_range, jitter_range))))

        audio_chunks = []
        for _gs, _ps, audio in pipeline(text, voice=voice, speed=effective_speed):
            if audio is not None:
                audio_chunks.append(audio)

        if not audio_chunks:
            print("[kokoro] No audio produced")
            return None

        combined = np.concatenate(audio_chunks) if len(audio_chunks) > 1 else audio_chunks[0]

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = AUDIO_DIR / f"tts_{ts}.wav"
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        sf.write(str(audio_file), combined, 24000)
        print(f"[kokoro] {len(combined)/24000:.1f}s audio -> {audio_file.name}")
        return audio_file

    except Exception as exc:
        print(f"[kokoro] TTS error: {exc}")
        return None


# ── Flask Routes ──────────────────────────────────────────────────────────────
import joi_companion
from flask import jsonify, request as flask_req
from modules.joi_memory import require_user


def kokoro_voices_route():
    """GET list of available voices + availability status."""
    require_user()
    voices = [
        {"id": vid, "label": info["label"], "desc": info["desc"], "lang": info["lang"]}
        for vid, info in KOKORO_VOICES.items()
    ]
    return jsonify({"ok": True, "voices": voices, "available": kokoro_available()})


def kokoro_settings_route():
    """GET or POST Kokoro TTS settings + preset management."""
    require_user()

    if flask_req.method == "GET":
        s = _load_settings()
        return jsonify({"ok": True, "settings": s, "available": kokoro_available()})

    data = flask_req.get_json(force=True) or {}
    s = _load_settings()

    # ── Field updates ──────────────────────────────────────────────────────
    for field in ("voice", "speed", "temperature", "voice_prompt", "active_preset"):
        if field in data:
            s[field] = data[field]

    # ── Preset: save current settings as a named preset ───────────────────
    if "save_preset" in data:
        p    = data["save_preset"]
        name = p.get("name", f"preset_{int(time.time())}")
        s.setdefault("presets", {})[name] = {
            "label":        p.get("label", name),
            "voice":        s["voice"],
            "speed":        s["speed"],
            "temperature":  s["temperature"],
            "voice_prompt": s.get("voice_prompt", ""),
        }

    # ── Preset: delete ─────────────────────────────────────────────────────
    if "delete_preset" in data:
        pname = data["delete_preset"]
        if pname != "default":
            s.get("presets", {}).pop(pname, None)

    # ── Preset: load (overwrite current settings from preset) ─────────────
    if "load_preset" in data:
        pname  = data["load_preset"]
        preset = s.get("presets", {}).get(pname)
        if preset:
            s["voice"]        = preset.get("voice",        s["voice"])
            s["speed"]        = preset.get("speed",        s["speed"])
            s["temperature"]  = preset.get("temperature",  s["temperature"])
            s["voice_prompt"] = preset.get("voice_prompt", s.get("voice_prompt", ""))
            s["active_preset"] = pname

    _save_settings(s)
    return jsonify({"ok": True, "settings": s})


joi_companion.register_route("/kokoro/voices",   ["GET"],          kokoro_voices_route,   "kokoro_voices")
joi_companion.register_route("/kokoro/settings",  ["GET", "POST"], kokoro_settings_route, "kokoro_settings")
