"""
modules/joi_reinforcement_graph.py

Joi v4.0 — Reinforcement Graph (Upgrade II)
===========================================
Transforms DPO signals into a quantitative skill and reliability model.

Storage: SQLite (joi_memory.db) — table `reinforcement_graph` (created on first use).
Fallback: JSON file at data/reinforcement_graph.json if DB unavailable.

Node types:
  skill       — per-skill category (coding, reasoning, research, planning, etc.)
  tool        — per registered tool name
  model       — per LLM model used
  brain_sector — per named brain sector (21 sectors)

Per-node:
  success_count, failure_count, confidence_score,
  latency_avg_ms, cost_avg_tokens, hallucination_flag_count

Drift detection: nodes where confidence has dropped > 15% in last 24h
"""

import json
import math
import time
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

GRAPH_JSON_PATH  = DATA_DIR / "reinforcement_graph.json"
DRIFT_THRESHOLD  = 0.15   # 15% confidence drop triggers drift alert
RECENCY_HALFLIFE = 24.0   # hours — older outcomes weighted by exponential decay
HALLUCINATION_PENALTY = 0.08  # per hallucination event

_lock = threading.Lock()


# ── SQLite helpers ─────────────────────────────────────────────────────────────

def _get_db_conn():
    """Return SQLite connection from joi_db, or None if unavailable."""
    try:
        from modules.joi_db import db_connect
        conn = db_connect()
        _ensure_table(conn)
        return conn
    except Exception:
        return None


def _ensure_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reinforcement_graph (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            node_id         TEXT NOT NULL,
            node_type       TEXT NOT NULL,
            success_count   INTEGER DEFAULT 0,
            failure_count   INTEGER DEFAULT 0,
            confidence_score REAL DEFAULT 0.5,
            latency_avg_ms  REAL DEFAULT 0.0,
            cost_avg_tokens REAL DEFAULT 0.0,
            hallucination_flag_count INTEGER DEFAULT 0,
            last_updated    TEXT,
            UNIQUE(node_id, node_type)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reinforcement_events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ts          TEXT NOT NULL,
            node_id     TEXT NOT NULL,
            node_type   TEXT NOT NULL,
            success     INTEGER NOT NULL,
            latency_ms  REAL,
            cost_tokens REAL,
            hallucination INTEGER DEFAULT 0
        )
    """)
    conn.commit()


# ── JSON fallback persistence ──────────────────────────────────────────────────

def _load_json_graph() -> Dict:
    if GRAPH_JSON_PATH.exists():
        try:
            return json.loads(GRAPH_JSON_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"nodes": {}, "events": []}


def _save_json_graph(data: Dict):
    GRAPH_JSON_PATH.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


# ── Confidence Calculation ─────────────────────────────────────────────────────

def _recency_weight(ts_iso: str, halflife_hours: float = RECENCY_HALFLIFE) -> float:
    """Weight an event by how recent it is (exponential decay)."""
    try:
        ts = datetime.fromisoformat(ts_iso)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        age_hours = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
        return math.exp(-0.693 * age_hours / halflife_hours)  # 0.693 = ln(2)
    except Exception:
        return 0.5


def _compute_confidence(success: int, failure: int, hallucinations: int,
                         recent_events: Optional[List] = None) -> float:
    """
    confidence = (weighted_successes / weighted_total) * hallucination_factor
    Falls back to simple ratio if no event history available.
    """
    total = success + failure
    if total == 0:
        return 0.5   # neutral prior

    if recent_events:
        weighted_success = 0.0
        weighted_total = 0.0
        for ev in recent_events[-100:]:  # last 100 events
            w = _recency_weight(ev.get("ts", ""))
            if ev.get("success"):
                weighted_success += w
            weighted_total += w
        base = weighted_success / weighted_total if weighted_total > 0 else (success / total)
    else:
        base = success / total

    # Hallucination penalty
    hallucination_factor = max(0.1, 1.0 - hallucinations * HALLUCINATION_PENALTY)
    return max(0.0, min(1.0, base * hallucination_factor))


# ── ReinforcementGraph ─────────────────────────────────────────────────────────

class ReinforcementGraph:
    """
    Quantitative skill and reliability model for Joi v4.0.

    All reads/writes go to SQLite via joi_db, with JSON fallback.
    Thread-safe via _lock.
    """

    def record_outcome(
        self,
        node_id: str,
        node_type: str,          # "skill" | "tool" | "model" | "brain_sector"
        success: bool,
        latency_ms: float = 0.0,
        cost_tokens: float = 0.0,
        hallucination: bool = False,
    ) -> None:
        """Record one outcome event and recompute the node's confidence score."""
        ts = datetime.now(timezone.utc).isoformat()
        with _lock:
            conn = _get_db_conn()
            if conn:
                try:
                    # Upsert node row
                    conn.execute("""
                        INSERT INTO reinforcement_graph
                            (node_id, node_type, success_count, failure_count,
                             confidence_score, latency_avg_ms, cost_avg_tokens,
                             hallucination_flag_count, last_updated)
                        VALUES (?, ?, ?, ?, 0.5, ?, ?, ?, ?)
                        ON CONFLICT(node_id, node_type) DO UPDATE SET
                            success_count = success_count + ?,
                            failure_count = failure_count + ?,
                            hallucination_flag_count = hallucination_flag_count + ?,
                            latency_avg_ms = (latency_avg_ms * (success_count + failure_count) + ?) /
                                             (success_count + failure_count + 1),
                            cost_avg_tokens = (cost_avg_tokens * (success_count + failure_count) + ?) /
                                              (success_count + failure_count + 1),
                            last_updated = ?
                    """, (
                        node_id, node_type,
                        1 if success else 0,
                        0 if success else 1,
                        latency_ms, cost_tokens,
                        1 if hallucination else 0,
                        ts,
                        # UPDATE values:
                        1 if success else 0,
                        0 if success else 1,
                        1 if hallucination else 0,
                        latency_ms,
                        cost_tokens,
                        ts,
                    ))
                    # Log event
                    conn.execute("""
                        INSERT INTO reinforcement_events
                            (ts, node_id, node_type, success, latency_ms, cost_tokens, hallucination)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (ts, node_id, node_type, 1 if success else 1 if not success else 0,
                          latency_ms, cost_tokens, 1 if hallucination else 0))
                    conn.commit()

                    # Recompute confidence from recent events
                    row = conn.execute("""
                        SELECT success_count, failure_count, hallucination_flag_count
                        FROM reinforcement_graph WHERE node_id=? AND node_type=?
                    """, (node_id, node_type)).fetchone()
                    events = conn.execute("""
                        SELECT ts, success FROM reinforcement_events
                        WHERE node_id=? AND node_type=? ORDER BY id DESC LIMIT 100
                    """, (node_id, node_type)).fetchall()
                    if row:
                        new_conf = _compute_confidence(
                            row[0], row[1], row[2],
                            [{"ts": e[0], "success": e[1]} for e in events]
                        )
                        conn.execute("""
                            UPDATE reinforcement_graph SET confidence_score=?
                            WHERE node_id=? AND node_type=?
                        """, (new_conf, node_id, node_type))
                        conn.commit()
                    conn.close()
                    return
                except Exception as e:
                    print(f"  [REINFORCE] DB write failed: {e}")
                    try:
                        conn.close()
                    except Exception:
                        pass

            # JSON fallback
            data = _load_json_graph()
            key = f"{node_type}::{node_id}"
            node = data["nodes"].get(key, {
                "node_id": node_id, "node_type": node_type,
                "success_count": 0, "failure_count": 0,
                "confidence_score": 0.5, "latency_avg_ms": 0.0,
                "cost_avg_tokens": 0.0, "hallucination_flag_count": 0,
                "last_updated": ts,
            })
            s, f = node["success_count"], node["failure_count"]
            total = s + f
            node["success_count"] = s + (1 if success else 0)
            node["failure_count"] = f + (0 if success else 1)
            node["hallucination_flag_count"] += 1 if hallucination else 0
            node["latency_avg_ms"] = (node["latency_avg_ms"] * total + latency_ms) / (total + 1)
            node["cost_avg_tokens"] = (node["cost_avg_tokens"] * total + cost_tokens) / (total + 1)
            node["last_updated"] = ts

            events_list = data.get("events", [])
            events_list.append({"ts": ts, "node_id": node_id, "node_type": node_type,
                                  "success": success, "hallucination": hallucination})
            if len(events_list) > 2000:
                events_list = events_list[-2000:]
            data["events"] = events_list

            node_events = [
                {"ts": e["ts"], "success": e["success"]}
                for e in events_list if e.get("node_id") == node_id
            ]
            node["confidence_score"] = _compute_confidence(
                node["success_count"], node["failure_count"],
                node["hallucination_flag_count"], node_events
            )
            data["nodes"][key] = node
            _save_json_graph(data)

    def get_reliability(self, node_id: str, node_type: str = "skill") -> Dict[str, Any]:
        """Return current metrics for a node."""
        conn = _get_db_conn()
        if conn:
            try:
                row = conn.execute("""
                    SELECT node_id, node_type, success_count, failure_count,
                           confidence_score, latency_avg_ms, cost_avg_tokens,
                           hallucination_flag_count, last_updated
                    FROM reinforcement_graph WHERE node_id=? AND node_type=?
                """, (node_id, node_type)).fetchone()
                conn.close()
                if row:
                    return {
                        "node_id": row[0], "node_type": row[1],
                        "success_count": row[2], "failure_count": row[3],
                        "confidence_score": round(row[4], 3),
                        "latency_avg_ms": round(row[5], 1),
                        "cost_avg_tokens": round(row[6], 1),
                        "hallucination_flag_count": row[7],
                        "last_updated": row[8],
                    }
            except Exception as e:
                print(f"  [REINFORCE] DB read failed: {e}")
                try:
                    conn.close()
                except Exception:
                    pass

        data = _load_json_graph()
        key = f"{node_type}::{node_id}"
        return data["nodes"].get(key, {"node_id": node_id, "node_type": node_type,
                                        "confidence_score": 0.5, "note": "no data yet"})

    def detect_drift(self, threshold: float = DRIFT_THRESHOLD) -> List[Dict]:
        """
        Return nodes where confidence has dropped significantly in the last 24 hours.
        Uses the event log to compute yesterday's confidence vs today's.
        """
        drifted = []
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()

        conn = _get_db_conn()
        if conn:
            try:
                nodes = conn.execute("""
                    SELECT node_id, node_type, confidence_score
                    FROM reinforcement_graph
                """).fetchall()
                for n_id, n_type, current_conf in nodes:
                    # Get events from last 24h vs older
                    old_events = conn.execute("""
                        SELECT success FROM reinforcement_events
                        WHERE node_id=? AND node_type=? AND ts < ?
                        ORDER BY id DESC LIMIT 50
                    """, (n_id, n_type, cutoff)).fetchall()
                    if len(old_events) < 3:
                        continue
                    old_success = sum(1 for e in old_events if e[0])
                    old_conf = old_success / len(old_events)
                    drop = old_conf - current_conf
                    if drop >= threshold:
                        drifted.append({
                            "node_id": n_id,
                            "node_type": n_type,
                            "previous_confidence": round(old_conf, 3),
                            "current_confidence": round(current_conf, 3),
                            "drop": round(drop, 3),
                        })
                conn.close()
                return drifted
            except Exception as e:
                print(f"  [REINFORCE] Drift detection DB error: {e}")
                try:
                    conn.close()
                except Exception:
                    pass

        # JSON fallback — simplified
        data = _load_json_graph()
        events_list = data.get("events", [])
        for key, node in data["nodes"].items():
            current_conf = node.get("confidence_score", 0.5)
            old_events = [
                e for e in events_list
                if e.get("node_id") == node["node_id"] and e.get("ts", "") < cutoff
            ]
            if len(old_events) < 3:
                continue
            old_success = sum(1 for e in old_events if e.get("success"))
            old_conf = old_success / len(old_events)
            if old_conf - current_conf >= threshold:
                drifted.append({
                    "node_id": node["node_id"],
                    "node_type": node["node_type"],
                    "previous_confidence": round(old_conf, 3),
                    "current_confidence": round(current_conf, 3),
                    "drop": round(old_conf - current_conf, 3),
                })
        return drifted

    def get_dashboard(self) -> Dict[str, Any]:
        """Return full snapshot of all nodes for telemetry dashboard."""
        conn = _get_db_conn()
        nodes = []
        if conn:
            try:
                rows = conn.execute("""
                    SELECT node_id, node_type, success_count, failure_count,
                           confidence_score, latency_avg_ms, cost_avg_tokens,
                           hallucination_flag_count, last_updated
                    FROM reinforcement_graph ORDER BY confidence_score ASC
                """).fetchall()
                conn.close()
                for r in rows:
                    total = r[2] + r[3]
                    nodes.append({
                        "node_id": r[0], "node_type": r[1],
                        "success_count": r[2], "failure_count": r[3],
                        "total_attempts": total,
                        "confidence_score": round(r[4], 3),
                        "latency_avg_ms": round(r[5], 1),
                        "cost_avg_tokens": round(r[6], 1),
                        "hallucination_flag_count": r[7],
                        "last_updated": r[8],
                    })
                return {
                    "total_nodes": len(nodes),
                    "nodes": nodes,
                    "drift_alerts": self.detect_drift(),
                    "generated_at": datetime.now().isoformat(),
                }
            except Exception as e:
                print(f"  [REINFORCE] Dashboard DB error: {e}")
                try:
                    conn.close()
                except Exception:
                    pass

        data = _load_json_graph()
        fallback_nodes = list(data["nodes"].values())
        return {
            "total_nodes": len(fallback_nodes),
            "nodes": fallback_nodes,
            "drift_alerts": self.detect_drift(),
            "generated_at": datetime.now().isoformat(),
            "source": "json_fallback",
        }


# ── Singleton ──────────────────────────────────────────────────────────────────
_graph_instance: Optional[ReinforcementGraph] = None


def get_reinforcement_graph() -> ReinforcementGraph:
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = ReinforcementGraph()
    return _graph_instance


# ── Tool Functions ─────────────────────────────────────────────────────────────

def get_reinforcement_stats(**kwargs) -> Dict:
    """Get full Reinforcement Graph dashboard including drift alerts."""
    graph = get_reinforcement_graph()
    return {"ok": True, **graph.get_dashboard()}


def record_reinforcement_outcome(**kwargs) -> Dict:
    """Record a skill/tool/model outcome event. Called by other modules."""
    graph = get_reinforcement_graph()
    graph.record_outcome(
        node_id=str(kwargs.get("node_id", "unknown")),
        node_type=str(kwargs.get("node_type", "skill")),
        success=bool(kwargs.get("success", True)),
        latency_ms=float(kwargs.get("latency_ms", 0.0)),
        cost_tokens=float(kwargs.get("cost_tokens", 0.0)),
        hallucination=bool(kwargs.get("hallucination", False)),
    )
    return {"ok": True, "recorded": True}


# ── Tool + Route Registration ──────────────────────────────────────────────────
try:
    import joi_companion
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "get_reinforcement_stats",
            "description": (
                "Get Joi's Reinforcement Graph dashboard — quantitative skill/tool/model "
                "reliability metrics, confidence scores, drift alerts, and hallucination counts."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []}
        }},
        get_reinforcement_stats
    )
    print("  [OK] joi_reinforcement_graph loaded (ReinforcementGraph active)")
except Exception as _e:
    print(f"  [WARN] joi_reinforcement_graph: tool registration skipped ({_e})")

try:
    import joi_companion

    def _rf_route():
        from flask import jsonify
        return jsonify(get_reinforcement_stats())

    joi_companion.register_route("/reinforcement/stats", ["GET"], _rf_route, "reinforcement_stats_route")
except Exception:
    pass
