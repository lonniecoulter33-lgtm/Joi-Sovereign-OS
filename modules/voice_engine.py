"""
modules/voice_engine.py

Description-to-Voice Middleware for Kokoro AI
================================================
Converts a plain-text description (e.g. "warm, deep, slow, British") into
an optimal set of Kokoro voice parameters:  voice ID, speed, temperature.

Public API
----------
  describe_to_voice(description: str) -> dict
      Returns {voice, speed, temperature, voice_prompt, description, matched_tags, scores}

Flask route
-----------
  POST /kokoro/voice_from_desc   {"description": "..."}
  -> {ok: True, profile: {...}}
"""

from __future__ import annotations

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Path helpers (shared with joi_tts_kokoro)
# ---------------------------------------------------------------------------
BASE_DIR      = Path(__file__).resolve().parent.parent
DATA_DIR      = BASE_DIR / "data"
SETTINGS_PATH = DATA_DIR / "kokoro_settings.json"

# ---------------------------------------------------------------------------
# Known Kokoro voices (mirrors joi_tts_kokoro.KOKORO_VOICES)
# ---------------------------------------------------------------------------
ALL_VOICES = [
    "af_heart",    # Warm, emotive female
    "af_bella",    # Bright, energetic female
    "af_nicole",   # Smooth, professional female
    "af_sarah",    # Clear, articulate female
    "af_sky",      # Airy, breathy female
    "am_adam",     # Deep, resonant male
    "am_michael",  # Natural, conversational male
    "bf_emma",     # Crisp British female
    "bf_isabella", # Warm British female
    "bm_george",   # Distinguished British male
    "bm_lewis",    # Rich British male
]

# ---------------------------------------------------------------------------
# TAGGING LIBRARY
# ---------------------------------------------------------------------------
# Each entry maps a keyword -> {voice_scores, speed_delta, temp_delta}
#
#   voice_scores: dict[voice_id -> float]   (additive; higher = better match)
#   speed_delta:  float   applied to base speed 1.0  (+/- 0.0–0.4)
#   temp_delta:   float   applied to base temp  0.5  (+/- 0.0–0.4)
# ---------------------------------------------------------------------------

VOICE_TAGS: Dict[str, dict] = {

    # ── Warmth ──────────────────────────────────────────────────────────────
    "warm": {
        "voice_scores": {"af_heart": 1.0, "bf_isabella": 0.85, "af_nicole": 0.6},
        "speed_delta": -0.05,
        "temp_delta":   0.05,
    },
    "cozy": {
        "voice_scores": {"af_heart": 0.9, "bf_isabella": 0.8, "af_nicole": 0.5},
        "speed_delta": -0.08,
        "temp_delta":   0.05,
    },
    "comforting": {
        "voice_scores": {"af_heart": 1.0, "bf_isabella": 0.75, "af_nicole": 0.55},
        "speed_delta": -0.1,
        "temp_delta":  -0.05,
    },

    # ── Brightness / Energy ──────────────────────────────────────────────────
    "bright": {
        "voice_scores": {"af_bella": 1.0, "af_sarah": 0.6, "bf_emma": 0.55},
        "speed_delta":  0.1,
        "temp_delta":   0.1,
    },
    "energetic": {
        "voice_scores": {"af_bella": 1.0, "af_sarah": 0.7, "af_sky": 0.5},
        "speed_delta":  0.15,
        "temp_delta":   0.15,
    },
    "lively": {
        "voice_scores": {"af_bella": 0.9, "af_sky": 0.65, "af_sarah": 0.55},
        "speed_delta":  0.12,
        "temp_delta":   0.12,
    },
    "peppy": {
        "voice_scores": {"af_bella": 1.0, "af_sky": 0.6},
        "speed_delta":  0.18,
        "temp_delta":   0.15,
    },

    # ── Airiness / Breathiness ───────────────────────────────────────────────
    "airy": {
        "voice_scores": {"af_sky": 1.0, "af_bella": 0.5},
        "speed_delta":  0.0,
        "temp_delta":   0.1,
    },
    "breathy": {
        "voice_scores": {"af_sky": 1.0, "af_heart": 0.45},
        "speed_delta": -0.05,
        "temp_delta":   0.1,
    },
    "whispery": {
        "voice_scores": {"af_sky": 0.95, "af_heart": 0.6},
        "speed_delta": -0.12,
        "temp_delta":   0.08,
    },

    # ── Depth / Resonance ────────────────────────────────────────────────────
    "deep": {
        "voice_scores": {"am_adam": 1.0, "bm_george": 0.85, "bm_lewis": 0.8},
        "speed_delta": -0.05,
        "temp_delta":  -0.05,
    },
    "resonant": {
        "voice_scores": {"am_adam": 1.0, "bm_george": 0.9},
        "speed_delta": -0.05,
        "temp_delta":  -0.08,
    },
    "booming": {
        "voice_scores": {"am_adam": 1.0, "bm_george": 0.7},
        "speed_delta": -0.08,
        "temp_delta":  -0.1,
    },
    "rich": {
        "voice_scores": {"bm_lewis": 1.0, "am_adam": 0.75, "bm_george": 0.7},
        "speed_delta": -0.05,
        "temp_delta":  -0.05,
    },

    # ── Smoothness / Professionalism ─────────────────────────────────────────
    "smooth": {
        "voice_scores": {"af_nicole": 1.0, "bf_emma": 0.65, "am_michael": 0.6},
        "speed_delta":  0.0,
        "temp_delta":  -0.1,
    },
    "professional": {
        "voice_scores": {"af_nicole": 1.0, "bf_emma": 0.8, "bm_george": 0.7},
        "speed_delta": -0.05,
        "temp_delta":  -0.15,
    },
    "crisp": {
        "voice_scores": {"bf_emma": 1.0, "af_sarah": 0.75, "af_nicole": 0.55},
        "speed_delta":  0.05,
        "temp_delta":  -0.1,
    },
    "clear": {
        "voice_scores": {"af_sarah": 1.0, "bf_emma": 0.75, "af_nicole": 0.6},
        "speed_delta":  0.0,
        "temp_delta":  -0.05,
    },
    "articulate": {
        "voice_scores": {"af_sarah": 1.0, "bf_emma": 0.8},
        "speed_delta": -0.05,
        "temp_delta":  -0.1,
    },

    # ── Naturalness ──────────────────────────────────────────────────────────
    "natural": {
        "voice_scores": {"am_michael": 1.0, "af_heart": 0.7, "af_nicole": 0.5},
        "speed_delta":  0.0,
        "temp_delta":   0.05,
    },
    "conversational": {
        "voice_scores": {"am_michael": 1.0, "af_heart": 0.65, "af_nicole": 0.45},
        "speed_delta":  0.03,
        "temp_delta":   0.08,
    },
    "casual": {
        "voice_scores": {"am_michael": 0.85, "af_bella": 0.6, "af_heart": 0.55},
        "speed_delta":  0.05,
        "temp_delta":   0.08,
    },

    # ── Speed descriptors ────────────────────────────────────────────────────
    "fast": {
        "voice_scores": {},
        "speed_delta":  0.30,
        "temp_delta":   0.05,
    },
    "quick": {
        "voice_scores": {},
        "speed_delta":  0.20,
        "temp_delta":   0.05,
    },
    "rapid": {
        "voice_scores": {},
        "speed_delta":  0.35,
        "temp_delta":   0.05,
    },
    "slow": {
        "voice_scores": {},
        "speed_delta": -0.25,
        "temp_delta":  -0.05,
    },
    "measured": {
        "voice_scores": {},
        "speed_delta": -0.15,
        "temp_delta":  -0.08,
    },
    "deliberate": {
        "voice_scores": {},
        "speed_delta": -0.20,
        "temp_delta":  -0.1,
    },

    # ── Expressiveness / Temperature ─────────────────────────────────────────
    "expressive": {
        "voice_scores": {"af_heart": 0.7, "af_bella": 0.6},
        "speed_delta":  0.05,
        "temp_delta":   0.20,
    },
    "dramatic": {
        "voice_scores": {"af_heart": 0.8, "am_adam": 0.5},
        "speed_delta":  0.0,
        "temp_delta":   0.25,
    },
    "emotional": {
        "voice_scores": {"af_heart": 0.9, "af_bella": 0.5},
        "speed_delta":  0.0,
        "temp_delta":   0.22,
    },
    "steady": {
        "voice_scores": {"af_sarah": 0.5, "af_nicole": 0.5, "am_michael": 0.5},
        "speed_delta":  0.0,
        "temp_delta":  -0.20,
    },
    "consistent": {
        "voice_scores": {"af_sarah": 0.5, "af_nicole": 0.5},
        "speed_delta":  0.0,
        "temp_delta":  -0.25,
    },
    "monotone": {
        "voice_scores": {},
        "speed_delta":  0.0,
        "temp_delta":  -0.35,
    },

    # ── Accent / Origin ──────────────────────────────────────────────────────
    "british": {
        "voice_scores": {"bf_emma": 1.0, "bf_isabella": 1.0, "bm_george": 1.0, "bm_lewis": 1.0},
        "speed_delta": -0.03,
        "temp_delta":  -0.05,
    },
    "english": {
        "voice_scores": {"bf_emma": 0.9, "bf_isabella": 0.9, "bm_george": 0.9, "bm_lewis": 0.9},
        "speed_delta":  0.0,
        "temp_delta":  -0.05,
    },
    "american": {
        "voice_scores": {"af_heart": 0.8, "af_bella": 0.8, "af_nicole": 0.8,
                         "af_sarah": 0.8, "af_sky": 0.8,
                         "am_adam": 0.8, "am_michael": 0.8},
        "speed_delta":  0.0,
        "temp_delta":   0.0,
    },

    # ── Gender ───────────────────────────────────────────────────────────────
    "female": {
        "voice_scores": {"af_heart": 0.6, "af_bella": 0.6, "af_nicole": 0.6,
                         "af_sarah": 0.6, "af_sky": 0.6,
                         "bf_emma": 0.6, "bf_isabella": 0.6},
        "speed_delta":  0.0,
        "temp_delta":   0.0,
    },
    "male": {
        "voice_scores": {"am_adam": 0.6, "am_michael": 0.6,
                         "bm_george": 0.6, "bm_lewis": 0.6},
        "speed_delta":  0.0,
        "temp_delta":   0.0,
    },

    # ── Authority / Power ────────────────────────────────────────────────────
    "authoritative": {
        "voice_scores": {"am_adam": 0.85, "bm_george": 0.85, "af_nicole": 0.6},
        "speed_delta": -0.1,
        "temp_delta":  -0.1,
    },
    "commanding": {
        "voice_scores": {"am_adam": 0.9, "bm_george": 0.8},
        "speed_delta": -0.08,
        "temp_delta":  -0.12,
    },
    "powerful": {
        "voice_scores": {"am_adam": 0.9, "bm_lewis": 0.7},
        "speed_delta":  0.0,
        "temp_delta":   0.08,
    },

    # ── Softness / Calm ──────────────────────────────────────────────────────
    "soft": {
        "voice_scores": {"af_sky": 0.75, "af_heart": 0.7, "bf_isabella": 0.6},
        "speed_delta": -0.08,
        "temp_delta":  -0.1,
    },
    "gentle": {
        "voice_scores": {"af_heart": 0.8, "bf_isabella": 0.75, "af_sky": 0.65},
        "speed_delta": -0.1,
        "temp_delta":  -0.08,
    },
    "calm": {
        "voice_scores": {"af_nicole": 0.7, "bf_isabella": 0.65, "am_michael": 0.6},
        "speed_delta": -0.1,
        "temp_delta":  -0.12,
    },
    "soothing": {
        "voice_scores": {"af_heart": 0.85, "bf_isabella": 0.75, "af_nicole": 0.55},
        "speed_delta": -0.12,
        "temp_delta":  -0.08,
    },

    # ── Playfulness ──────────────────────────────────────────────────────────
    "playful": {
        "voice_scores": {"af_bella": 0.9, "af_sky": 0.65, "af_heart": 0.5},
        "speed_delta":  0.1,
        "temp_delta":   0.18,
    },
    "fun": {
        "voice_scores": {"af_bella": 0.85, "af_sky": 0.6},
        "speed_delta":  0.1,
        "temp_delta":   0.15,
    },
    "upbeat": {
        "voice_scores": {"af_bella": 0.9, "af_sarah": 0.5},
        "speed_delta":  0.12,
        "temp_delta":   0.12,
    },

    # ── Distinguished / Formal ───────────────────────────────────────────────
    "distinguished": {
        "voice_scores": {"bm_george": 1.0, "af_nicole": 0.7},
        "speed_delta": -0.08,
        "temp_delta":  -0.1,
    },
    "formal": {
        "voice_scores": {"bm_george": 0.85, "af_nicole": 0.75, "bf_emma": 0.65},
        "speed_delta": -0.05,
        "temp_delta":  -0.12,
    },
    "elegant": {
        "voice_scores": {"bf_emma": 0.85, "bm_george": 0.8, "af_nicole": 0.7},
        "speed_delta": -0.05,
        "temp_delta":  -0.08,
    },

    # ── Mellow / Husky ───────────────────────────────────────────────────────
    "mellow": {
        "voice_scores": {"af_heart": 0.8, "bf_isabella": 0.7, "am_michael": 0.55},
        "speed_delta": -0.1,
        "temp_delta":   0.05,
    },
    "husky": {
        "voice_scores": {"am_adam": 0.75, "bm_lewis": 0.7},
        "speed_delta": -0.05,
        "temp_delta":   0.1,
    },
    "gravelly": {
        "voice_scores": {"am_adam": 0.8, "bm_lewis": 0.75},
        "speed_delta": -0.05,
        "temp_delta":   0.08,
    },
}

# Synonym / alias map (token -> canonical tag)
_ALIASES: Dict[str, str] = {
    "slowly":       "slow",
    "quickly":      "quick",
    "fast-paced":   "fast",
    "softly":       "soft",
    "gently":       "gentle",
    "warmly":       "warm",
    "deeply":       "deep",
    "crisply":      "crisp",
    "expressively": "expressive",
    "calmly":       "calm",
    "gb":           "british",
    "uk":           "british",
    "usa":          "american",
    "us":           "american",
    "woman":        "female",
    "man":          "male",
    "guy":          "male",
    "girl":         "female",
    "boy":          "male",
    "lady":         "female",
    "whisper":      "whispery",
    "monotonic":    "monotone",
    "robotic":      "monotone",
    "intense":      "dramatic",
}

# Base defaults
_BASE_SPEED = 1.0
_BASE_TEMP  = 0.5
_SPEED_MIN  = 0.5
_SPEED_MAX  = 2.0
_TEMP_MIN   = 0.0
_TEMP_MAX   = 1.0


# ---------------------------------------------------------------------------
# SCORING ENGINE
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> List[str]:
    """Lower-case, split on whitespace and punctuation."""
    tokens = re.findall(r"[a-z]+(?:[-'][a-z]+)*", text.lower())
    # Apply aliases
    return [_ALIASES.get(t, t) for t in tokens]


def _score_voices(tokens: List[str]) -> Tuple[Dict[str, float], float, float, List[str]]:
    """
    Return (voice_scores_dict, speed_delta, temp_delta, matched_tags).
    voice_scores_dict maps voice_id -> cumulative score.
    """
    voice_scores: Dict[str, float] = {v: 0.0 for v in ALL_VOICES}
    speed_delta = 0.0
    temp_delta  = 0.0
    matched: List[str] = []

    for token in tokens:
        tag = VOICE_TAGS.get(token)
        if tag is None:
            continue
        matched.append(token)
        speed_delta += tag["speed_delta"]
        temp_delta  += tag["temp_delta"]
        for voice_id, score in tag["voice_scores"].items():
            if voice_id in voice_scores:
                voice_scores[voice_id] += score

    return voice_scores, speed_delta, temp_delta, matched


# ---------------------------------------------------------------------------
# PUBLIC API
# ---------------------------------------------------------------------------

def describe_to_voice(description: str) -> dict:
    """
    Convert a plain-text description to a Kokoro voice parameter set.

    Args:
        description: Free-form text, e.g. "warm deep slow british male".

    Returns:
        {
            "voice":        "<voice_id>",
            "speed":        <float 0.5-2.0>,
            "temperature":  <float 0.0-1.0>,
            "voice_prompt": "<description>",
            "description":  "<original description>",
            "matched_tags": ["tag1", "tag2", ...],
            "scores":       {voice_id: score, ...}   # sorted by score desc
        }
    """
    tokens = _tokenize(description)
    scores, speed_delta, temp_delta, matched = _score_voices(tokens)

    # Pick best voice (or default to af_heart)
    best_voice = max(scores, key=lambda v: scores[v]) if any(scores.values()) else "af_heart"

    # Clamp speed & temperature
    speed = round(
        max(_SPEED_MIN, min(_SPEED_MAX, _BASE_SPEED + speed_delta)), 2
    )
    temperature = round(
        max(_TEMP_MIN, min(_TEMP_MAX, _BASE_TEMP + temp_delta)), 2
    )

    # Sort scores for display
    sorted_scores = dict(
        sorted(scores.items(), key=lambda x: x[1], reverse=True)
    )

    return {
        "voice":        best_voice,
        "speed":        speed,
        "temperature":  temperature,
        "voice_prompt": description.strip(),
        "description":  description.strip(),
        "matched_tags": matched,
        "scores":       sorted_scores,
    }


def _apply_profile_to_settings(profile: dict) -> None:
    """Save a generated voice profile to kokoro_settings.json."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        if SETTINGS_PATH.exists():
            settings = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        else:
            settings = {}
    except Exception:
        settings = {}

    settings["voice"]        = profile["voice"]
    settings["speed"]        = profile["speed"]
    settings["temperature"]  = profile["temperature"]
    settings["voice_prompt"] = profile["voice_prompt"]

    SETTINGS_PATH.write_text(json.dumps(settings, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# FLASK ROUTE
# ---------------------------------------------------------------------------

import joi_companion
from flask import jsonify, request as flask_req


def _voice_from_desc_route():
    """
    POST /kokoro/voice_from_desc
    Body: {"description": "warm deep slow british male"}
    Returns the generated voice profile and saves it to kokoro_settings.json.
    """
    from modules.joi_memory import require_user
    require_user()

    data = flask_req.get_json(force=True) or {}
    description = (data.get("description") or "").strip()

    if not description:
        return jsonify({"ok": False, "error": "No description provided."}), 400

    profile = describe_to_voice(description)
    _apply_profile_to_settings(profile)

    return jsonify({"ok": True, "profile": profile})


joi_companion.register_route(
    "/kokoro/voice_from_desc",
    ["POST"],
    _voice_from_desc_route,
    "kokoro_voice_from_desc",
)

print("  [voice_engine] Description-to-Voice middleware loaded.")
