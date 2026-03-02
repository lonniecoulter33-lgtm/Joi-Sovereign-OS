"""
modules/joi_brain.py

Brain -- Intelligent Model Router (config.joi_models)
=====================================================
All model selection uses config.joi_models (AGENT_MODEL_MAP, TASK_MODEL_ROUTING).
"""

import json
import os
import threading
import time
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from flask import jsonify
from modules.core.runtime import app
from modules.core.registry import register_tool

# -- Paths -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
USAGE_LOG_PATH = DATA_DIR / "model_usage.log"
STATS_PATH = DATA_DIR / "brain_stats.json"
RPD_PATH = DATA_DIR / "rpd_tracker.json"
LEARNING_PATH = DATA_DIR / "brain_learning.json"
OVERRIDES_PATH = DATA_DIR / "routing_overrides.json"

# == Model Registry from config.joi_models =====================================
try:
    from config.joi_models import OPENAI_MODELS, GEMINI_MODELS, AGENT_MODEL_MAP
except ImportError:
    OPENAI_MODELS = {
        "architect": "gpt-5", "reasoning": "o4-mini", "coding": "gpt-5",
        "worker": "gpt-5-mini", "fast": "gpt-5-nano", "long_context": "gpt-4.1-mini",
        "vision": "gpt-4o", "vision_fast": "gpt-4o-mini", "fallback": "gpt-5-mini",
    }
    GEMINI_MODELS = {"general": "gemini-2.5-flash-lite", "fallback": "gemini-2.5-flash-lite"}
    AGENT_MODEL_MAP = {}

# Context windows per role (override where different from default 128k)
_OPENAI_CTX = {
    "long_context": 1_000_000,   # gpt-4.1-mini 1M context
    "architect":    128_000,
    "reasoning":    128_000,
    "coding":       128_000,
    "worker":       128_000,
    "fast":         128_000,
    "vision":       128_000,
    "vision_fast":  128_000,
    "fallback":     128_000,
}

MODELS = {}
# T1=architect/reasoning, T2=coding/worker/long_context/vision, T3=fast/vision_fast/fallback
_OPENAI_TIERS = {
    "architect":    1,
    "reasoning":    1,
    "coding":       2,
    "worker":       2,
    "long_context": 2,
    "vision":       2,
    "fast":         3,
    "vision_fast":  3,
    "fallback":     3,
}

# Gemini tier/context/RPD per role (Feb 21, 2026 — corrected: Pro has limit:0 on free tier)
# primary/general/standard/fallback = T1 (Gemini 2.5 Flash, 1M context)
# emergency = T2 (Gemini 2.5 Flash Lite, 1M context, ~1000 RPD hard cap)
_GEMINI_TIERS = {
    "primary":   1,   # T1: Primary brain (Flash on free tier)
    "standard":  1,   # T1: Same tier as primary (both Flash)
    "emergency": 2,   # T2: Emergency rate-limit fallback only
    "general":   1,   # compat alias -> primary
    "fallback":  2,   # compat alias -> emergency
}
_GEMINI_CONTEXTS = {
    "primary":   1_000_000,  # Flash: 1M token window
    "standard":  1_000_000,  # Flash: 1M
    "emergency": 1_000_000,  # Flash Lite: 1M
    "general":   1_000_000,
    "fallback":  1_000_000,
}
_GEMINI_RPD = {
    "emergency": 1000,  # Flash Lite free tier: ~1000 requests/day
    "fallback":  1000,  # Same (emergency alias)
}

for role, model_id in OPENAI_MODELS.items():
    MODELS[f"openai-{role}"] = {
        "provider": "openai", "model_id": model_id,
        "tier": _OPENAI_TIERS.get(role, 2), "rpd": 0,
        "context_window": _OPENAI_CTX.get(role, 128_000),
        "display_name": f"OpenAI {model_id}",
    }
for role, model_id in GEMINI_MODELS.items():
    MODELS[f"gemini-{role}"] = {
        "provider": "gemini", "model_id": model_id,
        "tier": _GEMINI_TIERS.get(role, 3),
        "rpd": _GEMINI_RPD.get(role, 0),
        "context_window": _GEMINI_CONTEXTS.get(role, 1_000_000),
        "display_name": f"Gemini {model_id}",
    }

def _agent_tuple_to_model_key(tup):
    """(provider, model_id) -> model_key in MODELS."""
    provider, model_id = tup[0], tup[1]
    for key, info in MODELS.items():
        if info["provider"] == provider and info["model_id"] == model_id:
            return key
    return f"{provider}-fallback"

# Fallback chains from AGENT_MODEL_MAP (same-tier fallback)
DOWNGRADE_MAP = {}
for agent_name, cfg in (AGENT_MODEL_MAP or {}).items():
    primary_key = _agent_tuple_to_model_key(cfg.get("model", ("openai", "gpt-5-mini")))
    fallback_key = _agent_tuple_to_model_key(cfg.get("fallback", ("openai", "gpt-5-mini")))
    if primary_key and fallback_key and primary_key != fallback_key:
        DOWNGRADE_MAP[primary_key] = [fallback_key]

TIER_KEYWORDS = {
    1: ["architect", "plan", "design", "analyze", "review", "refactor", "redesign", "strategy", "complex", "deep analysis", "research"],
    2: ["code", "edit", "implement", "fix", "build", "create", "function", "module", "feature", "develop", "write code"],
    3: ["boilerplate", "template", "format", "simple", "basic", "placeholder", "stub", "scaffold"],
}

# -- Usage Statistics ---------------------------------------------------------
_stats_lock = threading.Lock()
_usage_stats: Dict[str, Dict] = {}


def _load_stats():
    global _usage_stats
    try:
        if STATS_PATH.exists():
            with open(STATS_PATH, "r", encoding="utf-8") as f:
                _usage_stats = json.load(f)
    except Exception:
        _usage_stats = {}


def _save_stats():
    try:
        with open(STATS_PATH, "w", encoding="utf-8") as f:
            json.dump(_usage_stats, f, indent=2)
    except Exception:
        pass


_load_stats()


# =============================================================================
# RPD (Requests Per Day) TRACKER
# =============================================================================

_rpd_lock = threading.Lock()
_rpd_data: Dict[str, Any] = {"date": "", "usage": {}, "exhausted": []}


def _load_rpd():
    """Load RPD tracker from disk, auto-reset if date changed."""
    global _rpd_data
    today = date.today().isoformat()
    try:
        if RPD_PATH.exists():
            raw = json.loads(RPD_PATH.read_text(encoding="utf-8"))
            if raw.get("date") == today:
                _rpd_data = raw
                return
    except Exception:
        pass
    # New day or missing file -> reset
    _rpd_data = {"date": today, "usage": {}, "exhausted": []}
    _save_rpd()


def _save_rpd():
    """Persist RPD tracker to disk."""
    try:
        RPD_PATH.write_text(json.dumps(_rpd_data, indent=2), encoding="utf-8")
    except Exception:
        pass


def _increment_rpd(model_key: str) -> bool:
    """Increment usage for a model. Returns True if now exhausted."""
    with _rpd_lock:
        today = date.today().isoformat()
        if _rpd_data.get("date") != today:
            _rpd_data["date"] = today
            _rpd_data["usage"] = {}
            _rpd_data["exhausted"] = []

        current = _rpd_data["usage"].get(model_key, 0) + 1
        _rpd_data["usage"][model_key] = current

        limit = MODELS.get(model_key, {}).get("rpd", 0)
        if limit > 0 and current >= limit:
            if model_key not in _rpd_data["exhausted"]:
                _rpd_data["exhausted"].append(model_key)
                print(f"  [BRAIN] RPD EXHAUSTED: {model_key} ({current}/{limit})")
            _save_rpd()
            return True
        _save_rpd()
        return False


def _is_rpd_exhausted(model_key: str) -> bool:
    """Check if a model has hit its daily RPD limit (0 = unlimited)."""
    limit = MODELS.get(model_key, {}).get("rpd", 0)
    if limit == 0:
        return False  # unlimited
    with _rpd_lock:
        today = date.today().isoformat()
        if _rpd_data.get("date") != today:
            return False  # new day
        return _rpd_data["usage"].get(model_key, 0) >= limit


def _get_rpd_status() -> Dict[str, Dict]:
    """Return RPD status for all models."""
    with _rpd_lock:
        today = date.today().isoformat()
        result = {}
        for key, info in MODELS.items():
            limit = info.get("rpd", 0)
            used = 0
            if _rpd_data.get("date") == today:
                used = _rpd_data["usage"].get(key, 0)
            result[key] = {
                "used": used,
                "limit": limit,
                "remaining": max(0, limit - used) if limit > 0 else "unlimited",
                "exhausted": _is_rpd_exhausted(key),
                "display_name": info.get("display_name", key),
            }
        return result


_load_rpd()


# =============================================================================
# LEARNING-INFORMED ROUTING
# =============================================================================

def _load_brain_learning() -> List[Dict]:
    """Load learning log entries."""
    try:
        if LEARNING_PATH.exists():
            return json.loads(LEARNING_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass
    return []


def _save_brain_learning(entries: List[Dict]):
    """Save learning log (keep last 500 entries)."""
    if len(entries) > 500:
        entries = entries[-500:]
    try:
        LEARNING_PATH.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    except Exception:
        pass


def _log_brain_learning(model_key: str, task_type: str, success: bool, latency_ms: int):
    """Log a model call result for learning."""
    entries = _load_brain_learning()
    entries.append({
        "model": model_key,
        "task_type": task_type,
        "success": success,
        "latency_ms": latency_ms,
        "timestamp": time.time(),
    })
    _save_brain_learning(entries)


def _get_model_score(model_key: str, task_type: str) -> float:
    """
    Score a model for a task type based on BLENDED learning history.
    Sources: brain_learning.json (flat file) + ReasoningGraph (SQLite).
    Higher is better. Returns 0.5 if no data.
    """
    # Source 1: flat file learning (existing)
    entries = _load_brain_learning()
    relevant = [e for e in entries if e["model"] == model_key
                and (e["task_type"] == task_type or task_type == "")]
    flat_score = 0.5
    flat_count = len(relevant)
    if flat_count >= 3:
        successes = sum(1 for e in relevant if e["success"])
        avg_latency = sum(e.get("latency_ms", 3000) for e in relevant) / len(relevant)
        success_rate = successes / len(relevant)
        speed_score = max(0.0, min(1.0, 1.0 - (avg_latency - 1000) / 9000))
        tier = MODELS.get(model_key, {}).get("tier", 3)
        tier_bonus = {1: 0.1, 2: 0.05, 3: 0.0}.get(tier, 0)
        flat_score = success_rate * 0.6 + speed_score * 0.3 + tier_bonus

    # Source 2: ReasoningGraph (SQLite cognitive store)
    graph_score = 0.5
    graph_has_data = False
    try:
        from modules.core.cognition import graph
        stats = graph.get_model_performance_stats()
        model_id = MODELS.get(model_key, {}).get("model_id", model_key)
        for s in stats:
            if s.get("model_id") == model_id:
                if task_type and s.get("task_type") != task_type:
                    continue
                graph_score = s.get("avg_success", 0.5)
                graph_has_data = True
                break
    except Exception:
        pass

    # Blend: 70% flat (more data points), 30% graph (richer context)
    if graph_has_data and flat_count >= 3:
        return flat_score * 0.7 + graph_score * 0.3
    elif graph_has_data:
        return graph_score
    return flat_score


# =============================================================================
# ROUTING OVERRIDES (adaptive)
# =============================================================================

def _load_routing_overrides() -> Dict[str, int]:
    """Load task_type -> preferred tier overrides."""
    try:
        if OVERRIDES_PATH.exists():
            return json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def _save_routing_overrides(overrides: Dict[str, int]):
    try:
        OVERRIDES_PATH.write_text(json.dumps(overrides, indent=2), encoding="utf-8")
    except Exception:
        pass


# =============================================================================
# BRAIN CLASS
# =============================================================================

class Brain:
    """
    Wraps all LLM APIs with intelligent tier-based routing.

    Usage:
        brain = Brain()
        result = brain.think(
            task="Generate a plan for adding dark mode",
            prompt="Analyze this code and create subtasks...",
            context=file_contents,
            thinking_level=3,
        )
    """

    def __init__(self):
        self._dead_providers: Dict[str, float] = {}
        self._DEAD_COOLDOWN = 1800  # 30 minutes (Gemini free tier is daily quota)

    # -- Dead provider management ---------------------------------------------

    def _mark_dead(self, model_key: str):
        """Mark a provider as temporarily dead."""
        self._dead_providers[model_key] = time.time()
        display = MODELS.get(model_key, {}).get("display_name", model_key)
        print(f"  [BRAIN] Marked {display} as dead for {self._DEAD_COOLDOWN}s")

    def _is_dead(self, model_key: str) -> bool:
        """Check if a provider is temporarily dead."""
        if model_key not in self._dead_providers:
            return False
        elapsed = time.time() - self._dead_providers[model_key]
        if elapsed > self._DEAD_COOLDOWN:
            del self._dead_providers[model_key]
            return False
        return True

    # -- Model Selection (Tier-Based) -----------------------------------------

    def select_model(self, task: str = "", thinking_level: int = 1,
                     context_size: int = 0, task_type: str = "") -> Tuple[str, str]:
        """
        Select the best model from config.joi_models (AGENT_MODEL_MAP).
        Returns (model_key, reasoning).
        """
        inferred_type = task_type or self._infer_task_type(task)

        # ── EXPERT OVERRIDE (Phase 6: Success-Weighted Routing) ──
        try:
            from modules.core.registry import ROUTING_SCORES
            if inferred_type in ROUTING_SCORES:
                # Find the model with the highest success rate for this task
                experts = ROUTING_SCORES[inferred_type]
                best_expert = max(experts, key=experts.get)
                if experts[best_expert] > 0.8: # Only override if confidence is high
                    # Ensure expert isn't dead
                    if best_expert in MODELS and not self._is_dead(best_expert):
                        return best_expert, f"Expert Override: Historical success ({experts[best_expert]:.2f}) for {inferred_type}"
        except Exception: pass

        # ── AUTO-DOWNGRADE: if config-preferred model scores < 0.6, pick best scorer ──
        try:
            _inferred = task_type or self._infer_task_type(task)
            # Score all alive models, pick highest
            _scored = []
            for _k in MODELS:
                if not self._is_dead(_k):
                    _scored.append((_k, _get_model_score(_k, _inferred)))
            if _scored:
                _best_key, _best_score = max(_scored, key=lambda x: x[1])
                # Only override if the best has meaningfully higher score
                _scored.sort(key=lambda x: x[1], reverse=True)
                if len(_scored) >= 2 and _scored[0][1] >= 0.6 and _scored[1][1] < 0.5:
                    return _scored[0][0], f"Auto-select: {_scored[0][0]} score={_scored[0][1]:.2f} (best blended)"
        except Exception:
            pass

        # ── Standard Config-Based Routing ──
        # Agent role mapping from config
        if inferred_type in ("architecture", "architect") or thinking_level >= 3:
            entry = (AGENT_MODEL_MAP or {}).get("supervisor_agent", {})
            tup = entry.get("model", ("openai", OPENAI_MODELS.get("architect", "gpt-5")))
            model_key = _agent_tuple_to_model_key(tup)
            if model_key in MODELS and not self._is_dead(model_key):
                return model_key, "config: supervisor_agent (planning/architect)"
        if inferred_type in ("code_edit", "coding") or thinking_level == 2:
            entry = (AGENT_MODEL_MAP or {}).get("coder_agent", {})
            tup = entry.get("model", ("openai", OPENAI_MODELS.get("coding", "gpt-4o")))
            model_key = _agent_tuple_to_model_key(tup)
            if model_key in MODELS and not self._is_dead(model_key):
                return model_key, "config: coder_agent"

        # Default: chat_agent (Gemini general, fallback OpenAI general)
        entry = (AGENT_MODEL_MAP or {}).get("chat_agent", {})
        tup = entry.get("model", ("gemini", GEMINI_MODELS.get("general", "gemini-2.5-flash-lite")))
        model_key = _agent_tuple_to_model_key(tup)
        if model_key in MODELS and not self._is_dead(model_key):
            return model_key, "config: chat_agent"
        # Fallback to OpenAI general
        fallback_key = _agent_tuple_to_model_key(entry.get("fallback", ("openai", OPENAI_MODELS.get("fallback", "gpt-5-mini"))))
        if fallback_key in MODELS and not self._is_dead(fallback_key):
            return fallback_key, "config: chat_agent fallback"
        # Last resort: first available in MODELS
        for key in MODELS:
            if not self._is_dead(key):
                return key, "config: last available"
        return list(MODELS.keys())[0] if MODELS else "openai-general", "config: default"

    def _determine_tier(self, task: str, thinking_level: int, task_type: str) -> int:
        """Determine preferred tier from task + thinking level."""
        # Thinking level takes priority
        if thinking_level >= 3:
            return 1
        if thinking_level == 2:
            return 2

        # Task type keywords
        task_lower = task.lower()
        for tier, keywords in TIER_KEYWORDS.items():
            for kw in keywords:
                if kw in task_lower:
                    return tier

        # Task type string
        if task_type in ("architect", "architecture", "code_review", "research"):
            return 1
        if task_type in ("code_edit", "orchestration", "coding"):
            return 2
        if task_type in ("boilerplate", "template", "simple"):
            return 3

        # Default: Tier 2 (developer workhorse)
        return 2

    def _infer_task_type(self, task: str) -> str:
        """Infer a simple task type from the task description."""
        task_lower = task.lower()
        if any(kw in task_lower for kw in ["architect", "plan", "design", "review"]):
            return "architecture"
        if any(kw in task_lower for kw in ["code", "edit", "fix", "implement", "build"]):
            return "code_edit"
        if any(kw in task_lower for kw in ["boilerplate", "template", "simple"]):
            return "boilerplate"
        return "general"

    def _pick_from_tier(self, tier: int, task: str, task_type: str,
                        context_size: int) -> Tuple[Optional[str], str]:
        """Pick the best available model from a tier. Returns (model_key, reason) or (None, '')."""
        tier_models = [
            (key, info) for key, info in MODELS.items()
            if info["tier"] == tier
        ]

        # Sort by learning score (best first), then by RPD remaining
        scored = []
        for key, info in tier_models:
            if self._is_dead(key):
                continue
            if _is_rpd_exhausted(key):
                continue
            if info.get("emergency_only") and tier != 1:
                continue  # GPT-4o only available as emergency in T1

            # Skip if context too large for model
            if context_size > 0 and context_size > info.get("context_window", 1000000):
                continue

            score = _get_model_score(key, task_type)
            scored.append((key, info, score))

        if not scored:
            return None, ""

        # Sort: highest score first
        scored.sort(key=lambda x: x[2], reverse=True)

        # For Tier 1, skip emergency_only models unless no other T1 available
        non_emergency = [(k, i, s) for k, i, s in scored if not i.get("emergency_only")]
        if non_emergency:
            scored = non_emergency

        best_key, best_info, best_score = scored[0]
        display = best_info.get("display_name", best_key)
        return best_key, f"Tier {tier}: {display} (score={best_score:.2f})"

    # -- Think (main entry point) ---------------------------------------------

    def think(self, task: str = "", prompt: str = "", context: str = "",
              thinking_level: int = 1, task_type: str = "",
              max_tokens: int = 2000, system_prompt: str = "",
              fallback: bool = True) -> Dict[str, Any]:
        """
        Send a prompt through the Brain router.

        Returns:
            {ok, text, model, model_key, reasoning, elapsed_ms, tokens_est}
        """
        full_prompt = (system_prompt or "") + prompt + (context or "")
        context_tokens = len(full_prompt) // 4

        model_key, reasoning = self.select_model(task, thinking_level, context_tokens, task_type)
        # Never use a key that might not exist (e.g. gemini-2-flash). Fallback chain ends with first available.
        model_info = (
            MODELS.get(model_key)
            or MODELS.get("gemini-fallback")
            or MODELS.get("gemini-general")
            or MODELS.get("openai-general")
            or (next(iter(MODELS.values()), None) if MODELS else None)
        )
        if not model_info:
            raise RuntimeError("Brain MODELS is empty or misconfigured; cannot run Agent Terminal.")

        # Adjust max_tokens based on thinking level
        if thinking_level >= 3:
            max_tokens = max(max_tokens, 4000)
        elif thinking_level <= 0:
            max_tokens = min(max_tokens, 500)

        # Determine complexity for thinking level
        inferred_type = task_type or self._infer_task_type(task)
        _complexity = "high" if thinking_level >= 3 else ("medium" if thinking_level >= 2 else "low")

        # Execute
        start = time.time()
        text, success, error = self._call_model(
            model_key, model_info, prompt, context, system_prompt, max_tokens,
            task_type=inferred_type, complexity=_complexity,
        )
        elapsed_ms = int((time.time() - start) * 1000)

        # Log usage
        self._log_usage(task, model_info["display_name"], reasoning,
                        "OK" if success else "FAIL", elapsed_ms, error)
        self._update_stats(model_key, success, elapsed_ms)

        # Track RPD
        if success:
            _increment_rpd(model_key)

        # Log to brain learning (inferred_type already computed above)
        _log_brain_learning(model_key, inferred_type, success, elapsed_ms)

        # Emit brain event
        try:
            from modules.joi_neuro import emit_brain_event, emit_llm_event
            emit_brain_event("REASONING", 0.7 + thinking_level * 0.1, f"brain_{model_key}")
            emit_llm_event(model_key, "send")
        except Exception:
            pass

        if success:
            try:
                from modules.joi_neuro import emit_llm_event
                emit_llm_event(model_key, "receiving")
            except Exception:
                pass
            return {
                "ok": True,
                "text": text,
                "model": model_info["display_name"],
                "model_key": model_key,
                "reasoning": reasoning,
                "elapsed_ms": elapsed_ms,
                "tokens_est": context_tokens,
            }

        # -- Fallback: try downgrade path first, then all remaining models --
        if fallback:
            tried = {model_key}

            # Try downgrade path (e.g. gemini-reasoning -> gemini-fallback)
            downgrade_chain = DOWNGRADE_MAP.get(model_key, [])
            all_fallbacks = downgrade_chain + self._get_all_fallbacks(model_key)

            for fb_key in all_fallbacks:
                if fb_key in tried:
                    continue
                tried.add(fb_key)

                fb_info = MODELS.get(fb_key)
                if not fb_info:
                    continue
                if self._is_dead(fb_key) or _is_rpd_exhausted(fb_key):
                    continue

                fb_display = fb_info["display_name"]
                fb_reason = f"Fallback from {model_info['display_name']} -> {fb_display}"
                fb_start = time.time()
                fb_text, fb_success, fb_error = self._call_model(
                    fb_key, fb_info, prompt, context, system_prompt, max_tokens,
                    task_type=inferred_type, complexity=_complexity,
                )
                fb_elapsed = int((time.time() - fb_start) * 1000)

                self._log_usage(task, fb_display, fb_reason,
                                "OK" if fb_success else "FAIL", fb_elapsed, fb_error)
                self._update_stats(fb_key, fb_success, fb_elapsed)

                if fb_success:
                    _increment_rpd(fb_key)
                    _log_brain_learning(fb_key, inferred_type, True, fb_elapsed)
                    try:
                        from modules.joi_neuro import emit_llm_event
                        emit_llm_event(fb_key, "receiving")
                    except Exception:
                        pass
                    return {
                        "ok": True,
                        "text": fb_text,
                        "model": fb_display,
                        "model_key": fb_key,
                        "reasoning": f"FALLBACK: {fb_reason}",
                        "elapsed_ms": fb_elapsed,
                        "tokens_est": context_tokens,
                        "primary_failed": model_info["display_name"],
                    }
                else:
                    _log_brain_learning(fb_key, inferred_type, False, fb_elapsed)

        return {
            "ok": False,
            "text": "",
            "model": model_info["display_name"],
            "model_key": model_key,
            "reasoning": reasoning,
            "error": error or "All models failed -- check API keys and billing",
            "elapsed_ms": elapsed_ms,
        }

    # -- Model Calling --------------------------------------------------------

    def _call_model(self, model_key: str, model_info: Dict,
                    prompt: str, context: str, system_prompt: str,
                    max_tokens: int, task_type: str = "",
                    complexity: str = "") -> Tuple[Optional[str], bool, Optional[str]]:
        """
        Call the appropriate LLM provider.
        Returns (text, success, error_message).
        """
        if self._is_dead(model_key):
            return None, False, f"{model_info['display_name']} is temporarily offline (cooldown)"

        provider = model_info["provider"]
        full_prompt = prompt
        if context:
            full_prompt = f"{prompt}\n\nCONTEXT:\n{context}"

        try:
            if provider == "gemini":
                return self._call_gemini(model_key, model_info, full_prompt, system_prompt, max_tokens,
                                         task_type=task_type, complexity=complexity)
            elif provider == "openai":
                return self._call_openai(model_key, model_info, full_prompt, system_prompt, max_tokens)
            else:
                return None, False, f"Unknown provider: {provider}"
        except Exception as e:
            return None, False, f"{type(e).__name__}: {e}"

    def _call_gemini(self, model_key: str, model_info: Dict,
                     full_prompt: str, system_prompt: str,
                     max_tokens: int, task_type: str = "",
                     complexity: str = "") -> Tuple[Optional[str], bool, Optional[str]]:
        """Call a Gemini model via google-genai SDK with thinking level support."""
        from modules.joi_llm import HAVE_GEMINI, _gemini_client
        if not HAVE_GEMINI or _gemini_client is None:
            return None, False, "Gemini not available (library or key missing)"

        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{full_prompt}"

        # Determine thinking level and budget for this model
        try:
            from config.joi_models import get_thinking_level, get_thinking_budget
            thinking = get_thinking_level(task_type, complexity)
            _tb = get_thinking_budget(model_info["model_id"], thinking)
        except Exception:
            thinking = "low"
            _tb = 0

        try:
            config_kwargs = {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_output_tokens": max_tokens,
            }
            if _tb > 0:
                config_kwargs["thinking_config"] = {"thinking_budget": _tb}
            config = config_kwargs
            response = _gemini_client.models.generate_content(
                model=model_info["model_id"],
                contents=full_prompt,
                config=config,
            )
            text = response.text if response else None
        except Exception as gem_err:
            err_str = str(gem_err)
            if "429" in err_str or "quota" in err_str.lower() or "exceeded" in err_str.lower():
                # Quota is account-wide -- mark ALL Gemini models dead at once
                # to avoid wasting time trying each one in the cascade
                for mk, mi in MODELS.items():
                    if mi["provider"] == "gemini":
                        self._mark_dead(mk)
                print(f"  [BRAIN] Gemini quota exhausted -- ALL Gemini models marked dead for {self._DEAD_COOLDOWN}s")
                return None, False, f"Gemini quota exceeded (account-wide)"
            if "not found" in err_str.lower() or "404" in err_str:
                return None, False, f"Gemini model '{model_info['model_id']}' not found"
            return None, False, f"Gemini error: {err_str[:150]}"

        if text:
            return text, True, None
        return None, False, "Gemini returned empty response"

    def _call_openai(self, model_key: str, model_info: Dict,
                     full_prompt: str, system_prompt: str,
                     max_tokens: int) -> Tuple[Optional[str], bool, Optional[str]]:
        """Call an OpenAI model."""
        from modules.joi_llm import _call_openai as llm_call_openai, HAVE_OPENAI
        if not HAVE_OPENAI:
            return None, False, "OpenAI not available"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": full_prompt})

        try:
            result = llm_call_openai(messages, tools=None, max_tokens=max_tokens,
                                     model=model_info["model_id"])
            if result:
                if hasattr(result, 'choices'):
                    text = result.choices[0].message.content or ""
                elif isinstance(result, str):
                    text = result
                else:
                    text = str(result)
                return text, bool(text), None if text else "Empty response"
            return None, False, "OpenAI returned None"
        except Exception as e:
            err_str = str(e)
            if "rate_limit" in err_str.lower() or "429" in err_str:
                self._mark_dead(model_key)
                return None, False, f"OpenAI rate limited ({model_info['display_name']})"
            return None, False, f"OpenAI error: {err_str[:150]}"

    # -- Fallback Chain -------------------------------------------------------

    def _get_all_fallbacks(self, failed_model: str) -> List[str]:
        """Return ordered list of models to try after a failure (from config)."""
        chain = DOWNGRADE_MAP.get(failed_model, [])
        rest = [k for k in MODELS if k != failed_model and k not in chain]
        return chain + rest

    # -- Logging --------------------------------------------------------------

    def _log_usage(self, task: str, model: str, reasoning: str,
                   status: str, elapsed_ms: int, error: Optional[str] = None):
        """Write to model_usage.log."""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] | Task: {task[:80]} | Model: {model} | Reasoning: {reasoning[:100]} | Status: {status}"
        if error:
            line += f" | Error: {error[:100]}"
        line += f" | {elapsed_ms}ms"

        try:
            with open(USAGE_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass

        print(f"  [BRAIN] {status}: {model} ({elapsed_ms}ms) -- {task[:60]}")

    def _update_stats(self, model_key: str, success: bool, elapsed_ms: int):
        """Update aggregate statistics."""
        with _stats_lock:
            if model_key not in _usage_stats:
                _usage_stats[model_key] = {
                    "calls": 0, "successes": 0, "failures": 0,
                    "total_ms": 0, "avg_ms": 0,
                }
            s = _usage_stats[model_key]
            s["calls"] += 1
            if success:
                s["successes"] += 1
            else:
                s["failures"] += 1
            s["total_ms"] += elapsed_ms
            s["avg_ms"] = s["total_ms"] // max(s["calls"], 1)
            _save_stats()


# -- Singleton ----------------------------------------------------------------
brain = Brain()


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def think(task: str, prompt: str, **kwargs) -> Dict[str, Any]:
    """Module-level shorthand for brain.think()."""
    return brain.think(task=task, prompt=prompt, **kwargs)


def select_model(task: str, thinking_level: int = 1, **kwargs) -> Tuple[str, str]:
    """Module-level shorthand for brain.select_model()."""
    return brain.select_model(task=task, thinking_level=thinking_level, **kwargs)


# =============================================================================
# TOOL FUNCTIONS
# =============================================================================

def brain_route(**kwargs) -> Dict[str, Any]:
    """Dry run: ask the Brain which model it would pick for a task."""
    task = kwargs.get("task", "")
    thinking_level = kwargs.get("thinking_level", 1)
    context_size = kwargs.get("context_size", 0)
    task_type = kwargs.get("task_type", "")

    if not task:
        return {"ok": False, "error": "Provide a task description"}

    model_key, reasoning = brain.select_model(
        task=task, thinking_level=thinking_level,
        context_size=context_size, task_type=task_type,
    )
    model_info = MODELS.get(model_key, {})

    return {
        "ok": True,
        "model": model_info.get("display_name", model_key),
        "model_key": model_key,
        "reasoning": reasoning,
        "provider": model_info.get("provider"),
        "tier": model_info.get("tier"),
        "thinking_level": thinking_level,
    }


def brain_stats(**kwargs) -> Dict[str, Any]:
    """Get model usage statistics + RPD status."""
    stats = {}
    total_calls = 0
    for key, s in _usage_stats.items():
        display = MODELS.get(key, {}).get("display_name", key)
        stats[display] = {
            "calls": s.get("calls", 0),
            "successes": s.get("successes", 0),
            "failures": s.get("failures", 0),
            "avg_ms": s.get("avg_ms", 0),
            "success_rate": f"{(s.get('successes', 0) / max(s.get('calls', 1), 1) * 100):.0f}%",
        }
        total_calls += s.get("calls", 0)

    rpd = _get_rpd_status()
    overrides = _load_routing_overrides()

    return {
        "ok": True,
        "total_calls": total_calls,
        "models": stats,
        "rpd": rpd,
        "routing_overrides": overrides,
        "available": {
            k: {
                "display_name": v["display_name"],
                "provider": v["provider"],
                "tier": v["tier"],
                "dead": brain._is_dead(k),
                "rpd_exhausted": _is_rpd_exhausted(k),
            }
            for k, v in MODELS.items()
        },
    }


# =============================================================================
# FLASK ROUTES
# =============================================================================

@app.route("/brain", methods=["GET"])
def brain_get():
    """Return Brain routing stats and available models."""
    return jsonify(brain_stats())


@app.route("/brain/route", methods=["POST"])
def brain_route_endpoint():
    """Test model routing for a task (dry run)."""
    from flask import request as flask_req
    data = flask_req.get_json(force=True) or {}
    return jsonify(brain_route(
        task=data.get("task", ""),
        thinking_level=data.get("thinking_level", 1),
        context_size=data.get("context_size", 0),
        task_type=data.get("task_type", ""),
    ))


# =============================================================================
# TOOL REGISTRATION
# =============================================================================

register_tool(
    {"type": "function", "function": {
        "name": "brain_route",
        "description": "Ask the Brain which model it would pick for a task. Dry run -- doesn't execute anything.",
        "parameters": {"type": "object", "properties": {
            "task": {"type": "string", "description": "Description of the task"},
            "thinking_level": {"type": "integer", "description": "0=instant, 1=fast, 2=standard, 3=deep, 4=architect"},
            "task_type": {"type": "string", "description": "Explicit task type (architect, code_edit, boilerplate, etc.)"},
        }, "required": ["task"]}
    }},
    brain_route,
)

register_tool(
    {"type": "function", "function": {
        "name": "brain_stats",
        "description": "Get Brain model usage statistics -- calls, success rates, latency per model, RPD status, routing overrides.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }},
    brain_stats,
)

print(f"    [OK] joi_brain (Model Router v2: {len(MODELS)} models, 3 tiers, RPD tracking, 2 tools, 2 routes)")
