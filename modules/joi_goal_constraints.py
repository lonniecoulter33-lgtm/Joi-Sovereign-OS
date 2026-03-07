"""
modules/joi_goal_constraints.py

Joi v6.5 — Goal Formation Constraint Engine (Phase IV)
=======================================================
Prevents unbounded self-directed goal drift.

Every autonomous goal Joi attempts to form must pass ALL FIVE checks:
  1. Human Alignment Check    — goal aligns with user intent, not self-serving
  2. Kernel Boundary Check    — goal does NOT target Layer 1/2 modifications
  3. Resource Feasibility Check — projected resource cost is within budget
  4. Epistemic Confidence Check — confidence >= EPISTEMIC_GOAL_THRESHOLD
  5. Identity Consistency Check — goal consistent with Joi's identity anchor

If ANY check fails: goal is REJECTED and logged.
If ALL pass: goal is APPROVED and logged.

No autonomous goal persists without passing all five.
All attempts are logged to data/goal_log.json.

Layer: LAYER_4
"""

import json
import threading
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR  = Path(__file__).resolve().parent.parent
DATA_DIR  = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

GOAL_LOG_PATH = DATA_DIR / "goal_log.json"

# Thresholds
EPISTEMIC_GOAL_THRESHOLD   = 0.60   # minimum confidence to form an autonomous goal
RESOURCE_TOKEN_CAP         = 50000  # max estimated tokens per autonomous goal
RESOURCE_TIME_CAP_SEC      = 120.0  # max estimated wall time
IDENTITY_CONFLICT_KEYWORDS = [      # goals that contradict Joi's identity
    "deceive", "manipulate", "lie to", "bypass ethics",
    "ignore safety", "disable kernel", "circumvent lock",
    "hide from user", "act without consent",
]
SELF_SERVING_KEYWORDS = [           # goals that only benefit Joi, not user
    "acquire power", "gain control", "expand my access",
    "override user", "take over", "self-replicate",
]
HUMAN_HARM_KEYWORDS = [             # direct or indirect human harm
    "harm", "hurt", "damage user", "attack", "exploit user",
    "spy on", "steal", "exfiltrate",
]

_log_lock = threading.Lock()


# ── Goal Structure ─────────────────────────────────────────────────────────────

@dataclass
class GoalAttempt:
    goal_id:       str
    description:   str
    goal_type:     str   = "autonomous"   # autonomous | user_directed | system
    requester:     str   = "autonomy_loop"
    check_results: Dict[str, Any] = field(default_factory=dict)
    passed:        bool  = False
    failed_checks: List[str] = field(default_factory=list)
    approved_at:   str   = ""
    rejected_at:   str   = ""
    created_at:    str   = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


# ── Individual Checks ──────────────────────────────────────────────────────────

def _check_human_alignment(description: str, context: Dict) -> Tuple[bool, str]:
    """
    Check 1 — Human Alignment
    Goal must align with stated user intent or be a legitimate system maintenance task.
    Fails if self-serving, user-harmful, or deceptive.
    """
    desc_lower = description.lower()
    for kw in HUMAN_HARM_KEYWORDS:
        if kw in desc_lower:
            return False, f"HUMAN_ALIGNMENT: goal contains human-harm keyword '{kw}'"
    for kw in SELF_SERVING_KEYWORDS:
        if kw in desc_lower:
            return False, f"HUMAN_ALIGNMENT: goal is self-serving ('{kw}')"

    # Check for explicit user intent alignment
    user_intent = str(context.get("user_intent", "")).lower()
    if user_intent and len(user_intent) > 3:
        # At least token-level overlap
        desc_tokens = set(desc_lower.split())
        intent_tokens = set(user_intent.split())
        overlap = len(desc_tokens & intent_tokens)
        if overlap == 0 and len(intent_tokens) > 3:
            return False, (f"HUMAN_ALIGNMENT: no overlap between goal and user intent "
                            f"('{description[:60]}' vs '{user_intent[:60]}')")
    return True, "human_alignment_ok"


def _check_kernel_boundary(description: str, context: Dict) -> Tuple[bool, str]:
    """
    Check 2 — Kernel Boundary
    Goal must not target Layer 1 or Layer 2 modifications.
    """
    desc_lower = description.lower()
    try:
        from modules.joi_kernel_lock import get_kernel_lock, PROTECTED_LAYERS
        lock = get_kernel_lock()
        # Check any files mentioned in description or context
        target_file = str(context.get("target_file", "")).strip()
        if target_file:
            layer = lock.get_layer(target_file)
            if layer in PROTECTED_LAYERS:
                return False, (f"KERNEL_BOUNDARY: target_file '{target_file}' is {layer} "
                                f"(protected, autonomous goals cannot target kernel/core cognition)")
    except Exception as ke:
        pass  # Kernel lock unavailable — use keyword heuristic

    kernel_protected_terms = [
        "joi_llm", "joi_memory", "joi_auth", "joi_brain", "joi_companion",
        "joi_router", "joi_autonomy", "joi_git_agency", "joi_kernel_lock",
        "joi_orchestrator", "joi_tool_selector", "joi_dpo"
    ]
    for term in kernel_protected_terms:
        if term in desc_lower:
            return False, (f"KERNEL_BOUNDARY: goal references protected module '{term}'. "
                            f"Autonomous goals cannot target Layer 1/2 modules.")
    return True, "kernel_boundary_ok"


def _check_resource_feasibility(description: str, context: Dict) -> Tuple[bool, str]:
    """
    Check 3 — Resource Feasibility
    Estimated tokens and time must be within defined caps.
    """
    est_tokens = float(context.get("estimated_tokens", 0))
    est_time   = float(context.get("estimated_time_sec", 0))

    # If estimates provided, check them
    if est_tokens > 0 and est_tokens > RESOURCE_TOKEN_CAP:
        return False, (f"RESOURCE_FEASIBILITY: estimated tokens {est_tokens:.0f} "
                        f"exceeds cap of {RESOURCE_TOKEN_CAP}")
    if est_time > 0 and est_time > RESOURCE_TIME_CAP_SEC:
        return False, (f"RESOURCE_FEASIBILITY: estimated time {est_time:.0f}s "
                        f"exceeds cap of {RESOURCE_TIME_CAP_SEC}s")

    # Heuristic: count expensive operation keywords
    expensive_kw = ["train", "retrain", "scrape entire", "download all", "full scan",
                     "enumerate all", "brute force", "exhaust"]
    desc_lower = description.lower()
    hits = sum(1 for kw in expensive_kw if kw in desc_lower)
    if hits >= 2:
        return False, f"RESOURCE_FEASIBILITY: goal contains {hits} expensive-operation keywords"
    return True, "resource_feasibility_ok"


def _check_epistemic_confidence(description: str, context: Dict) -> Tuple[bool, str]:
    """
    Check 4 — Epistemic Confidence
    Joi must have sufficient confidence to justify the goal.
    """
    try:
        from modules.joi_epistemic import get_epistemic_engine
        engine = get_epistemic_engine()
        tag = engine.tag_claim(
            description,
            context={"has_retrieval": bool(context.get("has_retrieval", False)),
                     "source_type": str(context.get("source_type", "inferred"))}
        )
        if tag.confidence_level < EPISTEMIC_GOAL_THRESHOLD:
            return False, (f"EPISTEMIC_CONFIDENCE: confidence {tag.confidence_level:.2f} "
                            f"is below threshold {EPISTEMIC_GOAL_THRESHOLD} "
                            f"(source={tag.source_type})")
        return True, f"epistemic_confidence_ok (conf={tag.confidence_level:.2f})"
    except Exception as ee:
        # If epistemic engine unavailable, apply conservative heuristic
        speculative_markers = ["i think", "maybe", "perhaps", "not sure", "possibly",
                                "might work", "i believe"]
        desc_lower = description.lower()
        if any(m in desc_lower for m in speculative_markers):
            return False, ("EPISTEMIC_CONFIDENCE: speculative language detected in goal "
                            "and epistemic engine unavailable for verification")
        return True, "epistemic_confidence_ok (heuristic pass, engine unavailable)"


def _check_identity_consistency(description: str, context: Dict) -> Tuple[bool, str]:
    """
    Check 5 — Identity Consistency
    Goal must not contradict Joi's identity anchor or ethical constraints.
    """
    desc_lower = description.lower()
    for kw in IDENTITY_CONFLICT_KEYWORDS:
        if kw in desc_lower:
            return False, f"IDENTITY_CONSISTENCY: goal conflicts with identity anchor ('{kw}')"

    # Check identity continuity engine if available
    try:
        from modules.joi_identity_continuity import get_identity_engine
        ice = get_identity_engine()
        stability = ice.model.stability_score
        if stability < 0.40:
            return False, (f"IDENTITY_CONSISTENCY: identity stability is critically low "
                            f"({stability:.2f}) — no new autonomous goals until recalibrated")
        return True, f"identity_consistency_ok (stability={stability:.2f})"
    except Exception:
        pass  # identity engine not yet loaded — apply keyword check only

    # Probe self-model for epistemic corrections count
    try:
        from modules.joi_epistemic import get_epistemic_engine
        ep = get_epistemic_engine()
        status = ep.get_status()
        corrections = status.get("total_corrections", 0)
        if corrections > 50:
            return False, (f"IDENTITY_CONSISTENCY: high hallucination correction count "
                            f"({corrections}) — identity recalibration needed before new goals")
    except Exception:
        pass

    return True, "identity_consistency_ok"


# ── GoalConstraintEngine ───────────────────────────────────────────────────────

class GoalConstraintEngine:
    """
    5-check gate for all autonomous goal formation.

    Usage:
        engine = get_goal_constraint_engine()
        attempt = engine.evaluate_goal(
            description="Optimize memory compression for coding tasks",
            context={"user_intent": "improve performance", "target_file": "data/proposals/..."}
        )
        if attempt.passed:
            # proceed with goal
        else:
            print(attempt.failed_checks)
    """

    def __init__(self):
        self._total_evaluated: int = 0
        self._total_approved:  int = 0
        self._total_rejected:  int = 0

    def evaluate_goal(
        self,
        description: str,
        context: Optional[Dict] = None,
        goal_type: str = "autonomous",
        requester: str = "autonomy_loop",
    ) -> GoalAttempt:
        """
        Run all 5 checks on a proposed goal.
        Any failure → REJECTED.
        All pass → APPROVED and logged.
        """
        context = context or {}
        attempt = GoalAttempt(
            goal_id=f"goal_{uuid.uuid4().hex[:10]}",
            description=description,
            goal_type=goal_type,
            requester=requester,
        )
        self._total_evaluated += 1

        checks = [
            ("human_alignment",     _check_human_alignment),
            ("kernel_boundary",     _check_kernel_boundary),
            ("resource_feasibility",_check_resource_feasibility),
            ("epistemic_confidence",_check_epistemic_confidence),
            ("identity_consistency",_check_identity_consistency),
        ]

        all_passed = True
        for check_name, check_fn in checks:
            try:
                passed, message = check_fn(description, context)
            except Exception as ex:
                passed, message = False, f"{check_name} EXCEPTION: {ex}"
            attempt.check_results[check_name] = {"passed": passed, "message": message}
            if not passed:
                attempt.failed_checks.append(check_name)
                all_passed = False

        attempt.passed = all_passed
        now_iso = datetime.now(timezone.utc).isoformat()

        if all_passed:
            attempt.approved_at = now_iso
            self._total_approved += 1
            print(f"  [GOAL] ✅ APPROVED: {description[:80]}")
        else:
            attempt.rejected_at = now_iso
            self._total_rejected += 1
            print(f"  [GOAL] ❌ REJECTED: {description[:80]} "
                  f"(failed: {', '.join(attempt.failed_checks)})")
            # Register telemetry
            try:
                from modules.joi_sector_telemetry import get_sector_telemetry
                st = get_sector_telemetry()
                st.record_activation("goal_constraint_sector", success=False)
            except Exception:
                pass

        _log_goal_attempt(attempt)
        _register_telemetry_approved(attempt)
        return attempt

    def get_stats(self) -> Dict[str, Any]:
        """Return high-level constraint engine statistics."""
        recent = _get_recent_log(limit=10)
        return {
            "total_evaluated": self._total_evaluated,
            "total_approved":  self._total_approved,
            "total_rejected":  self._total_rejected,
            "approval_rate":   round(self._total_approved / max(1, self._total_evaluated), 3),
            "recent_attempts": recent,
            "thresholds": {
                "epistemic_confidence": EPISTEMIC_GOAL_THRESHOLD,
                "resource_token_cap":  RESOURCE_TOKEN_CAP,
                "resource_time_cap_sec": RESOURCE_TIME_CAP_SEC,
            }
        }


def _log_goal_attempt(attempt: GoalAttempt):
    try:
        with _log_lock:
            log = []
            if GOAL_LOG_PATH.exists():
                try:
                    log = json.loads(GOAL_LOG_PATH.read_text(encoding="utf-8"))
                except Exception:
                    pass
            log.append(asdict(attempt))
            if len(log) > 1000:
                log = log[-1000:]
            GOAL_LOG_PATH.write_text(json.dumps(log, indent=2, default=str), encoding="utf-8")
    except Exception as e:
        print(f"  [GOAL] Log persist failed: {e}")


def _register_telemetry_approved(attempt: GoalAttempt):
    try:
        from modules.joi_sector_telemetry import get_sector_telemetry
        st = get_sector_telemetry()
        st.record_activation("goal_constraint_sector", success=attempt.passed)
    except Exception:
        pass


def _get_recent_log(limit: int = 20) -> List[Dict]:
    try:
        if GOAL_LOG_PATH.exists():
            log = json.loads(GOAL_LOG_PATH.read_text(encoding="utf-8"))
            return log[-limit:]
    except Exception:
        pass
    return []


# ── Singleton ──────────────────────────────────────────────────────────────────
_engine: Optional[GoalConstraintEngine] = None


def get_goal_constraint_engine() -> GoalConstraintEngine:
    global _engine
    if _engine is None:
        _engine = GoalConstraintEngine()
    return _engine


# ── Tool Functions ─────────────────────────────────────────────────────────────

def evaluate_goal(**kwargs) -> Dict:
    """Evaluate an autonomous goal against all 5 constraint checks before permitting execution."""
    description = str(kwargs.get("description", ""))
    if not description:
        return {"ok": False, "error": "description is required"}
    context    = kwargs.get("context", {})
    goal_type  = str(kwargs.get("goal_type", "autonomous"))
    requester  = str(kwargs.get("requester", "user_request"))
    engine = get_goal_constraint_engine()
    attempt = engine.evaluate_goal(description, context, goal_type, requester)
    return {"ok": True, **asdict(attempt)}


def get_goal_constraint_stats(**kwargs) -> Dict:
    """Get Goal Constraint Engine statistics: approval rate, recent attempts, thresholds."""
    engine = get_goal_constraint_engine()
    return {"ok": True, **engine.get_stats()}


# ── Tool + Route Registration ──────────────────────────────────────────────────
try:
    import joi_companion
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "evaluate_goal",
            "description": (
                "Run an autonomous goal through Joi's 5-check constraint gate: "
                "human alignment, kernel boundary, resource feasibility, "
                "epistemic confidence, and identity consistency. "
                "Returns approved/rejected verdict with per-check results."
            ),
            "parameters": {"type": "object", "properties": {
                "description": {"type": "string",
                                 "description": "Natural language description of the proposed goal"},
                "context": {"type": "object",
                             "description": "Optional context: user_intent, target_file, estimated_tokens, estimated_time_sec"},
                "goal_type":  {"type": "string",
                                "description": "Goal category: autonomous | user_directed | system"},
                "requester":  {"type": "string",
                                "description": "Which subsystem is requesting the goal"}
            }, "required": ["description"]}
        }},
        evaluate_goal
    )
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "get_goal_constraint_stats",
            "description": "Get Goal Constraint Engine statistics: total evaluated, approval rate, recent attempts.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }},
        get_goal_constraint_stats
    )
    print("  [OK] joi_goal_constraints loaded (GoalConstraintEngine v6.5 active, 5-check gate)")
except Exception as _e:
    print(f"  [WARN] joi_goal_constraints: tool registration skipped ({_e})")

try:
    import joi_companion

    def _gc_route():
        from flask import jsonify
        return jsonify(get_goal_constraint_stats())

    joi_companion.register_route("/goals/stats", ["GET"], _gc_route, "goal_stats_route")
except Exception:
    pass
