"""
modules/joi_voice_id.py

Voice Recognition + Speaker Identification
============================================

Browser records audio -> POST /voice/transcribe -> server decodes ->
Whisper STT -> speaker embedding -> compare vs enrolled voice.

Returns: { text: "...", speaker_match: true/false, confidence: 0.87 }

Dependencies (lazy-loaded, all optional):
  - faster-whisper   -- STT transcription
  - resemblyzer      -- speaker embeddings (256-dim d-vectors)
  - pydub            -- audio format conversion (webm -> wav)
  - numpy            -- cosine similarity math
"""

import io
import os
import json
import time
import base64
import struct
import threading
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import joi_companion
from flask import jsonify, request as flask_req

# ── Lazy imports for auth (joi_voice_id may load before joi_memory) ──────────
def _require_user():
    from modules.joi_memory import require_user
    return require_user()


# ── Optional dependency flags ────────────────────────────────────────────────
HAVE_FASTER_WHISPER = False
HAVE_RESEMBLYZER = False
HAVE_PYDUB = False
HAVE_NUMPY = False

try:
    import numpy as np
    HAVE_NUMPY = True
except ImportError:
    print("  [joi_voice_id] numpy not installed -- speaker ID unavailable")

try:
    from pydub import AudioSegment
    HAVE_PYDUB = True
except ImportError:
    print("  [joi_voice_id] pydub not installed -- audio conversion unavailable")

# faster-whisper and resemblyzer are lazy-loaded on first use (heavy models)

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
VOICE_PROFILE_PATH = DATA_DIR / "voice_profile.json"

# ── Model globals (lazy-loaded) ─────────────────────────────────────────────
_whisper_model = None
_voice_encoder = None
_model_lock = threading.Lock()

# ── Default settings ────────────────────────────────────────────────────────
DEFAULT_THRESHOLD = 0.75
WHISPER_MODEL_SIZE = os.getenv("JOI_WHISPER_MODEL", "base.en").strip()
SAMPLE_RATE = 16000           # 16 kHz for both Whisper and Resemblyzer
EMBEDDING_DIM = 256           # Resemblyzer d-vector dimension
ENROLLMENT_WINDOW_SEC = 3.0   # Sliding window for enrollment embeddings
MIN_ENROLLMENT_SEGMENTS = 5   # Minimum embedding segments for enrollment


# =============================================================================
# LAZY MODEL LOADERS
# =============================================================================

def _load_whisper_model():
    """Load faster-whisper model on first call. Thread-safe."""
    global _whisper_model, HAVE_FASTER_WHISPER
    with _model_lock:
        if _whisper_model is not None:
            return _whisper_model
        try:
            from faster_whisper import WhisperModel
            HAVE_FASTER_WHISPER = True
            print(f"  [joi_voice_id] loading Whisper model '{WHISPER_MODEL_SIZE}'...")
            _whisper_model = WhisperModel(
                WHISPER_MODEL_SIZE,
                device="cpu",
                compute_type="int8"
            )
            print(f"  [joi_voice_id] Whisper model loaded successfully")
            return _whisper_model
        except ImportError:
            print("  [joi_voice_id] faster-whisper not installed -- STT unavailable")
            return None
        except Exception as e:
            print(f"  [joi_voice_id] Whisper load error: {type(e).__name__}: {e}")
            return None


def _load_resemblyzer():
    """Load Resemblyzer VoiceEncoder on first call. Thread-safe."""
    global _voice_encoder, HAVE_RESEMBLYZER
    with _model_lock:
        if _voice_encoder is not None:
            return _voice_encoder
        try:
            from resemblyzer import VoiceEncoder
            HAVE_RESEMBLYZER = True
            print("  [joi_voice_id] loading Resemblyzer VoiceEncoder...")
            _voice_encoder = VoiceEncoder()
            print("  [joi_voice_id] VoiceEncoder loaded successfully")
            return _voice_encoder
        except ImportError:
            print("  [joi_voice_id] resemblyzer not installed -- speaker ID unavailable")
            return None
        except Exception as e:
            print(f"  [joi_voice_id] Resemblyzer load error: {type(e).__name__}: {e}")
            return None


# =============================================================================
# VOICE PROFILE STORAGE
# =============================================================================

def _load_voice_profile() -> Optional[Dict[str, Any]]:
    """Load voice profile from data/voice_profile.json."""
    if not VOICE_PROFILE_PATH.exists():
        return None
    try:
        profile = json.loads(VOICE_PROFILE_PATH.read_text(encoding="utf-8"))
        if "embeddings" in profile and "name" in profile:
            return profile
    except Exception as e:
        print(f"  [joi_voice_id] error loading voice profile: {e}")
    return None


def _save_voice_profile(profile: Dict[str, Any]):
    """Save voice profile to data/voice_profile.json."""
    VOICE_PROFILE_PATH.write_text(
        json.dumps(profile, indent=2, default=_json_serialize),
        encoding="utf-8"
    )


def _json_serialize(obj):
    """JSON serializer for numpy arrays and other non-standard types."""
    if HAVE_NUMPY and isinstance(obj, np.ndarray):
        return obj.tolist()
    if HAVE_NUMPY and isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


# =============================================================================
# AUDIO HELPERS
# =============================================================================

def _decode_audio(b64_data: str) -> Optional["np.ndarray"]:
    """
    Decode base64 audio (webm or wav) to a numpy array at 16kHz mono.

    Uses pydub for format conversion, falls back to raw WAV parsing.
    Returns None if decoding fails.
    """
    if not HAVE_NUMPY:
        return None

    try:
        raw_bytes = base64.b64decode(b64_data)
    except Exception as e:
        print(f"  [joi_voice_id] base64 decode error: {e}")
        return None

    # Try pydub first (handles webm, ogg, mp3, wav, etc.)
    if HAVE_PYDUB:
        try:
            # Detect format from header bytes
            fmt = _detect_audio_format(raw_bytes)
            audio = AudioSegment.from_file(io.BytesIO(raw_bytes), format=fmt)
            audio = audio.set_channels(1).set_frame_rate(SAMPLE_RATE).set_sample_width(2)
            samples = np.frombuffer(audio.raw_data, dtype=np.int16).astype(np.float32)
            samples /= 32768.0  # normalize to [-1, 1]
            return samples
        except Exception as e:
            print(f"  [joi_voice_id] pydub decode error ({fmt}): {e}")
            # Fall through to raw WAV parsing

    # Fallback: try parsing as raw WAV
    try:
        return _parse_wav_bytes(raw_bytes)
    except Exception as e:
        print(f"  [joi_voice_id] WAV parse error: {e}")
        return None


def _detect_audio_format(data: bytes) -> str:
    """Detect audio format from file header bytes."""
    if data[:4] == b"RIFF":
        return "wav"
    if data[:4] == b"fLaC":
        return "flac"
    if data[:4] == b"OggS":
        return "ogg"
    if data[:3] == b"ID3" or (len(data) > 1 and data[0] == 0xFF and (data[1] & 0xE0) == 0xE0):
        return "mp3"
    # WebM / Matroska header (EBML)
    if len(data) >= 4 and data[:4] == b"\x1a\x45\xdf\xa3":
        return "webm"
    # Default to webm (most common from MediaRecorder)
    return "webm"


def _parse_wav_bytes(data: bytes) -> Optional["np.ndarray"]:
    """Parse raw WAV bytes into a 16kHz mono float32 numpy array."""
    if not HAVE_NUMPY:
        return None
    if data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        raise ValueError("Not a valid WAV file")

    # Find 'fmt ' chunk
    pos = 12
    fmt_data = None
    audio_data = None
    while pos < len(data) - 8:
        chunk_id = data[pos:pos + 4]
        chunk_size = struct.unpack("<I", data[pos + 4:pos + 8])[0]
        if chunk_id == b"fmt ":
            fmt_data = data[pos + 8:pos + 8 + chunk_size]
        elif chunk_id == b"data":
            audio_data = data[pos + 8:pos + 8 + chunk_size]
        pos += 8 + chunk_size
        # Align to even boundary
        if chunk_size % 2 != 0:
            pos += 1

    if fmt_data is None or audio_data is None:
        raise ValueError("Missing fmt or data chunk in WAV")

    # Parse fmt chunk
    audio_format = struct.unpack("<H", fmt_data[0:2])[0]
    num_channels = struct.unpack("<H", fmt_data[2:4])[0]
    sample_rate = struct.unpack("<I", fmt_data[4:8])[0]
    bits_per_sample = struct.unpack("<H", fmt_data[14:16])[0]

    if audio_format != 1:  # PCM only for raw parsing
        raise ValueError(f"Unsupported WAV format: {audio_format} (only PCM supported)")

    # Convert to float32
    if bits_per_sample == 16:
        samples = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
    elif bits_per_sample == 32:
        samples = np.frombuffer(audio_data, dtype=np.int32).astype(np.float32) / 2147483648.0
    else:
        raise ValueError(f"Unsupported bit depth: {bits_per_sample}")

    # Convert to mono if stereo
    if num_channels > 1:
        samples = samples.reshape(-1, num_channels).mean(axis=1)

    # Resample to 16kHz if needed (simple linear interpolation)
    if sample_rate != SAMPLE_RATE:
        duration = len(samples) / sample_rate
        target_len = int(duration * SAMPLE_RATE)
        indices = np.linspace(0, len(samples) - 1, target_len)
        samples = np.interp(indices, np.arange(len(samples)), samples)

    return samples


# =============================================================================
# SPEAKER EMBEDDING + COMPARISON
# =============================================================================

def _extract_embedding(audio_array: "np.ndarray") -> Optional["np.ndarray"]:
    """
    Extract a 256-dim speaker embedding from audio using Resemblyzer.
    Returns None if the encoder is unavailable or extraction fails.
    """
    encoder = _load_resemblyzer()
    if encoder is None:
        return None

    try:
        from resemblyzer import preprocess_wav
        # Resemblyzer expects float64 at 16kHz
        wav = preprocess_wav(audio_array.astype(np.float64), source_sr=SAMPLE_RATE)
        if len(wav) < SAMPLE_RATE * 0.5:  # Need at least 0.5s of audio
            print("  [joi_voice_id] audio too short for embedding extraction")
            return None
        embedding = encoder.embed_utterance(wav)
        return embedding  # shape: (256,)
    except Exception as e:
        print(f"  [joi_voice_id] embedding extraction error: {type(e).__name__}: {e}")
        return None


def _extract_windowed_embeddings(
    audio_array: "np.ndarray",
    window_sec: float = ENROLLMENT_WINDOW_SEC,
    hop_sec: float = 1.5
) -> List["np.ndarray"]:
    """
    Extract multiple embeddings using sliding windows over the audio.
    Returns a list of 256-dim numpy arrays.
    """
    encoder = _load_resemblyzer()
    if encoder is None:
        return []

    try:
        from resemblyzer import preprocess_wav
        wav = preprocess_wav(audio_array.astype(np.float64), source_sr=SAMPLE_RATE)

        window_samples = int(window_sec * SAMPLE_RATE)
        hop_samples = int(hop_sec * SAMPLE_RATE)
        embeddings = []

        pos = 0
        while pos + window_samples <= len(wav):
            segment = wav[pos:pos + window_samples]
            emb = encoder.embed_utterance(segment)
            embeddings.append(emb)
            pos += hop_samples

        # If we didn't get enough windows, also embed the full utterance
        if len(embeddings) < MIN_ENROLLMENT_SEGMENTS and len(wav) >= SAMPLE_RATE:
            full_emb = encoder.embed_utterance(wav)
            embeddings.append(full_emb)

        return embeddings
    except Exception as e:
        print(f"  [joi_voice_id] windowed embedding error: {type(e).__name__}: {e}")
        return []


def _cosine_similarity(a: "np.ndarray", b: "np.ndarray") -> float:
    """Compute cosine similarity between two vectors. Returns float in [-1, 1]."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def _compare_speaker(embedding: "np.ndarray") -> Tuple[bool, float]:
    """
    Compare a speaker embedding against the enrolled voice profile.

    Returns:
        (is_match, confidence) -- is_match is True if confidence >= threshold
    """
    profile = _load_voice_profile()
    if profile is None:
        return False, 0.0

    threshold = profile.get("threshold", DEFAULT_THRESHOLD)
    stored_embeddings = profile.get("embeddings", [])

    if not stored_embeddings:
        return False, 0.0

    # Compare against each stored embedding, take the best score
    best_score = 0.0
    for stored_emb in stored_embeddings:
        stored_arr = np.array(stored_emb, dtype=np.float32)
        score = _cosine_similarity(embedding, stored_arr)
        if score > best_score:
            best_score = score

    # Also compare against the mean embedding for robustness
    mean_emb = np.mean([np.array(e, dtype=np.float32) for e in stored_embeddings], axis=0)
    mean_score = _cosine_similarity(embedding, mean_emb)
    best_score = max(best_score, mean_score)

    is_match = best_score >= threshold
    return is_match, round(best_score, 4)


# =============================================================================
# TRANSCRIPTION
# =============================================================================

def _transcribe(audio_array: "np.ndarray") -> str:
    """
    Transcribe audio using faster-whisper.
    Returns the transcribed text, or empty string on failure.
    """
    model = _load_whisper_model()
    if model is None:
        return ""

    try:
        # faster-whisper expects float32 numpy array at 16kHz
        segments, info = model.transcribe(
            audio_array,
            beam_size=5,
            language="en",
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=500,
                speech_pad_ms=200
            )
        )
        text_parts = []
        for segment in segments:
            text_parts.append(segment.text.strip())
        return " ".join(text_parts).strip()
    except Exception as e:
        print(f"  [joi_voice_id] transcription error: {type(e).__name__}: {e}")
        return ""


# =============================================================================
# TOOL FUNCTIONS
# =============================================================================

def enroll_voice(**kwargs) -> Dict[str, Any]:
    """
    Tool: Enroll a voice for speaker identification.

    Receives base64 audio (15+ seconds recommended), extracts multiple
    embedding segments, averages them, and saves to voice_profile.json.
    """
    _require_user()

    if not HAVE_NUMPY:
        return {"ok": False, "error": "numpy is required for voice enrollment."}

    audio_b64 = kwargs.get("audio_b64", "").strip()
    name = kwargs.get("name", "Lonnie").strip()

    if not audio_b64:
        return {
            "ok": False,
            "error": "No audio data provided. Send base64-encoded audio in the 'audio_b64' parameter."
        }

    # Decode audio
    audio_array = _decode_audio(audio_b64)
    if audio_array is None:
        return {"ok": False, "error": "Failed to decode audio data."}

    duration_sec = len(audio_array) / SAMPLE_RATE
    if duration_sec < 3.0:
        return {
            "ok": False,
            "error": f"Audio too short ({duration_sec:.1f}s). Need at least 3 seconds, recommend 15+."
        }

    # Extract windowed embeddings
    embeddings = _extract_windowed_embeddings(audio_array)
    if len(embeddings) == 0:
        return {"ok": False, "error": "Could not extract voice embeddings. Is resemblyzer installed?"}

    # Convert to serializable lists
    embedding_lists = [emb.tolist() for emb in embeddings]

    # Build and save profile
    profile = {
        "name": name,
        "embeddings": embedding_lists,
        "enrolled_at": datetime.now().isoformat(),
        "threshold": DEFAULT_THRESHOLD,
        "audio_duration_sec": round(duration_sec, 1),
        "num_segments": len(embedding_lists),
        "embedding_dim": len(embedding_lists[0]) if embedding_lists else 0
    }
    _save_voice_profile(profile)

    print(f"  [joi_voice_id] voice enrolled for '{name}' -- {len(embeddings)} segments, {duration_sec:.1f}s audio")

    return {
        "ok": True,
        "message": f"Voice profile enrolled for {name}! Saved {len(embeddings)} embedding segments from {duration_sec:.1f}s of audio.",
        "name": name,
        "segments": len(embeddings),
        "duration_sec": round(duration_sec, 1)
    }


def check_voice_id(**kwargs) -> Dict[str, Any]:
    """
    Tool: Test if the current speaker matches the enrolled voice profile.

    Receives base64 audio and compares the speaker embedding against
    the enrolled profile.
    """
    _require_user()

    if not HAVE_NUMPY:
        return {"ok": False, "error": "numpy is required for voice identification."}

    audio_b64 = kwargs.get("audio_b64", "").strip()
    if not audio_b64:
        return {"ok": False, "error": "No audio data provided."}

    profile = _load_voice_profile()
    if profile is None:
        return {
            "ok": False,
            "error": "No voice profile enrolled. Use enroll_voice first.",
            "enrolled": False
        }

    audio_array = _decode_audio(audio_b64)
    if audio_array is None:
        return {"ok": False, "error": "Failed to decode audio data."}

    embedding = _extract_embedding(audio_array)
    if embedding is None:
        return {"ok": False, "error": "Could not extract speaker embedding."}

    is_match, confidence = _compare_speaker(embedding)

    return {
        "ok": True,
        "speaker_match": is_match,
        "confidence": confidence,
        "threshold": profile.get("threshold", DEFAULT_THRESHOLD),
        "profile_name": profile.get("name", "unknown")
    }


def set_voice_threshold(**kwargs) -> Dict[str, Any]:
    """
    Tool: Adjust the speaker ID confidence threshold (0.5 - 0.95).

    Lower = more lenient (may false-match), Higher = stricter (may miss).
    """
    _require_user()

    value = kwargs.get("value")
    if value is None:
        return {"ok": False, "error": "Provide a 'value' between 0.5 and 0.95."}

    try:
        value = float(value)
    except (ValueError, TypeError):
        return {"ok": False, "error": f"Invalid threshold value: {value}"}

    if value < 0.5 or value > 0.95:
        return {"ok": False, "error": f"Threshold must be between 0.5 and 0.95 (got {value})."}

    profile = _load_voice_profile()
    if profile is None:
        return {"ok": False, "error": "No voice profile enrolled yet."}

    profile["threshold"] = round(value, 3)
    _save_voice_profile(profile)

    print(f"  [joi_voice_id] threshold updated to {value:.3f}")
    return {
        "ok": True,
        "message": f"Voice ID threshold set to {value:.3f}.",
        "threshold": round(value, 3)
    }


# =============================================================================
# FLASK ROUTES
# =============================================================================

def _voice_transcribe_route():
    """
    POST /voice/transcribe

    Receives base64 audio (1-10 seconds, webm or wav).
    Decodes -> extracts speaker embedding -> compares to profile ->
    if match: transcribe and return text.
    if no match: return empty text with speaker_match=false.
    """
    _require_user()

    data = flask_req.get_json(silent=True) or {}
    audio_b64 = data.get("audio_b64", "").strip()

    if not audio_b64:
        return jsonify({"ok": False, "error": "No audio_b64 provided"}), 400

    # Reject oversized payloads (>10MB base64 ~ 7.5MB raw)
    if len(audio_b64) > 10_000_000:
        return jsonify({"ok": False, "error": "Audio payload too large"}), 413

    # Decode audio
    audio_array = _decode_audio(audio_b64)
    if audio_array is None:
        return jsonify({"ok": False, "error": "Failed to decode audio"}), 400

    duration_sec = len(audio_array) / SAMPLE_RATE

    # Speaker identification (if profile exists and resemblyzer available)
    speaker_match = True  # Default to True if no profile enrolled (open mode)
    confidence = 1.0
    profile_name = None

    profile = _load_voice_profile()
    if profile is not None and HAVE_NUMPY:
        embedding = _extract_embedding(audio_array)
        if embedding is not None:
            speaker_match, confidence = _compare_speaker(embedding)
            profile_name = profile.get("name", "unknown")
        else:
            # Couldn't extract embedding -- proceed with transcription anyway
            speaker_match = True
            confidence = 0.0

    # If speaker doesn't match, return early without transcription
    if not speaker_match:
        return jsonify({
            "ok": True,
            "text": "",
            "speaker_match": False,
            "confidence": confidence,
            "profile_name": profile_name,
            "duration_sec": round(duration_sec, 1)
        })

    # Transcribe
    text = _transcribe(audio_array)

    return jsonify({
        "ok": True,
        "text": text,
        "speaker_match": speaker_match,
        "confidence": confidence,
        "profile_name": profile_name,
        "duration_sec": round(duration_sec, 1)
    })


def _voice_enroll_route():
    """
    POST /voice/enroll

    Receives 15+ seconds of base64 audio.
    Extracts speaker embeddings and saves the voice profile.
    """
    _require_user()

    data = flask_req.get_json(silent=True) or {}
    audio_b64 = data.get("audio_b64", "").strip()
    name = data.get("name", "Lonnie").strip()

    if not audio_b64:
        return jsonify({"ok": False, "error": "No audio_b64 provided"}), 400

    # Reject oversized payloads (>20MB base64 for longer enrollment clips)
    if len(audio_b64) > 20_000_000:
        return jsonify({"ok": False, "error": "Audio payload too large"}), 413

    result = enroll_voice(audio_b64=audio_b64, name=name)
    status_code = 200 if result.get("ok") else 400
    return jsonify(result), status_code


def _voice_status_route():
    """
    GET /voice/status

    Returns enrollment status, model readiness, and threshold.
    """
    _require_user()

    profile = _load_voice_profile()
    enrolled = profile is not None

    return jsonify({
        "ok": True,
        "enrolled": enrolled,
        "profile_name": profile.get("name") if profile else None,
        "threshold": profile.get("threshold", DEFAULT_THRESHOLD) if profile else DEFAULT_THRESHOLD,
        "num_segments": len(profile.get("embeddings", [])) if profile else 0,
        "enrolled_at": profile.get("enrolled_at") if profile else None,
        "whisper_loaded": _whisper_model is not None,
        "encoder_loaded": _voice_encoder is not None,
        "have_faster_whisper": HAVE_FASTER_WHISPER or _can_import("faster_whisper"),
        "have_resemblyzer": HAVE_RESEMBLYZER or _can_import("resemblyzer"),
        "have_pydub": HAVE_PYDUB,
        "have_numpy": HAVE_NUMPY
    })


def _can_import(module_name: str) -> bool:
    """Check if a module can be imported without actually loading it."""
    try:
        import importlib.util
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except (ModuleNotFoundError, ValueError):
        return False


def manage_voice_id(**kwargs) -> Dict[str, Any]:
    """Unified tool for managing voice profile operations."""
    action = kwargs.get("action")
    if not action:
        return {"ok": False, "error": "action parameter is required"}
        
    try:
        if action == "enroll": return enroll_voice(**kwargs)
        elif action == "check": return check_voice_id(**kwargs)
        elif action == "set_threshold": return set_voice_threshold(**kwargs)
        else: return {"ok": False, "error": f"Unknown action: {action}"}
    except Exception as exc:
        return {"ok": False, "error": f"Voice ID action {action} failed: {exc}"}

# =============================================================================
# TOOL REGISTRATION
# =============================================================================

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "manage_voice_id",
        "description": "Unified tool to manage voice ID operations (enroll, check, set threshold).",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["enroll", "check", "set_threshold"]
                },
                "audio_b64": {
                    "type": "string",
                    "description": "Base64-encoded audio data (webm or wav). Required for enroll and check."
                },
                "name": {
                    "type": "string",
                    "description": "Name to associate with this voice profile (for enroll, default: Lonnie)"
                },
                "value": {
                    "type": "number",
                    "description": "Threshold value between 0.5 and 0.95 (for set_threshold)"
                }
            },
            "required": ["action"]
        }
    }},
    manage_voice_id
)


# =============================================================================
# ROUTE REGISTRATION
# =============================================================================

joi_companion.register_route(
    "/voice/transcribe", ["POST"], _voice_transcribe_route, "voice_transcribe"
)
joi_companion.register_route(
    "/voice/enroll", ["POST"], _voice_enroll_route, "voice_enroll"
)
joi_companion.register_route(
    "/voice/status", ["GET"], _voice_status_route, "voice_status"
)


# =============================================================================
# MODULE LOAD STATUS
# =============================================================================

_profile = _load_voice_profile()
_enrolled_status = f"enrolled ({_profile['name']})" if _profile else "no profile"
print(
    f"  [joi_voice_id] voice ID module loaded -- "
    f"profile: {_enrolled_status}, "
    f"numpy: {'yes' if HAVE_NUMPY else 'NO'}, "
    f"pydub: {'yes' if HAVE_PYDUB else 'NO'}"
)
print("    + Voice ID tools registered (enroll_voice, check_voice_id, set_voice_threshold)")
print("    + Voice ID routes registered (/voice/transcribe, /voice/enroll, /voice/status)")
