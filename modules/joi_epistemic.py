"""
modules/joi_epistemic.py

Joi v4.0 — Epistemic Safety Layer (Upgrade IV)
===============================================
Gives Joi structured awareness of uncertainty.

Every generated claim can be tagged internally with:
  - confidence_level (0.0–1.0)
  - source_type: retrieved | inferred | speculative
  - verification_status: verified | unverified | contested

Speculative mode trigger (any of these):
  - confidence < SPECULATIVE_THRESHOLD
  - no retrieval support
  - claim conflicts with prior memory

Decision Thresholding:
  - Autonomous actions require confidence >= EXECUTION_THRESHOLD
  - Below threshold → request human confirmation

Hallucination Feedback Loop:
  - User correction detected → penalize ReinforcementGraph node
  - Lower epistemic certainty of related memory entries

This module is injected into the response pipeline via try/except in
joi_orchestrator.py / joi_companion.py — fully additive if not loaded.
"""

import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR   = Path(__file__).resolve().parent.parent
DATA_DIR   = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
STATE_PATH = DATA_DIR / "epistemic_state.json"

# ── Thresholds ─────────────────────────────────────────────────────────────────
SPECULATIVE_THRESHOLD = 0.55   # below → speculative mode
EXECUTION_THRESHOLD   = 0.75   # below → require human confirmation for autonomous actions
RETRIEVAL_BOOST       = 0.15   # confidence boost when claim has retrieval support

# Source type → base confidence adjustment
SOURCE_CONFIDENCE: Dict[str, float] = {
    "retrieved":   0.85,
    "inferred":    0.60,
    "speculative": 0.35,
}

# Correction keywords (user saying the AI was wrong)
CORRECTION_PREFIXES = (
    "no,", "no ", "actually,", "actually ", "that's wrong",
    "wrong,", "wrong ", "incorrect", "not right", "stop.",
    "wait,", "nope", "that's not", "i said", "try again",
)


# ── Data Structures ────────────────────────────────────────────────────────────

@dataclass
class EpistemicTag:
    """Epistemic metadata for a claim or action."""
    confidence_level:    float = 0.7          # 0.0–1.0
    source_type:         str   = "retrieved"  # retrieved | inferred | speculative
    verification_status: str   = "unverified" # verified | unverified | contested
    has_retrieval:       bool  = False
    reasoning:           str   = ""
    created_at:          str   = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    @property
    def is_speculative(self) -> bool:
        return (
            self.confidence_level < SPECULATIVE_THRESHOLD
            or self.source_type == "speculative"
            or self.verification_status == "contested"
        )

    @property
    def allows_autonomous_action(self) -> bool:
        return self.confidence_level >= EXECUTION_THRESHOLD

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["is_speculative"] = self.is_speculative
        d["allows_autonomous_action"] = self.allows_autonomous_action
        return d


# ── EpistemicEngine ────────────────────────────────────────────────────────────

class EpistemicEngine:
    """
    Core epistemic safety engine.

    Usage (in response pipeline, additive):
        try:
            from modules.joi_epistemic import get_epistemic_engine
            engine = get_epistemic_engine()
            tag = engine.tag_claim(reply_text, context={"has_retrieval": True})
            if tag.is_speculative:
                modifier = engine.get_response_modifier(tag)
                # prepend modifier to system prompt for this response
        except Exception:
            pass  # graceful degradation
    """

    def __init__(self):
        self._speculative_mode: bool = False
        self._current_tag: Optional[EpistemicTag] = None
        self._action_log: List[Dict] = []
        self._correction_count: int = 0

    # ── Claim Tagging ──────────────────────────────────────────────────────────

    def tag_claim(
        self,
        claim_text: str,
        context: Optional[Dict] = None,
    ) -> EpistemicTag:
        """
        Analyze a claim and return its epistemic tag.

        Context dict can include:
          has_retrieval (bool) — was this claim backed by a vector memory retrieval?
          source_type (str)   — override source type
          prior_conflicts (bool) — does this conflict with a prior memory?
        """
        ctx = context or {}
        has_retrieval  = bool(ctx.get("has_retrieval", False))
        source_type    = str(ctx.get("source_type", "inferred"))
        prior_conflicts = bool(ctx.get("prior_conflicts", False))

        # Base confidence from source type
        base_conf = SOURCE_CONFIDENCE.get(source_type, 0.6)

        # Boost for retrieval support
        if has_retrieval:
            base_conf = min(1.0, base_conf + RETRIEVAL_BOOST)
            source_type = "retrieved"

        # Penalty for conflicting priors
        if prior_conflicts:
            base_conf = max(0.1, base_conf - 0.20)

        # Speculative heuristics in the claim text itself
        speculative_markers = [
            "i think", "i believe", "probably", "might be", "could be",
            "not sure", "unclear", "i'm guessing", "possibly", "perhaps",
            "it seems", "may have",
        ]
        claim_lower = claim_text.lower()
        if any(m in claim_lower for m in speculative_markers):
            base_conf = max(0.1, base_conf - 0.10)
            source_type = "speculative" if base_conf < SPECULATIVE_THRESHOLD else source_type

        verification_status = "verified" if has_retrieval and not prior_conflicts else \
                              "contested" if prior_conflicts else "unverified"

        tag = EpistemicTag(
            confidence_level=round(base_conf, 3),
            source_type=source_type,
            verification_status=verification_status,
            has_retrieval=has_retrieval,
            reasoning=(
                f"source={source_type}, retrieval={has_retrieval}, "
                f"conflicts={prior_conflicts}"
            ),
        )
        self._current_tag = tag
        self._speculative_mode = tag.is_speculative
        return tag

    # ── Response Modifier ──────────────────────────────────────────────────────

    def get_response_modifier(self, tag: EpistemicTag) -> str:
        """
        Return a system-prompt tone modifier when speculative mode is active.
        Injected at the start of the response assembly system block.
        """
        if not tag.is_speculative:
            return ""

        if tag.confidence_level < 0.30:
            return (
                "[EPISTEMIC SAFETY: Low confidence. Present this as uncertain. "
                "Offer to verify with a tool or research. Do NOT state as fact.]"
            )
        elif tag.confidence_level < SPECULATIVE_THRESHOLD:
            return (
                "[EPISTEMIC SAFETY: Moderate uncertainty. Use hedged language "
                "(likely/probably/my best read is). Suggest verification if important.]"
            )
        else:
            return (
                "[EPISTEMIC SAFETY: Inferred claim — no retrieval support. "
                "Flag as inference, not established fact.]"
            )

    # ── Decision Thresholding ──────────────────────────────────────────────────

    def check_action_threshold(
        self, action_name: str, confidence: float
    ) -> Tuple[bool, str]:
        """
        Gate autonomous actions by confidence threshold.

        Returns:
            (True, "")                         — action allowed
            (False, "reason for confirmation") — action blocked, needs human OK
        """
        if confidence >= EXECUTION_THRESHOLD:
            self._log_action(action_name, confidence, allowed=True)
            return True, ""

        reason = (
            f"Action '{action_name}' requires confidence >= {EXECUTION_THRESHOLD:.0%} "
            f"but current estimate is {confidence:.0%}. "
            f"Please confirm you want me to proceed."
        )
        self._log_action(action_name, confidence, allowed=False, reason=reason)
        return False, reason

    def _log_action(self, action: str, conf: float, allowed: bool, reason: str = ""):
        entry = {
            "ts": datetime.now().isoformat(),
            "action": action,
            "confidence": conf,
            "allowed": allowed,
            "reason": reason,
        }
        self._action_log.append(entry)
        if len(self._action_log) > 200:
            self._action_log = self._action_log[-200:]

    # ── Hallucination Feedback Loop ────────────────────────────────────────────

    def record_hallucination_correction(
        self,
        user_correction: str,
        related_claim: str = "",
        related_skill: str = "reasoning",
    ) -> Dict:
        """
        Called when a user correction is detected.
        Penalizes the ReinforcementGraph node for the related skill.
        Returns a summary of what was penalized.
        """
        self._correction_count += 1
        ts = datetime.now().isoformat()

        # Penalize ReinforcementGraph
        try:
            from modules.joi_reinforcement_graph import get_reinforcement_graph
            graph = get_reinforcement_graph()
            graph.record_outcome(
                node_id=related_skill,
                node_type="skill",
                success=False,
                hallucination=True,
            )
            graph_penalized = True
        except Exception as ge:
            graph_penalized = False
            print(f"  [EPISTEMIC] ReinforcementGraph penalty failed: {ge}")

        # Persist correction event
        try:
            events = []
            if STATE_PATH.exists():
                events = json.loads(STATE_PATH.read_text(encoding="utf-8")).get("corrections", [])
            events.append({
                "ts": ts, "correction": user_correction[:200],
                "related_claim": related_claim[:200], "related_skill": related_skill,
                "graph_penalized": graph_penalized,
            })
            state = {"corrections": events[-100:], "correction_count": self._correction_count}
            STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")
        except Exception:
            pass

        print(f"  [EPISTEMIC] Hallucination correction recorded "
              f"(skill={related_skill}, graph_penalized={graph_penalized})")

        return {
            "ok": True,
            "correction_recorded": True,
            "graph_penalized": graph_penalized,
            "total_corrections": self._correction_count,
        }

    def detect_correction(self, user_message: str) -> bool:
        """Return True if user message looks like a correction of Joi's previous reply."""
        lower = user_message.lower().strip()
        return any(lower.startswith(p) or lower == p.strip() for p in CORRECTION_PREFIXES)

    # ── Status ─────────────────────────────────────────────────────────────────

    def get_status(self) -> Dict[str, Any]:
        tag_dict = self._current_tag.to_dict() if self._current_tag else None
        recent_actions = self._action_log[-10:]
        corrections_data = {}
        try:
            if STATE_PATH.exists():
                corrections_data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
        return {
            "speculative_mode": self._speculative_mode,
            "current_tag": tag_dict,
            "speculative_threshold": SPECULATIVE_THRESHOLD,
            "execution_threshold": EXECUTION_THRESHOLD,
            "total_corrections": corrections_data.get("correction_count", self._correction_count),
            "recent_actions": recent_actions,
        }


# ── Singleton ──────────────────────────────────────────────────────────────────
_engine: Optional[EpistemicEngine] = None


def get_epistemic_engine() -> EpistemicEngine:
    global _engine
    if _engine is None:
        _engine = EpistemicEngine()
    return _engine


# ── Tool Functions ─────────────────────────────────────────────────────────────

def get_epistemic_status(**kwargs) -> Dict:
    """Get current Epistemic Safety Layer status and thresholds."""
    return {"ok": True, **get_epistemic_engine().get_status()}


def record_epistemic_correction(**kwargs) -> Dict:
    """Record a user correction to trigger hallucination penalty loop."""
    engine = get_epistemic_engine()
    return engine.record_hallucination_correction(
        user_correction=str(kwargs.get("correction", "")),
        related_claim=str(kwargs.get("related_claim", "")),
        related_skill=str(kwargs.get("related_skill", "reasoning")),
    )


# ── Tool + Route Registration ──────────────────────────────────────────────────
try:
    import joi_companion
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "get_epistemic_status",
            "description": (
                "Get the Epistemic Safety Layer status: current speculative mode flag, "
                "confidence thresholds, and recent decision gate results."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []}
        }},
        get_epistemic_status
    )
    print("  [OK] joi_epistemic loaded (EpistemicEngine active)")
except Exception as _e:
    print(f"  [WARN] joi_epistemic: tool registration skipped ({_e})")

try:
    import joi_companion

    def _ep_route():
        from flask import jsonify
        return jsonify(get_epistemic_status())

    joi_companion.register_route("/epistemic/status", ["GET"], _ep_route, "epistemic_status_route")
except Exception:
    pass
