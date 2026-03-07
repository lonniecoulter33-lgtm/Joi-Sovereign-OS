"""
modules/joi_self_model.py

Joi v5.0 — Self-Model Embedding (Phase I)
==========================================
Maintains a structured, measurable internal representation of Joi's own
architecture state. NOT narrative personality — purely quantitative metrics.

Pulls live data from v4.0 subsystems:
  - joi_reinforcement_graph  → reliability/confidence snapshot
  - joi_sector_telemetry     → sector health snapshot
  - joi_memory_compression   → memory health snapshot
  - joi_epistemic            → epistemic profile

Exposes:
  refresh()                   → pull all live metrics
  generate_self_summary()     → structured JSON snapshot (no prose)
  predict_task_success(task)  → probability estimate (0.0–1.0)

Layer: LAYER_4 (Plugin layer — auto-apply OK, observable, degrades gracefully)

Safety: SelfModel CANNOT alter Kernel Lock, CANNOT modify epistemic thresholds,
        CANNOT write to Layer 1/2 files. Read-only consumer of v4.0 telemetry.
"""

import json
import time
import threading
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR   = Path(__file__).resolve().parent.parent
DATA_DIR   = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

SELF_MODEL_PATH     = DATA_DIR / "self_model_snapshot.json"
ARCHITECTURE_VERSION = "5.0"
REFRESH_INTERVAL_SEC = 30       # minimum seconds between auto-refreshes
SUCCESS_BASE_PRIOR   = 0.65     # neutral task success prior when no data available

# Planner escalation threshold: if predicted success < this, escalate
PLANNER_ESCALATION_THRESHOLD = 0.55

_lock = threading.Lock()


# ── Task Type → Sector Mapping ─────────────────────────────────────────────────
# Maps high-level task categories to the brain sectors most relevant for scoring
TASK_SECTOR_MAP: Dict[str, List[str]] = {
    "coding":       ["titan_logic", "reasoning_engine", "skill_synthesizer"],
    "research":     ["research_drive", "reasoning_engine", "memory_core"],
    "planning":     ["planning_center", "titan_logic", "context_manager"],
    "creative":     ["creativity_matrix", "reasoning_engine"],
    "memory":       ["memory_core", "context_manager"],
    "tool_use":     ["tool_executor", "planning_center"],
    "autonomy":     ["autonomy_governor", "planning_center", "reasoning_engine"],
    "git":          ["git_agency", "tool_executor"],
    "voice":        ["voice_engine"],
    "vision":       ["visual_cortex"],
    "market":       ["market_sensor", "research_drive"],
    "swarm":        ["swarm_coordinator", "planning_center"],
    "default":      ["reasoning_engine", "planning_center", "memory_core"],
}


# ── SelfModel Data Structure ───────────────────────────────────────────────────

@dataclass
class SelfModel:
    """
    Joi's structured internal self-representation.
    All fields are measurable, machine-readable metrics.
    """
    architecture_version:     str   = ARCHITECTURE_VERSION
    last_refreshed:           str   = ""
    system_confidence_score:  float = 0.5   # overall weighted confidence

    # Sub-snapshots (pulled from v4.0 modules)
    reliability_snapshot:     Dict[str, Any] = field(default_factory=dict)
    sector_snapshot:          Dict[str, Any] = field(default_factory=dict)
    memory_health_snapshot:   Dict[str, Any] = field(default_factory=dict)
    epistemic_profile:        Dict[str, Any] = field(default_factory=dict)

    # Derived state
    active_capabilities:      List[str] = field(default_factory=list)
    autonomy_profile:         Dict[str, Any] = field(default_factory=dict)
    recent_drift_flags:       List[Dict]     = field(default_factory=list)

    # Planner integration data
    sector_success_rates:     Dict[str, float] = field(default_factory=dict)
    low_confidence_skills:    List[str]         = field(default_factory=list)

    def __post_init__(self):
        if not self.last_refreshed:
            self.last_refreshed = datetime.now(timezone.utc).isoformat()


# ── SelfModelEngine ────────────────────────────────────────────────────────────

class SelfModelEngine:
    """
    Engine that owns and refreshes the SelfModel instance.

    Thread-safe via _lock.
    Persists latest snapshot to data/self_model_snapshot.json.
    """

    def __init__(self):
        self._model = SelfModel()
        self._last_refresh_ts: float = 0.0
        self._refresh_count: int = 0
        self._load_cached()

    def _load_cached(self):
        """Load persisted snapshot on startup."""
        if SELF_MODEL_PATH.exists():
            try:
                raw = json.loads(SELF_MODEL_PATH.read_text(encoding="utf-8"))
                for k, v in raw.items():
                    if hasattr(self._model, k):
                        setattr(self._model, k, v)
            except Exception:
                pass

    def _persist(self):
        try:
            SELF_MODEL_PATH.write_text(
                json.dumps(asdict(self._model), indent=2, default=str),
                encoding="utf-8"
            )
        except Exception as e:
            print(f"  [SELF_MODEL] Persist failed: {e}")

    # ── Refresh ────────────────────────────────────────────────────────────────

    def refresh(self) -> "SelfModelEngine":
        """
        Pull live metrics from all v4.0 subsystems.
        Thread-safe. Debounced to REFRESH_INTERVAL_SEC.
        Degrades gracefully if any subsystem is unavailable.
        """
        now = time.time()
        with _lock:
            if now - self._last_refresh_ts < REFRESH_INTERVAL_SEC and self._refresh_count > 0:
                return self   # debounce

            m = self._model
            m.last_refreshed = datetime.now(timezone.utc).isoformat()
            m.architecture_version = ARCHITECTURE_VERSION

            # ── 1. Reinforcement Graph ──────────────────────────────────────
            try:
                from modules.joi_reinforcement_graph import get_reinforcement_graph
                graph = get_reinforcement_graph()
                dashboard = graph.get_dashboard()
                m.reliability_snapshot = {
                    "total_nodes": dashboard.get("total_nodes", 0),
                    "drift_alerts": dashboard.get("drift_alerts", []),
                    "top_skills": self._top_nodes(dashboard.get("nodes", []), "skill", n=5),
                    "top_tools":  self._top_nodes(dashboard.get("nodes", []), "tool", n=5),
                }
                m.recent_drift_flags = dashboard.get("drift_alerts", [])

                # Collect per-skill confidence for low_confidence tracking
                low_conf = []
                for node in dashboard.get("nodes", []):
                    if node.get("node_type") == "skill" and node.get("confidence_score", 1.0) < 0.50:
                        low_conf.append(node.get("node_id", "?"))
                m.low_confidence_skills = low_conf[:10]
            except Exception as e:
                m.reliability_snapshot = {"error": str(e), "status": "unavailable"}

            # ── 2. Sector Telemetry ────────────────────────────────────────
            try:
                from modules.joi_sector_telemetry import get_sector_telemetry
                st = get_sector_telemetry()
                dashboard_s = st.get_dashboard()
                anomalies = dashboard_s.get("anomalies", [])
                heatmap = dashboard_s.get("heatmap", [])
                sector_rates = {}
                for entry in heatmap:
                    sector_rates[entry["sector"]] = entry.get("success_rate", 0.0)
                m.sector_snapshot = {
                    "total_sectors": dashboard_s.get("total_sectors", 0),
                    "anomaly_count": len(anomalies),
                    "anomalies": anomalies[:5],
                    "top_active": heatmap[:5],
                }
                m.sector_success_rates = sector_rates
            except Exception as e:
                m.sector_snapshot = {"error": str(e), "status": "unavailable"}

            # ── 3. Memory Compression Health ───────────────────────────────
            try:
                from modules.joi_memory_compression import get_memory_compressor
                mc = get_memory_compressor()
                health = mc.get_health_telemetry()
                m.memory_health_snapshot = health
            except Exception as e:
                m.memory_health_snapshot = {"error": str(e), "status": "unavailable"}

            # ── 4. Epistemic Profile ───────────────────────────────────────
            try:
                from modules.joi_epistemic import get_epistemic_engine
                ep = get_epistemic_engine()
                status = ep.get_status()
                m.epistemic_profile = {
                    "speculative_mode":      status.get("speculative_mode", False),
                    "speculative_threshold": status.get("speculative_threshold", 0.55),
                    "execution_threshold":   status.get("execution_threshold", 0.75),
                    "total_corrections":     status.get("total_corrections", 0),
                }
            except Exception as e:
                m.epistemic_profile = {"error": str(e), "status": "unavailable"}

            # ── 5. Autonomy Profile ────────────────────────────────────────
            try:
                from modules.joi_autonomy import get_autonomy_manager
                am = get_autonomy_manager()
                m.autonomy_profile = {
                    "enabled": getattr(am, "enabled", False),
                    "cycle_count": getattr(am, "cycle_count", 0),
                    "last_cycle": getattr(am, "last_cycle", None),
                }
            except Exception:
                m.autonomy_profile = {"enabled": False, "status": "unavailable"}

            # ── 6. Active Capabilities ─────────────────────────────────────
            m.active_capabilities = self._detect_active_capabilities()

            # ── 7. System Confidence Score ─────────────────────────────────
            m.system_confidence_score = self._compute_system_confidence(m)

            self._last_refresh_ts = now
            self._refresh_count += 1
            self._persist()
        return self

    def _top_nodes(self, nodes: List[Dict], node_type: str, n: int = 5) -> List[Dict]:
        filtered = [nd for nd in nodes if nd.get("node_type") == node_type]
        sorted_nodes = sorted(filtered, key=lambda x: -x.get("confidence_score", 0))
        return [
            {"id": nd.get("node_id"), "confidence": round(nd.get("confidence_score", 0), 3)}
            for nd in sorted_nodes[:n]
        ]

    def _detect_active_capabilities(self) -> List[str]:
        """Check which v4.0/v5.0 modules are importable (active)."""
        caps = []
        probe_map = {
            "kernel_lock":         "modules.joi_kernel_lock",
            "reinforcement_graph": "modules.joi_reinforcement_graph",
            "memory_compression":  "modules.joi_memory_compression",
            "epistemic_safety":    "modules.joi_epistemic",
            "sector_telemetry":    "modules.joi_sector_telemetry",
            "self_model":          "modules.joi_self_model",
        }
        import importlib
        for cap, mod_path in probe_map.items():
            try:
                importlib.import_module(mod_path)
                caps.append(cap)
            except Exception:
                pass
        return caps

    def _compute_system_confidence(self, m: SelfModel) -> float:
        """
        Weighted composite system confidence:
          40% from sector success rates (avg)
          30% from epistemic profile (not speculative)
          20% from low-confidence skill count (inverted)
          10% from memory health (1 - redundancy_score)
        """
        scores = []

        # Sector average success rate
        sr = list(m.sector_success_rates.values()) if m.sector_success_rates else []
        if sr:
            scores.append(("sector_avg", sum(sr) / len(sr), 0.40))

        # Epistemic — speculative mode is bad
        ep = m.epistemic_profile
        if "speculative_mode" in ep:
            ep_score = 0.30 if not ep["speculative_mode"] else 0.15
            scores.append(("epistemic", ep_score, 0.30))

        # Low confidence skills (inverted — fewer is better)
        total_skills = max(1, len(list(TASK_SECTOR_MAP.keys())))
        low_count = len(m.low_confidence_skills)
        skill_score = max(0.0, 1.0 - (low_count / total_skills))
        scores.append(("skill_health", skill_score, 0.20))

        # Memory health
        mem = m.memory_health_snapshot
        if isinstance(mem, dict) and "redundancy_score" in mem:
            mem_score = 1.0 - min(1.0, mem.get("redundancy_score", 0))
            scores.append(("memory_health", mem_score, 0.10))

        if not scores:
            return SUCCESS_BASE_PRIOR

        total_weight = sum(w for _, _, w in scores)
        weighted_sum = sum(s * w for _, s, w in scores)
        return round(weighted_sum / total_weight, 3) if total_weight > 0 else SUCCESS_BASE_PRIOR

    # ── Prediction ─────────────────────────────────────────────────────────────

    def predict_task_success(self, task_type: str) -> Dict[str, Any]:
        """
        Predict the probability of success for a given task type.

        Uses:
          - Sector success rates for relevant brain sectors
          - Reinforcement graph confidence for relevant skills
          - System confidence score as a floor

        Returns structured dict with probability and recommendation.
        """
        self.refresh()
        m = self._model

        sectors = TASK_SECTOR_MAP.get(task_type.lower(), TASK_SECTOR_MAP["default"])
        sector_rates = m.sector_success_rates

        relevant_scores = []
        for sector in sectors:
            if sector in sector_rates:
                relevant_scores.append(sector_rates[sector])

        if relevant_scores:
            sector_avg = sum(relevant_scores) / len(relevant_scores)
        else:
            sector_avg = SUCCESS_BASE_PRIOR

        # Blend with system confidence
        predicted = round(0.65 * sector_avg + 0.35 * m.system_confidence_score, 3)
        predicted = max(0.05, min(0.99, predicted))

        needs_escalation = predicted < PLANNER_ESCALATION_THRESHOLD

        recommendation = "proceed"
        if predicted < 0.35:
            recommendation = "decline_gracefully"
        elif predicted < PLANNER_ESCALATION_THRESHOLD:
            recommendation = "escalate_model_or_clarify"
        elif m.epistemic_profile.get("speculative_mode", False):
            recommendation = "request_clarification"

        return {
            "task_type":         task_type,
            "predicted_success": predicted,
            "needs_escalation":  needs_escalation,
            "recommendation":    recommendation,
            "relevant_sectors":  sectors,
            "sector_avg":        round(sector_avg, 3),
            "system_confidence": m.system_confidence_score,
            "low_confidence_skills": m.low_confidence_skills[:5],
        }

    # ── Summary Generation ─────────────────────────────────────────────────────

    def generate_self_summary(self) -> Dict[str, Any]:
        """
        Return structured JSON self-summary. NO prose. Machine-readable.
        Called by planner before major planning steps.
        """
        self.refresh()
        m = self._model
        return {
            "architecture_version": m.architecture_version,
            "last_refreshed":       m.last_refreshed,
            "system_confidence":    m.system_confidence_score,
            "active_capabilities":  m.active_capabilities,
            "reliability": {
                "total_nodes":          m.reliability_snapshot.get("total_nodes", 0),
                "drift_alert_count":    len(m.recent_drift_flags),
                "low_confidence_skills": m.low_confidence_skills,
            },
            "sectors": {
                "anomaly_count":  m.sector_snapshot.get("anomaly_count", 0),
                "top_active":     m.sector_snapshot.get("top_active", []),
            },
            "memory": {
                "total_nodes":    m.memory_health_snapshot.get("total_memory_nodes", 0),
                "compressed_ratio": m.memory_health_snapshot.get("compressed_ratio", 0),
                "stale_count":    m.memory_health_snapshot.get("stale_node_count", 0),
            },
            "epistemic": {
                "speculative_mode":    m.epistemic_profile.get("speculative_mode", False),
                "total_corrections":   m.epistemic_profile.get("total_corrections", 0),
            },
            "autonomy": {
                "enabled":     m.autonomy_profile.get("enabled", False),
                "cycle_count": m.autonomy_profile.get("cycle_count", 0),
            },
        }

    # ── Planner Integration Helper ─────────────────────────────────────────────

    def planner_pre_check(self, task_type: str) -> Dict[str, Any]:
        """
        Called by planner before any major planning step.
        Returns prediction + recommendation.
        If escalation needed, planner should adjust routing.
        """
        prediction = self.predict_task_success(task_type)
        summary = self.generate_self_summary()
        return {
            "ok": True,
            "prediction": prediction,
            "self_summary": summary,
            "escalate": prediction["needs_escalation"],
            "recommendation": prediction["recommendation"],
        }

    @property
    def model(self) -> SelfModel:
        return self._model


# ── Singleton ──────────────────────────────────────────────────────────────────
_engine: Optional[SelfModelEngine] = None


def get_self_model() -> SelfModelEngine:
    global _engine
    if _engine is None:
        _engine = SelfModelEngine()
    return _engine


# ── Tool Functions ─────────────────────────────────────────────────────────────

def get_self_model_summary(**kwargs) -> Dict:
    """Get Joi's structured self-model summary: capabilities, confidence, sector health, memory, epistemic state."""
    engine = get_self_model()
    return {"ok": True, **engine.generate_self_summary()}


def predict_task_success(**kwargs) -> Dict:
    """Predict Joi's success probability for a task type. Returns recommendation: proceed/escalate/decline."""
    task_type = str(kwargs.get("task_type", "default"))
    engine = get_self_model()
    return {"ok": True, **engine.predict_task_success(task_type)}


# ── Tool + Route Registration ──────────────────────────────────────────────────
try:
    import joi_companion
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "get_self_model_summary",
            "description": (
                "Get Joi's internal self-model: architecture version, system confidence score, "
                "active capabilities, sector health, memory stats, and epistemic state."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []}
        }},
        get_self_model_summary
    )
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "predict_task_success",
            "description": (
                "Predict Joi's probability of success for a given task type. "
                "Returns probability (0–1), needs_escalation flag, and recommendation "
                "(proceed / escalate_model_or_clarify / decline_gracefully)."
            ),
            "parameters": {"type": "object", "properties": {
                "task_type": {"type": "string",
                              "description": "Task category: coding, research, planning, creative, memory, tool_use, autonomy, git, voice, vision, market, swarm, default"}
            }, "required": ["task_type"]}
        }},
        predict_task_success
    )
    print("  [OK] joi_self_model loaded (SelfModel v5.0 active)")
except Exception as _e:
    print(f"  [WARN] joi_self_model: tool registration skipped ({_e})")

try:
    import joi_companion

    def _sm_route():
        from flask import jsonify
        return jsonify(get_self_model_summary())

    joi_companion.register_route("/self/model", ["GET"], _sm_route, "self_model_route")
except Exception:
    pass
