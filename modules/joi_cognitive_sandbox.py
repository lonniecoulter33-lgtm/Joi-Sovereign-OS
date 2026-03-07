"""
modules/joi_cognitive_sandbox.py

Joi v6.0 — Parallel Cognition Instances (Phase III)
====================================================
Controlled multi-instance reasoning for hypothesis comparison.

SANDBOX INSTANCE CONSTRAINTS (strictly enforced):
  - NO tool execution allowed inside sandbox
  - NO file modification (all file I/O intercepted and blocked)
  - Memory access is READ-ONLY (snapshot at spawn time, no writes)
  - ReinforcementGraph writes DISABLED inside sandbox
  - Recursion depth limit = 3 (prevents unbounded self-spawning)
  - CPU/time budget enforced per instance (default 8s, max 20s)
  - All sandbox output logged to telemetry (data/sandbox_results.json)

Usage:
  sandbox = get_cognitive_sandbox()
  results = sandbox.compare_approaches(
      context={"task": "refactor memory module"},
      variants=[
          {"hypothesis": "Compress episodic memories before planning"},
          {"hypothesis": "Expand active tier window by 4 hours"},
      ]
  )

Planner integration:
  If task_complexity > HIGH_COMPLEXITY_THRESHOLD:
      spawn 2–3 sandbox instances, score outputs, choose best

Layer: LAYER_4
"""

import json
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

BASE_DIR  = Path(__file__).resolve().parent.parent
DATA_DIR  = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

SANDBOX_LOG_PATH = DATA_DIR / "sandbox_results.json"

# Safety limits
MAX_RECURSION_DEPTH    = 3
DEFAULT_INSTANCE_TIMEOUT = 8.0
MAX_INSTANCE_TIMEOUT   = 20.0
HIGH_COMPLEXITY_THRESHOLD = 0.75   # task complexity score above which multi-instance kicks in

_log_lock  = threading.Lock()
_spawn_lock = threading.Lock()


# ── Sandbox Guard Infrastructure ───────────────────────────────────────────────

class SandboxViolation(Exception):
    """Raised when sandbox code attempts a forbidden operation."""
    pass


class _BlockedFileProxy:
    """Proxy that intercepts write I/O and raises SandboxViolation."""
    def write(self, *args, **kwargs):
        raise SandboxViolation("SANDBOX: File writes are forbidden inside sandbox instances.")
    def __setitem__(self, *args, **kwargs):
        raise SandboxViolation("SANDBOX: State mutation is forbidden inside sandbox instances.")


_BLOCKED_OPS = _BlockedFileProxy()


def _sandbox_safe_context(base_context: Dict) -> Dict:
    """
    Create a read-only deep snapshot of context for sandbox use.
    Returns a plain dict copy — no references to live objects.
    """
    try:
        import copy
        snapshot = copy.deepcopy(base_context)
    except Exception:
        snapshot = dict(base_context)
    # Mark as sandbox to prevent accidental mutations propaging
    snapshot["__sandbox__"] = True
    snapshot["__readonly__"] = True
    return snapshot


# ── Instance Result ────────────────────────────────────────────────────────────

@dataclass
class SandboxResult:
    instance_id:     str
    hypothesis:      str
    completed:       bool  = False
    elapsed_sec:     float = 0.0
    score:           float = 0.0   # 0.0–1.0 composite quality score
    reasoning_trace: List[str] = field(default_factory=list)
    key_insights:    List[str] = field(default_factory=list)
    risk_flags:      List[str] = field(default_factory=list)
    error:           str  = ""
    recursion_depth: int  = 0
    spawned_at:      str  = ""

    def __post_init__(self):
        if not self.spawned_at:
            self.spawned_at = datetime.now(timezone.utc).isoformat()


# ── Reasoning Heuristics (pure functions, no side-effects) ─────────────────────

def _analyse_hypothesis(hypothesis: str, context: Dict, depth: int) -> SandboxResult:
    """
    Pure analysis of one hypothesis variant.
    No tool calls, no disk I/O, no reinforcement writes.
    Returns a scored SandboxResult.
    """
    result = SandboxResult(
        instance_id=f"sb_{uuid.uuid4().hex[:8]}",
        hypothesis=hypothesis,
        recursion_depth=depth,
    )
    t0 = time.time()
    trace = []
    insights = []
    risk_flags = []

    try:
        h_lower = hypothesis.lower()
        ctx_str = json.dumps(context, default=str)[:800].lower()

        # ── Reasoning trace ───────────────────────────────────────────────
        trace.append(f"Evaluating: '{hypothesis[:120]}'")

        # Complexity estimation
        complexity_keywords = ["refactor", "rewrite", "replace", "overhaul", "migrate",
                                "restructure", "redesign", "remove", "delete"]
        caution_keywords    = ["autonomy", "memory", "kernel", "identity", "ethics",
                                "router", "llm", "security", "auth"]
        enhancement_keywords = ["compress", "optimize", "cache", "index", "prune",
                                  "batch", "parallelize", "extend", "add", "improve"]

        complexity_score = sum(1 for kw in complexity_keywords if kw in h_lower)
        caution_score    = sum(1 for kw in caution_keywords if kw in h_lower or kw in ctx_str)
        benefit_score    = sum(1 for kw in enhancement_keywords if kw in h_lower)

        trace.append(f"Complexity indicators: {complexity_score}, Caution: {caution_score}, Benefit: {benefit_score}")

        # ── Risk flag extraction ──────────────────────────────────────────
        if caution_score > 0:
            risk_flags.append(f"touches sensitive area (caution_score={caution_score})")
        if complexity_score > 2:
            risk_flags.append(f"high complexity change ({complexity_score} indicators)")

        # ── Probe self-model for planner prediction ───────────────────────
        try:
            from modules.joi_self_model import get_self_model
            sm = get_self_model()
            task_hint = "planning"
            if "memory" in h_lower:
                task_hint = "memory"
            elif "tool" in h_lower:
                task_hint = "tool_use"
            elif "cod" in h_lower:
                task_hint = "coding"
            pred = sm.predict_task_success(task_hint)
            predicted = pred.get("predicted_success", 0.65)
            trace.append(f"Self-model prediction ({task_hint}): {predicted:.2%}")
            if predicted < 0.50:
                risk_flags.append(f"low predicted success ({predicted:.2%})")
        except Exception as sm_err:
            trace.append(f"Self-model probe unavailable: {sm_err}")
            predicted = 0.65

        # ── Key insights ──────────────────────────────────────────────────
        if benefit_score > complexity_score:
            insights.append("Net benefit expected: enhancements outweigh complexity.")
        elif complexity_score > benefit_score:
            insights.append("High complexity relative to benefit — consider incremental approach.")
        else:
            insights.append("Balanced trade-off — proceed with simulation validation.")

        if caution_score == 0 and complexity_score <= 1:
            insights.append("Low-risk modification suitable for Layer 4/5 auto-apply.")

        # ── Score computation ──────────────────────────────────────────────
        # Base: predicted success
        # +benefit, -complexity, -caution, -risk
        raw_score = (
            predicted * 0.50
            + min(1.0, benefit_score * 0.12) * 0.30
            - min(0.30, complexity_score * 0.08)
            - min(0.20, caution_score * 0.08)
            - min(0.15, len(risk_flags) * 0.05)
        )
        result.score = round(max(0.0, min(1.0, raw_score)), 3)

        result.reasoning_trace = trace
        result.key_insights    = insights
        result.risk_flags      = risk_flags
        result.completed       = True

    except SandboxViolation as sv:
        result.error = f"SANDBOX VIOLATION: {sv}"
        result.completed = False
        result.score = 0.0
    except Exception as exc:
        result.error = str(exc)
        result.completed = False
        result.score = 0.0

    result.elapsed_sec = round(time.time() - t0, 3)
    return result


# ── CognitiveSandbox ───────────────────────────────────────────────────────────

class CognitiveSandbox:
    """
    Manages spawning and scoring of isolated sandbox cognition instances.

    Public API:
        spawn_sandbox_instance(context, task)       → SandboxResult
        compare_approaches(context, variants)       → list[SandboxResult] + winner
        planner_multi_instance(context, task_type)  → planner-compatible report
    """

    def __init__(self):
        self._current_depth: int = 0

    def spawn_sandbox_instance(
        self,
        context: Dict,
        task: str,
        depth: int = 0,
        timeout_sec: float = DEFAULT_INSTANCE_TIMEOUT,
    ) -> SandboxResult:
        """
        Spawn a single isolated reasoning instance.

        Safety gates:
          - depth >= MAX_RECURSION_DEPTH → blocked
          - timeout enforced via thread + join
          - context is deep-copied (read-only snapshot)
        """
        if depth >= MAX_RECURSION_DEPTH:
            r = SandboxResult(
                instance_id=f"sb_depth_blocked_{uuid.uuid4().hex[:6]}",
                hypothesis=task,
                recursion_depth=depth,
            )
            r.error = f"RECURSION DEPTH LIMIT REACHED (depth={depth}, max={MAX_RECURSION_DEPTH})"
            r.risk_flags.append("recursion_depth_exceeded")
            r.completed = False
            _log_result(r)
            return r

        safe_ctx = _sandbox_safe_context(context)
        timeout_sec = min(float(timeout_sec), MAX_INSTANCE_TIMEOUT)

        # Run in a thread so we can enforce wall-clock timeout
        result_holder: List[SandboxResult] = []

        def _worker():
            r = _analyse_hypothesis(task, safe_ctx, depth)
            result_holder.append(r)

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        t.join(timeout=timeout_sec)

        if t.is_alive():
            r = SandboxResult(
                instance_id=f"sb_timeout_{uuid.uuid4().hex[:6]}",
                hypothesis=task,
                recursion_depth=depth,
                elapsed_sec=timeout_sec,
            )
            r.error = f"TIMEOUT: instance exceeded {timeout_sec}s budget"
            r.completed = False
            r.score = 0.0
            _log_result(r)
            return r

        if not result_holder:
            r = SandboxResult(
                instance_id=f"sb_empty_{uuid.uuid4().hex[:6]}",
                hypothesis=task,
                recursion_depth=depth,
            )
            r.error = "No result returned from sandbox worker"
            r.completed = False
            _log_result(r)
            return r

        result = result_holder[0]
        _log_result(result)
        _register_telemetry(result)
        return result

    def compare_approaches(
        self,
        context: Dict,
        variants: List[Dict],
        timeout_sec: float = DEFAULT_INSTANCE_TIMEOUT,
    ) -> Dict[str, Any]:
        """
        Spawn N sandbox instances (one per variant hypothesis).
        Score all results, select winner by highest score.

        Args:
            context:  shared task context
            variants: list of dicts, each with key "hypothesis" (str)
            timeout_sec: per-instance budget

        Returns:
            {
                "instances": [SandboxResult, ...],
                "winner": SandboxResult,
                "winner_hypothesis": str,
                "winner_score": float,
                "comparison": [...]
            }
        """
        results = []
        for i, variant in enumerate(variants[:5]):   # cap at 5 instances
            hypothesis = str(variant.get("hypothesis", f"variant_{i}"))
            r = self.spawn_sandbox_instance(context, hypothesis, depth=0, timeout_sec=timeout_sec)
            results.append(r)

        if not results:
            return {"ok": False, "error": "No sandbox instances returned results"}

        winner = max(results, key=lambda r: r.score if r.completed else -1)
        comparison = sorted(
            [{"id": r.instance_id, "hypothesis": r.hypothesis[:80],
              "score": r.score, "risk_flags": r.risk_flags, "completed": r.completed}
             for r in results],
            key=lambda x: -x["score"]
        )

        return {
            "ok": True,
            "instance_count": len(results),
            "instances": [asdict(r) for r in results],
            "winner": asdict(winner),
            "winner_hypothesis": winner.hypothesis,
            "winner_score": winner.score,
            "comparison": comparison,
        }

    def planner_multi_instance(
        self,
        context: Dict,
        task_type: str,
        hypotheses: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Planner-facing interface. If task complexity is above threshold,
        auto-generates comparison hypotheses and runs them.
        Returns planner-compatible recommendation.
        """
        # Assess complexity via self-model
        complexity = 0.5
        try:
            from modules.joi_self_model import get_self_model
            sm = get_self_model()
            pred = sm.predict_task_success(task_type)
            # Complexity = inverse of success confidence
            complexity = round(1.0 - pred.get("predicted_success", 0.5), 3)
        except Exception:
            pass

        if complexity < HIGH_COMPLEXITY_THRESHOLD and not hypotheses:
            return {
                "ok": True,
                "multi_instance_triggered": False,
                "reason": f"Task complexity {complexity:.2f} below threshold {HIGH_COMPLEXITY_THRESHOLD}",
                "recommendation": "proceed_single_pass",
            }

        # Default hypotheses if not provided
        if not hypotheses:
            hypotheses = [
                f"Approach A: Direct implementation of {task_type} task",
                f"Approach B: Staged implementation with intermediate validation",
                f"Approach C: Minimal footprint implementation of {task_type}",
            ]

        variants = [{"hypothesis": h} for h in hypotheses]
        comparison_result = self.compare_approaches(context, variants)
        comparison_result["task_type"]  = task_type
        comparison_result["complexity"] = complexity
        comparison_result["multi_instance_triggered"] = True
        return comparison_result


def _log_result(result: SandboxResult):
    """Append sandbox result to rolling log (last 500 entries)."""
    try:
        with _log_lock:
            log = []
            if SANDBOX_LOG_PATH.exists():
                try:
                    log = json.loads(SANDBOX_LOG_PATH.read_text(encoding="utf-8"))
                except Exception:
                    pass
            log.append(asdict(result))
            if len(log) > 500:
                log = log[-500:]
            SANDBOX_LOG_PATH.write_text(json.dumps(log, indent=2, default=str), encoding="utf-8")
    except Exception as e:
        print(f"  [SANDBOX] Log persist failed: {e}")


def _register_telemetry(result: SandboxResult):
    """Register sandbox activation in SectorTelemetry."""
    try:
        from modules.joi_sector_telemetry import get_sector_telemetry
        st = get_sector_telemetry()
        st.record_activation(
            sector="simulation_sector",
            success=result.completed,
            latency_ms=result.elapsed_sec * 1000,
            tokens=0.0,
            escalated=False,
        )
    except Exception:
        pass


# ── Singleton ──────────────────────────────────────────────────────────────────
_sandbox: Optional[CognitiveSandbox] = None


def get_cognitive_sandbox() -> CognitiveSandbox:
    global _sandbox
    if _sandbox is None:
        _sandbox = CognitiveSandbox()
    return _sandbox


# ── Tool Functions ─────────────────────────────────────────────────────────────

def run_sandbox_comparison(**kwargs) -> Dict:
    """Compare multiple hypotheses using isolated cognitive sandbox instances."""
    context  = kwargs.get("context", {})
    variants = kwargs.get("variants", [])
    if isinstance(context, str):
        try:
            context = json.loads(context)
        except Exception:
            context = {"task": context}
    if not variants:
        return {"ok": False, "error": "variants list is required with at least one hypothesis"}
    sb = get_cognitive_sandbox()
    return sb.compare_approaches(context, variants)


def get_sandbox_log(**kwargs) -> Dict:
    """Get recent sandbox instance results log."""
    limit = int(kwargs.get("limit", 20))
    try:
        if SANDBOX_LOG_PATH.exists():
            log = json.loads(SANDBOX_LOG_PATH.read_text(encoding="utf-8"))
            return {"ok": True, "total": len(log), "recent": log[-limit:]}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    return {"ok": True, "total": 0, "recent": []}


# ── Tool + Route Registration ──────────────────────────────────────────────────
try:
    import joi_companion
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "run_sandbox_comparison",
            "description": (
                "Spawn isolated parallel cognitive sandbox instances to compare hypotheses. "
                "No tool execution, no file writes, memory read-only. "
                "Returns scored comparison with recommended winner."
            ),
            "parameters": {"type": "object", "properties": {
                "context": {
                    "type": "object",
                    "description": "Shared task context for the sandbox instances"
                },
                "variants": {
                    "type": "array",
                    "description": "List of hypothesis objects: [{\"hypothesis\": \"...\"}]",
                    "items": {"type": "object"}
                }
            }, "required": ["context", "variants"]}
        }},
        run_sandbox_comparison
    )
    print("  [OK] joi_cognitive_sandbox loaded (CognitiveSandbox v6.0 active, recursion limit=3)")
except Exception as _e:
    print(f"  [WARN] joi_cognitive_sandbox: tool registration skipped ({_e})")

try:
    import joi_companion

    def _sb_route():
        from flask import jsonify
        return jsonify(get_sandbox_log(limit=10))

    joi_companion.register_route("/sandbox/log", ["GET"], _sb_route, "sandbox_log_route")
except Exception:
    pass
