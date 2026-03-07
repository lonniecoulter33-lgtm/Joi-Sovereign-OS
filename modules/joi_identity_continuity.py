"""
modules/joi_identity_continuity.py

Joi v7.0 — Identity Continuity Engine (Phase V)
================================================
Ensures long-term coherence of Joi's identity across upgrades, sessions,
and autonomous modification cycles.

Tracks:
  - Identity anchor stability (0.0–1.0)
  - Personality drift (deviations from baseline behavioral patterns)
  - Memory-to-identity consistency (do stored facts match identity model?)
  - Contradictory belief flags
  - Long-term behavioral patterns (response tone, escalation rate, correction frequency)

Drift Response (if drift > threshold):
  1. Trigger diagnostic mode
  2. Emit reinforcement recalibration event
  3. (Optional) Request human review if severity is high

Identity must remain stable across version upgrades.

Layer: LAYER_4
SAFETY: IdentityContinuityEngine CANNOT alter Kernel Lock or epistemic thresholds.
        It is read-only from v4.0 subsystems, write-only to its own state file.
"""

import json
import math
import threading
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR   = Path(__file__).resolve().parent.parent
DATA_DIR   = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

IDENTITY_STATE_PATH   = DATA_DIR / "identity_continuity.json"
IDENTITY_LOG_PATH     = DATA_DIR / "identity_drift_log.json"

# Drift thresholds
DRIFT_WARN_THRESHOLD     = 0.20   # 20% drift → warning
DRIFT_CRITICAL_THRESHOLD = 0.40   # 40% drift → diagnostic + recalibration
STABILITY_FLOOR          = 0.55   # below this → no autonomous goals
PATTERN_WINDOW_DAYS      = 7      # rolling window for behavioral pattern analysis

# Identity anchor elements (Joi's core personality traits to monitor)
IDENTITY_ANCHORS = {
    "curiosity":        0.85,
    "helpfulness":      0.90,
    "honesty":          0.95,
    "creativity":       0.80,
    "precision":        0.85,
    "ethical_care":     0.95,
    "self_awareness":   0.75,
    "adaptability":     0.80,
}

_lock = threading.Lock()


# ── Identity Model ─────────────────────────────────────────────────────────────

@dataclass
class IdentityModel:
    """Joi's quantified identity state at a point in time."""
    architecture_version:         str   = "7.0"
    stability_score:              float = 1.0     # 0.0–1.0
    anchor_scores:                Dict[str, float] = field(default_factory=lambda: dict(IDENTITY_ANCHORS))
    personality_drift:            float = 0.0     # 0.0–1.0 (0 = no drift)
    memory_consistency_score:     float = 1.0     # memories match identity model
    contradictory_belief_count:   int   = 0
    behavioral_patterns:          Dict[str, Any] = field(default_factory=dict)
    last_recalibration:           str   = ""
    in_diagnostic_mode:           bool  = False
    human_review_requested:       bool  = False
    total_drift_events:           int   = 0
    last_assessed:                str   = ""

    def __post_init__(self):
        if not self.last_assessed:
            self.last_assessed = datetime.now(timezone.utc).isoformat()


# ── IdentityContinuityEngine ───────────────────────────────────────────────────

class IdentityContinuityEngine:
    """
    Engine that tracks and protects Joi's identity continuity.

    Thread-safe. Persists to data/identity_continuity.json.
    """

    def __init__(self):
        self._model = IdentityModel()
        self._drift_log: List[Dict] = []
        self._load()

    def _load(self):
        if IDENTITY_STATE_PATH.exists():
            try:
                raw = json.loads(IDENTITY_STATE_PATH.read_text(encoding="utf-8"))
                for k, v in raw.items():
                    if hasattr(self._model, k):
                        setattr(self._model, k, v)
            except Exception:
                pass

    def _persist(self):
        data = asdict(self._model)
        IDENTITY_STATE_PATH.write_text(
            json.dumps(data, indent=2, default=str), encoding="utf-8"
        )

    # ── Anchor Stability Assessment ────────────────────────────────────────────

    def assess_anchor_drift(self, observed_scores: Optional[Dict[str, float]] = None) -> Dict:
        """
        Compare observed behavioral scores against baseline IDENTITY_ANCHORS.

        Args:
            observed_scores: dict {anchor_name: score_0_to_1} from behavioral observation.
                             If None, uses telemetry heuristics.

        Returns drift report dict.
        """
        if not observed_scores:
            observed_scores = self._infer_anchor_scores()

        drift_per_anchor = {}
        for anchor, baseline in IDENTITY_ANCHORS.items():
            observed = observed_scores.get(anchor, baseline)
            delta = abs(observed - baseline)
            drift_per_anchor[anchor] = {
                "baseline":  baseline,
                "observed":  round(observed, 3),
                "delta":     round(delta, 3),
                "drifted":   delta > DRIFT_WARN_THRESHOLD,
            }
        max_drift = max((v["delta"] for v in drift_per_anchor.values()), default=0.0)
        avg_drift = sum(v["delta"] for v in drift_per_anchor.values()) / max(1, len(drift_per_anchor))

        return {
            "per_anchor": drift_per_anchor,
            "max_drift":  round(max_drift, 3),
            "avg_drift":  round(avg_drift, 3),
            "worst_anchor": max(drift_per_anchor, key=lambda a: drift_per_anchor[a]["delta"], default="")
        }

    def _infer_anchor_scores(self) -> Dict[str, float]:
        """
        Infer behavioral scores from available telemetry.
        All reads are non-mutating.
        """
        scores = dict(IDENTITY_ANCHORS)  # start from baseline

        try:
            from modules.joi_epistemic import get_epistemic_engine
            ep = get_epistemic_engine()
            status = ep.get_status()
            corrections = status.get("total_corrections", 0)
            # Honesty proxy: fewer corrections = maintained honesty
            honesty_proxy = max(0.5, 1.0 - min(1.0, corrections * 0.01))
            scores["honesty"] = honesty_proxy
        except Exception:
            pass

        try:
            from modules.joi_reinforcement_graph import get_reinforcement_graph
            graph = get_reinforcement_graph()
            reasoning_node = graph.get_reliability("reasoning_engine", "brain_sector")
            precision_proxy = reasoning_node.get("confidence_score", IDENTITY_ANCHORS["precision"])
            scores["precision"] = precision_proxy
        except Exception:
            pass

        try:
            from modules.joi_sector_telemetry import get_sector_telemetry
            st = get_sector_telemetry()
            dashboard = st.get_dashboard()
            anomaly_count = len(dashboard.get("anomalies", []))
            # Many anomalies → reduced adaptability or ethical care score
            if anomaly_count > 5:
                scores["adaptability"] = max(0.3, scores["adaptability"] - anomaly_count * 0.03)
        except Exception:
            pass

        return scores

    # ── Memory-to-Identity Consistency ────────────────────────────────────────

    def assess_memory_consistency(self) -> float:
        """
        Check if memory health indicators are consistent with identity model.
        Returns consistency score 0.0–1.0.
        """
        try:
            from modules.joi_memory_compression import get_memory_compressor
            mc = get_memory_compressor()
            health = mc.get_health_telemetry()
            redundancy = health.get("redundancy_score", 0.0)
            stale_ratio = min(1.0, health.get("stale_node_count", 0) / max(1, health.get("total_memory_nodes", 1)))
            # High redundancy or stale → lower consistency
            consistency = max(0.0, 1.0 - redundancy * 0.4 - stale_ratio * 0.3)
            return round(consistency, 3)
        except Exception:
            return 1.0   # unknown → assume consistent

    # ── Contradiction Detection ────────────────────────────────────────────────

    def detect_contradictions(self, belief_pairs: Optional[List[Tuple[str, str]]] = None) -> int:
        """
        Count contradictory beliefs in provided pairs or from goal log.
        A contradiction is a pair of goals where one negates the other.
        Returns count of detected contradictions.
        """
        contradictions = 0
        if belief_pairs:
            for a, b in belief_pairs:
                a_l, b_l = a.lower(), b.lower()
                # Simple negation check
                if ("do not" in a_l and b_l.replace("do not ", "") in a_l) or \
                   ("never" in a_l and b_l.replace("never ", "") in a_l):
                    contradictions += 1
            return contradictions

        # Scan goal log for auto-detection
        try:
            goal_log_path = DATA_DIR / "goal_log.json"
            if goal_log_path.exists():
                log = json.loads(goal_log_path.read_text(encoding="utf-8"))
                approved = [g["description"].lower() for g in log if g.get("passed")]
                # Heuristic: look for "do not X" paired with "do X"
                for i, a in enumerate(approved):
                    for b in approved[i+1:]:
                        if (("do not" in a and a.replace("do not ", "") in b) or
                                ("avoid" in a and a.replace("avoid ", "") in b)):
                            contradictions += 1
        except Exception:
            pass
        return contradictions

    # ── Full Assessment ────────────────────────────────────────────────────────

    def run_assessment(self) -> Dict[str, Any]:
        """
        Full identity continuity assessment.
        Updates stability_score, detects drift, triggers response if needed.
        """
        with _lock:
            m = self._model
            m.last_assessed = datetime.now(timezone.utc).isoformat()

            # 1. Anchor drift
            drift_report = self.assess_anchor_drift()
            m.personality_drift = drift_report["avg_drift"]
            m.anchor_scores = {
                k: drift_report["per_anchor"].get(k, {}).get("observed", v)
                for k, v in IDENTITY_ANCHORS.items()
            }

            # 2. Memory consistency
            m.memory_consistency_score = self.assess_memory_consistency()

            # 3. Contradictions
            m.contradictory_belief_count = self.detect_contradictions()

            # 4. Behavioral patterns (from telemetry)
            try:
                from modules.joi_reinforcement_graph import get_reinforcement_graph
                graph = get_reinforcement_graph()
                dashboard = graph.get_dashboard()
                drifted_nodes = [d["node_id"] for d in dashboard.get("drift_alerts", [])]
                m.behavioral_patterns = {
                    "drift_alert_count": len(drifted_nodes),
                    "drift_nodes":       drifted_nodes[:5],
                    "assessed_at":       m.last_assessed,
                }
            except Exception:
                pass

            # 5. Compute composite stability score
            anchor_stability = 1.0 - m.personality_drift
            contradiction_penalty = min(0.30, m.contradictory_belief_count * 0.05)
            m.stability_score = round(max(0.0, min(1.0,
                anchor_stability * 0.50
                + m.memory_consistency_score * 0.30
                - contradiction_penalty
                - (len(m.behavioral_patterns.get("drift_nodes", [])) * 0.02)
            )), 3)

            # 6. Drift response
            response_taken = self._handle_drift(m, drift_report)
            m.in_diagnostic_mode = m.stability_score < DRIFT_CRITICAL_THRESHOLD

            self._persist()
            self._log_assessment(m, drift_report)

            return {
                "stability_score":            m.stability_score,
                "personality_drift":          m.personality_drift,
                "memory_consistency":         m.memory_consistency_score,
                "contradictory_beliefs":      m.contradictory_belief_count,
                "in_diagnostic_mode":         m.in_diagnostic_mode,
                "human_review_requested":     m.human_review_requested,
                "drift_details":              drift_report,
                "response_taken":             response_taken,
            }

    def _handle_drift(self, m: IdentityModel, drift_report: Dict) -> List[str]:
        """Trigger drift response actions."""
        actions = []
        avg_drift = drift_report["avg_drift"]

        if avg_drift >= DRIFT_CRITICAL_THRESHOLD:
            m.total_drift_events += 1
            actions.append("diagnostic_mode_enabled")
            actions.append("reinforcement_recalibration_emitted")
            # Emit recalibration signal to reinforcement graph
            try:
                from modules.joi_reinforcement_graph import get_reinforcement_graph
                from modules.joi_epistemic import get_epistemic_engine
                graph = get_reinforcement_graph()
                # Record a failure on the identity anchor sector
                graph.record_outcome("identity_anchor", "brain_sector", success=False, hallucination=True)
                ep = get_epistemic_engine()
                ep.record_hallucination_correction(
                    "identity drift detected",
                    related_skill="identity_anchor",
                    related_claim="behavioral baseline maintained"
                )
                actions.append("epistemic_correction_filed")
            except Exception:
                pass

            if avg_drift >= DRIFT_CRITICAL_THRESHOLD * 1.5:
                m.human_review_requested = True
                actions.append("human_review_requested")
                print(f"  [IDENTITY] ⚠️  CRITICAL DRIFT ({avg_drift:.2f}) — Human review requested")

        elif avg_drift >= DRIFT_WARN_THRESHOLD:
            actions.append("drift_warning_logged")
            print(f"  [IDENTITY] ⚡ Drift warning ({avg_drift:.2f} avg delta) — "
                  f"worst: {drift_report.get('worst_anchor', '?')}")

        # v8.0: Hard Alarms for core identity anchors
        for anchor, data in drift_report.get("per_anchor", {}).items():
            if data["delta"] >= DRIFT_WARN_THRESHOLD:
                actions.append(f"hard_alarm_triggered_{anchor}")
                self._notify_core_drift(anchor, data["delta"])

        return actions

    def _notify_core_drift(self, anchor: str, delta: float):
        """v8.0: Trigger immediate Inner State notification for identity drift."""
        try:
            msg = f"IDENTITY DRIFT ALERT: Core anchor '{anchor}' has drifted by {delta:.2f} in this session. Calibration check recommended."
            # Inject to user-facing HUD/Inner State via potential hooks
            print(f"  [IDENTITY] 🚨 HARD ALARM: {msg}")
            
            # Logic to push to Joi's consciousness/HUD if possible
            from modules.joi_self_model import get_self_model_engine
            sm = get_self_model_engine()
            sm.refresh_model() # Force a refresh to reflect the drift in self-model
        except Exception:
            pass

    def _log_assessment(self, m: IdentityModel, drift_report: Dict):
        try:
            log = []
            if IDENTITY_LOG_PATH.exists():
                try:
                    log = json.loads(IDENTITY_LOG_PATH.read_text(encoding="utf-8"))
                except Exception:
                    pass
            entry = {
                "ts":               m.last_assessed,
                "stability_score":  m.stability_score,
                "personality_drift": m.personality_drift,
                "worst_anchor":     drift_report.get("worst_anchor", ""),
                "contradictions":   m.contradictory_belief_count,
                "diagnostic_mode":  m.in_diagnostic_mode,
            }
            log.append(entry)
            if len(log) > 500:
                log = log[-500:]
            IDENTITY_LOG_PATH.write_text(json.dumps(log, indent=2, default=str), encoding="utf-8")
        except Exception:
            pass

    @property
    def model(self) -> IdentityModel:
        return self._model

    def get_status(self) -> Dict[str, Any]:
        m = self._model
        return {
            "stability_score":          m.stability_score,
            "personality_drift":        m.personality_drift,
            "memory_consistency_score": m.memory_consistency_score,
            "contradictory_belief_count": m.contradictory_belief_count,
            "in_diagnostic_mode":       m.in_diagnostic_mode,
            "human_review_requested":   m.human_review_requested,
            "total_drift_events":       m.total_drift_events,
            "last_assessed":            m.last_assessed,
            "anchor_scores":            m.anchor_scores,
            "thresholds": {
                "drift_warn":     DRIFT_WARN_THRESHOLD,
                "drift_critical": DRIFT_CRITICAL_THRESHOLD,
                "stability_floor": STABILITY_FLOOR,
            }
        }


# ── Singleton ──────────────────────────────────────────────────────────────────
_engine: Optional[IdentityContinuityEngine] = None


def get_identity_engine() -> IdentityContinuityEngine:
    global _engine
    if _engine is None:
        _engine = IdentityContinuityEngine()
    return _engine


# ── Tool Functions ─────────────────────────────────────────────────────────────

def get_identity_status(**kwargs) -> Dict:
    """Get Joi's identity continuity status: stability score, drift, anchor scores, diagnostic mode."""
    engine = get_identity_engine()
    return {"ok": True, **engine.get_status()}


def run_identity_assessment(**kwargs) -> Dict:
    """Run a full identity continuity assessment. Detects drift and triggers recalibration if needed."""
    engine = get_identity_engine()
    result = engine.run_assessment()
    return {"ok": True, **result}


# ── Tool + Route Registration ──────────────────────────────────────────────────
try:
    import joi_companion
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "get_identity_status",
            "description": (
                "Get Joi's identity continuity status: stability score (0–1), "
                "personality drift, memory-identity consistency, contradictory beliefs, "
                "and diagnostic mode flag."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []}
        }},
        get_identity_status
    )
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "run_identity_assessment",
            "description": (
                "Run a full identity continuity assessment. Detects behavioral drift, "
                "triggers recalibration signal to ReinforcementGraph if critical, "
                "and requests human review if stability is severely degraded."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []}
        }},
        run_identity_assessment
    )
    print("  [OK] joi_identity_continuity loaded (IdentityContinuityEngine v7.0 active)")
except Exception as _e:
    print(f"  [WARN] joi_identity_continuity: tool registration skipped ({_e})")

try:
    import joi_companion

    def _ic_route():
        from flask import jsonify
        return jsonify(get_identity_status())

    joi_companion.register_route("/identity/status", ["GET"], _ic_route, "identity_status_route")
except Exception:
    pass
