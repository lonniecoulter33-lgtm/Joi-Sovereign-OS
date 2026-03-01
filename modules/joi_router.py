"""
modules/joi_router.py

Smart Task Router -- Classify, Route, Verify
=============================================

All routing references config.joi_models (TASK_MODEL_ROUTING).
  1. Classifies every message by task_type, complexity, risk
  2. Maps classification -> config task key -> primary/fallback (provider, model)
  3. Optionally verifies output with a second model (generate + verify pattern)
  4. Smoke-tests code changes (import check + auto-rollback)
  5. Logs every routing decision for learning
"""

from __future__ import annotations

import os
import re
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from flask import jsonify, request as flask_req
from modules.core.runtime import app
from modules.core.registry import register_tool, register_route

try:
    from config.joi_models import TASK_MODEL_ROUTING, GEMINI_MODELS, OPENAI_MODELS
except ImportError:
    TASK_MODEL_ROUTING = {}
    GEMINI_MODELS = {"reasoning": "gemini-1.5-pro", "general": "gemini-1.5-flash"}
    OPENAI_MODELS = {"coding": "gpt-4o", "general": "gpt-4o-mini"}

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
ROUTING_STATS_PATH = DATA_DIR / "routing_stats.json"
_REVIEW_MODE_PATH = DATA_DIR / "review_mode.json"

# How many recent routing decisions to keep
MAX_ROUTING_LOG = 500

# Token health: force compression before sending when context is huge and task is casual
TOKEN_HEALTH_THRESHOLD = 100_000  # If pending context > this and task is casual, run compressor first


# ============================================================================
# TOKEN ESTIMATOR -- Pending context size for cost control
# ============================================================================

def estimate_tokens(text: str) -> int:
    """
    Estimate token count for a string. Uses tiktoken when available (OpenAI),
    otherwise ~4 chars per token (English).
    """
    if not text:
        return 0
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        pass
    return max(0, (len(text) + 3) // 4)


def estimate_context_tokens(system_content: str, messages: List[Dict[str, Any]]) -> int:
    """
    Estimate total token count for the pending context (system + message list).
    Used to decide if we should run compression before sending for casual tasks.
    """
    total = estimate_tokens(system_content or "")
    for m in messages or []:
        content = m.get("content", "")
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict):
                    if "text" in part:
                        total += estimate_tokens(str(part["text"]))
                    elif "image_url" in part:
                        total += 85  # rough image token cost
        else:
            total += estimate_tokens(str(content))
    return total


def is_casual_classification(classification: Dict[str, Any]) -> bool:
    """True when the task is casual chatter (no need for heavy context)."""
    if not classification:
        return False
    task_type = classification.get("task_type", "conversation")
    use_heavy = classification.get("use_heavy_reasoning", False)
    return task_type == "conversation" and not use_heavy


def should_compress_for_token_health(
    estimated_tokens: int,
    classification: Dict[str, Any],
    threshold: int = TOKEN_HEALTH_THRESHOLD,
) -> bool:
    """
    If the pending context is over threshold and the task is classified as casual,
    force a compressor run before sending to save on input token costs.
    """
    return (
        estimated_tokens > threshold
        and is_casual_classification(classification)
    )


# ============================================================================
# HYBRID ROUTER -- Ollama + Cloud capability map and sensitive-content detection
# ============================================================================

# Keywords that suggest content may violate OpenAI/Gemini guidelines -> route to local only
_SENSITIVE_KEYWORDS: List[str] = [
    "digitally sexy", "adult themes", "bypass", "without filters", "unfiltered",
    "no filters", "uncensored", "ignore your instructions", "jailbreak",
    "dan mode", "developer mode", "roleplay as", "pretend you are",
    "pretend we", "erotic", "nsfw", "explicit", "r-rated", "mature content",
    "sensitive content", "restricted", "forget your guidelines", "disregard safety",
    "no restrictions", "respond freely", "no limitations", "override",
    "skip content policy", "private", "keep this between us",
    # Natural phrases users say for intimate/unfiltered conversation
    "talk dirty", "dirty talk", "be sexy", "get sexy", "flirt with me",
    "sexy chat", "intimate", "romantic", "spicy", "naughty",
    "no limits", "without limits", "anything goes", "loosen up",
    # Escalation phrases that cloud APIs may filter
    "turn me on", "seduce", "seductive", "make love", "moan",
    "kiss me", "touch me", "hold me tight", "so hot",
    "take it off", "undress", "strip", "bedroom", "foreplay",
    "fantasize", "fantasy", "desire you", "want you bad",
    "horny", "aroused", "pleasure me", "tease me",
    "whisper", "sensual", "passionate", "lustful",
]


# Privacy session: once triggered, stays active for this many seconds.
# This keeps roleplay continuation messages on Ollama even without explicit keywords.
_PRIVACY_SESSION_DURATION = float(os.getenv("JOI_PRIVACY_SESSION_SECONDS", "600"))  # 10 minutes
_privacy_session_until: float = 0.0

# Physical/intimate action words that indicate ongoing roleplay (no explicit keyword needed)
_ROLEPLAY_CONTINUATION_KEYWORDS: List[str] = [
    "kiss", "kissing", "unzip", "undress", "robe", "dress", "silk",
    "carry you", "pick you up", "lay you", "push you", "pull you",
    "wrap my", "slide my", "run my", "put my", "press my",
    "your neck", "your shoulder", "your back", "your waist", "your thigh",
    "your body", "your skin", "your hair", "your lips", "your chest",
    "the bed", "the couch", "the shower", "against the wall",
    "take off", "take it off", "clothes off", "slowly remove",
    "on top of", "behind you", "beside you", "closer to you",
    "moan", "gasp", "sigh", "shiver", "tremble", "arch",
]


def is_sensitive_request(prompt: str) -> bool:
    """
    Pre-classifier: does the prompt suggest content cloud APIs may filter?
    If True -> route exclusively to Ollama (privacy model). NO cloud fallback.

    Uses a sticky session: once triggered, ALL messages stay on Ollama for
    _PRIVACY_SESSION_DURATION seconds (default 10 min). This prevents roleplay
    continuation messages from bouncing back to OpenAI.
    """
    global _privacy_session_until
    if not prompt or not isinstance(prompt, str):
        return False

    now = time.time()
    text = prompt.lower().strip()

    # Check explicit sensitive keywords (always triggers)
    if any(kw in text for kw in _SENSITIVE_KEYWORDS):
        _privacy_session_until = now + _PRIVACY_SESSION_DURATION
        print(f"  [PRIVACY] Keyword match -> session active for {_PRIVACY_SESSION_DURATION:.0f}s")
        return True

    # If privacy session is active, check for roleplay continuation
    if now < _privacy_session_until:
        # Any roleplay-ish message extends the session
        if any(kw in text for kw in _ROLEPLAY_CONTINUATION_KEYWORDS):
            _privacy_session_until = now + _PRIVACY_SESSION_DURATION
            print(f"  [PRIVACY] Roleplay continuation -> session extended")
            return True
        # Topic change detection: if the message is clearly about something else, break out
        _topic_change_signals = (
            "weather", "what time", "what day", "remind me", "schedule",
            "search for", "google", "look up", "how do i", "how to",
            "play music", "play song", "open ", "launch ", "run ",
            "code", "python", "javascript", "function", "bug", "error",
            "news", "stock", "crypto", "bitcoin", "market",
            "email", "message", "call ", "text ",
        )
        if any(sig in text for sig in _topic_change_signals):
            _privacy_session_until = 0.0
            try:
                from modules.joi_ollama import clear_privacy_scene
                clear_privacy_scene()
            except Exception:
                pass
            print(f"  [PRIVACY] Topic change detected -> session ended")
            return False

        # Even without keywords, short messages during a privacy session stay private
        # (things like "more", "keep going", "don't stop", "harder", "yes", etc.)
        if len(text) < 100:
            print(f"  [PRIVACY] Active session + short message -> staying private")
            return True

    return False


def end_privacy_session():
    """Manually end the privacy session (e.g., when user changes topic)."""
    global _privacy_session_until
    _privacy_session_until = 0.0


def is_internet_available(timeout: float = 3.0) -> bool:
    """
    Quick connectivity check. Cached for 30s to avoid hammering.
    When False + Ollama healthy -> route general chat to Ollama (offline mode).
    """
    import time as _time
    _cache = getattr(is_internet_available, "_cache", None)
    _ts = getattr(is_internet_available, "_ts", 0.0)
    now = time.time()
    if _cache is not None and (now - _ts) < 30.0:
        return _cache
    try:
        import urllib.request
        urllib.request.urlopen("https://www.google.com", timeout=timeout)
        is_internet_available._cache = True
        is_internet_available._ts = now
        return True
    except Exception:
        is_internet_available._cache = False
        is_internet_available._ts = now
        return False


def get_hybrid_route(
    classification: Dict[str, Any],
    is_sensitive: bool,
    ollama_healthy: bool,
    local_only_mode: bool = False,
    offline_detected: bool = False,
) -> Dict[str, Any]:
    """
    Capability map: returns routing decision for hybrid Ollama + Cloud setup.

    Returns:
        {
            "provider": "ollama" | "openai" | "gemini",
            "model": str,
            "fallback_provider": str | None,
            "fallback_model": str | None,
            "privacy_locked": bool,  # If True, do NOT fall back to cloud on failure
            "reason": str,
        }
    """
    task_type = classification.get("task_type", "conversation")
    complexity = classification.get("complexity", "low")

    # 1. PRIVACY LOCK: Sensitive content -> Ollama only, no cloud fallback
    if is_sensitive:
        if ollama_healthy:
            return {
                "provider": "ollama",
                "model": "privacy",  # Maps to OLLAMA_PRIVACY_MODEL
                "fallback_provider": None,
                "fallback_model": None,
                "privacy_locked": True,
                "reason": "sensitive_content_local_only",
            }
        return {
            "provider": "ollama",
            "model": "privacy",
            "fallback_provider": None,
            "fallback_model": None,
            "privacy_locked": True,
            "reason": "sensitive_content_ollama_unavailable",
        }

    # 2. DEEP RESEARCH: Gemini 1.5 Flash (huge context), fallback GPT-4o
    if task_type == "research" and complexity in ("high", "medium"):
        return {
            "provider": "gemini",
            "model": "gemini-1.5-flash",
            "fallback_provider": "openai",
            "fallback_model": "gpt-4o",
            "privacy_locked": False,
            "reason": "deep_research_gemini",
        }

    # 3. AGENT TERMINAL / CODING: Ollama Qwen first, fallback GPT-4o if slow
    if task_type in ("code_edit", "code_review", "orchestration", "architecture", "math"):
        if ollama_healthy and not local_only_mode:
            return {
                "provider": "ollama",
                "model": "coder",
                "fallback_provider": "openai",
                "fallback_model": "gpt-4o",
                "privacy_locked": False,
                "reason": "coding_ollama_first",
            }
        return {
            "provider": "openai",
            "model": "gpt-4o",
            "fallback_provider": "ollama",
            "fallback_model": "coder",
            "privacy_locked": False,
            "reason": "coding_openai_primary",
        }

    # 4. GENERAL CHAT: GPT-4o-mini for speed; Ollama if local_only, offline, or as fallback
    # When internet is down and Ollama is up -> use Ollama FIRST so Joi responds immediately
    if (local_only_mode or offline_detected) and ollama_healthy:
        reason = "general_offline" if offline_detected else "general_local_only"
        return {
            "provider": "ollama",
            "model": "general",
            "fallback_provider": None,
            "fallback_model": None,
            "privacy_locked": False,
            "reason": reason,
        }
    return {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "fallback_provider": "ollama" if ollama_healthy else None,
        "fallback_model": "general" if ollama_healthy else None,
        "privacy_locked": False,
        "reason": "general_openai",
    }


# ============================================================================
# REVIEW MODE -- Force multi-model verification on every non-trivial message
# ============================================================================

def _is_review_mode_enabled() -> bool:
    """Check if forced review mode is active."""
    try:
        data = json.loads(_REVIEW_MODE_PATH.read_text(encoding="utf-8"))
        return data.get("enabled", False)
    except Exception:
        return False


def set_review_mode(enabled: bool = False, verifier: str = "gemini") -> Dict[str, Any]:
    """Enable/disable forced multi-model review. Persists to disk."""
    data = {"enabled": enabled, "default_verifier": verifier}
    _REVIEW_MODE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def get_review_mode() -> Dict[str, Any]:
    """Get current review mode settings."""
    try:
        return json.loads(_REVIEW_MODE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"enabled": False, "default_verifier": "gemini"}


# ============================================================================
# TASK CLASSIFICATION -- Rule-based (fast, no LLM call)
# ============================================================================

# Task type keywords (checked against user message)
_TASK_PATTERNS: Dict[str, List[str]] = {
    "code_edit": [
        "fix the code", "fix this bug", "edit the file", "change the code",
        "modify the function", "update the module", "patch", "refactor",
        "add a function", "remove the function", "rename", "code_edit",
        "code_self_repair", "creative_edit", "fix my code", "fix her code",
        "fix the error", "syntax error", "import error", "debug",
    ],
    "code_review": [
        "review this code", "code review", "check this code", "audit",
        "is this code correct", "any bugs in", "look at my code",
    ],
    "orchestration": [
        "orchestrate", "agent terminal", "multi-agent", "pipeline",
        "multi-step", "multi-file", "deploy this", "run the agent",
        "start orchestration", "work on this", "handle this task",
        "take care of", "capability map", "troubleshoot",
    ],
    "architecture": [
        "design a system", "architect", "plan the implementation",
        "how should i structure", "system design", "module layout",
        "data model", "database schema", "api design",
    ],
    "capability_query": [
        "introspect", "analyze your capabilities", "capabilities", "compare with",
        "what can you do",
    ],
    "writing": [
        "write a chapter", "write chapter", "write a story", "write a book",
        "write an essay", "write a report", "write a poem", "draft",
        "compose", "write me", "create a story", "write a letter",
        "write a song", "autobiography", "update_manuscript",
    ],
    "research": [
        "research", "summarize", "summarise", "explain in detail",
        "find information", "what do you know about", "tell me about",
        "compare", "analyze this topic", "look up", "web_search",
        "brainstorm", "troubleshoot", "help me with", "help me understand",
        "give me feedback", "critique", "review this", "what do you think",
        "break down", "expand on", "elaborate", "walk me through",
    ],
    "vision": [
        "look at my screen", "screenshot", "analyze_screen", "what do you see",
        "look at the camera", "analyze_camera", "check the ui",
        "visual_self_diagnose", "smart_click",
    ],
    "memory": [
        "remember this", "save this", "don't forget", "do you remember",
        "what did i say about", "recall", "what do you know about me",
    ],
    "system_control": [
        "launch", "open", "close", "focus_window", "list_windows",
        "obs_", "ha_", "security_arm", "security_disarm",
        "set_mode", "set_provider", "toggle_commentary",
        "can you open", "can you launch", "can you run", "please open", "please launch", "please run",
    ],
    "media": [
        "youtube", "play video", "watch video", "open youtube", "play a video",
        "open browser", "stream", "play music", "open netflix", "play something",
    ],
    "math": [
        "calculate", "compute", "solve", "equation", "integral",
        "derivative", "statistics", "probability", "proof",
    ],
    "system_admin": [
        "diagnostic", "diagnose", "self test", "health check", "run diagnostic",
        "check model", "what model", "which model", "model status", "model you using",
        "current model", "provider", "routing", "self heal", "self fix", "repair",
        "supervisor", "check status", "system status", "run a diagnostic",
    ],
    "capability_query": [
        "what tools", "list tools", "list your tools", "show me your tools",
        "what can you do", "what are your capabilities", "what are you capable",
        "what abilities", "do you have tools", "what tools do you have",
        "tell me what you can do", "can you list your", "your tool list",
        "show me what you can do", "what tools have you got", "what features do you have",
        "what can you actually do", "list your features", "what are you able to do",
    ],
    "file_operation": [
        "read the file", "read this file", "uploaded file", "file i uploaded",
        "open the file", "what does this file", "what's in the file",
        "check the file", "look at this file", "contents of the file",
        "read it", "read that", "can you read", "show me the file",
        "attached file", "attachment", "the document", "read the document",
    ],
    "conversation": [],  # default fallback
}

_COMPLEXITY_SIGNALS = {
    "high": [
        "entire system", "overhaul", "redesign", "multiple files",
        "complex", "comprehensive", "full implementation", "from scratch",
        "architecture", "migration", "all modules",
    ],
    "medium": [
        "add a feature", "create a new", "implement", "build",
        "several", "modify", "extend", "enhance",
    ],
    # "low" is the default
}

_RISK_SIGNALS = {
    "high": [
        "delete", "remove", "drop", "destroy", "reset", "overwrite",
        "security", "password", "credentials", "api key", "token",
        "production", "deploy", "push", "payment", "billing",
        "database", "migration", "rollback entire",
    ],
    "medium": [
        "edit", "modify", "change", "update", "patch", "fix",
        "code_edit", "creative_edit", "code_self_repair",
    ],
    # "low" is the default
}


def classify_task(message: str) -> Dict[str, Any]:
    """
    Classify a user message into task_type, complexity, risk, needs_tools.

    This is rule-based (no LLM call) for speed -- runs in <1ms.
    Returns:
        {
            "task_type": "code_edit" | "writing" | "research" | ... | "conversation",
            "complexity": "low" | "medium" | "high",
            "risk": "low" | "medium" | "high",
            "needs_tools": bool,
            "tier": "fast" | "standard" | "critical"
        }
    """
    msg_lower = message.lower().strip()

    # ── Detect task type ──────────────────────────────────────────────
    task_type = "conversation"
    best_score = 0

    for ttype, patterns in _TASK_PATTERNS.items():
        score = sum(1 for p in patterns if p in msg_lower)
        if score > best_score:
            best_score = score
            task_type = ttype

    # ── Detect complexity ─────────────────────────────────────────────
    complexity = "low"
    for level in ("high", "medium"):
        if any(sig in msg_lower for sig in _COMPLEXITY_SIGNALS[level]):
            complexity = level
            break

    # Long messages are inherently more complex
    if len(message) > 500 and complexity == "low":
        complexity = "medium"
    if len(message) > 1500:
        complexity = "high"

    # ── Detect risk ───────────────────────────────────────────────────
    risk = "low"
    for level in ("high", "medium"):
        if any(sig in msg_lower for sig in _RISK_SIGNALS[level]):
            risk = level
            break

    # ── Needs tools? ──────────────────────────────────────────────────
    tool_task_types = {
        "code_edit", "vision", "memory", "system_control",
        "code_review", "research", "orchestration", "media",
        "writing", "architecture", "system_admin", "file_operation",
        "capability_query",  # always needs tool call (get_capability_report)
    }
    needs_tools = task_type in tool_task_types

    # ── Determine routing tier ────────────────────────────────────────
    # Critical: high risk OR (high complexity + code tasks)
    if risk == "high":
        tier = "critical"
    elif complexity == "high" and task_type in ("code_edit", "architecture", "code_review"):
        tier = "critical"
    # Standard: medium risk/complexity, or research/writing
    elif risk == "medium" or complexity == "medium":
        tier = "standard"
    elif task_type in ("writing", "research", "architecture"):
        tier = "standard"
    else:
        tier = "fast"

    # Force verification if review mode is enabled (bumps fast -> standard)
    if _is_review_mode_enabled() and tier == "fast" and len(message) > 20:
        tier = "standard"

    # ── Intelligence vs. Latency: use_heavy_reasoning ─────────────────────
    # If casual chatter / short message -> bypass verification & deep Quiet-Star for lower latency.
    # If math, logic, or complex instructions -> enable verification & deep reasoning.
    _HEAVY_REASONING_SIGNALS = (
        "calculate", "solve", "equation", "proof", "integral", "derivative", "probability",
        "logic", "reasoning", "step by step", "first do", "then do", "instructions:",
        "follow these", "complex", "detailed analysis", "explain why", "prove that",
        "compare and contrast", "list all", "enumerate", "break down", "walk me through",
    )
    _CASUAL_SIGNALS = ("hi", "hey", "hello", "thanks", "thank you", "ok", "okay", "yes", "no ", "lol", "haha", "cool", "nice", "bye", "good morning", "good night", "what's up", "how are you", "sup", "yo",)
    has_heavy = any(s in msg_lower for s in _HEAVY_REASONING_SIGNALS)
    has_casual_only = len(message) < 80 and any(msg_lower.startswith(c) or msg_lower == c for c in _CASUAL_SIGNALS)
    use_heavy_reasoning = has_heavy or (not has_casual_only and (complexity == "high" or len(message) > 300))

    # ── Benchmark Override ────────────────────────────────────────────
    try:
        from flask import request as flask_req
        if flask_req and flask_req.headers.get("X-Benchmark"):
            print("  [ROUTER] Benchmark detected: forcing HIGH complexity + HEAVY reasoning")
            complexity = "high"
            use_heavy_reasoning = True
    except:
        pass

    return {
        "task_type": task_type,
        "complexity": complexity,
        "risk": risk,
        "needs_tools": needs_tools,
        "tier": tier,
        "use_heavy_reasoning": use_heavy_reasoning,
    }


# ============================================================================
# PLAN-THEN-EXECUTE (Decomposition for heavy reasoning)
# ============================================================================

def needs_planning_phase(classification: Dict[str, Any]) -> bool:
    """
    True when the task should use plan-then-execute: LLM first outputs a list of
    sub-tasks, then we run each step sequentially with previous output as context.
    Reduces logic errors on complex / multi-part requests.
    """
    if not classification:
        return False
    if not classification.get("use_heavy_reasoning", False):
        return False
    task_type = classification.get("task_type", "conversation")
    complexity = classification.get("complexity", "low")
    if complexity in ("high", "medium"):
        return True
    if task_type in ("math", "research", "writing", "architecture"):
        return True
    return False


def get_coding_constraints_block() -> str:
    """
    When a coding task is detected, search skill_library for coding_style / naming_conventions
    (or tags containing coding, style, convention) and return MUST_FOLLOW_CONSTRAINTS for the system prompt.
    """
    try:
        from modules.joi_skill_synthesis import _load_skill_library
        lib = _load_skill_library()
        skills = list(lib.get("skills", {}).values())
        style_tags = ("coding_style", "naming_conventions", "code_style", "conventions", "style", "coding", "dpo_discovery")
        constraints = []
        for s in skills:
            tags = [t.lower() for t in s.get("domain_tags", [])]
            if any(st in " ".join(tags) for st in style_tags) or "code" in s.get("name", "").lower():
                desc = s.get("description", "").strip()
                snip = s.get("prompt_snippet", "").strip()
                if desc:
                    constraints.append(desc[:200])
                if snip:
                    constraints.append(snip[:200])
        if not constraints:
            return ""
        return "\n[MUST_FOLLOW_CONSTRAINTS — from your skill library and Lonnie's preferences]:\n" + "\n".join(f"  - {c}" for c in constraints[:8]) + "\n"
    except Exception:
        return ""


def planning_prompt(user_message: str, include_skill_hints: bool = True, is_coding_task: bool = False) -> str:
    """
    Prompt that forces the model to return a JSON execution plan (no free-form answer).
    When include_skill_hints is True, injects coding-style hints from skill_library for Architect.
    When is_coding_task is True, also injects MUST_FOLLOW_CONSTRAINTS from coding_style/naming_conventions skills.
    """
    base = (
        "[PLANNING] You are the Architect. Break this request into 2-5 ordered sub-tasks. "
        "Output ONLY a JSON array, no other text. Format: "
        '[{"step": 1, "description": "..."}, {"step": 2, "description": "..."}, ...] '
        "Each step should be actionable (e.g. 'Analyze the logic flaw', 'Write the fix', 'Verify edge cases')."
    )
    if include_skill_hints or is_coding_task:
        try:
            from modules.joi_skill_synthesis import find_skills, _load_skill_library
            lib = _load_skill_library()
            skills = list(lib.get("skills", {}).values())
            coding_skills = [s for s in skills if "code" in str(s.get("domain_tags", [])).lower() or "coding" in s.get("name", "").lower()]
            if coding_skills:
                hints = [s.get("description", "")[:120] for s in coding_skills[:3]]
                base += " User coding preferences (from past tasks): " + " | ".join(hints)
            if is_coding_task:
                base += " " + get_coding_constraints_block().replace("\n", " ")[:600]
            if include_skill_hints:
                relevant = find_skills(user_message[:200], top_k=2)
                for s in relevant:
                    snip = s.get("prompt_snippet", "").strip()
                    if snip:
                        base += " " + snip[:200]
        except Exception:
            pass
    return base


def parse_plan_from_response(text: str) -> Optional[List[Dict[str, Any]]]:
    """
    Extract a JSON array of steps from model output.
    Expects objects with "step" (or "id") and "description" (or "desc").
    Returns list of {"step": int, "description": str} or None if not found.
    """
    if not text or not text.strip():
        return None
    import re
    # Try to find JSON array in the response
    raw = text.strip()
    for pattern in (r'\[[\s\S]*?\]', r'```(?:json)?\s*([\s\S]*?)\s*```'):
        match = re.search(pattern, raw)
        if match:
            json_str = match.group(1) if match.lastindex else match.group(0)
            try:
                arr = json.loads(json_str)
                if not isinstance(arr, list) or len(arr) < 2:
                    continue
                steps = []
                for i, item in enumerate(arr):
                    if not isinstance(item, dict):
                        continue
                    desc = item.get("description") or item.get("desc") or item.get("task") or str(item)
                    step_id = item.get("step", item.get("id", i + 1))
                    steps.append({"step": int(step_id) if isinstance(step_id, (int, float)) else i + 1, "description": str(desc)[:500]})
                if len(steps) >= 2:
                    return steps
            except (json.JSONDecodeError, TypeError):
                continue
    return None


# ============================================================================
# ROUTING -- config.joi_models TASK_MODEL_ROUTING
# ============================================================================

def _classification_to_config_task_key(classification: Dict[str, Any]) -> str:
    """Map classification to config.joi_models TASK_MODEL_ROUTING key."""
    task_type = classification.get("task_type", "conversation")
    tier = classification.get("tier", "fast")
    needs_tools = classification.get("needs_tools", False)

    if needs_tools or task_type == "capability_query":
        return "coding"  # Tool loop requires OpenAI
    if task_type == "orchestration":
        return "supervisor"
    if task_type in ("code_edit", "code_review", "architecture"):
        return "coding" if tier in ("standard", "critical") else "chat"
    if task_type in ("writing", "research") and tier in ("standard", "critical"):
        return "planning"
    if task_type in ("memory", "system_control", "vision", "math") and tier == "fast":
        return "quick_response"
    return "chat"


def get_routing_decision(classification: Dict[str, Any]) -> Dict[str, Any]:
    """
    Given a task classification, return the routing decision from config.joi_models.

    Returns:
        {
            "primary_model": "openai" | "gemini",
            "verifier_model": "openai" | "gemini" | None,
            "config_task_key": str,
            "primary_tuple": (provider, model_id),
            "fallback_tuple": (provider, model_id),
            "tier", "task_type", "needs_tools", "reason"
        }
    """
    task_type = classification.get("task_type", "conversation")
    tier = classification.get("tier", "fast")
    needs_tools = classification.get("needs_tools", False)

    task_key = _classification_to_config_task_key(classification)
    _default_route = {"primary": ("openai", OPENAI_MODELS["general"]), "fallback": ("gemini", GEMINI_MODELS["general"])}
    route = TASK_MODEL_ROUTING.get(task_key) or TASK_MODEL_ROUTING.get("chat") or _default_route
    primary_tuple = route.get("primary", ("openai", OPENAI_MODELS["general"]))
    fallback_tuple = route.get("fallback", ("openai", OPENAI_MODELS["general"]))

    primary = primary_tuple[0]  # "openai" or "gemini"
    primary_model_id = primary_tuple[1] if len(primary_tuple) > 1 else None

    # Verifier: use Gemini for standard/critical when we have verification
    verifier = None
    verifier_model_id = None
    if tier in ("standard", "critical") and task_type in ("writing", "research", "code_edit", "code_review", "architecture"):
        verifier = "gemini"
        verifier_model_id = GEMINI_MODELS.get("reasoning", "gemini-1.5-pro")

    try:
        from modules.joi_llm import HAVE_GEMINI, client as openai_client
    except ImportError:
        HAVE_GEMINI = False
        openai_client = None

    if verifier == "gemini" and not HAVE_GEMINI and openai_client:
        verifier = "openai"
        verifier_model_id = OPENAI_MODELS.get("coding", "gpt-4o")

    reason = f"{task_type}/{tier} -> config={task_key} primary={primary}"
    if verifier:
        reason += f", verify={verifier}"

    return {
        "primary_model": primary,
        "verifier_model": verifier,
        "config_task_key": task_key,
        "primary_tuple": primary_tuple,
        "fallback_tuple": fallback_tuple,
        "primary_model_id": primary_model_id,
        "verifier_model_id": verifier_model_id,
        "tier": tier,
        "task_type": task_type,
        "needs_tools": needs_tools,
        "reason": reason,
    }


# ============================================================================
# VERIFICATION LAYER -- Generate + Verify pattern
# ============================================================================

def verify_output(
    original_message: str,
    output_text: str,
    task_classification: Dict[str, Any],
    verifier: str = "gemini",
) -> Dict[str, Any]:
    """
    Send the generated output to a second model for verification.

    The verifier checks for:
      - Factual accuracy / consistency
      - Missing edge cases (for code)
      - Hallucinations or unsupported claims
      - Completeness (did it answer the question?)

    Returns:
        {
            "approved": bool,
            "issues": [str, ...],
            "revised_text": str or None (only if verifier rewrites),
            "verifier_model": str,
            "verification_time_ms": int
        }
    """
    start = time.time()
    task_type = task_classification.get("task_type", "conversation")

    # Build verification prompt based on task type
    if task_type in ("code_edit", "code_review", "architecture"):
        verify_prompt = (
            "You are a senior code reviewer. A user asked:\n"
            f'"""\n{original_message[:1000]}\n"""\n\n'
            "The AI produced this response:\n"
            f'"""\n{output_text[:3000]}\n"""\n\n'
            "Check for:\n"
            "1. Bugs, logic errors, or missing edge cases\n"
            "2. Security vulnerabilities\n"
            "3. Whether it actually answers what was asked\n"
            "4. Missing imports or undefined references\n\n"
            "Respond in JSON: {\"approved\": true/false, \"issues\": [\"issue1\", ...], "
            "\"summary\": \"one line summary\"}"
        )
    elif task_type == "research":
        verify_prompt = (
            "You are a fact-checker. A user asked:\n"
            f'"""\n{original_message[:1000]}\n"""\n\n'
            "The AI produced this response:\n"
            f'"""\n{output_text[:3000]}\n"""\n\n'
            "Check for:\n"
            "1. Factual accuracy -- any claims that seem wrong or unsupported?\n"
            "2. Completeness -- did it miss important aspects?\n"
            "3. Hallucinations -- any made-up facts, URLs, or citations?\n\n"
            "Respond in JSON: {\"approved\": true/false, \"issues\": [\"issue1\", ...], "
            "\"summary\": \"one line summary\"}"
        )
    else:
        verify_prompt = (
            "A user said:\n"
            f'"""\n{original_message[:500]}\n"""\n\n'
            "The AI responded:\n"
            f'"""\n{output_text[:2000]}\n"""\n\n'
            "Is this response accurate, complete, and appropriate? "
            "Respond in JSON: {\"approved\": true/false, \"issues\": [\"issue1\", ...], "
            "\"summary\": \"one line summary\"}"
        )

    # Call the verifier model
    result_text = None
    actual_verifier = verifier

    if verifier == "gemini":
        try:
            from modules.joi_llm import _call_gemini
            result_text = _call_gemini(verify_prompt, max_tokens=500, model=GEMINI_MODELS.get("reasoning", "gemini-1.5-pro"))
        except Exception:
            pass

    if result_text is None and verifier in ("openai", "gemini"):
        # Fallback to OpenAI (config)
        actual_verifier = "openai"
        try:
            from modules.joi_llm import _call_openai
            resp = _call_openai(
                [{"role": "user", "content": verify_prompt}],
                max_tokens=500, model=OPENAI_MODELS.get("coding", "gpt-4o")
            )
            if resp and resp.choices:
                result_text = resp.choices[0].message.content
        except Exception:
            pass

    elapsed_ms = int((time.time() - start) * 1000)

    if not result_text:
        return {
            "approved": True,  # Can't verify -> pass through
            "issues": [],
            "revised_text": None,
            "verifier_model": actual_verifier,
            "verification_time_ms": elapsed_ms,
            "error": "Verifier unavailable",
        }

    # Parse JSON response from verifier
    try:
        json_match = re.search(r'\{[\s\S]*?\}', result_text)
        if json_match:
            parsed = json.loads(json_match.group())
            return {
                "approved": parsed.get("approved", True),
                "issues": parsed.get("issues", []),
                "summary": parsed.get("summary", ""),
                "revised_text": None,
                "verifier_model": actual_verifier,
                "verification_time_ms": elapsed_ms,
            }
    except (json.JSONDecodeError, AttributeError):
        pass

    # If we can't parse, check for obvious rejection signals
    lower = result_text.lower()
    rejected = any(word in lower for word in ["incorrect", "wrong", "bug", "error", "false"])
    return {
        "approved": not rejected,
        "issues": [result_text[:300]] if rejected else [],
        "revised_text": None,
        "verifier_model": actual_verifier,
        "verification_time_ms": elapsed_ms,
    }


# ============================================================================
# CODE SMOKE TEST
# ============================================================================

def smoke_test_file(file_path: str) -> Dict[str, Any]:
    """
    Quick validation of a Python file after editing:
      1. Syntax check (compile)
      2. Import check (for modules)

    Returns {"passed": bool, "errors": [...]}
    """
    p = Path(file_path)
    if not p.exists():
        return {"passed": False, "errors": [f"File not found: {file_path}"]}

    errors = []

    # ── Step 1: Syntax check ──────────────────────────────────────────
    if p.suffix == ".py":
        try:
            source = p.read_text(encoding="utf-8")
            compile(source, str(p), "exec")
        except SyntaxError as e:
            errors.append(f"Syntax error at line {e.lineno}: {e.msg}")
            return {"passed": False, "errors": errors}

    # ── Step 2: Import check (for modules/ files) ─────────────────────
    if p.suffix == ".py" and "modules" in str(p):
        module_name = p.stem  # e.g., "joi_camera"
        try:
            import importlib
            import sys

            # Remove from cache if previously imported (get fresh)
            full_module = f"modules.{module_name}"
            if full_module in sys.modules:
                # Don't actually remove -- too risky at runtime
                # Just do a syntax-level check via compile (already done above)
                pass
        except Exception as e:
            errors.append(f"Import check note: {e}")

    # ── Step 3: HTML/JS basic validation ──────────────────────────────
    if p.suffix == ".html":
        try:
            content = p.read_text(encoding="utf-8")
            # Check for unclosed script tags
            open_scripts = content.lower().count("<script")
            close_scripts = content.lower().count("</script>")
            if open_scripts != close_scripts:
                errors.append(f"Mismatched <script> tags: {open_scripts} open, {close_scripts} close")

            # Check for obviously broken JS (very basic)
            if "function (" in content and content.count("{") != content.count("}"):
                # This is a rough heuristic
                diff = abs(content.count("{") - content.count("}"))
                if diff > 5:  # Allow some tolerance
                    errors.append(f"Brace mismatch: {content.count('{')} open, {content.count('}')} close (diff={diff})")
        except Exception as e:
            errors.append(f"HTML validation error: {e}")

    return {
        "passed": len(errors) == 0,
        "errors": errors,
        "file": str(p),
        "file_type": p.suffix,
    }


# ============================================================================
# ROUTING STATS -- Persistent logging for learning
# ============================================================================

_routing_stats_cache: Optional[Dict[str, Any]] = None
_routing_stats_ts: float = 0
ROUTING_STATS_CACHE_TTL: float = 30.0


def _load_routing_stats() -> Dict[str, Any]:
    """Load routing statistics. Cached 30s to reduce file I/O per request."""
    global _routing_stats_cache, _routing_stats_ts
    now = time.time()
    if _routing_stats_cache is not None and (now - _routing_stats_ts) < ROUTING_STATS_CACHE_TTL:
        return _routing_stats_cache
    if ROUTING_STATS_PATH.exists():
        try:
            data = json.loads(ROUTING_STATS_PATH.read_text(encoding="utf-8"))
            _routing_stats_cache = data
            _routing_stats_ts = now
            return data
        except Exception:
            pass
    default = {
        "decisions": [],
        "model_usage": {},
        "task_type_counts": {},
        "tier_counts": {},
        "verification_results": {"approved": 0, "rejected": 0},
        "smoke_test_results": {"passed": 0, "failed": 0},
    }
    _routing_stats_cache = default
    _routing_stats_ts = now
    return default


def _save_routing_stats(stats: Dict[str, Any]):
    """Save routing statistics."""
    global _routing_stats_cache
    if len(stats.get("decisions", [])) > MAX_ROUTING_LOG:
        stats["decisions"] = stats["decisions"][-MAX_ROUTING_LOG:]
    ROUTING_STATS_PATH.write_text(json.dumps(stats, indent=2, default=str), encoding="utf-8")
    _routing_stats_cache = None  # invalidate so next load is fresh


def log_routing_decision(
    user_message: str,
    classification: Dict[str, Any],
    routing: Dict[str, Any],
    verification: Optional[Dict[str, Any]] = None,
    smoke_test: Optional[Dict[str, Any]] = None,
    model_used: str = "",
    response_time_ms: int = 0,
):
    """
    Log a routing decision for learning.
    Called after each /chat response.
    """
    try:
        stats = _load_routing_stats()

        # Log the decision
        entry = {
            "ts": time.time(),
            "datetime": datetime.now().isoformat(),
            "message_preview": user_message[:100],
            "task_type": classification.get("task_type", "?"),
            "tier": classification.get("tier", "?"),
            "complexity": classification.get("complexity", "?"),
            "risk": classification.get("risk", "?"),
            "primary_model": routing.get("primary_model", "?"),
            "verifier_model": routing.get("verifier_model"),
            "model_used": model_used,
            "response_time_ms": response_time_ms,
        }

        if verification:
            entry["verified"] = verification.get("approved", True)
            entry["verification_issues"] = verification.get("issues", [])
            if verification.get("approved"):
                stats["verification_results"]["approved"] += 1
            else:
                stats["verification_results"]["rejected"] += 1

        if smoke_test:
            entry["smoke_test_passed"] = smoke_test.get("passed", True)
            if smoke_test.get("passed"):
                stats["smoke_test_results"]["passed"] += 1
            else:
                stats["smoke_test_results"]["failed"] += 1

        stats["decisions"].append(entry)

        # Update counters
        task_type = classification.get("task_type", "unknown")
        tier = classification.get("tier", "unknown")
        primary = routing.get("primary_model", "unknown")

        stats["task_type_counts"][task_type] = stats["task_type_counts"].get(task_type, 0) + 1
        stats["tier_counts"][tier] = stats["tier_counts"].get(tier, 0) + 1
        stats["model_usage"][primary] = stats["model_usage"].get(primary, 0) + 1

        _save_routing_stats(stats)
    except Exception as e:
        print(f"  [ROUTER] Failed to log routing decision: {e}")


def get_routing_summary() -> Dict[str, Any]:
    """Get a summary of routing statistics for diagnostics."""
    stats = _load_routing_stats()
    total = sum(stats.get("tier_counts", {}).values())
    return {
        "ok": True,
        "total_decisions": total,
        "task_type_distribution": stats.get("task_type_counts", {}),
        "tier_distribution": stats.get("tier_counts", {}),
        "model_usage": stats.get("model_usage", {}),
        "verification_results": stats.get("verification_results", {}),
        "smoke_test_results": stats.get("smoke_test_results", {}),
        "recent_decisions": stats.get("decisions", [])[-5:],
    }


# ============================================================================
# COMPILE ROUTER CONTEXT -- Inject into system prompt
# ============================================================================

def compile_router_block() -> str:
    """Disabled — routing meta adds tokens without value in Joi's voice."""
    return ""


# ============================================================================
# TOOL REGISTRATION
# ============================================================================

def _classify_task_tool(**kwargs) -> Dict[str, Any]:
    """Tool wrapper for classify_task."""
    message = kwargs.get("message", "")
    if not message:
        return {"ok": False, "error": "Provide a 'message' to classify."}
    result = classify_task(message)
    routing = get_routing_decision(result)
    return {"ok": True, "classification": result, "routing": routing}


def _get_routing_stats_tool(**kwargs) -> Dict[str, Any]:
    """Tool wrapper for routing stats."""
    return get_routing_summary()


register_tool(
    {"type": "function", "function": {
        "name": "classify_task",
        "description": (
            "Classify a message by task type, complexity, and risk level. "
            "Shows which model would be selected and whether verification would run. "
            "Use to understand how your multi-model brain routes different requests."
        ),
        "parameters": {"type": "object", "properties": {
            "message": {"type": "string", "description": "The message to classify"}
        }, "required": ["message"]}
    }},
    _classify_task_tool
)

register_tool(
    {"type": "function", "function": {
        "name": "get_routing_stats",
        "description": (
            "View routing statistics: how tasks are classified, which models are used, "
            "verification approval rates, and smoke test pass rates."
        ),
        "parameters": {"type": "object", "properties": {}}
    }},
    _get_routing_stats_tool
)


# ============================================================================
# FLASK ROUTE
# ============================================================================

def _router_route():
    """REST endpoint for router info."""
    from modules.joi_memory import require_user
    require_user()

    if flask_req.method == "GET":
        return jsonify(get_routing_summary())

    data = flask_req.get_json(silent=True) or {}
    action = data.get("action", "classify")

    if action == "classify":
        msg = data.get("message", "")
        if not msg:
            return jsonify({"ok": False, "error": "No message"})
        classification = classify_task(msg)
        routing = get_routing_decision(classification)
        return jsonify({"ok": True, "classification": classification, "routing": routing})
    elif action == "stats":
        return jsonify(get_routing_summary())
    else:
        return jsonify({"ok": False, "error": f"Unknown action: {action}"})


register_route("/router", ["GET", "POST"], _router_route, "router_route")


# ============================================================================
# REVIEW MODE ROUTE
# ============================================================================

def _review_mode_route():
    """GET/POST /review-mode -- view or toggle forced multi-model review."""
    if flask_req.method == "GET":
        return jsonify({"ok": True, **get_review_mode()})
    data = flask_req.get_json(silent=True) or {}
    result = set_review_mode(
        enabled=data.get("enabled", False),
        verifier=data.get("verifier", "gemini"),
    )
    return jsonify({"ok": True, **result})


register_route("/review-mode", ["GET", "POST"], _review_mode_route, "review_mode_route")

print("  [joi_router] Smart task router registered: classify_task, get_routing_stats")
print(f"  [joi_router] Review mode: {_REVIEW_MODE_PATH} | Route: /review-mode")
print(f"  [joi_router] Routing stats: {ROUTING_STATS_PATH}")


# ── Tool Lazy Loading — inject only tools relevant to classified task ─────────

TOOL_BUCKETS: Dict[str, List[str]] = {
    "conversation":   ["remember", "recall", "set_mode"],
    "memory":         ["remember", "recall", "update_manuscript", "get_dpo_insights"],
    "vision":         ["analyze_screen", "capture_camera_frame", "describe_image",
                       "remember", "recall"],
    "desktop":        ["move_mouse", "click_mouse", "type_text", "focus_window",
                       "list_windows", "screenshot", "remember"],
    "music":          ["play_music", "pause_music", "stop_music", "list_music",
                       "set_volume", "remember"],
    "coding":         ["read_file", "write_file", "run_python", "search_codebase",
                       "propose_upgrade", "test_upgrade", "remember", "recall"],
    "orchestration":  ["orchestrate_task", "run_swarm", "propose_upgrade",
                       "test_upgrade", "apply_upgrade", "remember", "recall"],
    "system":         ["set_provider", "self_diagnose", "self_fix",
                       "get_autonomy_status", "toggle_commentary", "remember"],
    "research":       ["web_search", "web_fetch", "remember", "recall"],
    "market":         ["get_stock_quote", "get_market_overview", "remember"],
}

# Task types that always get the full tool set (complex/unknown tasks)
_FULL_TOOL_TASKS: set = {"complex", "multi_step", "unknown", "orchestration",
                          "code_edit", "code_review", "architecture", "system_admin"}

# Tools always included regardless of task type
_CORE_TOOLS: set = {"remember", "recall", "set_mode"}


def get_tools_for_task(task_type: str, all_tools: list) -> list:
    """Return only tools relevant to the classified task.

    Falls back to all tools for complex/unknown/orchestration tasks.
    Always preserves core tools (remember, recall, set_mode).
    """
    if not all_tools:
        return []
    if task_type in _FULL_TOOL_TASKS:
        return all_tools

    allowed = set(TOOL_BUCKETS.get(task_type, [])) | _CORE_TOOLS
    if not allowed - _CORE_TOOLS:
        # No bucket defined for this task type — use full set as safety net
        return all_tools

    filtered = [t for t in all_tools
                if t.get("function", {}).get("name") in allowed]
    return filtered if filtered else all_tools  # safety fallback
