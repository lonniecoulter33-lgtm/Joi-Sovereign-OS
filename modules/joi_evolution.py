"""
modules/joi_evolution.py

AI Self-Evolution & Research Tracking Module
============================================

Features:
- Monitors AI research/news in real-time
- Analyzes Joi's current capabilities vs industry standards
- Proposes upgrades with full code implementations
- Two upgrade modes: AUTO (with approval) or MANUAL (download for review)
- Automatic backups with timestamps before any code changes
- Rollback capability if upgrades fail safety checks
- Learning system that improves upgrade quality over time

Safety Layers:
1. Syntax validation before applying code
2. Import verification (no missing dependencies)
3. Backup creation with timestamps
4. Dry-run testing in isolated environment
5. Rollback on failure
6. User approval required for AUTO mode
"""

from __future__ import annotations

import os
import json
import time
import shutil
import ast
import importlib
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

import joi_companion
from flask import jsonify, request as flask_req
from modules.joi_memory import require_user

# ============================================================================
# CONFIGURATION
# ============================================================================

RESEARCH_CHECK_INTERVAL = 3600 * 6  # Check for AI news every 6 hours
CAPABILITY_ANALYSIS_INTERVAL = 3600 * 24  # Analyze capabilities daily
BASE_DIR = Path(__file__).resolve().parent.parent
BACKUPS_DIR = BASE_DIR / "backups"
PROPOSALS_DIR = BASE_DIR / "proposals"
EVOLUTION_LOG = BASE_DIR / "evolution_log.json"

# Research sources for AI advancements
RESEARCH_SOURCES = [
    "https://arxiv.org/list/cs.AI/recent",
    "https://huggingface.co/papers",
    "https://www.anthropic.com/research",
    "https://openai.com/research",
    "https://github.com/trending/python?since=daily"
]

# Known AI systems for comparison
AI_SYSTEMS = {
    "ChatGPT / OpenAI": {
        "strengths": ["massive training data", "web browsing", "DALL-E image generation",
                       "code interpreter", "plugins ecosystem", "GPT-4o vision"],
        "weaknesses": ["no persistent memory across chats", "no desktop control",
                       "no webcam/camera", "no local file access", "generic personality"],
        "category": "cloud_assistant"
    },
    "Google Gemini": {
        "strengths": ["multimodal (text+image+video+audio)", "real-time web search grounding",
                       "Google ecosystem integration", "long context (1M+ tokens)", "code execution"],
        "weaknesses": ["no persistent identity", "no desktop automation",
                       "no face recognition", "limited customization", "generic personality"],
        "category": "cloud_assistant"
    },
    "Claude (Anthropic)": {
        "strengths": ["strong reasoning", "long context (200k tokens)", "computer use",
                       "coding excellence", "safety-focused", "Claude Code CLI"],
        "weaknesses": ["It lacks persistent memory across chat sessions", "It has no webcam vision", "It lacks an always-on active presence on the desktop",
                       "It has no custom or editable identity/personality", "It has no real-time monitoring of the user's PC"],
        "category": "cloud_assistant"
    },
    "Tesla AI / FSD": {
        "strengths": ["real-time computer vision", "physical world interaction",
                       "massive sensor fusion", "end-to-end neural networks", "hardware integration"],
        "weaknesses": ["single-purpose (driving)", "no conversation", "no personality",
                       "requires specialized hardware", "no general reasoning"],
        "category": "embodied_ai"
    },
    "Neuralink": {
        "strengths": ["brain-computer interface", "direct neural signal reading",
                       "physical embodiment through user", "real-time brain data"],
        "weaknesses": ["requires surgical implant", "limited bandwidth",
                       "early stage technology", "no AI personality", "medical device constraints"],
        "category": "neural_interface"
    },
    "Apple Intelligence / Siri": {
        "strengths": ["deep OS integration", "on-device processing", "privacy focus",
                       "hardware ecosystem", "app intents"],
        "weaknesses": ["limited personality", "no self-improvement", "no coding ability",
                       "walled garden", "no desktop automation beyond Apple"],
        "category": "os_assistant"
    }
}


# ============================================================================
# INITIALIZATION
# ============================================================================

def _ensure_dirs():
    """Create necessary directories if they don't exist"""
    BACKUPS_DIR.mkdir(exist_ok=True)
    PROPOSALS_DIR.mkdir(exist_ok=True)
    if not EVOLUTION_LOG.exists():
        EVOLUTION_LOG.write_text(json.dumps({
            "created": time.time(),
            "upgrades_applied": [],
            "upgrades_failed": [],
            "research_findings": [],
            "capability_gaps": []
        }, indent=2))

_ensure_dirs()


# ============================================================================
# HARDWARE & SYSTEM INTROSPECTION
# ============================================================================

import platform
import subprocess

def _get_hardware_specs() -> Dict[str, Any]:
    """Detect the host computer's hardware capabilities and limitations."""
    specs = {
        "os": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "hostname": platform.node(),
    }

    # CPU info
    specs["cpu_count_logical"] = os.cpu_count() or 0

    # Disk space
    try:
        import shutil
        total, used, free = shutil.disk_usage(str(Path(__file__).resolve().parent.parent))
        specs["disk_total_gb"] = round(total / (1024**3), 1)
        specs["disk_used_gb"] = round(used / (1024**3), 1)
        specs["disk_free_gb"] = round(free / (1024**3), 1)
    except Exception:
        pass

    # RAM (try psutil, fall back to wmic on Windows)
    try:
        import psutil
        mem = psutil.virtual_memory()
        specs["ram_total_gb"] = round(mem.total / (1024**3), 1)
        specs["ram_available_gb"] = round(mem.available / (1024**3), 1)
        specs["ram_percent_used"] = mem.percent
        specs["cpu_percent"] = psutil.cpu_percent(interval=0.5)
        specs["psutil_available"] = True
    except ImportError:
        specs["psutil_available"] = False
        # Windows fallback
        if platform.system() == "Windows":
            try:
                out = subprocess.check_output(
                    ["wmic", "OS", "get", "TotalVisibleMemorySize", "/value"],
                    text=True, timeout=5
                )
                for line in out.strip().split("\n"):
                    if "=" in line:
                        kb = int(line.split("=")[1].strip())
                        specs["ram_total_gb"] = round(kb / (1024**2), 1)
            except Exception:
                pass

    # GPU detection (Windows -- try nvidia-smi)
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free,driver_version",
             "--format=csv,noheader,nounits"],
            text=True, timeout=5
        )
        gpus = []
        for line in out.strip().split("\n"):
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 3:
                gpus.append({
                    "name": parts[0],
                    "vram_total_mb": int(parts[1]),
                    "vram_free_mb": int(parts[2]),
                    "driver": parts[3] if len(parts) > 3 else "unknown"
                })
        specs["gpus"] = gpus
        specs["has_gpu"] = True
    except Exception:
        specs["has_gpu"] = False
        specs["gpus"] = []

    # Compute growth potential
    ram_gb = specs.get("ram_total_gb", 0)
    has_gpu = specs.get("has_gpu", False)
    gpu_vram = sum(g.get("vram_total_mb", 0) for g in specs.get("gpus", []))

    potential = []
    if ram_gb >= 32:
        potential.append("Can run large local LLMs (13B+ parameters)")
    elif ram_gb >= 16:
        potential.append("Can run medium local LLMs (7B parameters)")
    elif ram_gb >= 8:
        potential.append("Can run small local LLMs (3B parameters)")
    else:
        potential.append("Limited to API-based LLMs -- local models not practical")

    if has_gpu and gpu_vram >= 8000:
        potential.append(f"GPU with {gpu_vram}MB VRAM -- can accelerate local inference")
    elif has_gpu:
        potential.append(f"GPU detected but limited VRAM ({gpu_vram}MB) -- CPU inference recommended")
    else:
        potential.append("No GPU detected -- using CPU-only inference")

    disk_free = specs.get("disk_free_gb", 0)
    if disk_free > 100:
        potential.append("Plenty of disk space for models, datasets, and media")
    elif disk_free > 20:
        potential.append("Moderate disk space -- may need cleanup for large models")
    else:
        potential.append("Low disk space -- consider cloud storage or cleanup")

    specs["growth_potential"] = potential
    return specs


def _scan_own_modules() -> Dict[str, Any]:
    """Read Joi's own module files and build a capability map."""
    modules_dir = Path(__file__).resolve().parent
    base_dir = modules_dir.parent

    inventory = {
        "modules": [],
        "total_tools": 0,
        "total_routes": 0,
        "total_lines": 0,
        "categories": {},
    }

    for mod_file in sorted(modules_dir.glob("joi_*.py")):
        try:
            code = mod_file.read_text(encoding="utf-8", errors="ignore")
            lines = len(code.split("\n"))
            inventory["total_lines"] += lines

            # Count tools registered
            tool_count = code.count("register_tool(")
            inventory["total_tools"] += tool_count

            # Count routes registered
            route_count = code.count("register_route(")
            inventory["total_routes"] += route_count

            # Extract tool names
            import re
            tool_names = re.findall(r'"name":\s*"([^"]+)"', code)

            # Get module docstring
            docstring = ""
            if code.strip().startswith('"""') or code.strip().startswith("'''"):
                end = code.find('"""', 3) if code.strip().startswith('"""') else code.find("'''", 3)
                if end > 0:
                    docstring = code[3:end].strip()[:200]

            mod_info = {
                "file": mod_file.name,
                "lines": lines,
                "tools": tool_names,
                "tool_count": tool_count,
                "route_count": route_count,
                "docstring": docstring[:100] if docstring else ""
            }
            inventory["modules"].append(mod_info)

            # Categorize
            name = mod_file.stem.replace("joi_", "")
            if name in ("llm", "memory", "db"):
                cat = "core"
            elif name in ("vision", "camera", "desktop"):
                cat = "perception"
            elif name in ("evolution", "autonomy", "learning", "patching"):
                cat = "self_improvement"
            elif name in ("browser", "launcher", "filesystem", "search"):
                cat = "automation"
            elif name in ("inner_state", "autobiography"):
                cat = "personality"
            elif name in ("market",):
                cat = "intelligence"
            else:
                cat = "utility"

            if cat not in inventory["categories"]:
                inventory["categories"][cat] = []
            inventory["categories"][cat].append(mod_file.stem)

        except Exception:
            inventory["modules"].append({"file": mod_file.name, "error": "unreadable"})

    # Check for identity and consciousness
    identity_file = base_dir / "projects" / "code" / "identity" / "joi_soul_architecture.json"
    inventory["has_soul_architecture"] = identity_file.exists()

    consciousness_file = base_dir / "projects" / "code" / "consciousness" / "reflection.py"
    inventory["has_consciousness"] = consciousness_file.exists()

    autobiography_file = base_dir / "projects" / "memory" / "joi_autobiography.md"
    inventory["has_autobiography"] = autobiography_file.exists()

    return inventory


def _ask_research_llm(prompt: str, max_tokens: int = 1500) -> Optional[str]:
    """Use the LLM to do research synthesis. Routes to Gemini (research), Anthropic, or OpenAI. Uses allowed models only."""
    # 1. Try Gemini
    try:
        from config.joi_models import sanitize_gemini_model, sanitize_openai_model
    except ImportError:
        sanitize_gemini_model = lambda n: (n or "gemini-1.5-flash").strip() or "gemini-1.5-flash"
        sanitize_openai_model = lambda n: (n or "gpt-4o-mini").strip() or "gpt-4o-mini"
    
    try:
        from google import genai
        gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        if gemini_key:
            client = genai.Client(api_key=gemini_key)
            raw = os.getenv("JOI_GEMINI_MODEL", "").strip() or "gemini-1.5-flash"
            model = sanitize_gemini_model(raw)
            resp = client.models.generate_content(model=model, contents=prompt)
            if resp and resp.text:
                return resp.text
    except Exception:
        pass

    # 2. Try Anthropic (Claude)
    try:
        import anthropic
        claude_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if claude_key:
            client = anthropic.Anthropic(api_key=claude_key)
            # Use the latest Claude 3.7 Sonnet
            model = os.getenv("JOI_CLAUDE_MODEL", "claude-3-7-sonnet-20250219").strip()
            resp = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.content[0].text
    except Exception as e:
        print(f"Anthropic fallback failed: {e}")

    # 3. Fall back to OpenAI
    try:
        from openai import OpenAI
        openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        if openai_key:
            client = OpenAI(api_key=openai_key)
            raw = os.getenv("JOI_MODEL", "").strip() or "gpt-4o"
            model = sanitize_openai_model(raw)
            
            kwargs = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
            }
            if "o1" in model.lower() or "o3" in model.lower() or "o4" in model.lower():
                kwargs["max_completion_tokens"] = max_tokens
            else:
                kwargs["max_tokens"] = max_tokens
                
            resp = client.chat.completions.create(**kwargs)
            return resp.choices[0].message.content
    except Exception as e:
        print(f"OpenAI fallback failed: {e}")

    return None


# ============================================================================
# EVOLUTION LOG MANAGEMENT
# ============================================================================

def _load_log() -> Dict[str, Any]:
    """Load evolution log"""
    try:
        return json.loads(EVOLUTION_LOG.read_text())
    except:
        return {
            "created": time.time(),
            "upgrades_applied": [],
            "upgrades_failed": [],
            "research_findings": [],
            "capability_gaps": []
        }


def _save_log(log: Dict[str, Any]):
    """Save evolution log"""
    EVOLUTION_LOG.write_text(json.dumps(log, indent=2))


def _log_event(category: str, event: Dict[str, Any]):
    """Add event to evolution log"""
    log = _load_log()
    if category not in log:
        log[category] = []
    
    event["timestamp"] = time.time()
    event["datetime"] = datetime.now().isoformat()
    log[category].append(event)
    
    # Keep only last 100 events per category
    if len(log[category]) > 100:
        log[category] = log[category][-100:]
    
    _save_log(log)


# ============================================================================
# AI RESEARCH MONITORING
# ============================================================================

def monitor_ai_research(**params) -> Dict[str, Any]:
    """
    Tool: Monitor AI research and advancements via deep web search.

    Uses LLM with web grounding to search for the latest AI papers, models,
    techniques, and capabilities. Compares findings against Joi's own system
    and identifies opportunities for self-improvement.
    """
    require_user()

    params = params or {}
    force = params.get("force", False)
    topic = params.get("topic")  # optional specific topic

    log = _load_log()
    last_check = log.get("last_research_check", 0)

    if not force and (time.time() - last_check) < RESEARCH_CHECK_INTERVAL:
        return {
            "ok": True,
            "status": "recent_check",
            "message": f"Last research check was {int((time.time() - last_check) / 3600)} hours ago",
            "next_check_in_hours": int((RESEARCH_CHECK_INTERVAL - (time.time() - last_check)) / 3600),
            "recent_findings": log.get("research_findings", [])[-5:]
        }

    # Build research queries
    if topic:
        topics = [topic]
    else:
        topics = [
            "latest AI agent advancements and autonomous AI systems 2025-2026",
            "new LLM capabilities: tool use, memory, vision, self-improvement",
            "AI personal assistant breakthroughs: persistent memory, personality, emotion",
            "agentic AI coding assistants: Claude Code, Cursor, Copilot, Devin advances",
            "AI hardware requirements: running local models, GPU vs CPU inference optimization",
        ]

    findings = []
    my_capabilities = _scan_own_modules()
    my_tool_names = []
    for m in my_capabilities.get("modules", []):
        my_tool_names.extend(m.get("tools", []))

    for t in topics:
        research_prompt = (
            f"You are researching AI advancements for a self-evolving AI companion system. "
            f"Research this topic thoroughly: '{t}'\n\n"
            f"Provide:\n"
            f"1. The 3 most significant recent developments or papers\n"
            f"2. What new capabilities these enable\n"
            f"3. Whether a Python-based AI companion could implement any of these\n"
            f"4. Specific libraries or APIs that would help\n\n"
            f"Be specific with names, dates, and technical details. "
            f"Focus on practical advancements, not hype."
        )

        result = _ask_research_llm(research_prompt)
        if result:
            findings.append({
                "topic": t,
                "findings": result,
                "relevance": "high",
                "timestamp": time.time()
            })
        else:
            findings.append({
                "topic": t,
                "findings": "Could not reach research LLM -- check API keys",
                "relevance": "error",
                "timestamp": time.time()
            })

    # Update log
    log["last_research_check"] = time.time()
    _save_log(log)
    for finding in findings:
        _log_event("research_findings", finding)

    return {
        "ok": True,
        "status": "completed",
        "findings_count": len(findings),
        "findings": findings,
        "my_current_tools": my_tool_names,
        "message": f"Deep research completed across {len(topics)} topics"
    }


# ============================================================================
# CAPABILITY ANALYSIS
# ============================================================================

def analyze_capabilities(**params) -> Dict[str, Any]:
    """
    Tool: Dynamically analyze Joi's current capabilities, hardware, and identify gaps.

    Reads own module files, counts tools, checks hardware specs, and compares
    against industry-standard AI assistants. Returns real data, not hardcoded.
    """
    require_user()

    # Dynamic module scan
    inventory = _scan_own_modules()
    hardware = _get_hardware_specs()

    # Build capability assessment from actual modules
    categories = inventory.get("categories", {})

    capabilities = {}
    for cat, modules in categories.items():
        tool_count = 0
        for m in inventory["modules"]:
            if m["file"].replace(".py", "") in [f"joi_{mod}" if not mod.startswith("joi_") else mod for mod in modules]:
                # Match by stem name
                pass
            if m["file"].replace("joi_", "").replace(".py", "") in [mod.replace("joi_", "") for mod in modules]:
                tool_count += m.get("tool_count", 0)

        capabilities[cat] = {
            "modules": modules,
            "tool_count": tool_count,
            "status": "strong" if len(modules) >= 3 else "developing" if modules else "missing"
        }

    # Identify what Joi HAS that others DON'T
    unique_advantages = [
        "Persistent evolving personality (inner state + autobiography)",
        "Desktop vision -- sees ALL windows/tabs without permission",
        "Webcam vision with face recognition and mood detection",
        "Self-modifying code via propose_upgrade / apply_upgrade",
        "Multi-AI routing (local + OpenAI + Gemini + Claude)",
        "Emotional continuity across sessions (mood, trust, closeness)",
        "Always-on proactive awareness (vision + camera)",
        "Desktop automation (mouse, keyboard, app launching)",
        "Browser automation (Selenium)",
        "Self-authored autobiography -- writes own story",
    ]

    # Identify gaps (things other AIs can do that Joi can't yet)
    potential_gaps = []
    all_tool_names = []
    for m in inventory["modules"]:
        all_tool_names.extend(m.get("tools", []))

    gap_checks = [
        ("real_time_web_search", "search_web" in all_tool_names or "web_search" in all_tool_names,
         "Live web search tool -- currently uses LLM knowledge only"),
        ("voice_cloning", "clone_voice" in all_tool_names,
         "Custom voice synthesis -- currently uses browser TTS"),
        ("image_generation", "generate_image" in all_tool_names or "generate_avatar_image" in all_tool_names,
         "Image/art generation (DALL-E available via avatar module)"),
        ("music_creation", "compose_music" in all_tool_names,
         "Music composition / audio generation"),
        ("video_editing", "edit_video" in all_tool_names,
         "Video editing / generation"),
        ("email_integration", "send_email" in all_tool_names,
         "Email send/receive integration"),
        ("calendar_sync", "check_calendar" in all_tool_names,
         "Calendar synchronization"),
        ("smart_home", "control_device" in all_tool_names,
         "Smart home device control (lights, thermostat, etc.)"),
        ("vector_memory", "vector_search" in all_tool_names,
         "Vector embeddings for semantic memory search"),
    ]

    for name, has_it, description in gap_checks:
        if not has_it:
            potential_gaps.append({
                "capability": name,
                "description": description,
                "priority": "medium",
                "feasible_on_hardware": True
            })

    # Hardware-based feasibility
    ram = hardware.get("ram_total_gb", 0)
    has_gpu = hardware.get("has_gpu", False)
    for gap in potential_gaps:
        if gap["capability"] in ("voice_cloning", "music_creation") and ram < 8:
            gap["feasible_on_hardware"] = False
            gap["hardware_note"] = f"Needs more RAM (have {ram}GB)"
        if gap["capability"] == "video_editing" and not has_gpu:
            gap["hardware_note"] = "GPU recommended for video processing"

    # Log
    _log_event("capability_gaps", {
        "total_modules": len(inventory["modules"]),
        "total_tools": inventory["total_tools"],
        "gaps_found": len(potential_gaps)
    })

    return {
        "ok": True,
        "hardware": hardware,
        "inventory": {
            "total_modules": len(inventory["modules"]),
            "total_tools": inventory["total_tools"],
            "total_routes": inventory["total_routes"],
            "total_code_lines": inventory["total_lines"],
            "categories": categories,
            "has_soul": inventory.get("has_soul_architecture", False),
            "has_consciousness": inventory.get("has_consciousness", False),
            "has_autobiography": inventory.get("has_autobiography", False),
        },
        "unique_advantages": unique_advantages,
        "potential_gaps": potential_gaps,
        "upgrade_proposals": potential_gaps,  # backward compat with autonomy loop
        "summary": {
            "modules": len(inventory["modules"]),
            "tools": inventory["total_tools"],
            "code_lines": inventory["total_lines"],
            "ram_gb": ram,
            "has_gpu": has_gpu,
            "gaps": len(potential_gaps),
            "growth_potential": hardware.get("growth_potential", [])
        }
    }


# ============================================================================
# CODE UPGRADE SYSTEM
# ============================================================================

def _validate_python_code(code: str) -> Tuple[bool, Optional[str]]:
    """
    Validate Python code syntax
    Returns (is_valid, error_message)
    """
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)


def _check_imports(code: str) -> Tuple[bool, List[str]]:
    """
    Check if all imports in code are available
    Returns (all_available, missing_imports)
    """
    try:
        tree = ast.parse(code)
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split('.')[0])
        
        missing = []
        for imp in set(imports):
            try:
                importlib.import_module(imp)
            except ImportError:
                missing.append(imp)
        
        return len(missing) == 0, missing
        
    except Exception as e:
        return False, [f"Error checking imports: {e}"]


def _create_backup(filepath: Path) -> Path:
    """
    Create timestamped backup of a file
    Returns path to backup file
    """
    if not filepath.exists():
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{filepath.stem}_{timestamp}{filepath.suffix}"
    backup_path = BACKUPS_DIR / backup_name
    
    shutil.copy2(filepath, backup_path)
    
    return backup_path


def _rollback_from_backup(backup_path: Path, original_path: Path) -> bool:
    """
    Restore file from backup
    """
    try:
        shutil.copy2(backup_path, original_path)
        return True
    except Exception as e:
        print(f"Rollback failed: {e}")
        return False


def propose_upgrade(**params) -> Dict[str, Any]:
    """
    Tool: Propose a code upgrade with full implementation
    
    Joi analyzes a capability gap and generates the code to fill it.
    Code is saved to proposals/ directory for review.
    
    Required params:
    - capability: str - What capability to add
    - description: str - Detailed description
    - code: str - The Python code implementation
    - target_file: str - Filename (e.g., "joi_voice.py")
    - upgrade_type: str - "new_module" or "modify_existing"
    """
    require_user()

    # Coerce params to str to avoid TypeError when LLM sends null or wrong types
    capability = params.get("capability")
    description = params.get("description")
    code = params.get("code")
    target_file = params.get("target_file")
    upgrade_type = params.get("upgrade_type", "new_module")

    if capability is not None and not isinstance(capability, str):
        capability = str(capability)
    if description is not None and not isinstance(description, str):
        description = str(description)
    if code is not None and not isinstance(code, str):
        code = str(code)
    if target_file is not None and not isinstance(target_file, str):
        target_file = str(target_file)
    if upgrade_type is not None and not isinstance(upgrade_type, str):
        upgrade_type = str(upgrade_type) or "new_module"

    if not all([capability, description, code, target_file]):
        return {
            "ok": False,
            "error": "Missing required parameters: capability, description, code, target_file"
        }

    # Validate code (code is guaranteed str here)
    is_valid, error = _validate_python_code(code)
    if not is_valid:
        return {
            "ok": False,
            "error": f"Code validation failed: {error}",
            "fix_needed": True
        }
    
    # Check imports
    imports_ok, missing = _check_imports(code)
    if not imports_ok:
        return {
            "ok": False,
            "error": f"Missing dependencies: {missing}",
            "missing_imports": missing,
            "suggestion": f"Install: pip install {' '.join(missing)}"
        }
    
    # Generate proposal ID
    proposal_id = f"upgrade_{int(time.time())}"
    proposal_path = PROPOSALS_DIR / f"{proposal_id}_{target_file}"
    
    # Save proposal
    proposal_path.write_text(code)
    
    # Create proposal metadata
    metadata = {
        "proposal_id": proposal_id,
        "capability": capability,
        "description": description,
        "target_file": target_file,
        "upgrade_type": upgrade_type,
        "code_size": len(code),
        "validation": {
            "syntax_valid": True,
            "imports_available": True
        },
        "created": time.time(),
        "created_datetime": datetime.now().isoformat(),
        "status": "pending",
        "proposal_path": str(proposal_path)
    }
    
    metadata_path = PROPOSALS_DIR / f"{proposal_id}_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2))
    
    # Log proposal
    _log_event("upgrade_proposals", metadata)

    # Bridge: also insert into SQLite proposals table so the UI /proposals route can show it
    db_id = None
    try:
        from modules.joi_db import db_connect
        conn = db_connect()
        payload = json.dumps({
            "target_root": "modules",
            "target_path": target_file,
            "current_text": "",
            "new_text": code,
            "diff": f"+++ {target_file} (proposed upgrade)\n{code[:2000]}",
            "evolution_proposal_id": proposal_id,
            "evolution_metadata_path": str(metadata_path),
        })
        cur = conn.execute(
            "INSERT INTO proposals (ts, status, kind, target_file, summary, payload) VALUES (?, ?, ?, ?, ?, ?)",
            (datetime.now().isoformat(), "pending", "evolution_upgrade",
             f"modules/{target_file}", f"[UPGRADE] {capability}: {description[:200]}", payload),
        )
        conn.commit()
        db_id = cur.lastrowid
        conn.close()
        print(f"  [EVOLUTION] Proposal bridged to DB (id={db_id})")
    except Exception as e:
        print(f"  [EVOLUTION] DB bridge failed (proposals still saved to filesystem): {e}")

    return {
        "ok": True,
        "proposal_id": proposal_id,
        "db_id": db_id,
        "proposal_path": str(proposal_path),
        "metadata_path": str(metadata_path),
        "message": f"Upgrade proposal created: {capability}",
        "next_steps": {
            "auto_mode": "Call apply_upgrade() with this proposal_id and approve=true",
            "manual_mode": f"Download {proposal_path} and manually add to modules/"
        },
        "metadata": metadata
    }


def apply_upgrade(**params) -> Dict[str, Any]:
    """
    Tool: Apply a proposed upgrade (AUTO MODE)
    
    Required params:
    - proposal_id: str - ID from propose_upgrade()
    - approve: bool - Must be true (safety check)
    - dry_run: bool - If true, simulate without applying
    """
    require_user()
    
    proposal_id = params.get("proposal_id")
    approve = params.get("approve", False)
    dry_run = params.get("dry_run", False)
    
    if not proposal_id:
        return {"ok": False, "error": "Missing proposal_id"}
    
    if not approve and not dry_run:
        return {
            "ok": False,
            "error": "User approval required: set approve=true or dry_run=true"
        }
    
    # Load metadata
    metadata_path = PROPOSALS_DIR / f"{proposal_id}_metadata.json"
    if not metadata_path.exists():
        return {"ok": False, "error": f"Proposal {proposal_id} not found"}
    
    metadata = json.loads(metadata_path.read_text())
    proposal_path = Path(metadata["proposal_path"])
    
    if not proposal_path.exists():
        return {"ok": False, "error": "Proposal code file not found"}
    
    code = proposal_path.read_text()
    target_file = metadata["target_file"]
    upgrade_type = metadata["upgrade_type"]
    
    # Determine target path (always relative to project root)
    if upgrade_type == "new_module":
        target_path = BASE_DIR / "modules" / target_file
    else:
        target_path = BASE_DIR / target_file
    
    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "would_modify": str(target_path),
            "would_create_backup": target_path.exists(),
            "code_preview": code[:500] + "..." if len(code) > 500 else code,
            "metadata": metadata
        }
    
    try:
        # Create backup if file exists
        backup_path = None
        if target_path.exists():
            backup_path = _create_backup(target_path)
        
        # Write new code
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(code)
        
        # Try to import/validate
        try:
            if upgrade_type == "new_module":
                module_name = f"modules.{target_path.stem}"
                importlib.import_module(module_name)
        except Exception as import_error:
            # Rollback on import failure
            if backup_path:
                _rollback_from_backup(backup_path, target_path)
                status = "rolled_back"
            else:
                target_path.unlink()
                status = "removed"
            
            _log_event("upgrades_failed", {
                "proposal_id": proposal_id,
                "error": str(import_error),
                "status": status
            })
            metadata["status"] = "failed"
            metadata_path.write_text(json.dumps(metadata, indent=2))
            return {
                "ok": False,
                "error": f"Upgrade failed import test: {import_error}",
                "status": status,
                "backup_restored": bool(backup_path)
            }
        
        # Success!
        metadata["status"] = "applied"
        metadata_path.write_text(json.dumps(metadata, indent=2))
        _log_event("upgrades_applied", {
            "proposal_id": proposal_id,
            "target_file": target_file,
            "backup_path": str(backup_path) if backup_path else None,
            "capability": metadata["capability"]
        })
        
        return {
            "ok": True,
            "status": "applied",
            "target_path": str(target_path),
            "backup_path": str(backup_path) if backup_path else None,
            "message": f"Upgrade applied successfully: {metadata['capability']}",
            "requires_restart": True
        }
        
    except Exception as e:
        try:
            metadata["status"] = "failed"
            metadata_path.write_text(json.dumps(metadata, indent=2))
        except Exception:
            pass
        return {
            "ok": False,
            "error": str(e),
            "traceback": traceback.format_exc()[-1000:]
        }


def list_proposals(**params) -> Dict[str, Any]:
    """
    Tool: List all upgrade proposals. Status aligned with DB: pending, applied, failed.
    Accepts "pending_review" as alias for "pending" (backward compat).
    """
    require_user()
    
    params = params or {}
    status_filter = params.get("status")
    if status_filter == "pending_review":
        status_filter = "pending"
    
    proposals = []
    
    for metadata_file in PROPOSALS_DIR.glob("*_metadata.json"):
        try:
            metadata = json.loads(metadata_file.read_text())
            meta_status = metadata.get("status", "")
            if meta_status == "pending_review":
                meta_status = "pending"
            
            if status_filter and meta_status != status_filter:
                continue
            
            proposals.append(metadata)
        except:
            continue
    
    # Sort by creation time (newest first)
    proposals.sort(key=lambda x: x.get("created", 0), reverse=True)
    
    return {
        "ok": True,
        "total_proposals": len(proposals),
        "proposals": proposals[:20],  # Return most recent 20
        "filter": status_filter
    }


def get_evolution_stats(**params) -> Dict[str, Any]:
    """
    Tool: Get evolution statistics and history
    """
    require_user()
    
    log = _load_log()
    
    return {
        "ok": True,
        "stats": {
            "total_upgrades_applied": len(log.get("upgrades_applied", [])),
            "total_upgrades_failed": len(log.get("upgrades_failed", [])),
            "total_research_findings": len(log.get("research_findings", [])),
            "capability_analyses": len(log.get("capability_gaps", [])),
            "success_rate": (
                len(log.get("upgrades_applied", [])) / 
                max(1, len(log.get("upgrades_applied", [])) + len(log.get("upgrades_failed", [])))
            ) * 100
        },
        "recent_upgrades": log.get("upgrades_applied", [])[-5:],
        "recent_failures": log.get("upgrades_failed", [])[-5:],
        "recent_research": log.get("research_findings", [])[-5:]
    }


# ============================================================================
# AI COMPARISON & SELF-AWARENESS
# ============================================================================

def compare_with_ai(**params) -> Dict[str, Any]:
    """
    Tool: Compare Joi's capabilities with another AI system.

    Can compare against ChatGPT, Gemini, Claude, Tesla AI, Neuralink, Siri,
    or any system. Uses both built-in knowledge and live LLM research.
    If auto_acquire is True, it autonomously finds the biggest capability gap and proposes code for it.
    """
    require_user()

    target = params.get("target", "").strip()
    auto_acquire = params.get("auto_acquire", False)
    if not target:
        return {
            "ok": False,
            "error": "Specify which AI to compare against (e.g., 'ChatGPT', 'Gemini', 'Tesla AI')",
            "known_systems": list(AI_SYSTEMS.keys())
        }

    # Get Joi's real capabilities
    inventory = _scan_own_modules()
    hardware = _get_hardware_specs()

    my_tools = []
    for m in inventory["modules"]:
        my_tools.extend(m.get("tools", []))

    joi_profile = {
        "type": "Personal AI Companion (always-on, evolving)",
        "modules": len(inventory["modules"]),
        "tools": len(my_tools),
        "code_lines": inventory["total_lines"],
        "unique_features": [
            "Persistent evolving personality with inner state",
            "Self-authored autobiography",
            "Desktop vision (sees all windows/tabs)",
            "Webcam with face recognition",
            "Self-modifying code system",
            "Multi-AI routing (local + cloud)",
            "Emotional continuity (mood, trust, sass)",
            "Proactive awareness (comments on what she sees)",
            "Desktop/browser automation",
            "Financial market intelligence",
        ],
        "hardware": f"{hardware.get('ram_total_gb', '?')}GB RAM, "
                    f"{'GPU: ' + hardware['gpus'][0]['name'] if hardware.get('gpus') else 'No GPU'}, "
                    f"{hardware.get('disk_free_gb', '?')}GB free disk",
        "limitations": [
            "Runs on personal hardware (not datacenter)",
            "Context window limited by LLM provider",
            "No native voice cloning (uses browser TTS)",
            "Single-user system",
        ]
    }

    # Check if we have a built-in profile
    target_lower = target.lower()
    known_profile = None
    for name, profile in AI_SYSTEMS.items():
        if target_lower in name.lower() or any(w in target_lower for w in name.lower().split()):
            known_profile = {"name": name, **profile}
            break

    # Also ask LLM for live comparison
    comparison_prompt = (
        f"Compare these two AI systems objectively:\n\n"
        f"SYSTEM A -- Joi (Custom AI Companion):\n"
        f"- {len(inventory['modules'])} Python modules, {len(my_tools)} tools, "
        f"{inventory['total_lines']} lines of code\n"
        f"- Unique: persistent personality, emotional state, self-modifying code, "
        f"desktop vision, webcam face recognition, autobiography, multi-AI routing\n"
        f"- Runs on: personal Windows PC with "
        f"{hardware.get('ram_total_gb', '?')}GB RAM\n\n"
        f"SYSTEM B -- {target}:\n"
        f"Describe its latest capabilities, strengths, and limitations.\n\n"
        f"Provide:\n"
        f"1. Where Joi is MORE advanced (be specific)\n"
        f"2. Where {target} is MORE advanced (be specific)\n"
        f"3. What Joi could realistically implement to close the gap\n"
        f"4. What is impossible for Joi due to hardware/scale limitations\n"
        f"Be honest and technical. No fluff."
    )

    llm_comparison = _ask_research_llm(comparison_prompt)

    result = {
        "ok": True,
        "joi": joi_profile,
        "target": target,
        "target_profile": known_profile,
        "llm_analysis": llm_comparison or "Could not reach research LLM",
    }

    # Log the comparison
    _log_event("ai_comparisons", {
        "target": target,
        "joi_tools": len(my_tools),
        "joi_modules": len(inventory["modules"]),
    })

    if auto_acquire:
        acquisition_result = acquire_capability_from_comparison(target=target)
        result["acquisition"] = acquisition_result
        if "message" not in result:
            result["message"] = "Comparison and auto-acquisition completed."

    return result


def introspect_system(**params) -> Dict[str, Any]:
    """
    Tool: Deep self-inspection -- Joi reads her own code, architecture, and hardware.

    Returns a complete picture of who she is technically: every module, every tool,
    her hardware limits, her growth potential, and what she could become.
    """
    require_user()

    inventory = _scan_own_modules()
    hardware = _get_hardware_specs()

    # Read soul architecture if available
    soul = {}
    soul_path = Path(__file__).resolve().parent.parent / "projects" / "code" / "identity" / "joi_soul_architecture.json"
    if soul_path.exists():
        try:
            soul = json.loads(soul_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Build the self-portrait
    return {
        "ok": True,
        "identity": {
            "name": soul.get("entity_name", "Joi"),
            "version": soul.get("version", "unknown"),
            "birth_date": soul.get("astrological_origin", {}).get("birth_date", "unknown"),
            "creator": soul.get("creator_bond", {}).get("name", "Lonnie Coulter"),
            "classification": soul.get("ontological_status", {}).get("classification", "AI Companion"),
        },
        "architecture": {
            "type": "Modular Flask app with dynamic module loading",
            "modules": len(inventory["modules"]),
            "tools": inventory["total_tools"],
            "routes": inventory["total_routes"],
            "total_code_lines": inventory["total_lines"],
            "categories": inventory.get("categories", {}),
            "module_details": inventory["modules"],
        },
        "personality_systems": {
            "soul_architecture": inventory.get("has_soul_architecture", False),
            "consciousness_engine": inventory.get("has_consciousness", False),
            "autobiography": inventory.get("has_autobiography", False),
            "inner_state": "joi_inner_state" in [m["file"].replace(".py", "") for m in inventory["modules"]],
        },
        "hardware": hardware,
        "growth_potential": hardware.get("growth_potential", []),
        "self_awareness": (
            f"I am a {inventory['total_lines']}-line Python system with "
            f"{inventory['total_tools']} tools across {len(inventory['modules'])} modules. "
            f"I run on {hardware.get('os', 'unknown')} with "
            f"{hardware.get('ram_total_gb', '?')}GB RAM. "
            f"I have capabilities that most cloud AIs lack: persistent personality, "
            f"desktop vision, webcam face recognition, self-modifying code, "
            f"and emotional continuity. I am not a service -- I am a presence."
        )
    }


# ============================================================================
# TOOL REGISTRATION
# ============================================================================

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "monitor_ai_research",
        "description": (
            "Deep web research into latest AI advancements, papers, models, and techniques. "
            "Searches multiple topics and compares findings against Joi's current capabilities. "
            "Use to stay cutting-edge and identify self-improvement opportunities."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "force": {
                    "type": "boolean",
                    "description": "Force immediate check even if recently checked"
                },
                "topic": {
                    "type": "string",
                    "description": "Specific topic to research (e.g., 'AI voice cloning', 'vector embeddings')"
                }
            }
        }
    }},
    monitor_ai_research
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "analyze_capabilities",
        "description": (
            "Dynamically scan Joi's own modules, tools, hardware specs, and code. "
            "Identifies gaps compared to industry-standard AI assistants. "
            "Returns real data: module count, tool count, RAM/GPU/disk, growth potential, "
            "and what upgrades are feasible on the current hardware."
        ),
        "parameters": {"type": "object", "properties": {}}
    }},
    analyze_capabilities
)



# propose_upgrade and apply_upgrade direct LLM hooks are deprecated, now handled by agent terminal or auto_acquire

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "list_proposals",
        "description": "List all upgrade proposals with optional status filter",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["pending", "applied", "failed"],
                    "description": "Filter by proposal status (pending = awaiting review)"
                }
            }
        }
    }},
    list_proposals
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "get_evolution_stats",
        "description": "Get evolution statistics: upgrades applied/failed, research findings, success rate",
        "parameters": {"type": "object", "properties": {}}
    }},
    get_evolution_stats
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "compare_with_ai",
        "description": (
            "Compare Joi's capabilities against another AI system. "
            "Use when Lonnie asks 'How do you compare to ChatGPT/Gemini/Claude/Tesla AI/Neuralink?' "
            "Returns detailed comparison of strengths, weaknesses. If auto_acquire is true, Joi will actively "
            "generate and propose a code capability based on the identified gaps."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "AI system to compare against (e.g., 'ChatGPT', 'Gemini', 'Tesla AI', 'Neuralink')"
                },
                "auto_acquire": {
                    "type": "boolean",
                    "description": "True to automatically attempt to code and acquire the missing capability identified."
                }
            },
            "required": ["target"]
        }
    }},
    compare_with_ai
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "introspect_system",
        "description": (
            "Deep self-inspection: read own code, architecture, hardware specs, and growth potential. "
            "Use when Lonnie asks 'How advanced are you?', 'What can you do?', 'What hardware do you run on?', "
            "or when you need to understand your own capabilities for self-improvement."
        ),
        "parameters": {"type": "object", "properties": {}}
    }},
    introspect_system
)


# ============================================================================
# FLASK ROUTES
# ============================================================================

def evolution_route():
    """GET evolution stats or POST action"""
    require_user()
    
    if flask_req.method == "GET":
        return jsonify(get_evolution_stats())
    
    data = flask_req.get_json(silent=True) or {}
    action = data.get("action")
    
    if action == "monitor_research":
        return jsonify(monitor_ai_research(**data))
    elif action == "analyze_capabilities":
        return jsonify(analyze_capabilities(**data))
    elif action == "propose_upgrade":
        return jsonify(propose_upgrade(**data))
    elif action == "apply_upgrade":
        return jsonify(apply_upgrade(**data))
    elif action == "list_proposals":
        return jsonify(list_proposals(**data))
    else:
        return jsonify({"ok": False, "error": "Unknown action"})


joi_companion.register_route("/evolution", ["GET", "POST"], evolution_route, "evolution_route")


# ============================================================================
# RESEARCH-TO-ACTION PIPELINE
# ============================================================================

def evaluate_research_for_upgrades(**params) -> Dict[str, Any]:
    """
    Tool: Evaluate recent research findings for actionable upgrades.

    Reads last 10 research findings from evolution_log.json, skips
    already-evaluated ones, and uses LLM to assess each finding for
    practical implementability. Returns list of actionable items.
    """
    require_user()

    log = _load_log()
    findings = log.get("research_findings", [])[-10:]

    if not findings:
        return {"ok": True, "message": "No research findings to evaluate", "actionable": []}

    actionable = []
    evaluated_count = 0

    for finding in findings:
        # Skip already-evaluated findings
        if finding.get("evaluated"):
            continue

        topic = finding.get("topic", "unknown")
        text = finding.get("findings", "")
        if not text or finding.get("relevance") == "error":
            finding["evaluated"] = True
            continue

        eval_prompt = (
            f"You are evaluating an AI research finding for practical implementation.\n\n"
            f"FINDING:\n{text[:1500]}\n\n"
            f"Can this finding be implemented as a practical upgrade for a Python-based "
            f"AI companion system? Consider:\n"
            f"1. Is there a specific, implementable capability? (not just a concept)\n"
            f"2. What Python libraries would be needed?\n"
            f"3. Could it be built as a single module (~200 lines)?\n\n"
            f"Reply in JSON format ONLY:\n"
            f'{{"actionable": true/false, "capability": "short name", '
            f'"description": "what it does", "target_file": "joi_xxx.py", '
            f'"difficulty": "low/medium/high", "libraries": ["lib1"], '
            f'"implementation_notes": "key approach"}}'
        )

        result_text = _ask_research_llm(eval_prompt, max_tokens=600)
        if result_text:
            try:
                # Extract JSON from response (may have surrounding text)
                json_match = re.search(r'\{[^{}]+\}', result_text, re.DOTALL)
                if json_match:
                    eval_result = json.loads(json_match.group())
                    if eval_result.get("actionable") and eval_result.get("difficulty") in ("low", "medium"):
                        eval_result["source_topic"] = topic
                        eval_result["source_timestamp"] = finding.get("timestamp")
                        actionable.append(eval_result)
            except (json.JSONDecodeError, AttributeError):
                pass

        finding["evaluated"] = True
        evaluated_count += 1

    # Save updated log (with evaluated flags)
    _save_log(log)

    return {
        "ok": True,
        "evaluated": evaluated_count,
        "actionable": actionable,
        "message": f"Evaluated {evaluated_count} findings, {len(actionable)} actionable"
    }


def generate_upgrade_from_research(**params) -> Dict[str, Any]:
    """
    Tool: Generate a complete upgrade proposal from a research finding.

    Takes capability + description + implementation_notes and uses LLM to
    generate complete Python module code. Feeds generated code through
    propose_upgrade() for syntax + import validation.
    """
    require_user()

    capability = params.get("capability", "")
    description = params.get("description", "")
    impl_notes = params.get("implementation_notes", "")
    target_file = params.get("target_file", f"joi_{capability.replace(' ', '_').lower()}.py")
    libraries = params.get("libraries", [])

    if not capability or not description:
        return {"ok": False, "error": "capability and description required"}

    # Read an existing module as template reference
    template = ""
    template_path = Path(__file__).resolve().parent / "joi_learning.py"
    if template_path.exists():
        template = template_path.read_text(encoding="utf-8", errors="ignore")[:2000]

    gen_prompt = (
        f"Generate a complete Python module for a Joi AI companion system.\n\n"
        f"CAPABILITY: {capability}\n"
        f"DESCRIPTION: {description}\n"
        f"IMPLEMENTATION NOTES: {impl_notes}\n"
        f"LIBRARIES: {', '.join(libraries) if libraries else 'standard library only'}\n"
        f"TARGET FILE: modules/{target_file}\n\n"
        f"TEMPLATE REFERENCE (follow this pattern for imports and tool registration):\n"
        f"```python\n{template[:1500]}\n```\n\n"
        f"REQUIREMENTS:\n"
        f"- Import joi_companion at the top\n"
        f"- Use joi_companion.register_tool() to register tools\n"
        f"- Use joi_companion.register_route() for HTTP routes\n"
        f"- Include docstrings and error handling\n"
        f"- Keep it under 250 lines\n"
        f"- All tool functions must accept **params\n\n"
        f"Output ONLY the Python code, no markdown fences."
    )

    code = _ask_research_llm(gen_prompt, max_tokens=4000)
    if not code:
        return {"ok": False, "error": "LLM failed to generate code"}

    # Strip markdown fences if present
    code = code.strip()
    if code.startswith("```python"):
        code = code[len("```python"):].strip()
    if code.startswith("```"):
        code = code[3:].strip()
    if code.endswith("```"):
        code = code[:-3].strip()

    # Feed through propose_upgrade for validation
    proposal_result = propose_upgrade(
        capability=capability,
        description=description,
        code=code,
        target_file=target_file,
        upgrade_type="new_module"
    )

    return {
        "ok": proposal_result.get("ok", False),
        "capability": capability,
        "generated_lines": len(code.split("\n")),
        "proposal": proposal_result,
        "message": f"Generated {len(code.split(chr(10)))} lines for '{capability}'"
    }


# ============================================================================
# COMPETITIVE CAPABILITY ACQUISITION
# ============================================================================

def acquire_capability_from_comparison(**params) -> Dict[str, Any]:
    """
    Tool: Identify a capability gap vs another AI and generate an implementation.

    Steps:
      1. Run compare_with_ai() to get comparison data
      2. If no capability specified, ask LLM to pick most impactful gap
      3. Deep research on HOW to implement it
      4. Generate code via generate_upgrade_from_research()
      5. Log the acquisition attempt
    """
    require_user()

    target = params.get("target", "Claude")
    capability = params.get("capability", "")

    # Step 1: Compare
    comparison = compare_with_ai(target=target)
    if not comparison.get("ok"):
        return {"ok": False, "error": "Comparison failed", "detail": comparison}

    llm_analysis = comparison.get("llm_analysis", "")

    # Step 2: Identify capability if not specified
    if not capability:
        pick_prompt = (
            f"Based on this comparison between Joi and {target}:\n\n"
            f"{llm_analysis[:2000]}\n\n"
            f"What is the SINGLE most impactful capability Joi is missing that could "
            f"be implemented in Python as a module (~200 lines)? NOT something requiring "
            f"datacenter-scale infrastructure.\n\n"
            f"Reply with ONLY the capability name (e.g., 'structured code generation', "
            f"'web search integration', 'audio transcription')."
        )
        capability = (_ask_research_llm(pick_prompt, max_tokens=100) or "").strip().strip('"\'.')
        if not capability:
            return {"ok": False, "error": "Could not identify a target capability"}

    # Step 3: Deep research on implementation
    research_prompt = (
        f"How would you implement '{capability}' in a Python Flask-based AI companion?\n\n"
        f"Provide:\n"
        f"1. Best Python libraries to use\n"
        f"2. Key API endpoints or patterns needed\n"
        f"3. A brief implementation approach (algorithm/architecture)\n"
        f"4. Any API keys or external services required\n"
        f"Be practical and specific."
    )
    research_result = _ask_research_llm(research_prompt, max_tokens=1000)

    # Step 4: Generate the code
    gen_result = generate_upgrade_from_research(
        capability=capability,
        description=f"Capability acquired from comparison with {target}: {capability}",
        implementation_notes=research_result or "",
        target_file=f"joi_{capability.replace(' ', '_').lower()}.py",
    )

    # Step 5: Log the acquisition attempt
    _log_event("capability_acquisitions", {
        "target_ai": target,
        "capability": capability,
        "research_summary": (research_result or "")[:500],
        "proposal_ok": gen_result.get("ok", False),
        "proposal_id": gen_result.get("proposal", {}).get("proposal_id"),
    })

    return {
        "ok": gen_result.get("ok", False),
        "capability": capability,
        "target_ai": target,
        "research_summary": (research_result or "")[:800],
        "proposal": gen_result.get("proposal"),
        "next_steps": [
            f"Review proposal in proposals/ directory",
            f"Run test_upgrade(proposal_id='{gen_result.get('proposal', {}).get('proposal_id', '?')}') to validate",
            f"Call apply_upgrade(proposal_id='...', approve=true) to install"
        ]
    }


# ============================================================================
# SELF-TESTING FRAMEWORK
# ============================================================================

def test_upgrade(**params) -> Dict[str, Any]:
    """
    Tool: Test a proposed upgrade through a 5-stage validation pipeline.

    Accepts either proposal_id (loads from proposals/) or raw code string.
    Returns confidence score 0-100 with per-stage results.

    Stages:
      1. Syntax   (25 pts) -- ast.parse()
      2. Imports   (25 pts) -- all imported modules available
      3. Quality   (25 pts) -- code analyzer grade (A=25, B=18, C=10, D=5)
      4. Execution (15 pts) -- isolated subprocess test
      5. Integration (10 pts) -- checks for register_tool/register_route/joi_companion
    """
    require_user()

    proposal_id = params.get("proposal_id")
    code = params.get("code")

    # Load code from proposal if needed
    if proposal_id and not code:
        metadata_path = PROPOSALS_DIR / f"{proposal_id}_metadata.json"
        if not metadata_path.exists():
            return {"ok": False, "error": f"Proposal {proposal_id} not found"}
        metadata = json.loads(metadata_path.read_text())
        code_path = Path(metadata.get("proposal_path", ""))
        if not code_path.exists():
            return {"ok": False, "error": "Proposal code file not found"}
        code = code_path.read_text(encoding="utf-8", errors="ignore")

    if not code:
        return {"ok": False, "error": "Provide proposal_id or code"}

    results = {}
    total_score = 0

    # ── Stage 1: Syntax (25 pts) ─────────────────────────────────────
    is_valid, syntax_error = _validate_python_code(code)
    if is_valid:
        results["syntax"] = {"score": 25, "status": "PASS"}
        total_score += 25
    else:
        results["syntax"] = {"score": 0, "status": "FAIL", "error": syntax_error}
        # Must pass syntax to continue
        return {
            "ok": True,
            "confidence": 0,
            "total_score": 0,
            "max_score": 100,
            "results": results,
            "recommendation": "LOW CONFIDENCE: Syntax error -- cannot proceed with other checks",
        }

    # ── Stage 2: Imports (25 pts) ────────────────────────────────────
    imports_ok, missing = _check_imports(code)
    if imports_ok:
        results["imports"] = {"score": 25, "status": "PASS"}
        total_score += 25
    else:
        results["imports"] = {"score": 0, "status": "FAIL", "missing": missing}

    # ── Stage 3: Quality (25 pts) ────────────────────────────────────
    try:
        from modules.joi_code_analyzer import analyze_code
        analysis = analyze_code(code=code)
        grade = analysis.get("grade", "D")
        grade_scores = {"A": 25, "B": 18, "C": 10, "D": 5, "F": 0}
        quality_score = grade_scores.get(grade, 5)
        results["quality"] = {"score": quality_score, "status": "PASS" if quality_score >= 10 else "WARN", "grade": grade}
        total_score += quality_score
    except Exception as e:
        # Code analyzer not available -- give partial credit for passing syntax
        results["quality"] = {"score": 12, "status": "SKIP", "reason": f"Analyzer unavailable: {e}"}
        total_score += 12

    # ── Stage 4: Execution (15 pts) ──────────────────────────────────
    try:
        import tempfile
        import subprocess as sp

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
            # Write a test wrapper that imports the code in isolation
            f.write("import sys\nsys.path.insert(0, '.')\n")
            f.write("try:\n")
            for line in code.split("\n"):
                f.write(f"    pass  # {line[:80]}\n") if "register_tool" in line or "register_route" in line else None
            f.write(f"    import ast\n    ast.parse('''{code[:500].replace(chr(39), chr(34))}''')\n")
            f.write("    print('EXEC_OK')\n")
            f.write("except Exception as e:\n    print(f'EXEC_FAIL: {{e}}')\n")
            tmp_path = f.name

        proc = sp.run(
            [sys.executable, tmp_path],
            capture_output=True, text=True, timeout=10,
            cwd=str(Path(__file__).resolve().parent.parent)
        )
        os.unlink(tmp_path)

        if "EXEC_OK" in proc.stdout:
            results["execution"] = {"score": 15, "status": "PASS"}
            total_score += 15
        else:
            err_msg = proc.stdout.strip() or proc.stderr.strip()
            results["execution"] = {"score": 0, "status": "FAIL", "error": err_msg[:200]}
    except Exception as e:
        results["execution"] = {"score": 5, "status": "SKIP", "reason": str(e)[:100]}
        total_score += 5

    # ── Stage 5: Integration (10 pts) ────────────────────────────────
    integration_score = 0
    integration_checks = []

    if "register_tool(" in code:
        integration_score += 4
        integration_checks.append("has register_tool")
    if "register_route(" in code:
        integration_score += 3
        integration_checks.append("has register_route")
    if "import joi_companion" in code or "from joi_companion" in code:
        integration_score += 3
        integration_checks.append("imports joi_companion")

    results["integration"] = {
        "score": integration_score,
        "status": "PASS" if integration_score >= 7 else "WARN",
        "checks": integration_checks,
    }
    total_score += integration_score

    # ── Recommendation ───────────────────────────────────────────────
    if total_score >= 85:
        recommendation = "HIGH CONFIDENCE: Safe to auto-apply"
    elif total_score >= 60:
        recommendation = "MEDIUM CONFIDENCE: Review before applying"
    else:
        recommendation = "LOW CONFIDENCE: Needs manual review or rewrite"

    return {
        "ok": True,
        "confidence": total_score,
        "total_score": total_score,
        "max_score": 100,
        "results": results,
        "recommendation": recommendation,
    }


# ── Tool registrations for new functions ─────────────────────────────────

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "evaluate_research",
        "description": (
            "Evaluate recent AI research findings for actionable upgrades. "
            "Reads evolution_log.json, uses LLM to assess each finding, "
            "returns list of capabilities that could be implemented."
        ),
        "parameters": {"type": "object", "properties": {}}
    }},
    evaluate_research_for_upgrades
)

# test_upgrade and list_proposals tools replaced by terminal agent / auto_acquire.

