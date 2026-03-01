"""
modules/joi_self_awareness.py

Dynamic Self-Awareness Engine
=============================
Replaces hardcoded tool lists with runtime introspection.
Joi knows EXACTLY what she can do because this module reads her actual
registered tools, loaded modules, and subsystem status at runtime.

Provides:
- compile_awareness_block() -- injected into system prompt (compact summary)
- get_full_capability_report() -- detailed report for self_diagnose
- get_tool_registry_block() -- dynamic tool list for _build_system_prompt
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

import joi_companion

BASE_DIR = Path(__file__).resolve().parent.parent
MODULES_DIR = BASE_DIR / "modules"

# ── Tool category detection (maps tool names to human-readable domains) ──────

_DOMAIN_KEYWORDS = {
    "memory": ["remember", "recall", "record_interaction", "learn_communication",
               "analyze_learning", "suggest_improvements", "get_learning_stats"],
    "vision": ["analyze_screen", "screenshot", "analyze_camera", "enroll_face",
               "update_face", "list_known_faces", "forget_face", "learn_face",
               "visual_self_diagnose"],
    "desktop": ["move_mouse", "click_mouse", "type_text", "press_key",
                "get_mouse_position", "smart_click", "list_windows",
                "find_window", "focus_window", "close_window", "launch_app",
                "play_media", "find_file_smart"],
    "browser": ["open_url", "click_element", "fill_input", "extract_text",
                "browser_screenshot", "execute_js", "wait_for_element"],
    "files": ["fs_list", "fs_read", "fs_search", "search_files", "generate_file",
              "save_code_file", "save_text_file", "save_research_findings",
              "list_files", "get_file_content", "save_binary_file", "project_tree",
              "read_upload", "list_uploads"],
    "code_editing": ["code_edit", "code_insert", "code_read_section", "code_search",
                     "code_rollback", "code_list_backups", "creative_edit",
                     "code_backup", "analyze_code", "render_diff"],
    "orchestration": ["orchestrate_task", "approve_subtask", "reject_subtask",
                      "get_orchestrator_status", "cancel_orchestration",
                      "create_orchestration_proposal"],
    "swarm": ["swarm_orchestrate", "swarm_status", "swarm_cancel", "send_agent_message"],
    "evolution": ["monitor_ai_research", "analyze_capabilities",
                  "get_evolution_stats", "compare_with_ai", "introspect_system",
                  "evaluate_research", "create_plugin"],
    "self_repair": ["self_diagnose", "self_fix", "code_self_repair",
                    "run_system_diagnostic", "visual_self_diagnose"],
    "consciousness": ["reflect", "read_journal", "how_have_i_grown",
                      "update_manuscript", "internal_monologue"],
    "llm_routing": ["set_provider", "get_current_provider", "brain_route",
                    "brain_stats", "classify_task", "get_routing_stats"],
    "home_automation": ["ha_get_entities", "ha_get_state", "ha_turn_on",
                        "ha_turn_off", "ha_set_temperature", "ha_call_service",
                        "ha_camera_snapshot"],
    "obs_studio": ["obs_connect", "manage_obs"],
    "security": ["security_arm", "security_disarm", "security_status",
                 "security_get_recordings", "security_set_sensitivity"],
    "skills": ["synthesize_skill", "find_skill", "run_self_correction",
               "generate_practice_goals", "get_skill_stats"],
    "modes": ["set_mode", "toggle_commentary", "set_scene"],
    "scheduler": ["scheduler_control", "configure_scheduler"],
    "market": ["get_market_summary", "analyze_crypto", "analyze_stock",
               "create_price_alert", "check_price_alerts"],
    "projects": ["scan_projects", "organise_projects", "scaffold_project",
                 "list_templates", "build_project", "run_setup_command",
                 "get_build_configs"],
    "autonomy": ["start_autonomy", "stop_autonomy", "get_autonomy_status",
                 "run_autonomy_cycle"],
    "voice": ["enroll_voice", "check_voice_id", "set_voice_threshold"],
    "web": ["web_search", "web_fetch"],
    "watchdog": ["watchdog_status", "manual_checkpoint", "manual_revert"],
    "avatar": ["generate_avatar_image"],
}

# Reverse lookup
_TOOL_TO_DOMAIN: Dict[str, str] = {}
for _dom, _tools in _DOMAIN_KEYWORDS.items():
    for _t in _tools:
        _TOOL_TO_DOMAIN[_t] = _dom


def _get_registered_tools() -> List[Dict]:
    """Get all currently registered tools from joi_companion.TOOLS."""
    return getattr(joi_companion, "TOOLS", [])


def _get_tool_names() -> List[str]:
    """Get sorted list of all registered tool names."""
    tools = _get_registered_tools()
    return sorted([
        t.get("function", {}).get("name", "?")
        for t in tools
        if t.get("function", {}).get("name")
    ])


def _categorize_tools() -> Dict[str, List[str]]:
    """Group registered tools by domain."""
    tool_names = _get_tool_names()
    categorized: Dict[str, List[str]] = {}
    uncategorized = []

    for name in tool_names:
        domain = _TOOL_TO_DOMAIN.get(name)
        if domain:
            categorized.setdefault(domain, []).append(name)
        else:
            uncategorized.append(name)

    if uncategorized:
        categorized["other"] = uncategorized

    return categorized


def _count_loaded_modules() -> Tuple[int, List[str]]:
    """Count and list loaded joi modules."""
    loaded = []
    for name, mod in sys.modules.items():
        if name.startswith("modules.joi_") or name.startswith("modules.core."):
            loaded.append(name.replace("modules.", ""))
    return len(loaded), sorted(loaded)


def _check_subsystems() -> Dict[str, str]:
    """Check status of core subsystems."""
    status = {}

    # Kernel
    try:
        from modules.core.kernel import _booted
        status["kernel"] = "running" if _booted else "not booted"
    except Exception:
        try:
            from modules.core import kernel
            status["kernel"] = "loaded"
        except Exception:
            status["kernel"] = "not loaded"

    # Engine
    try:
        from modules.core.engine import _engine_running
        status["cognitive_engine"] = "running" if _engine_running else "stopped"
    except Exception:
        try:
            from modules.core import engine
            status["cognitive_engine"] = "loaded"
        except Exception:
            status["cognitive_engine"] = "not loaded"

    # Cognition / ReasoningGraph
    try:
        from modules.core.cognition import graph
        status["reasoning_graph"] = "active" if graph else "loaded"
    except Exception:
        status["reasoning_graph"] = "not loaded"

    # Introspection
    try:
        from modules.core.introspection import engine as intro
        cap_count = len(intro.capabilities) if hasattr(intro, "capabilities") else 0
        status["introspection"] = f"active ({cap_count} capabilities scanned)"
    except Exception:
        status["introspection"] = "not loaded"

    # Brain router
    try:
        from modules.joi_brain import brain as _brain
        alive = sum(1 for m in _brain._models if not _brain._is_dead(m))
        status["brain_router"] = f"active ({alive} models alive)"
    except Exception:
        status["brain_router"] = "not loaded"

    # Vector memory
    try:
        from modules.memory.memory_manager import _store
        status["vector_memory"] = "active" if _store else "no backend"
    except Exception:
        status["vector_memory"] = "not loaded"

    # Watchdog
    try:
        from modules.joi_watchdog import _circuit_state
        status["watchdog"] = f"active (circuit: {_circuit_state})"
    except Exception:
        status["watchdog"] = "not loaded"

    return status


# ── Public API ───────────────────────────────────────────────────────────────


def get_tool_registry_block() -> str:
    """
    Generate a DYNAMIC tool list for the system prompt.
    Replaces the hardcoded list in _build_system_prompt().
    Compact format: domain -> tool names (no descriptions, saves tokens).
    """
    categorized = _categorize_tools()
    total = sum(len(v) for v in categorized.values())

    lines = [f"\nYOUR TOOLS ({total} registered -- USE THEM, they are your real capabilities):"]

    # Priority ordering for display
    priority_order = [
        "memory", "consciousness", "files", "code_editing", "desktop",
        "browser", "vision", "web", "orchestration", "swarm",
        "self_repair", "evolution", "llm_routing", "skills",
        "home_automation", "obs_studio", "security", "market",
        "modes", "scheduler", "projects", "autonomy", "watchdog",
        "voice", "avatar", "other",
    ]

    # Friendly domain names
    domain_labels = {
        "memory": "MEMORY & LEARNING",
        "consciousness": "CONSCIOUSNESS & THINKING",
        "files": "FILE SYSTEM",
        "code_editing": "CODE EDITING",
        "desktop": "DESKTOP CONTROL",
        "browser": "BROWSER AUTOMATION",
        "vision": "VISION & CAMERAS",
        "web": "WEB SEARCH",
        "orchestration": "MULTI-AGENT PIPELINE",
        "swarm": "SWARM (PARALLEL AGENTS)",
        "self_repair": "SELF-DIAGNOSIS & REPAIR",
        "evolution": "SELF-EVOLUTION",
        "llm_routing": "LLM BRAIN ROUTING",
        "skills": "SKILL LIBRARY",
        "home_automation": "HOME ASSISTANT (IoT)",
        "obs_studio": "OBS STUDIO",
        "security": "SECURITY SYSTEM",
        "market": "MARKET & FINANCE",
        "modes": "MODES & SETTINGS",
        "scheduler": "SCHEDULER",
        "projects": "PROJECT MANAGEMENT",
        "autonomy": "AUTONOMOUS MODE",
        "watchdog": "GIT SAFETY (WATCHDOG)",
        "voice": "VOICE ID",
        "avatar": "IMAGE GENERATION",
        "other": "OTHER",
    }

    for domain in priority_order:
        tools = categorized.get(domain)
        if not tools:
            continue
        label = domain_labels.get(domain, domain.upper())
        tool_str = ", ".join(f"`{t}`" for t in tools)
        lines.append(f"- {label}: {tool_str}")

    return "\n".join(lines) + "\n"


def compile_awareness_block() -> str:
    """
    Compact self-awareness block for system prompt injection.
    Tells Joi about her subsystems and module count.
    """
    parts = []

    # Subsystem status (compact)
    subsystems = _check_subsystems()
    active = [f"{k}={v}" for k, v in subsystems.items() if "active" in v or "running" in v]
    if active:
        parts.append(f"[SYSTEM STATUS]: {', '.join(active)}")

    # Module count
    mod_count, mod_list = _count_loaded_modules()
    parts.append(f"[LOADED MODULES]: {mod_count} modules active")

    # Tool count
    tool_count = len(_get_tool_names())
    parts.append(
        f"[SELF-AWARENESS]: You have {tool_count} tools across "
        f"{len(_categorize_tools())} capability domains. "
        f"You can introspect yourself with `self_diagnose`, `introspect_system`, "
        f"`get_system_health`, or `brain_stats`. "
        f"If you're unsure whether you have a capability, check your tool list -- don't guess."
    )

    block = "\n".join(parts)
    return block[:400] if len(block) > 400 else block


def get_full_capability_report(**kwargs) -> Dict[str, Any]:
    """Full capability report -- returns a human-readable text summary for the LLM to output directly."""
    categorized = _categorize_tools()
    mod_count, _ = _count_loaded_modules()
    tool_names = _get_tool_names()

    # Build human-readable text the LLM can output directly
    domain_labels = {
        "memory": "Memory & Learning",
        "consciousness": "Consciousness & Thinking",
        "files": "File System",
        "code_editing": "Code Editing",
        "desktop": "Desktop Control",
        "browser": "Browser Automation",
        "vision": "Vision & Cameras",
        "web": "Web Search",
        "orchestration": "Multi-Agent Pipeline",
        "swarm": "Swarm (Parallel Agents)",
        "self_repair": "Self-Diagnosis & Repair",
        "evolution": "Self-Evolution",
        "llm_routing": "LLM Brain Routing",
        "skills": "Skill Library",
        "home_automation": "Home Assistant (IoT)",
        "obs_studio": "OBS Studio",
        "security": "Security System",
        "market": "Market & Finance",
        "modes": "Modes & Settings",
        "scheduler": "Scheduler",
        "projects": "Project Management",
        "autonomy": "Autonomous Mode",
        "watchdog": "Git Safety (Watchdog)",
        "voice": "Voice ID",
        "avatar": "Image Generation",
        "other": "Other",
    }

    lines = [f"I have **{len(tool_names)} tools** across {len(categorized)} categories:\n"]
    for domain, tools in categorized.items():
        if not tools:
            continue
        label = domain_labels.get(domain, domain.replace("_", " ").title())
        tool_str = ", ".join(f"`{t}`" for t in sorted(tools))
        lines.append(f"**{label}** ({len(tools)}): {tool_str}")

    formatted_text = "\n".join(lines)

    return {
        "ok": True,
        "total_tools": len(tool_names),
        "total_modules": mod_count,
        "report": formatted_text,
        "generated_at": datetime.now().isoformat(),
    }


# ── Registration ─────────────────────────────────────────────────────────────

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "get_capability_report",
        "description": "Get a full report of all your registered tools, loaded modules, and subsystem status. Use this when asked about your capabilities.",
        "parameters": {"type": "object", "properties": {}}
    }},
    get_full_capability_report,
)

print(f"    [OK] joi_self_awareness (Self-Awareness: {len(_get_tool_names())} tools mapped, 1 tool)")
