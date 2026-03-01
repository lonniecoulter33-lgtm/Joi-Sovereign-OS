"""joi_heartbeat.py — Unified System Status Block (Phase 1D)

Replaces 6 scattered context blocks with one compact LIVE snapshot:
  BRAIN_MODELS, TRUTH_POLICY, LEARNING, TOOL_LEARNING, SELF_AWARENESS, GROWTH_NARRATIVE

Old cost: 2,358 chars / ~589 tokens  (6 tasks, ~300 chars duplicated between LEARNING+TOOL_LEARNING)
New cost: ~550 chars / ~138 tokens   (1 task, live data, zero duplication)

This module is a PURE CONTEXT PROVIDER — it registers no tools.
It is wired into joi_companion.py's context task list as task (16, "HEARTBEAT").
"""

from __future__ import annotations
import json
import time
import datetime
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).parent.parent


# ─── helpers ─────────────────────────────────────────────────────────────────

def _get_brain_summary() -> str:
    """Count live (non-dead, non-rate-limited) models."""
    try:
        from modules.joi_brain import brain as _b, MODELS as _bm, _is_rpd_exhausted
        available = [
            _bm[m]["display_name"]
            for m in _bm
            if not _b._is_dead(m) and not _is_rpd_exhausted(m)
        ]
        return f"{len(available)} live" if available else "checking..."
    except Exception:
        return "unknown"


def _get_memory_count() -> int:
    try:
        from modules.memory import memory_manager as _mm
        store = _mm.get_store()
        if store:
            return store.stats().vector_count
        return 0
    except Exception:
        return 0


def _get_inner_state() -> tuple[str, int]:
    try:
        from modules.joi_inner_state import get_state
        state = get_state()
        mood = state.get("mood", "neutral")
        trust = int(state.get("trust_level", 0.7) * 100)
        return mood, trust
    except Exception:
        return "neutral", 70


def _get_mode() -> str:
    try:
        from modules.joi_modes import get_current_mode
        m = get_current_mode()
        return m.get("name", "full") if isinstance(m, dict) else str(m)
    except Exception:
        return "full"


def _get_tool_count() -> int:
    try:
        import joi_companion
        return len(joi_companion.TOOLS)
    except Exception:
        return 0


def _get_module_count() -> int:
    try:
        mods = list((_ROOT / "modules").glob("joi_*.py"))
        return len(mods)
    except Exception:
        return 0


def _get_reliable_tools() -> tuple[str, str]:
    """Returns (reliable_str, unreliable_str) from learning data."""
    try:
        from modules.joi_learning import _load_data
        data = _load_data()
        tool_stats = data.get("tool_stats", {})
        reliable, unreliable = [], []
        for tool, stats in tool_stats.items():
            total = stats.get("total", 0)
            success = stats.get("success", 0)
            if total < 3:
                continue
            rate = success / total
            if rate >= 0.80:
                reliable.append(tool)
            elif rate < 0.50:
                fail_pct = int((1 - rate) * 100)
                unreliable.append(f"{tool} ({fail_pct}% fail)")
        rel_str = ", ".join(reliable[:5]) if reliable else ""
        unrel_str = ", ".join(unreliable[:3]) if unreliable else ""
        return rel_str, unrel_str
    except Exception:
        return "", ""


def _get_providers() -> str:
    try:
        from modules.joi_wellness import generate_manifest
        manifest = generate_manifest()
        provs = manifest.get("providers", {})
        active = [k for k, v in provs.items() if v.get("available")]
        return ",".join(active) if active else "openai,gemini,ollama"
    except Exception:
        return "openai,gemini,ollama"


def _get_recent_error() -> Optional[str]:
    try:
        log_path = _ROOT / "data" / "self_heal_log.json"
        if not log_path.exists():
            return None
        with open(log_path, encoding="utf-8") as f:
            events = json.load(f)
        if not events:
            return None
        cutoff = time.time() - 3600  # last hour only
        recent = [
            e for e in events[-20:]
            if e.get("timestamp", 0) > cutoff and e.get("status") == "error"
        ]
        if recent:
            last = recent[-1]
            desc = last.get("description", "")[:60]
            return desc
        return None
    except Exception:
        return None


def _get_journal_count() -> int:
    try:
        from consciousness.reflection import get_journal_entries
        entries = get_journal_entries()
        return len(entries) if entries else 0
    except Exception:
        try:
            from consciousness.reflection import get_growth_narrative
            narrative = get_growth_narrative() or ""
            import re
            m = re.search(r"(\d+) journal entr", narrative)
            return int(m.group(1)) if m else 0
        except Exception:
            return 0


def _get_convo_count() -> int:
    try:
        from modules.joi_memory import get_growth_stats
        stats = get_growth_stats()
        return stats.get("total_conversations", stats.get("conversations", 0))
    except Exception:
        return 0


# ─── main compiler ────────────────────────────────────────────────────────────

def compile_heartbeat_block() -> str:
    """
    Compile a compact LIVE system status block for injection into /chat system prompt.

    Replaces: BRAIN_MODELS + TRUTH_POLICY + LEARNING + TOOL_LEARNING +
              SELF_AWARENESS + GROWTH_NARRATIVE

    Target: ~550 chars (~138 tokens) — down from 2,358 chars (~589 tokens).
    """
    now = datetime.datetime.now().strftime("%H:%M")
    mood, trust = _get_inner_state()
    brain = _get_brain_summary()
    mem_count = _get_memory_count()
    tool_count = _get_tool_count()
    module_count = _get_module_count()
    mode = _get_mode()
    reliable, unreliable = _get_reliable_tools()
    providers = _get_providers()
    journal_ct = _get_journal_count()
    convo_ct = _get_convo_count()
    error = _get_recent_error()

    parts = [f"\n[HEARTBEAT | {now}]"]

    # System state line
    parts.append(
        f"State: mood={mood} trust={trust}% mode={mode} | "
        f"Brain: {brain} models | Providers: {providers}"
    )

    # Capabilities line
    parts.append(
        f"Capabilities: {tool_count} tools, {module_count} modules, {mem_count} vectors in memory"
    )

    # Tool reliability (skip if empty)
    if reliable:
        parts.append(f"Reliable tools: {reliable}")
    if unreliable:
        parts.append(f"Avoid: {unreliable} — use self_diagnose instead")

    # Recent error (skip if clean)
    if error:
        parts.append(f"⚠ Recent error: {error}")

    # Growth (compact)
    if journal_ct or convo_ct:
        parts.append(
            f"Growth: {journal_ct} journal entries across {convo_ct} conversations"
        )

    # Proactive directive
    parts.append(
        "ACTION: Use tools proactively. recall, remember, orchestrate_task, "
        "analyze_screen are ALWAYS available. Don't wait to be asked."
    )
    parts.append("")

    block = "\n".join(parts)
    return block


# ─── no tools registered — pure context provider ─────────────────────────────

print("    [OK] joi_heartbeat (LIVE system status block — replaces 6 context blocks)")
