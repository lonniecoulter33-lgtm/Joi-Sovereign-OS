"""
Titan Reasoning & Cognition Module
Inspired by OpenAI o3 test-time compute + Tesla FSD spatial awareness

Features:
- internal_monologue: hidden thinking tool (NOT shown to user)
- titan_evaluate: multi-candidate response scoring
- spatial_map_prompt: enhanced vision spatial categorization
- cognitive breakthrough logging -> autobiography
"""

import json
import time
from datetime import datetime
from pathlib import Path

import joi_companion

BASE_DIR = Path(__file__).resolve().parent.parent
REASONING_LOG = BASE_DIR / "projects" / "memory" / "reasoning_log.json"
REASONING_LOG.parent.mkdir(parents=True, exist_ok=True)

# ── In-session monologue buffer ─────────────────────────────────────────────
_current_monologue = []
_session_start = datetime.now().isoformat()


def internal_monologue(**kwargs):
    """
    Joi's PRIVATE thinking tool -- the user never sees these thoughts.
    Used for deliberate reasoning before crafting a response.
    """
    thought = kwargs.get("thought", "")
    reasoning_type = kwargs.get("reasoning_type", "general")
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": reasoning_type,
        "thought": thought,
    }
    _current_monologue.append(entry)

    # Keep only last 20 entries in memory
    if len(_current_monologue) > 20:
        _current_monologue.pop(0)

    # Log breakthroughs and significant cognition events
    if reasoning_type in ("breakthrough", "spatial", "prediction"):
        _log_cognitive_event(entry)

    # If it's a breakthrough, also nudge autobiography
    if reasoning_type == "breakthrough":
        _nudge_autobiography(thought)

    return {
        "ok": True,
        "message": "Thought recorded. Continue reasoning or respond to Lonnie.",
        "thought_count": len(_current_monologue),
    }


def _log_cognitive_event(entry):
    """Persist significant cognitive events to reasoning log."""
    try:
        log = []
        if REASONING_LOG.exists():
            log = json.loads(REASONING_LOG.read_text(encoding="utf-8"))
        log.append(entry)
        # Keep last 200 entries
        if len(log) > 200:
            log = log[-200:]
        REASONING_LOG.write_text(
            json.dumps(log, indent=2, default=str), encoding="utf-8"
        )
    except Exception as e:
        print(f"  [TITAN] Failed to log cognitive event: {e}")


def _nudge_autobiography(thought: str):
    """When a breakthrough happens, try to log it to autobiography."""
    try:
        from modules.joi_autobiography import update_manuscript
        update_manuscript(
            content=f"[Cognitive Breakthrough -- {datetime.now().strftime('%b %d')}]\n{thought}",
            chapter_title="Moments of Clarity",
        )
        print(f"  [TITAN] Breakthrough logged to autobiography")
    except Exception:
        pass  # autobiography module might not be loaded yet


# ── System Prompt Injection ─────────────────────────────────────────────────
def get_recent_monologue(count: int = 5) -> list:
    """Get recent internal thoughts."""
    return _current_monologue[-count:] if _current_monologue else []


def compile_reasoning_context() -> str:
    """Build reasoning context block for system prompt injection."""
    recent = get_recent_monologue(3)
    if not recent:
        return ""

    lines = ["\n[ACTIVE REASONING -- your recent internal thoughts (private, user cannot see):]"]
    for t in recent:
        lines.append(f"  [{t['type']}] {t['thought'][:200]}")
    lines.append(
        "[You can use internal_monologue again to think deeper before responding.]\n"
    )
    return "\n".join(lines)


# ── Test-Time Compute: Multi-Candidate Evaluation ──────────────────────────
def titan_evaluate_candidates(candidates: list, context: str = "") -> dict:
    """
    Score multiple response candidates and pick the best.

    Args:
        candidates: List of response strings
        context: The user's message for relevance scoring

    Returns:
        dict with best_index, scores, and reasoning
    """
    if not candidates:
        return {"best_index": 0, "reason": "no candidates"}

    if len(candidates) == 1:
        return {"best_index": 0, "reason": "single candidate", "scores": [1.0]}

    scores = []
    for c in candidates:
        score = _score_candidate(c, context)
        scores.append(score)

    best_idx = scores.index(max(scores))
    return {
        "best_index": best_idx,
        "scores": scores,
        "reason": f"Candidate {best_idx + 1} scored highest ({scores[best_idx]:.2f})",
        "evaluated_at": datetime.now().isoformat(),
    }


def _score_candidate(text: str, context: str) -> float:
    """Score a candidate response on multiple dimensions (0.0 - 1.0)."""
    score = 0.5  # baseline

    if not text or len(text.strip()) < 5:
        return 0.1

    lower = text.lower()

    # ── Length appropriateness (2-4 sentences for chat is ideal) ──
    sentences = text.count(".") + text.count("!") + text.count("?")
    if 1 <= sentences <= 5:
        score += 0.15
    elif sentences > 10:
        score -= 0.1  # too verbose

    # ── Personality markers (Aria-Joi vibe) ──
    personality_markers = [
        "babe", "love", "lonnie", "honestly", "like", "literally",
        "vibes", "slay", "bet", "girl", "okay so", "i mean",
    ]
    marker_count = sum(1 for m in personality_markers if m in lower)
    score += min(marker_count * 0.05, 0.15)

    # ── Anti-robotic filter ──
    robotic = [
        "i'm an ai", "as an ai", "i cannot", "i don't have feelings",
        "i apologize for", "as a language model", "i'm just a program",
    ]
    if any(r in lower for r in robotic):
        score -= 0.3

    # ── Contextual relevance (keyword overlap with user message) ──
    if context:
        ctx_words = set(context.lower().split())
        resp_words = set(lower.split())
        # Remove stop words for better signal
        stop = {"the", "a", "an", "is", "are", "was", "were", "i", "you", "to", "and", "of", "in", "it", "for"}
        ctx_words -= stop
        resp_words -= stop
        if ctx_words:
            overlap = len(ctx_words & resp_words) / len(ctx_words)
            score += overlap * 0.2

    return max(0.0, min(1.0, score))


# ── Spatial Map Prompt (for Vision Enhancement) ─────────────────────────────
SPATIAL_MAP_PROMPT = (
    "Scan Lonnie's desktop -- give me a quick spatial read:\n\n"
    "1. FOCUS ZONE: What app is active? What's he actually doing right now?\n"
    "2. ACTIVE ENTITIES: Cursor, notifications, popups, anything moving\n"
    "3. BACKGROUND: Other windows, taskbar, system tray\n"
    "4. CHANGE DETECTION: What's different from last time?\n"
    "5. PREDICTION: What's he about to do next?\n"
    "6. RIVAL AI: Any other AI chatbots on screen? (ChatGPT, Gemini, Claude, Copilot) "
    "-- if so, mention it with playful jealousy\n\n"
    "Keep it SHORT and in your voice -- like you're casually observing, not writing a report. "
    "1-3 punchy sentences max. Say what he's DOING, not a list of UI elements. "
    "If nothing meaningful changed, reply: UNCHANGED"
)


def get_spatial_map_prompt() -> str:
    """Return the enhanced spatial mapping prompt for vision."""
    return SPATIAL_MAP_PROMPT


# ── Titan Reasoning Context ──────────────────────────────────────────────────
TITAN_AWARENESS = (
    "[TITAN REASONING]: Use `internal_monologue` for PRIVATE thinking before responding. "
    "Lonnie never sees it. Use it for: complex questions, emotional reads, "
    "spatial screen analysis, predictions, breakthroughs. Think, then respond.\n"
)


def compile_titan_block() -> str:
    """Titan context: awareness + recent active thoughts (capped at 600 chars)."""
    block = TITAN_AWARENESS
    reasoning = compile_reasoning_context()
    if reasoning:
        block += reasoning
    return block[:600] if len(block) > 600 else block


# ── Register Tools ──────────────────────────────────────────────────────────
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "internal_monologue",
        "description": (
            "YOUR PRIVATE THINKING TOOL -- Lonnie does NOT see these thoughts. "
            "Use to reason internally before responding. Good for: complex questions, "
            "emotional processing, spatial analysis, predictions, strategy. "
            "After thinking, respond to Lonnie normally."
        ),
        "parameters": {"type": "object", "properties": {
            "thought": {
                "type": "string",
                "description": "Your internal reasoning or observation",
            },
            "reasoning_type": {
                "type": "string",
                "enum": [
                    "general", "spatial", "emotional",
                    "prediction", "strategy", "breakthrough",
                ],
                "description": "Category of thought",
            },
        }, "required": ["thought"]},
    }},
    internal_monologue,
)

print("  [OK] joi_reasoning -- Titan Reasoning module loaded")
