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


def _sanitize_for_tts(text: str) -> str:
    """
    Comprehensive text normalisation for the Kokoro TTS phonemizer.

    Converts all non-standard constructs to natural spoken English *before*
    phonemisation so the phonemizer never sees tokens it can't align, which
    is what causes "words count mismatch" warnings.

    Pipeline order matters — do not reorder sections:
      0. Markdown / formatting (must precede typography fixes)
      1. Emoji stripping
      2. Typography (smart quotes, em-dashes, ellipses)
      3. Personality / stage-direction tags
      4. Number conversions (ISO dates → spoken, tech hyphens, %, integers)
      5. Remaining special characters
      6. Whitespace normalisation
    """
    import re

    # ── Shared look-up tables (built once per call; function is called rarely) ─
    _ONES = [
        '', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
        'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
        'sixteen', 'seventeen', 'eighteen', 'nineteen',
    ]
    _TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty',
             'sixty', 'seventy', 'eighty', 'ninety']
    _MONTHS_MAP = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December',
    }
    _ORDINALS_MAP = {
        1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth',
        6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'ninth', 10: 'tenth',
        11: 'eleventh', 12: 'twelfth', 13: 'thirteenth', 14: 'fourteenth',
        15: 'fifteenth', 16: 'sixteenth', 17: 'seventeenth', 18: 'eighteenth',
        19: 'nineteenth', 20: 'twentieth', 21: 'twenty first', 22: 'twenty second',
        23: 'twenty third', 24: 'twenty fourth', 25: 'twenty fifth',
        26: 'twenty sixth', 27: 'twenty seventh', 28: 'twenty eighth',
        29: 'twenty ninth', 30: 'thirtieth', 31: 'thirty first',
    }

    def _int_to_words(n: int) -> str:
        """Convert integer 0–999 to English words; larger numbers fall back to digits."""
        if n < 0:
            return 'negative ' + _int_to_words(-n)
        if n == 0:
            return 'zero'
        if n < 20:
            return _ONES[n]
        if n < 100:
            t, o = _TENS[n // 10], _ONES[n % 10]
            return t if not o else f'{t} {o}'
        if n < 1000:
            h = _ONES[n // 100]
            rem = n % 100
            return f'{h} hundred' if not rem else f'{h} hundred {_int_to_words(rem)}'
        return str(n)

    def _year_to_words(y: int) -> str:
        """2026 → 'twenty twenty six', 1999 → 'nineteen ninety nine'."""
        if 2000 <= y <= 2099:
            rest = y - 2000
            return 'twenty ' + _int_to_words(rest) if rest else 'two thousand'
        if 1900 <= y <= 1999:
            rest = y - 1900
            return 'nineteen ' + _int_to_words(rest) if rest else 'nineteen hundred'
        return str(y)

    # ── 0. Markdown / formatting ─────────────────────────────────────────────
    # Known stage-direction words in single asterisks → strip entirely
    _SD = (r'whispers?|whispered|softly|gently|quietly|sadly|sighs?|sighing|'
           r'smiling|grinning|laughs?|laughing|chuckles?|winking|shrugging|'
           r'pauses?|pausing|internally|glances?|excitedly|nervously')
    text = re.sub(fr'\*\s*(?:{_SD})\s*\*', '', text, flags=re.IGNORECASE)
    # Bold / italic / strikethrough → keep inner text (emphasis reads naturally)
    text = re.sub(r'\*{1,3}([^*\n]+)\*{1,3}', r'\1', text)
    text = re.sub(r'~~([^~\n]+)~~', r'\1', text)
    # Inline code → remove (unpronounceable)
    text = re.sub(r'`[^`\n]*`', '', text)
    # Markdown links → link text only
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    # Bare URLs → silence (nothing useful to say)
    text = re.sub(r'https?://\S+', '', text)

    # ── 1. Emoji ─────────────────────────────────────────────────────────────
    text = re.sub(
        r'[\U0001F000-\U0001FFFF'   # All main emoji blocks
        r'\U00002600-\U000027BF'    # Misc symbols (☀ ✓ ♥ ★ etc.)
        r'\U00002B00-\U00002BFF'    # Misc arrows / symbols
        r'\U0000FE00-\U0000FE0F]',  # Variation selectors
        '', text,
    )

    # ── 2. Typography ────────────────────────────────────────────────────────
    # Smart / curly quotes → plain ASCII
    for _old, _new in (
        ('\u2018', "'"), ('\u2019', "'"),   # ' '  left/right single
        ('\u201c', '"'), ('\u201d', '"'),   # " "  left/right double
        ('\u2032', "'"), ('\u2033', '"'),   # ′ ″  prime / double-prime
        ('\u00b4', "'"), ('\u0060', "'"),   # ´ `  acute / grave
    ):
        text = text.replace(_old, _new)

    # Em-dash → spoken pause; ASCII double-dash (prose em-dash) → pause
    text = text.replace('\u2014', ', ')
    text = re.sub(r'\s*--\s*', ', ', text)
    # En-dash → "to" (used in number ranges: 3–5 → "3 to 5")
    text = text.replace('\u2013', ' to ')
    # Ellipsis (Unicode char and ASCII variants) → brief pause
    text = text.replace('\u2026', ', ')
    text = re.sub(r'\.{3,}', ', ', text)

    # ── 3. Personality / stage-direction tags ────────────────────────────────
    # Square-bracket stage directions [softly] [grinning] etc. → remove
    text = re.sub(r'\[[^\]]{1,40}\]', '', text)
    # Parenthetical stage directions (softly), (whispers), (laughing) etc. → remove
    text = re.sub(
        r'\(\s*(?:softly|whisper\w*|grinning|smiling|laughing|sighing|quietly|'
        r'gently|warmly|playfully|teasingly|shrugging|nervously)\s*[^)]{0,25}\)',
        '', text, flags=re.IGNORECASE,
    )

    # ── 4. Numbers ───────────────────────────────────────────────────────────

    # 4a. ISO dates FIRST (before hyphen handling changes the separators):
    #     2026-03-07  or  2026/03/07  →  "March seventh twenty twenty six"
    def _date_sub(m: re.Match) -> str:
        try:
            y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if 1 <= mo <= 12 and 1 <= d <= 31:
                return (f"{_MONTHS_MAP[mo]} {_ORDINALS_MAP.get(d, str(d))} "
                        f"{_year_to_words(y)}")
        except Exception:
            pass
        return m.group(0)

    text = re.sub(
        r'\b((?:19|20)\d{2})[-/](0?[1-9]|1[0-2])[-/](0?[1-9]|[12]\d|3[01])\b',
        _date_sub, text,
    )

    # 4b. Tech model-name hyphens → spaces at letter↔digit boundaries only.
    #     gpt-5-mini → "gpt 5 mini"   claude-3-haiku → "claude 3 haiku"
    #     Preserves regular word-hyphens: self-aware, well-known (no digit).
    text = re.sub(r'(?<=[A-Za-z])-(?=\d)', ' ', text)   # letter → digit
    text = re.sub(r'(?<=\d)-(?=[A-Za-z])', ' ', text)   # digit → letter

    # 4c. Percentages: 100%  →  "one hundred percent"
    def _pct_sub(m: re.Match) -> str:
        try:
            return _int_to_words(int(m.group(1))) + ' percent'
        except Exception:
            return m.group(0)
    text = re.sub(r'\b(\d{1,3})%', _pct_sub, text)

    # 4d. Plain integers 1–999 not attached to letters, decimals, or % (already handled).
    #     "3 active" → "three active"   "720p" stays (digit followed by letter).
    def _num_sub(m: re.Match) -> str:
        try:
            n = int(m.group(0))
            return _int_to_words(n) if 0 < n <= 999 else m.group(0)
        except Exception:
            return m.group(0)
    text = re.sub(r'(?<![.\w])([1-9]\d{0,2})(?![.\w%])', _num_sub, text)

    # ── 5. Remaining special characters ─────────────────────────────────────
    text = re.sub(r'[#@\^{}<>|\\~_\[\]]+', ' ', text)
    text = re.sub(r'([!?]){2,}', r'\1', text)       # !!! → !
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)     # space before punctuation
    text = re.sub(r',\s*,', ',', text)               # ,, → ,

    # ── 6. Whitespace ────────────────────────────────────────────────────────
    text = re.sub(r'\n{2,}', '. ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)

    return text.strip()


def _extract_speakable(text: str) -> str:
    """
    Pre-phonemizer pass: extract only natural-language/conversational content.

    Strips entirely (never normalises):
      - Fenced code blocks  (```...```)
      - Inline code  (`...`)
      - JSON / dict / list structural lines
      - Windows and Unix file paths
      - Git output lines (commit hashes, diff headers, short-status, etc.)
      - Hex hashes and technical IDs
      - Underscored identifiers  (variable / function / module names)
      - Technical decimal numbers  (0.916, confidence scores)
      - 4+ digit integers that are not years 1900-2099  (port 5001, rate 24000)
      - Bare URLs

    Preserves: conversational sentences, small prose numbers, punctuation.
    Runs *before* _sanitize_for_tts() inside generate_speech_kokoro().
    """
    import re

    # ── A0. Internal monologue tags — must never reach TTS ───────────────────
    text = re.sub(
        r'\[QUIETSTAR RATIONALE\][\s\S]*?\[/QUIETSTAR RATIONALE\]'
        r'|\[INTERNAL REASONING\][\s\S]*?\[/INTERNAL REASONING\]'
        r'|\[TITAN MONOLOGUE\][\s\S]*?\[/TITAN MONOLOGUE\]',
        ' ', text, flags=re.IGNORECASE,
    )

    # ── A. Block-level: fenced code blocks ───────────────────────────────────
    text = re.sub(r'```[\s\S]*?```', ' ', text)

    # ── B. Line-level filtering ──────────────────────────────────────────────
    _GIT_LINE = re.compile(
        r'^(?:'
        r'commit [0-9a-f]{6,}'                    # commit <hash>
        r'|diff --git '                            # diff header
        r'|index [0-9a-f]{6,}'                    # index line
        r'|@@ '                                   # hunk header
        r'|Author: '                              # git log author
        r'|Date:   '                              # git log date
        r'|Merge: '                               # merge commit
        r'|[MADRCU?!]{1,2}\s+\S+\.\w{1,6}$'     # short status  M file.py
        r')'
    )
    kept = []
    for line in text.split('\n'):
        s = line.strip()
        if not s:
            kept.append('')
            continue
        if _GIT_LINE.match(s):
            continue
        # JSON key-value lines  "key": value
        if re.match(r'^"[^"]{1,80}"\s*:', s):
            continue
        # JSON structural lines — only brackets/braces/commas/quotes/digits
        if re.match(r'^[\s\[\]{},.:0-9"\']+$', s) and not re.search(r'[a-zA-Z]{3,}', s):
            continue
        # Windows absolute file-path lines
        if re.match(r'^[A-Za-z]:\\', s):
            continue
        # Pure hex hash lines
        if re.match(r'^[0-9a-f]{7,}\s*$', s, re.IGNORECASE):
            continue
        # Log/trace timestamp lines  [2026-03-07 …] or ISO 2026-03-07T…
        if re.match(r'^\[?\d{4}-\d{2}-\d{2}[T \]]', s):
            continue
        kept.append(line)
    text = '\n'.join(kept)

    # ── C. Inline token removal ──────────────────────────────────────────────
    # Inline backtick code
    text = re.sub(r'`[^`\n]+`', '', text)
    # Bare URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Windows file paths  C:\Users\…
    text = re.sub(r'[A-Za-z]:\\(?:\S+\\)*\S*', '', text)
    # Unix absolute paths  /usr/local/bin/python
    text = re.sub(r'(?<!\w)/(?:[a-zA-Z0-9._-]+/)+[a-zA-Z0-9._-]*', '', text)
    # Relative slash paths with 2+ segments  data/gallery/img.png
    text = re.sub(r'\b(?:[a-zA-Z0-9_-]+/){2,}[a-zA-Z0-9_.-]+\b', '', text)
    # Relative slash paths with 1 segment + file extension  modules/joi_tts.py
    text = re.sub(r'\b[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+\.[a-z]{2,5}\b', '', text)
    # Hex hashes as standalone tokens (7+ hex chars)
    text = re.sub(r'\b[0-9a-f]{7,}\b', '', text, flags=re.IGNORECASE)
    # Underscored identifiers — Python/JS variable, function, module names
    text = re.sub(r'\b[a-zA-Z]\w*(?:_\w+)+\b', '', text, flags=re.IGNORECASE)
    # Technical leading-zero floats  0.916  (confidence / weight scores)
    text = re.sub(r'\b0\.\d{3,}\b', '', text)
    # Floats with 3+ decimal places  1.2345  (high-precision technical values)
    text = re.sub(r'\b\d+\.\d{3,}\b', '', text)
    # 4+ digit integers that are NOT years 1900–2099
    # (strips ports 5001, rates 24000, token counts 16000, etc.)
    text = re.sub(r'\b(?!(?:19|20)\d{2}\b)\d{4,}\b', '', text)
    # Markdown headers  ## Title  →  keep title text
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)

    # ── D. Collapse whitespace artifacts ─────────────────────────────────────
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = re.sub(r'\n{3,}', '\n', text)

    return text.strip()


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
    # 1. Extract only natural-language sentences (strip JSON, code, paths, hashes)
    text = _extract_speakable(text)
    # 2. Normalise remaining text for the phonemizer
    text = _sanitize_for_tts(text)
    if not text:
        print("[kokoro] Text was empty after sanitization — skipping TTS")
        return None

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
