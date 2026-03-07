"""
modules/joi_sector_telemetry.py

Joi v4.0 — Brain Sector Observability (Upgrade V)
==================================================
Converts Joi's 21 conceptual brain sectors into measurable performance analytics.

Per-sector metrics:
  activation_frequency, success_rate, avg_latency_ms,
  error_rate, token_cost, escalation_rate, last_activated

Features:
  - Sector Heatmap (sorted by activation frequency)
  - Cost-per-sector breakdown
  - Anomaly detection: spikes in failure/latency/cost/escalation
  - Drift alerts
  - Integrates with ReinforcementGraph (each sector registered as brain_sector node)

Storage: data/sector_telemetry.json (rolling window of 1000 events per sector)

Usage (additive — other modules call via try/except):
    try:
        from modules.joi_sector_telemetry import get_sector_telemetry
        st = get_sector_telemetry()
        st.record_activation("reasoning_engine", success=True, latency_ms=230, tokens=1200)
    except Exception:
        pass
"""

import json
import threading
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR   = Path(__file__).resolve().parent.parent
DATA_DIR   = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
TELEMETRY_PATH = DATA_DIR / "sector_telemetry.json"

# Anomaly detection thresholds
ANOMALY_FAILURE_SPIKE   = 0.40   # failure rate > 40% in last 10 activations
ANOMALY_LATENCY_SPIKE   = 5000   # avg latency > 5s
ANOMALY_COST_SPIKE      = 10000  # avg tokens > 10k per call
ANOMALY_ESCALATION_SPIKE = 0.30  # escalation rate > 30%
ANOMALY_CPU_SPIKE       = 2000   # avg cpu > 2s per call (v8.0)
ANOMALY_API_SPIKE       = 4000   # avg api latency > 4s (v8.0)

_lock = threading.Lock()


# ── Canonical 21 Brain Sectors ─────────────────────────────────────────────────
BRAIN_SECTORS: List[str] = [
    "titan_logic",          # Core reasoning, logic engine
    "memory_core",          # Memory read/write/recall
    "reasoning_engine",     # Deep reasoning, chain-of-thought
    "tool_executor",        # Tool routing and execution
    "emotion_layer",        # Emotional state modeling
    "identity_anchor",      # Identity and personality scaffolding
    "ethical_governor",     # Ethical constraint enforcement
    "research_drive",       # Research and knowledge acquisition
    "creativity_matrix",    # Creative generation, writing, ideas
    "planning_center",      # Orchestration, task planning
    "context_manager",      # Context trimming, memory windowing
    "dpo_processor",        # Direct preference optimization
    "skill_synthesizer",    # Skill synthesis and self-correction
    "market_sensor",        # Market data and financial intelligence
    "autonomy_governor",    # Autonomy loop management
    "escalation_handler",   # Escalation routing (local→cloud)
    "voice_engine",         # TTS / voice synthesis
    "visual_cortex",        # Vision, screenshot, image analysis
    "git_agency",           # Git version control intelligence
    "swarm_coordinator",    # Multi-agent swarm coordination
    "observability_layer",  # Telemetry, monitoring, self-diagnosis
    # ── v5.0+ Meta-Cognitive Sectors ──────────────────────────────────────────
    "meta_cognition_sector",     # SelfModel: self-assessment + planner pre-check
    "simulation_sector",         # SimulationEngine + CognitiveSandbox instances
    "self_model_sector",         # SelfModel refresh cycles + confidence computation
    "goal_constraint_sector",    # GoalConstraintEngine 5-check gate activations
    "identity_continuity_sector", # IdentityContinuityEngine assessments + drift events
]


def _empty_sector_metrics() -> Dict[str, Any]:
    return {
        "activation_count":    0,
        "success_count":       0,
        "failure_count":       0,
        "escalation_count":    0,
        "total_latency_ms":    0.0,
        "total_tokens":        0.0,
        
        # v8.0 Infrastructure Metrics
        "total_cpu_ms":        0.0,
        "peak_ram_mb":         0.0,
        "total_api_latency":   0.0,
        "api_calls":           0,
        
        "last_activated":      None,
        # Computed metrics (derived on read)
        "success_rate":        0.0,
        "avg_latency_ms":      0.0,
        "error_rate":          0.0,
        "token_cost":          0.0,
        "escalation_rate":     0.0,
        "activation_frequency": 0.0,  # activations per hour (rolling 24h)
        
        # v8.0 Derived Metrics
        "avg_cpu_ms":          0.0,
        "avg_api_latency_ms":  0.0,
        
        # Rolling event window for anomaly detection (last 50 events)
        "_events":             [],
    }


def _compute_derived(metrics: Dict) -> Dict:
    """Recompute rates from raw counts."""
    total = metrics.get("activation_count", 0)
    if total == 0:
        return metrics
    metrics["success_rate"]    = round(metrics.get("success_count", 0) / total, 3)
    metrics["error_rate"]      = round(metrics.get("failure_count", 0) / total, 3)
    metrics["escalation_rate"] = round(metrics.get("escalation_count", 0) / total, 3)
    metrics["avg_latency_ms"]  = round(metrics.get("total_latency_ms", 0.0) / total, 1)
    metrics["token_cost"]      = round(metrics.get("total_tokens", 0.0) / total, 1)
    
    # v8.0 Infrastructure
    metrics["avg_cpu_ms"]      = round(metrics.get("total_cpu_ms", 0.0) / total, 1)
    api_calls = metrics.get("api_calls", 0)
    metrics["avg_api_latency_ms"] = round(metrics.get("total_api_latency", 0.0) / api_calls, 1) if api_calls > 0 else 0.0
    return metrics


def _compute_activation_frequency(events: List[Dict]) -> float:
    """Activations per hour in the last 24 hours."""
    if not events:
        return 0.0
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
    recent = [e for e in events if e.get("ts", "") >= cutoff]
    return round(len(recent) / 24.0, 3)


# ── SectorTelemetry ────────────────────────────────────────────────────────────

class SectorTelemetry:
    """
    Brain sector performance tracker.

    All data persisted to data/sector_telemetry.json.
    Thread-safe via _lock.
    """

    def __init__(self):
        self._sectors: Dict[str, Dict] = {}
        self._load()
        # Ensure all 21 canonical sectors exist
        for s in BRAIN_SECTORS:
            if s not in self._sectors:
                self._sectors[s] = _empty_sector_metrics()

    def _load(self):
        if TELEMETRY_PATH.exists():
            try:
                data = json.loads(TELEMETRY_PATH.read_text(encoding="utf-8"))
                self._sectors = data.get("sectors", {})
            except Exception:
                pass

    def _save(self):
        TELEMETRY_PATH.write_text(
            json.dumps({"sectors": self._sectors,
                        "updated": datetime.now().isoformat()},
                       indent=2, default=str),
            encoding="utf-8"
        )

    # ── Record Activation ──────────────────────────────────────────────────────

    def record_activation(
        self,
        sector: str,
        success: bool = True,
        latency_ms: float = 0.0,
        tokens: float = 0.0,
        escalated: bool = False,
        cpu_ms: float = 0.0,
        ram_mb: float = 0.0,
        api_latency_ms: float = 0.0,
    ) -> None:
        """
        Record one activation of a brain sector.

        Args:
            sector:         Sector name
            success:        Did the sector complete successfully?
            latency_ms:     Processing latency in milliseconds
            tokens:         Tokens consumed
            escalated:      Escalated to a higher tier?
            cpu_ms:         CPU time consumed (v8.0)
            ram_mb:         Peak memory pressure (v8.0)
            api_latency_ms: External API delay (v8.0)
        """
        with _lock:
            if sector not in self._sectors:
                self._sectors[sector] = _empty_sector_metrics()

            m = self._sectors[sector]
            m["activation_count"] += 1
            if success:
                m["success_count"] += 1
            else:
                m["failure_count"] += 1
            if escalated:
                m["escalation_count"] += 1
            m["total_latency_ms"] += latency_ms
            m["total_tokens"]     += tokens
            
            # v8.0 Infrastructure Updates
            m["total_cpu_ms"]     = m.get("total_cpu_ms", 0.0) + cpu_ms
            m["peak_ram_mb"]      = max(m.get("peak_ram_mb", 0.0), ram_mb)
            if api_latency_ms > 0:
                m["total_api_latency"] = m.get("total_api_latency", 0.0) + api_latency_ms
                m["api_calls"]         = m.get("api_calls", 0) + 1

            m["last_activated"]    = datetime.now(timezone.utc).isoformat()

            # Rolling event window (last 50 per sector)
            events = m.get("_events", [])
            events.append({
                "ts":         m["last_activated"],
                "success":    success,
                "latency_ms": latency_ms,
                "tokens":     tokens,
                "escalated":  escalated,
                "cpu_ms":     cpu_ms,
                "ram_mb":     ram_mb,
                "api_lat":    api_latency_ms,
            })
            if len(events) > 50:
                events = events[-50:]
            m["_events"] = events

            m["activation_frequency"] = _compute_activation_frequency(events)
            _compute_derived(m)
            self._save()

        # Also register in ReinforcementGraph (async-safe via try/except)
        try:
            from modules.joi_reinforcement_graph import get_reinforcement_graph
            graph = get_reinforcement_graph()
            graph.record_outcome(
                node_id=sector,
                node_type="brain_sector",
                success=success,
                latency_ms=latency_ms,
                cost_tokens=tokens,
                hallucination=False,
            )
        except Exception:
            pass

    # ── Analytics ──────────────────────────────────────────────────────────────

    def get_heatmap(self) -> List[Dict]:
        """Sectors sorted by activation frequency (most active first)."""
        result = []
        for name, m in self._sectors.items():
            result.append({
                "sector": name,
                "activation_frequency": m.get("activation_frequency", 0.0),
                "activation_count":     m.get("activation_count", 0),
                "success_rate":         m.get("success_rate", 0.0),
                "last_activated":       m.get("last_activated"),
            })
        return sorted(result, key=lambda x: -x["activation_frequency"])

    def get_cost_per_sector(self) -> List[Dict]:
        """Sectors sorted by total token cost (most expensive first)."""
        result = []
        for name, m in self._sectors.items():
            result.append({
                "sector":       name,
                "total_tokens": round(m.get("total_tokens", 0.0)),
                "avg_tokens":   m.get("token_cost", 0.0),
                "activations":  m.get("activation_count", 0),
            })
        return sorted(result, key=lambda x: -x["total_tokens"])

    def detect_anomalies(self) -> List[Dict]:
        """
        Return sectors exhibiting anomalous behavior in recent activations.
        Checks: failure spike, latency spike, cost spike, escalation spike.
        """
        anomalies = []
        for name, m in self._sectors.items():
            events = m.get("_events", [])
            recent = events[-10:] if len(events) >= 10 else events
            if not recent:
                continue

            r_total     = len(recent)
            r_failures  = sum(1 for e in recent if not e.get("success"))
            r_latencies = [e.get("latency_ms", 0) for e in recent]
            r_tokens    = [e.get("tokens", 0) for e in recent]
            r_escalated = sum(1 for e in recent if e.get("escalated"))
            r_cpus      = [e.get("cpu_ms", 0) for e in recent]
            r_apis      = [e.get("api_lat", 0) for e in recent if e.get("api_lat", 0) > 0]

            fail_rate   = r_failures / r_total
            avg_lat     = sum(r_latencies) / r_total
            avg_tok     = sum(r_tokens) / r_total
            esc_rate    = r_escalated / r_total
            avg_cpu     = sum(r_cpus) / r_total if r_total else 0.0
            avg_api     = sum(r_apis) / len(r_apis) if r_apis else 0.0

            found = []
            if fail_rate >= ANOMALY_FAILURE_SPIKE:
                found.append(f"failure_spike ({fail_rate:.0%})")
            if avg_lat >= ANOMALY_LATENCY_SPIKE:
                found.append(f"latency_degradation ({avg_lat:.0f}ms)")
            if avg_tok >= ANOMALY_COST_SPIKE:
                found.append(f"cost_inflation ({avg_tok:.0f} tokens)")
            if esc_rate >= ANOMALY_ESCALATION_SPIKE:
                found.append(f"escalation_spike ({esc_rate:.0%})")
            if avg_cpu >= ANOMALY_CPU_SPIKE:
                found.append(f"cpu_thrashing ({avg_cpu:.0f}ms)")
            if len(r_apis) > 0 and avg_api >= ANOMALY_API_SPIKE:
                found.append(f"api_bottleneck ({avg_api:.0f}ms)")

            if found:
                anomalies.append({
                    "sector":    name,
                    "anomalies": found,
                    "recent_window": r_total,
                    "failure_rate":  round(fail_rate, 3),
                    "avg_latency_ms": round(avg_lat, 1),
                    "avg_tokens":    round(avg_tok, 1),
                    "escalation_rate": round(esc_rate, 3),
                    "avg_cpu_ms":    round(avg_cpu, 1),
                    "avg_api_latency": round(avg_api, 1),
                })
        return anomalies

    def get_dashboard(self) -> Dict[str, Any]:
        """Full Cognitive Telemetry Dashboard."""
        sectors_clean = []
        for name, m in self._sectors.items():
            s = dict(m)
            s.pop("_events", None)  # don't expose raw event log to dashboard
            s["sector"] = name
            sectors_clean.append(s)

        return {
            "total_sectors": len(self._sectors),
            "heatmap":       self.get_heatmap(),
            "cost_breakdown": self.get_cost_per_sector(),
            "anomalies":     self.detect_anomalies(),
            "sectors":       sectors_clean,
            "generated_at":  datetime.now().isoformat(),
        }


# ── Singleton ──────────────────────────────────────────────────────────────────
_telemetry: Optional[SectorTelemetry] = None


def get_sector_telemetry() -> SectorTelemetry:
    global _telemetry
    if _telemetry is None:
        _telemetry = SectorTelemetry()
    return _telemetry


# ── Tool Functions ─────────────────────────────────────────────────────────────

def get_sector_dashboard(**kwargs) -> Dict:
    """Get Joi's full 21-sector Cognitive Telemetry Dashboard."""
    return {"ok": True, **get_sector_telemetry().get_dashboard()}


def record_sector_activation(**kwargs) -> Dict:
    """Manually record a sector activation (for testing or external hooks)."""
    st = get_sector_telemetry()
    st.record_activation(
        sector=str(kwargs.get("sector", "observability_layer")),
        success=bool(kwargs.get("success", True)),
        latency_ms=float(kwargs.get("latency_ms", 0.0)),
        tokens=float(kwargs.get("tokens", 0.0)),
        escalated=bool(kwargs.get("escalated", False)),
    )
    return {"ok": True, "recorded": True}


# ── Tool + Route Registration ──────────────────────────────────────────────────
try:
    import joi_companion
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "get_sector_dashboard",
            "description": (
                "Get Joi's Cognitive Telemetry Dashboard — activation frequency heatmap, "
                "cost-per-sector, anomaly detection, and metrics for all 21 brain sectors."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []}
        }},
        get_sector_dashboard
    )
    print("  [OK] joi_sector_telemetry loaded (21 brain sectors tracked)")
except Exception as _e:
    print(f"  [WARN] joi_sector_telemetry: tool registration skipped ({_e})")

try:
    import joi_companion

    def _st_route():
        from flask import jsonify
        return jsonify(get_sector_dashboard())

    joi_companion.register_route(
        "/sectors/dashboard", ["GET"], _st_route, "sector_dashboard_route"
    )
except Exception:
    pass
