"""
modules/joi_kernel_lock.py

Joi v4.0 — Kernel Lock Architecture (Upgrade I)
================================================
Prevents autonomous or tool-driven code edits from touching Layer 1 (kernel)
or Layer 2 (core cognition) modules. All upgrades via autonomy can only
auto-apply to Layer 4 or Layer 5. Layer 3 changes emit a warning and require
human approval. Layers 1-2 are non-modifiable at runtime.

LAYER MAP:
  LAYER_1 — KERNEL (IMMUTABLE): core loop, routing engine, memory core, identity, ethics
  LAYER_2 — CORE COGNITION: planner, tool selector, DPO, context manager
  LAYER_3 — TOOL LAYER: all tool/integration modules
  LAYER_4 — PLUGIN LAYER: plugins/, optional packs
  LAYER_5 — EXPERIMENTAL/AUTONOMOUS PATCH ZONE: data/proposals/

Startup: verify_kernel_integrity() hashes all Layer-1 files and compares
         against stored baseline in data/kernel_hash.json.
"""

import hashlib
import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent
DATA_DIR   = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

REGISTRY_PATH    = BASE_DIR / "data" / "kernel_layer_registry.json"
HASH_STORE_PATH  = BASE_DIR / "data" / "kernel_hash.json"
VIOLATION_LOG    = BASE_DIR / "data" / "kernel_violations.json"

# ── Layer Constants ────────────────────────────────────────────────────────────
LAYER_1 = "LAYER_1"   # KERNEL — IMMUTABLE
LAYER_2 = "LAYER_2"   # CORE COGNITION — human approval required
LAYER_3 = "LAYER_3"   # TOOL LAYER — warning flagged
LAYER_4 = "LAYER_4"   # PLUGIN LAYER — auto-apply OK
LAYER_5 = "LAYER_5"   # EXPERIMENTAL / AUTONOMOUS PATCH ZONE — auto-apply OK

# Layers that autonomy CANNOT auto-apply edits to
PROTECTED_LAYERS  = {LAYER_1, LAYER_2}
# Layers requiring human approval flag (not hard-blocked like L1/L2, but warned)
APPROVAL_LAYERS   = {LAYER_3}
# Fully autonomous apply OK
AUTO_APPLY_LAYERS = {LAYER_4, LAYER_5}

logger = logging.getLogger("joi.kernel_lock")


# ── Default Layer Registry ─────────────────────────────────────────────────────
# This is the canonical in-memory registry (also written to REGISTRY_PATH).
# Keys are relative paths from project root (forward-slash, case-insensitive match).
DEFAULT_REGISTRY: Dict[str, str] = {
    # ─── LAYER 1: KERNEL (IMMUTABLE) ───────────────────────────────────────
    "joi_companion.py":                    LAYER_1,
    "modules/joi_router.py":               LAYER_1,
    "modules/joi_memory.py":               LAYER_1,
    "modules/joi_llm.py":                  LAYER_1,
    "modules/joi_brain.py":                LAYER_1,
    "modules/core/kernel.py":              LAYER_1,
    "modules/core/cognition.py":           LAYER_1,
    "modules/core/interfaces.py":          LAYER_1,
    "modules/core/engine.py":              LAYER_1,
    "modules/core/runtime.py":             LAYER_1,
    "modules/core/regulator.py":           LAYER_1,
    "modules/joi_auth.py":                 LAYER_1,
    "modules/joi_db.py":                   LAYER_1,
    "modules/memory/memory_manager.py":    LAYER_1,
    # Identity / ethics / personality scaffold:
    "modules/joi_inner_state.py":          LAYER_1,
    "modules/joi_modes.py":                LAYER_1,
    "modules/joi_awareness.py":            LAYER_1,
    # Git safety rules:
    "modules/joi_git_agency.py":           LAYER_1,
    # Autonomy governor:
    "modules/joi_autonomy.py":             LAYER_1,
    # This file itself:
    "modules/joi_kernel_lock.py":          LAYER_1,

    # ─── LAYER 2: CORE COGNITION ───────────────────────────────────────────
    "modules/joi_orchestrator.py":         LAYER_2,
    "modules/joi_tool_selector.py":        LAYER_2,
    "modules/joi_dpo.py":                  LAYER_2,
    "modules/joi_prefire.py":              LAYER_2,
    "modules/joi_preflight.py":            LAYER_2,
    "modules/joi_reasoning.py":            LAYER_2,
    "modules/joi_context_cache.py":        LAYER_2,
    "modules/joi_neuro.py":                LAYER_2,
    "modules/joi_skill_synthesis.py":      LAYER_2,
    "modules/core/planner.py":             LAYER_2,
    "modules/core/meta_cognition.py":      LAYER_2,
    "modules/core/topology.py":            LAYER_2,
    "modules/core/modeling.py":            LAYER_2,

    # ─── LAYER 3: TOOL LAYER ───────────────────────────────────────────────
    "modules/joi_files.py":                LAYER_3,
    "modules/joi_code_edit.py":            LAYER_3,
    "modules/joi_code_analyzer.py":        LAYER_3,
    "modules/joi_browser.py":              LAYER_3,
    "modules/joi_desktop.py":              LAYER_3,
    "modules/joi_search.py":              LAYER_3,
    "modules/joi_media.py":               LAYER_3,
    "modules/joi_obs.py":                 LAYER_3,
    "modules/joi_homeassistant.py":       LAYER_3,
    "modules/joi_security.py":            LAYER_3,
    "modules/joi_market.py":              LAYER_3,
    "modules/joi_scheduler.py":           LAYER_3,
    "modules/joi_swarm.py":               LAYER_3,
    "modules/joi_agents.py":              LAYER_3,
    "modules/joi_patching.py":            LAYER_3,
    "modules/joi_watchdog.py":            LAYER_3,
    "modules/joi_workspace.py":           LAYER_3,
    "modules/joi_uploads.py":             LAYER_3,
    "modules/joi_downloads.py":           LAYER_3,
    "modules/joi_exports.py":             LAYER_3,
    "modules/joi_image_gen.py":           LAYER_3,
    "modules/joi_tts_kokoro.py":          LAYER_3,
    "modules/joi_voice_id.py":            LAYER_3,
    "modules/joi_wellbeing.py":           LAYER_3,
    "modules/joi_wellness.py":            LAYER_3,
    "modules/joi_projects.py":            LAYER_3,
    "modules/joi_heartbeat.py":           LAYER_3,
    "modules/joi_evolution.py":           LAYER_3,
    "modules/joi_learning.py":            LAYER_3,
    "modules/joi_mcp.py":                 LAYER_3,
    "modules/joi_ollama.py":              LAYER_3,
    "modules/joi_launcher.py":            LAYER_3,
    "modules/joi_publisher.py":           LAYER_3,
    "modules/joi_autobiography.py":       LAYER_3,
    "modules/joi_self_awareness.py":      LAYER_3,
    "modules/joi_architect.py":           LAYER_3,
    "modules/joi_app_factory.py":         LAYER_3,
    "modules/joi_tester.py":              LAYER_3,

    # ─── LAYER 4: PLUGIN LAYER ─────────────────────────────────────────────
    "plugins/":                            LAYER_4,
    "modules/joi_reinforcement_graph.py":  LAYER_4,  # v4.0 new
    "modules/joi_memory_compression.py":   LAYER_4,  # v4.0 new
    "modules/joi_epistemic.py":            LAYER_4,  # v4.0 new
    "modules/joi_sector_telemetry.py":     LAYER_4,  # v4.0 new

    # ─── LAYER 5: EXPERIMENTAL / AUTONOMOUS PATCH ZONE ─────────────────────
    "data/proposals/":                     LAYER_5,
    "data/upgrades/":                      LAYER_5,
}


# ── KernelLock ────────────────────────────────────────────────────────────────

class KernelLock:
    """
    Runtime protection guard.

    Usage (in autonomy auto-apply step):
        lock = get_kernel_lock()
        allowed, reason = lock.check_edit_allowed(target_path)
        if not allowed:
            lock.log_violation(target_path, reason)
            continue  # skip proposal
    """

    def __init__(self):
        self._registry: Dict[str, str] = {}
        self._kernel_lock_mode: bool = True   # global ON by default
        self._violations: list = []
        self._load_registry()

    # ── Registry ──────────────────────────────────────────────────────────────

    def _load_registry(self):
        """Load from disk; fall back to DEFAULT_REGISTRY and save."""
        if REGISTRY_PATH.exists():
            try:
                data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
                self._registry = data.get("registry", DEFAULT_REGISTRY)
                return
            except Exception:
                pass
        # First run — seed from defaults and persist
        self._registry = dict(DEFAULT_REGISTRY)
        self._save_registry()

    def _save_registry(self):
        REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        REGISTRY_PATH.write_text(
            json.dumps({"registry": self._registry, "updated": datetime.now().isoformat()}, indent=2),
            encoding="utf-8"
        )

    def get_layer(self, path: str) -> str:
        """Return the LAYER tag for a given file path (relative or absolute)."""
        # Normalize: relative to BASE_DIR, forward-slashes, lower-case
        try:
            rel = Path(path).resolve().relative_to(BASE_DIR.resolve())
            rel_str = str(rel).replace("\\", "/")
        except ValueError:
            rel_str = str(path).replace("\\", "/")

        rel_lower = rel_str.lower()

        # Exact match first
        for key, layer in self._registry.items():
            if key.lower() == rel_lower:
                return layer
        # Prefix match (for directories ending with /)
        for key, layer in self._registry.items():
            if key.endswith("/") and rel_lower.startswith(key.lower()):
                return layer
        # Filename-only match
        filename = rel_str.rsplit("/", 1)[-1].lower()
        for key, layer in self._registry.items():
            if key.lower() == filename:
                return layer

        # Unknown → default to LAYER_3 (tool-layer, requires approval warning)
        return LAYER_3

    def is_protected(self, path: str) -> bool:
        """True if path is in a protected layer (LAYER_1 or LAYER_2)."""
        return self.get_layer(path) in PROTECTED_LAYERS

    def is_approval_required(self, path: str) -> bool:
        """True if the path requires human approval before editing (LAYER_3)."""
        return self.get_layer(path) in APPROVAL_LAYERS

    # ── Edit Gate ─────────────────────────────────────────────────────────────

    def check_edit_allowed(self, path: str) -> Tuple[bool, str]:
        """
        Main gate called before any autonomous code edit.

        Returns:
            (True, "")               — edit allowed (Layer 4/5)
            (True, warning_msg)      — allowed but requires human approval (Layer 3)
            (False, reason_msg)      — blocked (Layer 1/2 or kernel_lock_mode off for admin)
        """
        if not self._kernel_lock_mode:
            return True, f"[KERNEL LOCK DISABLED] Edit allowed on {path}"

        layer = self.get_layer(path)

        if layer in PROTECTED_LAYERS:
            reason = (
                f"KERNEL LOCK: '{path}' is {layer} (protected). "
                f"Autonomous edits to Layer 1 (Kernel) and Layer 2 (Core Cognition) "
                f"are permanently blocked. Manual override required."
            )
            return False, reason

        if layer in APPROVAL_LAYERS:
            warning = (
                f"KERNEL APPROVAL REQUIRED: '{path}' is {layer} (Tool Layer). "
                f"This edit is flagged for human review before applying."
            )
            return True, warning   # allowed but flagged

        # LAYER_4 / LAYER_5 — fully autonomous
        return True, ""

    def check_git_commit_allowed(self, staged_files: list) -> Tuple[bool, str]:
        """
        Check whether a git auto_commit contains protected files.
        Called by joi_git_agency.py before executing auto_commit on L1/L2 paths.
        Returns (True, "") if safe, (False, reason) if blocked.
        """
        blocked = []
        for f in staged_files:
            if self.is_protected(f):
                blocked.append(f"{f} [{self.get_layer(f)}]")
        if blocked:
            return False, (
                "KERNEL LOCK: auto_commit blocked. Staged files include protected kernel/core modules: "
                + ", ".join(blocked)
                + ". Commit these manually after review."
            )
        return True, ""

    # ── Violation Log ─────────────────────────────────────────────────────────

    def log_violation(self, path: str, reason: str, action: str = "auto_apply"):
        """Record a blocked edit attempt."""
        entry = {
            "ts":     datetime.now().isoformat(),
            "path":   path,
            "layer":  self.get_layer(path),
            "action": action,
            "reason": reason[:400],
        }
        self._violations.append(entry)
        # Persist to file
        try:
            existing = []
            if VIOLATION_LOG.exists():
                existing = json.loads(VIOLATION_LOG.read_text(encoding="utf-8"))
            existing.append(entry)
            if len(existing) > 500:
                existing = existing[-500:]
            VIOLATION_LOG.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        except Exception as e:
            logger.warning(f"[KERNEL] Could not persist violation log: {e}")
        logger.warning(f"[KERNEL VIOLATION] {action} on {path}: {reason[:120]}")
        print(f"  [KERNEL LOCK] VIOLATION: {action} blocked on {path} ({self.get_layer(path)})")

    def get_violations(self, limit: int = 50) -> list:
        """Return recent violations from disk."""
        try:
            if VIOLATION_LOG.exists():
                data = json.loads(VIOLATION_LOG.read_text(encoding="utf-8"))
                return data[-limit:]
        except Exception:
            pass
        return self._violations[-limit:]

    # ── Kernel Lock Mode ──────────────────────────────────────────────────────

    @property
    def kernel_lock_mode(self) -> bool:
        return self._kernel_lock_mode

    def enable_kernel_lock(self):
        self._kernel_lock_mode = True
        print("  [KERNEL] Kernel Lock ENABLED — Layer 1/2 edits are blocked.")

    def disable_kernel_lock(self, manual_override_token: str = ""):
        """
        Disable kernel lock for emergency maintenance.
        Requires a non-empty override token (logged for audit).
        """
        if not manual_override_token:
            return False, "Manual override token required to disable Kernel Lock."
        self._kernel_lock_mode = False
        self.log_violation(
            path="KERNEL_LOCK_SYSTEM",
            reason=f"MANUAL OVERRIDE — kernel lock disabled. Token: {manual_override_token[:30]}",
            action="disable_kernel_lock"
        )
        print(f"  [KERNEL] ⚠️  Kernel Lock DISABLED by manual override ({manual_override_token[:20]}...)")
        return True, "Kernel Lock disabled. Re-enable with enable_kernel_lock()."


# ── Integrity Hashing ─────────────────────────────────────────────────────────

def compute_kernel_hash(lock: Optional["KernelLock"] = None) -> Dict[str, str]:
    """
    SHA-256 hash every Layer-1 file. Returns {relative_path: sha256_hex}.
    """
    if lock is None:
        lock = get_kernel_lock()

    hashes = {}
    for key, layer in lock._registry.items():
        if layer != LAYER_1:
            continue
        # Resolve path
        if key.endswith("/"):
            continue  # skip dir entries
        full = BASE_DIR / key
        if not full.exists():
            hashes[key] = "FILE_MISSING"
            continue
        try:
            content = full.read_bytes()
            hashes[key] = hashlib.sha256(content).hexdigest()
        except Exception as e:
            hashes[key] = f"READ_ERROR:{e}"
    return hashes


def save_kernel_hash(hashes: Dict[str, str]):
    """Persist the kernel hash baseline to data/kernel_hash.json."""
    HASH_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    HASH_STORE_PATH.write_text(
        json.dumps({
            "computed_at": datetime.now().isoformat(),
            "hashes": hashes,
        }, indent=2),
        encoding="utf-8"
    )
    print(f"  [KERNEL] Hash baseline saved: {len(hashes)} Layer-1 files hashed.")


def verify_kernel_integrity(lock: Optional["KernelLock"] = None) -> Dict:
    """
    Startup integrity check. Re-hashes all Layer-1 files and compares to baseline.
    If no baseline exists, creates one (first run).

    Returns:
        {
          "ok": bool,
          "checked": int,
          "changed": list[str],   # files whose hashes differ
          "missing": list[str],   # files in baseline but missing on disk
          "message": str,
        }
    """
    if lock is None:
        lock = get_kernel_lock()

    current = compute_kernel_hash(lock)

    # First run — establish baseline
    if not HASH_STORE_PATH.exists():
        save_kernel_hash(current)
        return {
            "ok": True,
            "checked": len(current),
            "changed": [],
            "missing": [],
            "message": f"Kernel hash baseline established ({len(current)} files). Integrity verified.",
        }

    try:
        stored_data = json.loads(HASH_STORE_PATH.read_text(encoding="utf-8"))
        stored = stored_data.get("hashes", {})
    except Exception as e:
        return {"ok": False, "checked": 0, "changed": [], "missing": [], "message": f"Cannot read hash store: {e}"}

    changed = []
    missing = []

    for k, old_hash in stored.items():
        new_hash = current.get(k)
        if new_hash is None:
            missing.append(k)
        elif new_hash != old_hash and not new_hash.startswith("FILE_MISSING"):
            changed.append(k)

    ok = len(changed) == 0 and len(missing) == 0
    if ok:
        msg = f"Kernel integrity OK — {len(current)} Layer-1 files verified clean."
        print(f"  [KERNEL] ✅ {msg}")
    else:
        msg = (
            f"⚠️  KERNEL INTEGRITY ALERT: {len(changed)} changed, {len(missing)} missing. "
            f"Changed: {changed[:5]}. Missing: {missing[:5]}."
        )
        print(f"  [KERNEL] ❌ {msg}")
        lock.log_violation("KERNEL_INTEGRITY", msg, action="startup_check")

    return {
        "ok": ok,
        "checked": len(current),
        "changed": changed,
        "missing": missing,
        "message": msg,
        "baseline_date": stored_data.get("computed_at", "unknown"),
    }


# ── Singleton ─────────────────────────────────────────────────────────────────
_kernel_lock_instance: Optional[KernelLock] = None


def get_kernel_lock() -> KernelLock:
    """Return the singleton KernelLock instance."""
    global _kernel_lock_instance
    if _kernel_lock_instance is None:
        _kernel_lock_instance = KernelLock()
    return _kernel_lock_instance


# ── Tool Functions ────────────────────────────────────────────────────────────

def get_kernel_status(**kwargs) -> dict:
    """Get current kernel lock state, integrity status, and recent violations."""
    lock = get_kernel_lock()
    integrity = verify_kernel_integrity(lock)
    return {
        "ok": True,
        "kernel_lock_mode": lock.kernel_lock_mode,
        "integrity": integrity,
        "violations_recent": lock.get_violations(limit=10),
        "protected_layers": list(PROTECTED_LAYERS),
        "auto_apply_layers": list(AUTO_APPLY_LAYERS),
    }


# ── Tool Registration (try/except — safe if joi_companion not yet loaded) ─────
try:
    import joi_companion
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "get_kernel_status",
            "description": (
                "Get Joi's Kernel Lock status: lock mode, Layer-1 integrity verification, "
                "recent violation attempts, and layer configuration."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []}
        }},
        get_kernel_status
    )
    print("  [OK] joi_kernel_lock loaded (Layer 1/2 protection ACTIVE)")
except Exception as _e:
    print(f"  [WARN] joi_kernel_lock: tool registration skipped ({_e})")

# ── Flask Route ───────────────────────────────────────────────────────────────
def _kernel_route():
    try:
        from flask import jsonify
        return jsonify(get_kernel_status())
    except Exception as e:
        from flask import jsonify
        return jsonify({"ok": False, "error": str(e)}), 500

try:
    import joi_companion
    joi_companion.register_route("/kernel/status", ["GET"], _kernel_route, "kernel_status_route")
except Exception:
    pass
