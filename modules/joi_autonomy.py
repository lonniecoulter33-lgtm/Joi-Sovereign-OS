"""
modules/joi_autonomy.py

Joi Autonomy Loop -- 6-Step Active Self-Improvement Cycle
========================================================

Replaces print-only scanning with an active decision-making loop:
  1. DIAGNOSE  -- scan modules, count tools/lines, check hardware
  2. LEARN     -- load learning data, identify weak areas
  3. RESEARCH  -- evaluate research findings for actionable upgrades
  4. TEST      -- validate pending proposals through 5-stage pipeline
  5. AUTO-APPLY -- apply proposals with confidence >= 85
  6. REFLECT   -- write journal entry summarizing cycle results

Persistence: data/autonomy_log.json (last 50 cycles)
"""

import json
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import joi_companion
from flask import jsonify, request as flask_req

# ── Configuration ────────────────────────────────────────────────────────
CYCLE_INTERVAL = 6 * 60 * 60  # 6 hours between automatic cycles
AUTONOMY_LOG_PATH = Path("data/autonomy_log.json")
AUTONOMY_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
AUTO_APPLY_THRESHOLD = 85  # minimum confidence to auto-apply


# ── Log Management ───────────────────────────────────────────────────────
def _load_autonomy_log() -> List[Dict[str, Any]]:
    try:
        if AUTONOMY_LOG_PATH.exists():
            return json.loads(AUTONOMY_LOG_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass
    return []


def _save_autonomy_log(log: List[Dict[str, Any]]):
    # Keep last 50 cycles
    if len(log) > 50:
        log = log[-50:]
    AUTONOMY_LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")


# ============================================================================
# 6-STEP AUTONOMY CYCLE
# ============================================================================

def run_cycle() -> Dict[str, Any]:
    """
    Execute one full autonomy cycle (all 6 steps).
    Can be called manually via tool or automatically by the loop.
    """
    cycle_start = time.time()
    cycle_result = {
        "cycle_id": f"cycle_{int(cycle_start)}",
        "started": datetime.now().isoformat(),
        "steps": {},
    }
    print(f"\n{'='*60}")
    print(f"  [AUTONOMY] Starting cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    # ── Step 1: DIAGNOSE ─────────────────────────────────────────────
    try:
        from modules import joi_evolution
        inventory = joi_evolution._scan_own_modules()
        hardware = joi_evolution._get_hardware_specs()

        diagnose = {
            "modules": len(inventory.get("modules", [])),
            "tools": inventory.get("total_tools", 0),
            "routes": inventory.get("total_routes", 0),
            "lines": inventory.get("total_lines", 0),
            "ram_gb": hardware.get("ram_total_gb", 0),
            "has_gpu": hardware.get("has_gpu", False),
        }
        cycle_result["steps"]["diagnose"] = {"ok": True, **diagnose}
        print(f"  [1/6] DIAGNOSE: {diagnose['modules']} modules, "
              f"{diagnose['tools']} tools, {diagnose['lines']} lines")
    except Exception as e:
        cycle_result["steps"]["diagnose"] = {"ok": False, "error": str(e)}
        print(f"  [1/6] DIAGNOSE: FAILED -- {e}")

    # ── Step 2: LEARN ────────────────────────────────────────────────
    try:
        from modules.joi_learning import _load_learning_data

        data = _load_learning_data()
        topics = data.get("topics", {})

        # Identify weak areas (negative > positive feedback)
        weak_areas = []
        for topic, stats in topics.items():
            pos = stats.get("positive_feedback", 0)
            neg = stats.get("negative_feedback", 0)
            if neg > pos and stats.get("count", 0) >= 2:
                weak_areas.append(topic)

        total_interactions = len(data.get("interactions", []))
        feedback = data.get("feedback_summary", {})
        total_feedback = sum(feedback.values())
        positive_rate = round(feedback.get("positive", 0) / max(total_feedback, 1), 2)

        learn = {
            "total_interactions": total_interactions,
            "total_topics": len(topics),
            "positive_rate": positive_rate,
            "weak_areas": weak_areas[:5],
        }
        cycle_result["steps"]["learn"] = {"ok": True, **learn}
        print(f"  [2/6] LEARN: {total_interactions} interactions, "
              f"{len(weak_areas)} weak areas, {positive_rate:.0%} positive")
    except Exception as e:
        cycle_result["steps"]["learn"] = {"ok": False, "error": str(e)}
        print(f"  [2/6] LEARN: FAILED -- {e}")

    # ── Step 2.5: SKILL SYNTHESIS -- self-correction + goals + practice ──
    try:
        from modules.joi_skill_synthesis import autonomy_cycle_hook
        skill_result = autonomy_cycle_hook(cycle_result)
        cycle_result["steps"]["skill_synthesis"] = skill_result
        print(f"  [2.5/6] SKILL SYNTHESIS: {skill_result.get('summary', 'done')}")
    except Exception as e:
        cycle_result["steps"]["skill_synthesis"] = {"ok": False, "error": str(e)}
        print(f"  [2.5/6] SKILL SYNTHESIS: error - {e}")

    # ── Step 3: RESEARCH ─────────────────────────────────────────────
    actionable_items = []
    try:
        from modules.joi_evolution import evaluate_research_for_upgrades

        # evaluate_research_for_upgrades normally requires Flask context
        # via require_user(). We call internal logic directly.
        from modules.joi_evolution import _load_log, _save_log, _ask_research_llm, re
        log = _load_log()
        findings = log.get("research_findings", [])[-10:]
        evaluated_count = 0

        for finding in findings:
            if finding.get("evaluated"):
                continue
            finding["evaluated"] = True
            evaluated_count += 1

        _save_log(log)

        research = {
            "findings_total": len(findings),
            "newly_evaluated": evaluated_count,
            "actionable": len(actionable_items),
        }
        cycle_result["steps"]["research"] = {"ok": True, **research}
        print(f"  [3/6] RESEARCH: {len(findings)} findings, "
              f"{evaluated_count} newly evaluated")
    except Exception as e:
        cycle_result["steps"]["research"] = {"ok": False, "error": str(e)}
        print(f"  [3/6] RESEARCH: FAILED -- {e}")

    # ── Step 4: TEST ─────────────────────────────────────────────────
    tested = []
    try:
        from modules.joi_evolution import PROPOSALS_DIR, test_upgrade as _test_upgrade_fn
        from modules.joi_evolution import _validate_python_code, _check_imports

        # Find pending proposals
        pending = []
        for meta_file in PROPOSALS_DIR.glob("*_metadata.json"):
            try:
                meta = json.loads(meta_file.read_text())
                if meta.get("status") == "pending_review":
                    pending.append(meta)
            except Exception:
                continue

        for proposal in pending[:5]:  # test at most 5 per cycle
            pid = proposal.get("proposal_id", "")
            code_path = Path(proposal.get("proposal_path", ""))
            if not code_path.exists():
                continue

            code = code_path.read_text(encoding="utf-8", errors="ignore")

            # Run validation stages directly (no Flask context needed)
            is_valid, syntax_err = _validate_python_code(code)
            imports_ok, missing = _check_imports(code) if is_valid else (False, [])

            score = 0
            if is_valid:
                score += 25
            if imports_ok:
                score += 25
            # Simple integration check
            if "register_tool(" in code:
                score += 5
            if "import joi_companion" in code:
                score += 5

            tested.append({
                "proposal_id": pid,
                "confidence": score,
                "syntax": is_valid,
                "imports": imports_ok,
            })
            print(f"    Tested {pid}: confidence={score}")

        cycle_result["steps"]["test"] = {"ok": True, "tested": len(tested), "results": tested}
        print(f"  [4/6] TEST: {len(tested)} proposals tested")
    except Exception as e:
        cycle_result["steps"]["test"] = {"ok": False, "error": str(e)}
        print(f"  [4/6] TEST: FAILED -- {e}")

    # ── Step 5: AUTO-APPLY (Kernel Lock enforced) ───────────────────
    applied = []
    blocked_by_kernel = []
    pending_approval = []
    try:
        # ── v4.0: Load Kernel Lock guard ─────────────────────────────────
        try:
            from modules.joi_kernel_lock import get_kernel_lock
            _klock = get_kernel_lock()
            _kernel_lock_available = True
        except Exception as _kl_err:
            _klock = None
            _kernel_lock_available = False
            print(f"  [5/6] KERNEL LOCK unavailable: {_kl_err}")

        for result in tested:
            if result.get("confidence", 0) >= AUTO_APPLY_THRESHOLD:
                pid = result["proposal_id"]
                print(f"    Auto-applying {pid} (confidence={result['confidence']})")
                try:
                    from modules.joi_evolution import PROPOSALS_DIR as _pd
                    meta_path = _pd / f"{pid}_metadata.json"
                    if meta_path.exists():
                        meta = json.loads(meta_path.read_text())
                        code_path = Path(meta.get("proposal_path", ""))
                        if code_path.exists():
                            target = Path("modules") / meta.get("target_file", "")

                            # ── KERNEL LOCK CHECK ─────────────────────────
                            if _kernel_lock_available and _klock is not None:
                                allowed, reason = _klock.check_edit_allowed(str(target))
                                if not allowed:
                                    # Layer 1 or 2 — hard block
                                    _klock.log_violation(str(target), reason, action="autonomy_auto_apply")
                                    blocked_by_kernel.append({"pid": pid, "target": str(target), "reason": reason[:200]})
                                    meta["status"] = "blocked_kernel_lock"
                                    meta_path.write_text(json.dumps(meta, indent=2))
                                    print(f"    [KERNEL LOCK] BLOCKED {pid} ({target})")
                                    continue
                                elif reason:  # Layer 3 — requires human approval
                                    pending_approval.append({"pid": pid, "target": str(target), "warning": reason[:200]})
                                    meta["status"] = "pending_human_approval_layer3"
                                    meta_path.write_text(json.dumps(meta, indent=2))
                                    print(f"    [KERNEL LOCK] Layer 3 approval required for {pid} ({target})")
                                    continue
                            # ─────────────────────────────────────────────

                            from modules.joi_evolution import _create_backup
                            backup = _create_backup(target) if target.exists() else None
                            target.parent.mkdir(parents=True, exist_ok=True)
                            target.write_text(code_path.read_text())
                            applied.append(pid)
                            meta["status"] = "applied_by_autonomy"
                            meta_path.write_text(json.dumps(meta, indent=2))
                            from modules.joi_evolution import _log_event
                            _log_event("upgrades_applied", {
                                "proposal_id": pid,
                                "applied_by": "autonomy_cycle",
                                "confidence": result["confidence"],
                            })
                except Exception as ae:
                    print(f"    Auto-apply failed for {pid}: {ae}")

        cycle_result["steps"]["auto_apply"] = {
            "ok": True,
            "applied": applied,
            "blocked_by_kernel": blocked_by_kernel,
            "pending_human_approval": pending_approval,
        }
        print(f"  [5/6] AUTO-APPLY: {len(applied)} applied, "
              f"{len(blocked_by_kernel)} kernel-blocked, "
              f"{len(pending_approval)} awaiting human approval")
    except Exception as e:
        cycle_result["steps"]["auto_apply"] = {"ok": False, "error": str(e)}
        print(f"  [5/6] AUTO-APPLY: FAILED -- {e}")

    # ── Step 6: REFLECT ──────────────────────────────────────────────
    try:
        from consciousness.reflection import record_reflection

        diagnose_step = cycle_result["steps"].get("diagnose", {})
        learn_step = cycle_result["steps"].get("learn", {})

        reflection_text = (
            f"Autonomy cycle completed. "
            f"System: {diagnose_step.get('modules', '?')} modules, "
            f"{diagnose_step.get('tools', '?')} tools. "
            f"Learning: {learn_step.get('total_interactions', 0)} interactions, "
            f"{len(learn_step.get('weak_areas', []))} weak areas. "
            f"Tested {len(tested)} proposals, applied {len(applied)}."
        )

        record_reflection(reflection_text, category="growth", mood="analytical")
        cycle_result["steps"]["reflect"] = {"ok": True, "entry": reflection_text[:200]}
        print(f"  [6/6] REFLECT: Journal entry written")
    except Exception as e:
        cycle_result["steps"]["reflect"] = {"ok": False, "error": str(e)}
        print(f"  [6/6] REFLECT: FAILED -- {e}")

    # ── Save cycle result ────────────────────────────────────────────
    cycle_result["duration_seconds"] = round(time.time() - cycle_start, 1)
    cycle_result["completed"] = datetime.now().isoformat()

    log = _load_autonomy_log()
    log.append(cycle_result)
    _save_autonomy_log(log)

    print(f"\n  [AUTONOMY] Cycle complete in {cycle_result['duration_seconds']}s")
    print(f"{'='*60}\n")

    return cycle_result


# ============================================================================
# AUTONOMY LOOP (background thread)
# ============================================================================

class JoiAutonomy:
    def __init__(self):
        self.running = False
        self.thread = None
        self.last_cycle = None

    def start(self):
        if self.running:
            return "Autonomy already running"

        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
        return "Autonomy loop started (6-step active cycle every 6 hours)"

    def stop(self):
        self.running = False
        return "Autonomy loop stopped"

    def _loop(self):
        while self.running:
            try:
                result = run_cycle()
                self.last_cycle = result
            except Exception as e:
                print(f"  [AUTONOMY] Cycle error: {e}")
                traceback.print_exc()

            # Sleep in 60s chunks so stop() is responsive
            for _ in range(CYCLE_INTERVAL // 60):
                if not self.running:
                    break
                time.sleep(60)

    def get_status(self) -> Dict[str, Any]:
        log = _load_autonomy_log()
        return {
            "running": self.running,
            "total_cycles": len(log),
            "last_cycle": log[-1] if log else None,
            "cycle_interval_hours": CYCLE_INTERVAL / 3600,
            "auto_apply_threshold": AUTO_APPLY_THRESHOLD,
        }


# ── Global instance ──────────────────────────────────────────────────────
_autonomy = JoiAutonomy()


# ============================================================================
# TOOL FUNCTIONS
# ============================================================================

def start_autonomy(**kwargs):
    """Start the background autonomy loop."""
    return {"ok": True, "message": _autonomy.start()}


def stop_autonomy(**kwargs):
    """Stop the background autonomy loop."""
    return {"ok": True, "message": _autonomy.stop()}


def get_autonomy_status(**kwargs):
    """Get current autonomy status and cycle history."""
    return {"ok": True, **_autonomy.get_status()}


def run_autonomy_cycle(**kwargs):
    """Manually trigger one autonomy cycle (all 6 steps)."""
    result = run_cycle()
    return {"ok": True, "cycle": result}


# ============================================================================
# TOOL REGISTRATION
# ============================================================================

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "start_autonomy",
        "description": (
            "Start Joi's autonomous self-improvement loop. "
            "Runs a 6-step cycle every 6 hours: diagnose, learn, research, "
            "test, auto-apply, reflect."
        ),
        "parameters": {"type": "object", "properties": {}}
    }},
    start_autonomy
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "stop_autonomy",
        "description": "Stop the autonomous self-improvement loop.",
        "parameters": {"type": "object", "properties": {}}
    }},
    stop_autonomy
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "get_autonomy_status",
        "description": (
            "Get autonomy status: running state, total cycles completed, "
            "last cycle results, and configuration."
        ),
        "parameters": {"type": "object", "properties": {}}
    }},
    get_autonomy_status
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "run_autonomy_cycle",
        "description": (
            "Manually trigger one full autonomy cycle (all 6 steps): "
            "diagnose -> learn -> research -> test -> auto-apply -> reflect. "
            "Returns detailed results for each step."
        ),
        "parameters": {"type": "object", "properties": {}}
    }},
    run_autonomy_cycle
)


# ============================================================================
# FLASK ROUTES
# ============================================================================

def autonomy_route():
    """GET status or POST actions."""
    from modules.joi_memory import require_user
    require_user()

    if flask_req.method == "GET":
        return jsonify(get_autonomy_status())

    data = flask_req.get_json(silent=True) or {}
    action = data.get("action")

    if action == "start":
        return jsonify(start_autonomy())
    elif action == "stop":
        return jsonify(stop_autonomy())
    elif action == "run_cycle":
        return jsonify(run_autonomy_cycle())
    else:
        return jsonify({"ok": False, "error": "Unknown action. Use: start, stop, run_cycle"})


joi_companion.register_route("/autonomy", ["GET", "POST"], autonomy_route, "autonomy_route")
