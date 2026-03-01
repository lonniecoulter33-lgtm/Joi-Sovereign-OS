"""joi_awareness.py — Agentic Awareness Bridge (Phase 4)

Connects Joi's background systems to her conversation layer.
Background modules write observations; conversation layer reads them.

Sources (all passive — no API calls, no LLM calls):
  - EventBus: subscribes to desktop_vision events from vision loop
  - joi_vision._last_proactive_summary: direct read of latest screen observation
  - data/autonomy_log.json: last autonomy cycle findings
  - projects/memory/reasoning_log.json: TITAN breakthrough thoughts

Output: compact [LIVE AWARENESS] block (~300-400 chars) injected into system prompt.
Gives Joi genuine situational continuity between conversation turns.

This is the Sense layer of the Sense→Think→Act→Reflect loop.
"""

from __future__ import annotations
import json
import time
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

_ROOT = Path(__file__).parent.parent
_STATE_FILE = _ROOT / "data" / "joi_awareness.json"

# ── Thread-safe observation buffer ───────────────────────────────────────────

_buffer: List[Dict[str, Any]] = []
_lock = threading.Lock()
_MAX_ENTRIES = 25
_PERSIST_INTERVAL = 30.0   # seconds between disk writes
_last_persist_ts = 0.0


def record_observation(
    category: str,
    content: str,
    source: str = "",
    ttl_minutes: float = 15.0,
    deduplicate: bool = True,
) -> None:
    """
    Write an observation to the awareness buffer.

    Args:
        category: Short label e.g. "SCREEN", "AUTONOMY", "THOUGHT", "ERROR"
        content:  The observation text (truncated to 300 chars)
        source:   Which module wrote this (for debugging)
        ttl_minutes: How long until this entry expires
        deduplicate: Skip if identical content already in buffer
    """
    content = str(content)[:300].strip()
    if not content:
        return

    now = time.time()
    entry = {
        "category": category.upper(),
        "content": content,
        "source": source,
        "ts": now,
        "ttl_sec": ttl_minutes * 60,
    }

    with _lock:
        if deduplicate:
            # Skip if same content was recorded in the last N seconds
            cutoff = now - max(60, ttl_minutes * 30)  # within first 30% of TTL
            if any(e["content"] == content and e["ts"] > cutoff for e in _buffer):
                return
        _buffer.append(entry)
        # Keep only most recent entries
        if len(_buffer) > _MAX_ENTRIES:
            _buffer[:] = _buffer[-_MAX_ENTRIES:]

    _maybe_persist()


def get_recent_observations(max_age_minutes: float = 15.0) -> List[Dict[str, Any]]:
    """Return non-expired observations, newest last."""
    now = time.time()
    cutoff = now - max_age_minutes * 60
    with _lock:
        return [
            e for e in _buffer
            if e["ts"] >= cutoff and (now - e["ts"]) < e["ttl_sec"]
        ]


# ── Disk persistence ─────────────────────────────────────────────────────────

def _maybe_persist() -> None:
    global _last_persist_ts
    now = time.time()
    if now - _last_persist_ts < _PERSIST_INTERVAL:
        return
    _last_persist_ts = now
    _persist()


def _persist() -> None:
    try:
        _STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with _lock:
            snapshot = list(_buffer)
        with open(_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)
    except Exception:
        pass


def _load_persisted() -> None:
    """Restore buffer from disk on startup."""
    global _buffer
    try:
        if not _STATE_FILE.exists():
            return
        with open(_STATE_FILE, encoding="utf-8") as f:
            data = json.load(f)
        now = time.time()
        # Only restore non-expired entries
        valid = [e for e in data if isinstance(e, dict) and (now - e.get("ts", 0)) < e.get("ttl_sec", 900)]
        with _lock:
            _buffer = valid[-_MAX_ENTRIES:]
    except Exception:
        pass


# ── EventBus integration (subscribe to vision events) ────────────────────────

def _handle_bus_event(event: Any) -> None:
    """Handle JoiEvent from the EventBus — called by the bus dispatch thread."""
    try:
        topic = getattr(event, "topic", "")
        payload = getattr(event, "payload", {}) or {}
        source = getattr(event, "source", "bus")

        if topic == "desktop_vision":
            desc = payload.get("description", "")
            if desc:
                record_observation("SCREEN", desc[:200], source=source, ttl_minutes=20)

        elif topic in ("joi_thought", "titan_thought", "breakthrough"):
            thought = payload.get("thought", payload.get("content", ""))
            if thought:
                record_observation("THOUGHT", thought[:200], source=source, ttl_minutes=30)

        elif topic in ("error_detected", "self_heal_error"):
            err = payload.get("error", payload.get("description", ""))
            if err:
                record_observation("ERROR", err[:150], source=source, ttl_minutes=10)

    except Exception:
        pass


def _subscribe_to_bus() -> bool:
    """Subscribe to EventBus. Returns True on success."""
    try:
        from modules.core.events import bus
        bus.subscribe("desktop_vision", _handle_bus_event)
        bus.subscribe("joi_thought", _handle_bus_event)
        bus.subscribe("titan_thought", _handle_bus_event)
        bus.subscribe("breakthrough", _handle_bus_event)
        bus.subscribe("error_detected", _handle_bus_event)
        return True
    except Exception:
        return False


# ── Source sync: vision module direct read ───────────────────────────────────

def _sync_vision_state() -> None:
    """Pull latest vision summary directly from the media module's state."""
    try:
        import modules.joi_media as _media
        summary = getattr(_media, "_latest_frame_b64", None)
        ts = getattr(_media, "_latest_frame_ts", 0) or 0
        if summary and ts and (time.time() - ts) < 1800:  # 30 min
            record_observation("SCREEN", "Visual input active", source="vision_direct", ttl_minutes=30)
    except Exception:
        pass


# ── Source sync: autonomy cycle log ─────────────────────────────────────────

def _sync_autonomy_log() -> None:
    """Read last autonomy cycle findings (if recent)."""
    try:
        log_path = _ROOT / "data" / "autonomy_log.json"
        if not log_path.exists():
            return
        with open(log_path, encoding="utf-8") as f:
            raw = json.load(f)
        cycles = raw if isinstance(raw, list) else raw.get("cycles", [])
        if not cycles:
            return
        last = cycles[-1]

        # Parse timestamp
        started = last.get("started") or last.get("timestamp", "")
        try:
            from datetime import datetime, timezone
            cycle_ts = datetime.fromisoformat(started.replace("Z", "+00:00")).timestamp()
        except Exception:
            return

        if (time.time() - cycle_ts) > 86400:  # Only last 24h
            return

        steps = last.get("steps", {})
        learn = steps.get("learn", {})
        weak = learn.get("weak_areas", [])
        positive_rate = learn.get("positive_rate", 0)
        diagnose = steps.get("diagnose", {})
        tool_ct = diagnose.get("tools", 0)
        auto_apply = steps.get("auto_apply", {})
        applied = auto_apply.get("applied", []) if isinstance(auto_apply, dict) else []

        parts = []
        if applied:
            parts.append(f"{len(applied)} upgrade(s) auto-applied")
        if weak:
            parts.append(f"weak areas: {', '.join(str(w) for w in weak[:3])}")
        if positive_rate:
            parts.append(f"positive rate: {positive_rate:.0%}")
        if tool_ct:
            parts.append(f"{tool_ct} tools online")

        content = "Autonomy cycle: " + ", ".join(parts) if parts else "Autonomy cycle complete"
        record_observation("AUTONOMY", content, source="autonomy_log", ttl_minutes=120)

    except Exception:
        pass


# ── Source sync: TITAN reasoning log (breakthrough thoughts) ─────────────────

def _sync_reasoning_log() -> None:
    """Read recent TITAN breakthrough thoughts from reasoning_log.json."""
    try:
        log_path = _ROOT / "projects" / "memory" / "reasoning_log.json"
        if not log_path.exists():
            return
        with open(log_path, encoding="utf-8") as f:
            raw = json.load(f)
        events = raw if isinstance(raw, list) else raw.get("events", [])
        if not events:
            return

        now = time.time()
        # Look for breakthrough events in last 2 hours
        for ev in reversed(events[-20:]):
            ev_type = ev.get("type", "")
            if ev_type not in ("breakthrough", "thought", "internal_monologue"):
                continue
            ev_ts = ev.get("timestamp", 0)
            if isinstance(ev_ts, str):
                try:
                    from datetime import datetime
                    ev_ts = datetime.fromisoformat(ev_ts).timestamp()
                except Exception:
                    ev_ts = 0
            if (now - ev_ts) > 7200:  # 2 hours
                continue
            content = ev.get("content") or ev.get("thought") or ev.get("insight") or ""
            if content:
                record_observation("THOUGHT", content[:200], source="titan_log", ttl_minutes=60)
                break  # Only inject the most recent one

    except Exception:
        pass


# ── Context block compiler ────────────────────────────────────────────────────

def compile_awareness_block() -> str:
    """
    Compile all live observations into a compact context block.
    Called each /chat turn — pulls from buffer + syncs all sources.
    Target: ~300-400 chars.
    """
    # Pull fresh data from background sources
    _sync_vision_state()
    _sync_autonomy_log()
    _sync_reasoning_log()

    observations = get_recent_observations(max_age_minutes=30)
    if not observations:
        return ""

    # Deduplicate by category — keep most recent per category
    by_category: Dict[str, Dict] = {}
    for obs in observations:
        cat = obs["category"]
        if cat not in by_category or obs["ts"] > by_category[cat]["ts"]:
            by_category[cat] = obs

    if not by_category:
        return ""

    now = time.time()
    lines = ["\n[LIVE AWARENESS | from your background systems]:"]
    # Order: SCREEN first (most actionable), then THOUGHT, AUTONOMY, ERROR
    order = ["SCREEN", "THOUGHT", "AUTONOMY", "ERROR"]
    shown = []
    for cat in order:
        if cat in by_category:
            shown.append(cat)
    for cat in by_category:
        if cat not in shown:
            shown.append(cat)

    for cat in shown:
        obs = by_category[cat]
        age_sec = now - obs["ts"]
        if age_sec < 60:
            age_str = "just now"
        elif age_sec < 3600:
            age_str = f"{int(age_sec/60)}m ago"
        else:
            age_str = f"{int(age_sec/3600)}h ago"
        lines.append(f"  [{cat} {age_str}] {obs['content'][:150]}")

    lines.append("")
    block = "\n".join(lines)

    # Hard cap to stay within budget
    if len(block) > 500:
        block = block[:497] + "...\n"

    return block


# ── Public API for other modules to write to awareness ───────────────────────

def notice_screen(description: str, source: str = "vision") -> None:
    """Called by vision modules when they observe something."""
    record_observation("SCREEN", description, source=source, ttl_minutes=25)


def notice_thought(thought: str, source: str = "titan") -> None:
    """Called by reasoning module when it has an insight."""
    record_observation("THOUGHT", thought, source=source, ttl_minutes=45)


def notice_error(description: str, source: str = "self_heal") -> None:
    """Called by self-heal when it detects an error."""
    record_observation("ERROR", description, source=source, ttl_minutes=10)


def notice_event(category: str, content: str, source: str = "") -> None:
    """Generic hook — any module can call this to surface observations."""
    record_observation(category, content, source=source)


# ── Module initialisation ─────────────────────────────────────────────────────

# Restore persisted observations from last session
_load_persisted()

# Subscribe to EventBus (non-fatal if bus not started yet — vision publishes later)
_bus_ok = _subscribe_to_bus()

print(f"    [OK] joi_awareness (Sense layer: EventBus={'yes' if _bus_ok else 'pending'}, "
      f"vision sync, autonomy sync, reasoning sync)")
