"""
modules/joi_skill_synthesis.py

Skill Synthesis & Lifelong Learning -- Voyager-style skill library
=================================================================

Allows Joi to:
  - Compose multiple tools into multi-step workflows (skills)
  - Remember and reuse proven tool sequences
  - Self-correct recurring failures
  - Generate practice goals from weak areas
  - Bridge vision observations to logic/diagnosis actions
  - Auto-capture successful tool chains from chat

Data files (auto-created in data/):
  - skill_library.json   -- Proven tool compositions
  - skill_goals.json     -- Practice goals from weak areas
  - self_correction_log.json -- Recurring failure patterns + fixes
"""

import json
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import joi_companion
from flask import jsonify, request as flask_req

# ── Paths ────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

SKILL_LIBRARY_PATH = DATA_DIR / "skill_library.json"
SKILL_GOALS_PATH = DATA_DIR / "skill_goals.json"
SELF_CORRECTION_PATH = DATA_DIR / "self_correction_log.json"

MAX_SKILLS = 500
MAX_GOALS = 20
MAX_CORRECTIONS = 100

# ══════════════════════════════════════════════════════════════════════════
# 1A. DATA STRUCTURES -- Load / Save helpers
# ══════════════════════════════════════════════════════════════════════════

def _load_json(path: Path, default: Any = None) -> Any:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  [SKILL] Load error {path.name}: {e}")
    return default if default is not None else {}


def _save_json(path: Path, data: Any):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    except Exception as e:
        print(f"  [SKILL] Save error {path.name}: {e}")


SKILL_CACHE_TTL: float = 45.0
_skill_library_cache: Optional[Dict] = None
_skill_library_ts: float = 0
_goals_cache: Optional[Dict] = None
_goals_cache_ts: float = 0
_corrections_cache: Optional[Dict] = None
_corrections_cache_ts: float = 0


def _load_skill_library() -> Dict:
    global _skill_library_cache, _skill_library_ts
    now = time.time()
    if _skill_library_cache is not None and (now - _skill_library_ts) < SKILL_CACHE_TTL:
        return _skill_library_cache
    default = {"version": 1, "skills": {}, "stats": {"total_skills": 0, "total_executions": 0, "total_successes": 0}}
    lib = _load_json(SKILL_LIBRARY_PATH, default)
    if "skills" not in lib:
        lib["skills"] = {}
    if "stats" not in lib:
        lib["stats"] = {"total_skills": 0, "total_executions": 0, "total_successes": 0}
    _skill_library_cache = lib
    _skill_library_ts = now
    return lib


def _save_skill_library(lib: Dict):
    global _skill_library_cache
    skills = lib.get("skills", {})
    if len(skills) > MAX_SKILLS:
        sorted_skills = sorted(skills.items(), key=lambda x: x[1].get("last_used", 0))
        to_remove = len(skills) - MAX_SKILLS
        for sid, _ in sorted_skills[:to_remove]:
            del skills[sid]
    lib["stats"]["total_skills"] = len(skills)
    _save_json(SKILL_LIBRARY_PATH, lib)
    _skill_library_cache = None  # invalidate so next load is fresh


def _load_goals() -> Dict:
    global _goals_cache, _goals_cache_ts
    now = time.time()
    if _goals_cache is not None and (now - _goals_cache_ts) < SKILL_CACHE_TTL:
        return _goals_cache
    default = {"active_goals": [], "completed_goals": [], "last_goal_generation": None}
    _goals_cache = _load_json(SKILL_GOALS_PATH, default)
    _goals_cache_ts = now
    return _goals_cache


def _save_goals(goals: Dict):
    global _goals_cache
    if len(goals.get("active_goals", [])) > MAX_GOALS:
        goals["active_goals"] = goals["active_goals"][:MAX_GOALS]
    if len(goals.get("completed_goals", [])) > 50:
        goals["completed_goals"] = goals["completed_goals"][-50:]
    _save_json(SKILL_GOALS_PATH, goals)
    _goals_cache = None  # invalidate so next load is fresh


def _load_corrections() -> Dict:
    global _corrections_cache, _corrections_cache_ts
    now = time.time()
    if _corrections_cache is not None and (now - _corrections_cache_ts) < SKILL_CACHE_TTL:
        return _corrections_cache
    default = {"patterns_detected": [], "fixes_applied": [], "last_review": None}
    _corrections_cache = _load_json(SELF_CORRECTION_PATH, default)
    _corrections_cache_ts = now
    return _corrections_cache


def _save_corrections(corr: Dict):
    global _corrections_cache
    if len(corr.get("patterns_detected", [])) > MAX_CORRECTIONS:
        corr["patterns_detected"] = corr["patterns_detected"][-MAX_CORRECTIONS:]
    if len(corr.get("fixes_applied", [])) > 50:
        corr["fixes_applied"] = corr["fixes_applied"][-50:]
    _save_json(SELF_CORRECTION_PATH, corr)
    _corrections_cache = None  # invalidate so next load is fresh


def record_self_correction(previous_reply: str, user_correction: str) -> None:
    """
    Record a user correction (e.g. "No, ..." / "Actually, ...") for self-correction learning.
    Appends to fixes_applied so the system can learn from mistakes.
    """
    corr = _load_corrections()
    fixes = corr.get("fixes_applied", [])
    fixes.append({
        "ts": datetime.now().isoformat(),
        "type": "user_correction",
        "previous_reply": previous_reply[:500],
        "user_correction": user_correction[:500],
    })
    corr["fixes_applied"] = fixes[-50:]  # keep last 50
    corr["last_review"] = datetime.now().isoformat()
    _save_corrections(corr)


# ══════════════════════════════════════════════════════════════════════════
# 1B. SKILL LIBRARY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════

def save_skill(
    name: str,
    description: str,
    tool_sequence: List[Dict],
    domain_tags: List[str],
    variables: Optional[List[str]] = None,
    source: str = "manual",
    confidence: int = 75,
    prompt_snippet: Optional[str] = None,
) -> Dict:
    """Save a proven tool composition to the skill library + vector memory.
    prompt_snippet: optional system-prompt text for DPO-discovered behavioral skills."""
    lib = _load_skill_library()
    ts = int(time.time())
    skill_id = f"skill_{ts}"

    # Dedup: check if a skill with same name or very similar tool sequence exists
    for sid, existing in lib["skills"].items():
        if existing["name"].lower() == name.lower():
            # Update existing instead of creating duplicate
            existing["tool_sequence"] = tool_sequence
            existing["description"] = description
            existing["domain_tags"] = domain_tags
            existing["confidence"] = max(existing.get("confidence", 0), confidence)
            if prompt_snippet is not None:
                existing["prompt_snippet"] = prompt_snippet
            existing["last_used"] = time.time()
            _save_skill_library(lib)
            _save_skill_to_vector(existing)
            return {"ok": True, "skill_id": sid, "action": "updated", "skill": existing}

        # Check tool sequence overlap
        existing_tools = [s.get("tool") for s in existing.get("tool_sequence", [])]
        new_tools = [s.get("tool") for s in tool_sequence]
        if existing_tools == new_tools and len(existing_tools) > 0:
            existing["name"] = name
            existing["description"] = description
            existing["confidence"] = max(existing.get("confidence", 0), confidence)
            existing["last_used"] = time.time()
            _save_skill_library(lib)
            _save_skill_to_vector(existing)
            return {"ok": True, "skill_id": sid, "action": "merged", "skill": existing}

    # Create new skill (prompt_snippet optional, for DPO-discovered behavioral skills)
    skill = {
        "id": skill_id,
        "name": name,
        "description": description,
        "domain_tags": domain_tags or [],
        "tool_sequence": tool_sequence,
        "variables": variables or [],
        "success_count": 0,
        "fail_count": 0,
        "last_used": time.time(),
        "created": time.time(),
        "source": source,
        "confidence": confidence,
    }
    if prompt_snippet is not None:
        skill["prompt_snippet"] = prompt_snippet
    lib["skills"][skill_id] = skill
    _save_skill_library(lib)
    _save_skill_to_vector(skill)
    return {"ok": True, "skill_id": skill_id, "action": "created", "skill": skill}


def _save_skill_to_vector(skill: Dict):
    """Save skill to vector memory for semantic retrieval."""
    try:
        from modules.memory.memory_manager import save_memory
        snippet = skill.get("prompt_snippet", "")
        text = f"Skill: {skill['name']}. {skill['description']}. Tools: {', '.join(s.get('tool','') for s in skill.get('tool_sequence',[]))}. Tags: {', '.join(skill.get('domain_tags',[]))}"
        if snippet:
            text += f" Snippet: {snippet}"
        save_memory(text, namespace="skills", metadata={"skill_id": skill["id"]})
    except Exception as e:
        print(f"  [SKILL] Vector save failed: {e}")


# ── DPO-driven skill discovery (emergent skill library) ─────────────────────
DISCOVERY_MIN_POSITIVE_COUNT = 3
_last_discovery_run: float = 0
DISCOVERY_COOLDOWN_SEC = 300  # 5 min


def _normalize_user_preview(text: str, max_len: int = 60) -> str:
    """Normalize user message for grouping (lowercase, collapse whitespace, truncate)."""
    if not text:
        return ""
    t = " ".join(str(text).lower().split())
    return t[:max_len]


def discover_skills_from_dpo() -> Dict[str, Any]:
    """
    Scan DPO signal_log for repeated high-preference interactions (e.g. praise, positive deltas).
    If the same interaction type (normalized user_preview) happens >= DISCOVERY_MIN_POSITIVE_COUNT
    times, create a skill with a system prompt snippet so the AI 'levels up' from usage.
    """
    global _last_discovery_run
    now = time.time()
    if now - _last_discovery_run < DISCOVERY_COOLDOWN_SEC:
        return {"ok": True, "action": "cooldown", "created": 0}
    _last_discovery_run = now

    try:
        from modules.joi_dpo import _load_dpo
        data = _load_dpo()
    except Exception as e:
        print(f"  [SKILL] DPO load failed: {e}")
        return {"ok": False, "error": str(e), "created": 0}

    signals = data.get("signal_log", [])
    # High preference = praise or positive delta
    positive = [
        s for s in signals
        if s.get("signal") == "praise" or (isinstance(s.get("delta"), (int, float)) and s.get("delta", 0) > 0)
    ]
    if len(positive) < DISCOVERY_MIN_POSITIVE_COUNT:
        return {"ok": True, "action": "insufficient_signals", "created": 0}

    # Group by normalized user_preview
    pattern_counts: Dict[str, List[Dict]] = {}
    for entry in positive:
        preview = entry.get("user_preview") or entry.get("trigger") or ""
        pattern = _normalize_user_preview(preview)
        if not pattern or len(pattern) < 4:
            continue
        pattern_counts.setdefault(pattern, []).append(entry)

    lib = _load_skill_library()
    existing_patterns = {
        s.get("dpo_pattern") for s in lib.get("skills", {}).values()
        if s.get("source") == "dpo_discovery" and s.get("dpo_pattern")
    }

    created = 0
    for pattern, entries in pattern_counts.items():
        if len(entries) < DISCOVERY_MIN_POSITIVE_COUNT or pattern in existing_patterns:
            continue
        existing_patterns.add(pattern)
        name = f"User preference: {pattern[:40]}{'…' if len(pattern) > 40 else ''}"
        description = "User has responded positively multiple times when Joi handled requests like this."
        prompt_snippet = (
            f"When the user asks for something like \"{pattern}\", they have responded positively before; "
            "prefer a similar approach and style."
        )
        result = save_skill(
            name=name,
            description=description,
            tool_sequence=[],
            domain_tags=["dpo_discovery", "user_preference"],
            source="dpo_discovery",
            confidence=min(90, 70 + len(entries) * 5),
            prompt_snippet=prompt_snippet,
        )
        if result.get("action") in ("created", "updated"):
            created += 1
            # Store dpo_pattern on skill so we don't re-create for same pattern
            sid = result.get("skill_id")
            if sid:
                lib = _load_skill_library()
                if sid in lib.get("skills", {}):
                    lib["skills"][sid]["dpo_pattern"] = pattern
                    _save_skill_library(lib)

    return {"ok": True, "action": "discovery", "created": created}


def find_skills(query: str, top_k: int = 5) -> List[Dict]:
    """Search skill library semantically via vector memory, then load full details."""
    results = []

    # 1. Try vector memory semantic search
    try:
        from modules.memory.memory_manager import recall_memory
        hits = recall_memory(query, namespace="skills", top_k=top_k)
        if hits and isinstance(hits, list):
            lib = _load_skill_library()
            for hit in hits:
                meta = hit.get("metadata", {}) if isinstance(hit, dict) else {}
                sid = meta.get("skill_id", "")
                if sid and sid in lib["skills"]:
                    results.append(lib["skills"][sid])
    except Exception as e:
        print(f"  [SKILL] Vector search failed ({e}), falling back to keyword")

    # 2. Keyword fallback if vector returned nothing
    if not results:
        lib = _load_skill_library()
        query_lower = query.lower()
        query_words = set(query_lower.split())
        scored = []
        for sid, skill in lib["skills"].items():
            score = 0
            name_lower = skill.get("name", "").lower()
            desc_lower = skill.get("description", "").lower()
            tags = [t.lower() for t in skill.get("domain_tags", [])]

            # Name match
            for w in query_words:
                if w in name_lower:
                    score += 3
                if w in desc_lower:
                    score += 1
                if w in tags:
                    score += 2

            if score > 0:
                scored.append((score, skill))

        scored.sort(key=lambda x: -x[0])
        results = [s[1] for s in scored[:top_k]]

    return results


def increment_skill_usage(skill_id: str, success: bool):
    """Update usage counters for a skill."""
    lib = _load_skill_library()
    if skill_id in lib["skills"]:
        skill = lib["skills"][skill_id]
        if success:
            skill["success_count"] = skill.get("success_count", 0) + 1
            lib["stats"]["total_successes"] = lib["stats"].get("total_successes", 0) + 1
        else:
            skill["fail_count"] = skill.get("fail_count", 0) + 1
        skill["last_used"] = time.time()
        lib["stats"]["total_executions"] = lib["stats"].get("total_executions", 0) + 1
        _save_skill_library(lib)


# ══════════════════════════════════════════════════════════════════════════
# 1C. SKILL SYNTHESIS ENGINE
# ══════════════════════════════════════════════════════════════════════════

def synthesize_skill(**kwargs) -> Dict:
    """
    TOOL: Decompose a complex request into sub-tasks, compose tools, execute, save.
    Params: request (str), dry_run (bool, default False)
    """
    request_text = kwargs.get("request", "")
    dry_run = kwargs.get("dry_run", False)

    if not request_text:
        return {"ok": False, "error": "No request provided"}

    # 1. Check if we already have a matching skill
    existing = find_skills(request_text, top_k=3)
    if existing:
        best = existing[0]
        if best.get("confidence", 0) >= 70 and best.get("success_count", 0) > 0:
            if not dry_run:
                result = _execute_plan(best.get("tool_sequence", []), {"request": request_text})
                increment_skill_usage(best["id"], result.get("success", False))
                return {
                    "ok": True,
                    "source": "skill_library",
                    "skill_name": best["name"],
                    "skill_id": best["id"],
                    "execution": result,
                }
            else:
                return {
                    "ok": True,
                    "source": "skill_library",
                    "skill_name": best["name"],
                    "dry_run": True,
                    "plan": best.get("tool_sequence", []),
                }

    # 2. Decompose request into sub-tasks
    subtasks = _decompose_request(request_text)
    if not subtasks:
        return {"ok": False, "error": "Could not decompose request into actionable steps"}

    # 3. Find tools for each sub-task
    plan = []
    for i, subtask in enumerate(subtasks):
        tool_match = _find_tool_for_subtask(subtask)
        step = {
            "step": i + 1,
            "description": subtask.get("description", ""),
            "tool": tool_match.get("tool_name") if tool_match else None,
            "params_template": tool_match.get("params_template", {}) if tool_match else {},
            "source": tool_match.get("source", "none") if tool_match else "none",
            "purpose": subtask.get("description", ""),
        }
        plan.append(step)

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "plan": plan,
            "subtasks": subtasks,
            "note": "Set dry_run=false to execute this plan",
        }

    # 4. Execute the plan
    result = _execute_plan(plan, {"request": request_text})

    # 5. If all succeeded, save as new skill
    if result.get("success"):
        skill_name = _generate_skill_name(request_text)
        tags = _extract_domain_tags(request_text, plan)
        save_result = save_skill(
            name=skill_name,
            description=request_text,
            tool_sequence=plan,
            domain_tags=tags,
            source="synthesized",
            confidence=75,
        )
        result["saved_skill"] = save_result

    return {"ok": True, "execution": result, "plan": plan}


def _decompose_request(request_text: str) -> List[Dict]:
    """Use LLM to decompose request into ordered sub-tasks."""
    prompt = f"""Decompose this user request into 2-5 ordered sub-tasks that a tool-using AI can execute.
Each sub-task should map to one tool call.

Request: "{request_text}"

Return ONLY valid JSON (no markdown, no explanation):
[
  {{"description": "what to do", "expected_tool_category": "filesystem|web|desktop|code|media|memory|system", "input_from": null}},
  {{"description": "next step", "expected_tool_category": "...", "input_from": 0}}
]

input_from is the 0-indexed step whose output feeds into this step (null if none).
Keep it practical -- only steps that map to real tool actions."""

    try:
        from modules.joi_evolution import _ask_research_llm
        response = _ask_research_llm(prompt, max_tokens=500)
        if response:
            # Extract JSON from response
            text = response.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
            subtasks = json.loads(text)
            if isinstance(subtasks, list):
                return subtasks
    except Exception as e:
        print(f"  [SKILL] Decomposition failed: {e}")

    return []


def _find_tool_for_subtask(subtask: Dict) -> Optional[Dict]:
    """Find the best tool for a sub-task. Checks skill library, then TOOL_EXECUTORS."""
    desc = subtask.get("description", "")
    category = subtask.get("expected_tool_category", "")

    # 1. Check skill library for a matching sub-skill
    matches = find_skills(desc, top_k=1)
    if matches and matches[0].get("confidence", 0) >= 60:
        best = matches[0]
        if best.get("tool_sequence"):
            first_step = best["tool_sequence"][0]
            return {
                "tool_name": first_step.get("tool"),
                "params_template": first_step.get("params_template", {}),
                "source": "skill_library",
            }

    # 2. Keyword match against available TOOL_EXECUTORS
    executors = joi_companion.TOOL_EXECUTORS
    tool_defs = joi_companion.TOOLS

    # Build a lookup: tool_name -> description
    tool_descs = {}
    for tdef in tool_defs:
        fn = tdef.get("function", {})
        tool_descs[fn.get("name", "")] = fn.get("description", "").lower()

    # Score each tool by keyword overlap
    desc_lower = desc.lower()
    cat_lower = category.lower()
    desc_words = set(desc_lower.split())
    best_score = 0
    best_tool = None

    # Category-to-tool prefix mapping
    cat_prefixes = {
        "filesystem": ["fs_", "read_file", "write_file", "search_files"],
        "web": ["web_", "fetch"],
        "desktop": ["screenshot", "move_mouse", "click_", "type_text", "launch_app"],
        "code": ["code_edit", "code_read", "code_search", "code_insert", "propose_patch"],
        "media": ["generate_avatar", "generate_file"],
        "memory": ["remember", "recall", "save_fact", "search_facts"],
        "system": ["self_diagnose", "self_fix", "set_mode", "set_provider"],
    }

    for tool_name, tool_desc in tool_descs.items():
        if tool_name not in executors:
            continue
        score = 0

        # Category match
        prefixes = cat_prefixes.get(cat_lower, [])
        for pfx in prefixes:
            if tool_name.startswith(pfx) or pfx in tool_name:
                score += 5

        # Word overlap with description
        tool_words = set(tool_desc.split())
        overlap = len(desc_words & tool_words)
        score += overlap * 2

        # Direct name match
        for w in desc_words:
            if w in tool_name:
                score += 3

        if score > best_score:
            best_score = score
            best_tool = tool_name

    if best_tool and best_score >= 3:
        return {
            "tool_name": best_tool,
            "params_template": {},
            "source": "tool_executor",
        }

    return None


def _execute_plan(plan: List[Dict], context: Dict) -> Dict:
    """Execute a skill plan step by step, passing outputs forward."""
    executors = joi_companion.TOOL_EXECUTORS
    results = []
    all_success = True

    for step in plan:
        tool_name = step.get("tool")
        if not tool_name or tool_name not in executors:
            results.append({
                "step": step.get("step", "?"),
                "tool": tool_name,
                "success": False,
                "error": f"Tool '{tool_name}' not found",
            })
            all_success = False
            continue

        params = dict(step.get("params_template", {}))

        # Substitute variables from context
        for key, val in params.items():
            if isinstance(val, str) and "{" in val:
                for ctx_key, ctx_val in context.items():
                    val = val.replace(f"{{{ctx_key}}}", str(ctx_val))
                params[key] = val

        try:
            result = executors[tool_name](**params)
            step_ok = True
            if isinstance(result, dict) and result.get("ok") is False:
                step_ok = False
                all_success = False

            results.append({
                "step": step.get("step", "?"),
                "tool": tool_name,
                "success": step_ok,
                "result_summary": _summarize_result(result),
            })

            # Store output for downstream steps
            context[f"step_{step.get('step', 0)}_output"] = result

        except Exception as e:
            results.append({
                "step": step.get("step", "?"),
                "tool": tool_name,
                "success": False,
                "error": str(e)[:200],
            })
            all_success = False

    return {
        "success": all_success,
        "results": results,
        "failed_step": next((r["step"] for r in results if not r["success"]), None),
    }


def _summarize_result(result: Any) -> str:
    """Summarize a tool result to a short string."""
    if isinstance(result, dict):
        if result.get("ok"):
            msg = result.get("message", result.get("summary", "success"))
            return str(msg)[:100]
        else:
            return f"error: {result.get('error', '?')}"[:100]
    return str(result)[:100]


def _generate_skill_name(request: str) -> str:
    """Generate a concise snake_case skill name from the request."""
    # Simple approach: take key words, snake_case them
    words = request.lower().split()
    # Remove filler words
    filler = {"a", "the", "an", "to", "for", "of", "in", "on", "and", "or", "this", "that", "my", "me", "i"}
    key_words = [w for w in words if w not in filler and w.isalpha()][:5]
    return "_".join(key_words) if key_words else f"skill_{int(time.time())}"


def _extract_domain_tags(request: str, plan: List[Dict]) -> List[str]:
    """Extract domain tags from request and plan."""
    tags = set()
    text = request.lower()

    tag_keywords = {
        "media": ["video", "audio", "image", "gif", "mp3", "mp4", "convert", "ffmpeg"],
        "web": ["search", "fetch", "url", "website", "browse", "download"],
        "filesystem": ["file", "folder", "directory", "read", "write", "save", "create"],
        "code": ["code", "edit", "patch", "fix", "bug", "function", "module"],
        "desktop": ["open", "launch", "app", "window", "click", "screenshot"],
        "memory": ["remember", "recall", "fact", "memory"],
        "system": ["diagnose", "repair", "provider", "mode", "config"],
    }

    for tag, keywords in tag_keywords.items():
        for kw in keywords:
            if kw in text:
                tags.add(tag)
                break

    # Add tags from tools used
    for step in plan:
        tool = step.get("tool", "")
        if tool.startswith("fs_") or tool in ("read_file", "write_file"):
            tags.add("filesystem")
        elif tool.startswith("web_"):
            tags.add("web")
        elif tool in ("launch_app", "screenshot"):
            tags.add("desktop")

    return list(tags) or ["general"]


# ══════════════════════════════════════════════════════════════════════════
# 1D. SELF-CORRECTION LOOP
# ══════════════════════════════════════════════════════════════════════════

def run_self_correction(**kwargs) -> Dict:
    """
    TOOL: Review logs for recurring failures, detect patterns, propose fixes.
    """
    patterns = _detect_recurring_failures()
    corr = _load_corrections()
    new_patterns = 0
    fixes_proposed = 0

    for pattern in patterns:
        # Check if already tracked
        existing_ids = {p["id"] for p in corr.get("patterns_detected", [])}
        pattern_key = f"{pattern['tool']}:{pattern['context_hash']}"
        if pattern_key in existing_ids:
            # Update occurrence count
            for p in corr["patterns_detected"]:
                if p["id"] == pattern_key:
                    p["occurrences"] = pattern["occurrences"]
            continue

        # New pattern
        corr_entry = {
            "id": pattern_key,
            "pattern": pattern["description"],
            "tool": pattern["tool"],
            "occurrences": pattern["occurrences"],
            "first_seen": pattern.get("first_seen", datetime.now().isoformat()),
            "fix_applied": False,
        }
        corr["patterns_detected"].append(corr_entry)
        new_patterns += 1

        # If 3+ occurrences, try to generate a fix
        if pattern["occurrences"] >= 3:
            fix = _generate_fix_for_pattern(pattern)
            if fix:
                fixes_proposed += 1
                corr_entry["proposed_fix"] = fix

    corr["last_review"] = datetime.now().isoformat()
    _save_corrections(corr)

    return {
        "ok": True,
        "patterns_found": len(patterns),
        "new_patterns": new_patterns,
        "fixes_proposed": fixes_proposed,
        "total_tracked": len(corr.get("patterns_detected", [])),
    }


def _detect_recurring_failures() -> List[Dict]:
    """Analyze tool_usage_log.json, group failures, return patterns with 3+ occurrences."""
    try:
        from modules.joi_learning import _load_tool_log
        log = _load_tool_log()
    except Exception:
        return []

    # Group failures by tool name
    failures: Dict[str, List[Dict]] = {}
    entries = log.get("entries", log.get("tools", {}))

    if isinstance(entries, dict):
        # Format: {tool_name: {successes, failures, ...}}
        for tool_name, stats in entries.items():
            fail_count = stats.get("failures", 0) if isinstance(stats, dict) else 0
            if fail_count >= 3:
                failures[tool_name] = [{
                    "tool": tool_name,
                    "count": fail_count,
                }]
    elif isinstance(entries, list):
        for entry in entries:
            if isinstance(entry, dict) and not entry.get("success", True):
                tool_name = entry.get("tool_name", entry.get("name", "unknown"))
                if tool_name not in failures:
                    failures[tool_name] = []
                failures[tool_name].append(entry)

    patterns = []
    for tool_name, fail_list in failures.items():
        count = len(fail_list) if isinstance(fail_list, list) else 0
        if isinstance(fail_list, list) and fail_list and isinstance(fail_list[0], dict) and "count" in fail_list[0]:
            count = fail_list[0]["count"]

        if count >= 3:
            context_hash = tool_name[:20]
            patterns.append({
                "tool": tool_name,
                "occurrences": count,
                "context_hash": context_hash,
                "description": f"Tool '{tool_name}' has failed {count} times",
                "first_seen": datetime.now().isoformat(),
            })

    return patterns


def _generate_fix_for_pattern(pattern: Dict) -> Optional[Dict]:
    """Use LLM to analyze a failure pattern and suggest a fix."""
    try:
        from modules.joi_evolution import _ask_research_llm

        prompt = f"""A tool in an AI companion system has a recurring failure pattern:

Tool: {pattern['tool']}
Failures: {pattern['occurrences']} times
Pattern: {pattern['description']}

Suggest ONE concrete fix. Return JSON only:
{{"fix_type": "code_patch|alternative_tool|skill_route|config_change",
 "description": "what to fix",
 "confidence": 0-100}}"""

        response = _ask_research_llm(prompt, max_tokens=300)
        if response:
            text = response.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
            return json.loads(text)
    except Exception as e:
        print(f"  [SKILL] Fix generation failed: {e}")

    return None


# ══════════════════════════════════════════════════════════════════════════
# 1E. GOAL SETTING
# ══════════════════════════════════════════════════════════════════════════

def generate_practice_goals(**kwargs) -> Dict:
    """
    TOOL: Analyze weak areas from learning data + tool failures, generate 1-3 practice goals.
    """
    goals_data = _load_goals()
    weak_areas = []
    tool_failures = []

    # 1. Load learning weak areas
    try:
        from modules.joi_learning import _load_learning_data
        learn_data = _load_learning_data()
        topics = learn_data.get("topics", {})
        for topic, stats in topics.items():
            pos = stats.get("positive_feedback", 0)
            neg = stats.get("negative_feedback", 0)
            if neg > pos and stats.get("count", 0) >= 2:
                weak_areas.append({"area": topic, "neg": neg, "pos": pos})
    except Exception:
        pass

    # 2. Load tool failure rates (>30% failure)
    try:
        from modules.joi_learning import _load_tool_log
        log = _load_tool_log()
        entries = log.get("entries", log.get("tools", {}))
        if isinstance(entries, dict):
            for tool_name, stats in entries.items():
                if not isinstance(stats, dict):
                    continue
                total = stats.get("successes", 0) + stats.get("failures", 0)
                if total >= 3:
                    fail_rate = stats.get("failures", 0) / total
                    if fail_rate > 0.3:
                        tool_failures.append({
                            "tool": tool_name,
                            "fail_rate": round(fail_rate, 2),
                            "total": total,
                        })
    except Exception:
        pass

    # 3. Cross-reference with skill library gaps
    lib = _load_skill_library()
    existing_tags = set()
    for skill in lib["skills"].values():
        existing_tags.update(skill.get("domain_tags", []))

    # Generate goals
    new_goals = []
    active_areas = {g["skill_area"] for g in goals_data.get("active_goals", [])}

    for wa in weak_areas[:2]:
        area = wa["area"]
        if area in active_areas:
            continue
        new_goals.append({
            "id": f"goal_{int(time.time())}_{len(new_goals)}",
            "skill_area": area,
            "description": f"Improve performance in '{area}' (negative feedback: {wa['neg']}, positive: {wa['pos']})",
            "priority": "high" if wa["neg"] > wa["pos"] * 2 else "medium",
            "practice_count": 0,
            "status": "active",
            "created": datetime.now().isoformat(),
        })

    for tf in tool_failures[:1]:
        tool = tf["tool"]
        if tool in active_areas:
            continue
        new_goals.append({
            "id": f"goal_{int(time.time())}_{len(new_goals)}",
            "skill_area": tool,
            "description": f"Reduce failure rate for '{tool}' (currently {tf['fail_rate']:.0%} over {tf['total']} uses)",
            "priority": "medium",
            "practice_count": 0,
            "status": "active",
            "created": datetime.now().isoformat(),
        })

    goals_data["active_goals"].extend(new_goals)
    goals_data["last_goal_generation"] = datetime.now().isoformat()
    _save_goals(goals_data)

    return {
        "ok": True,
        "new_goals": len(new_goals),
        "goals": new_goals,
        "total_active": len(goals_data["active_goals"]),
        "weak_areas_found": len(weak_areas),
        "tool_failures_found": len(tool_failures),
    }


def _practice_goal(goal: Dict) -> Dict:
    """Simulate practice for a goal using dry_run synthesis."""
    area = goal.get("skill_area", "")
    result = synthesize_skill(request=f"practice: {area}", dry_run=True)
    goal["practice_count"] = goal.get("practice_count", 0) + 1

    if goal["practice_count"] >= 5:
        goal["status"] = "completed"

    return {"goal_id": goal["id"], "practice_result": result.get("ok", False)}


# ══════════════════════════════════════════════════════════════════════════
# 1F. CROSS-DOMAIN ADAPTATION
# ══════════════════════════════════════════════════════════════════════════

def cross_domain_lookup(problem: str, current_domain: str) -> str:
    """Query vector memory for solutions from OTHER domains."""
    try:
        from modules.memory.memory_manager import recall_memory
        hits = recall_memory(problem, namespace="skills", top_k=5)
        if not hits or not isinstance(hits, list):
            return ""

        cross_domain = []
        for hit in hits:
            meta = hit.get("metadata", {}) if isinstance(hit, dict) else {}
            skill_id = meta.get("skill_id", "")
            if skill_id:
                lib = _load_skill_library()
                skill = lib["skills"].get(skill_id)
                if skill:
                    tags = skill.get("domain_tags", [])
                    if current_domain not in tags:
                        cross_domain.append(
                            f"- {skill['name']} ({', '.join(tags)}): {skill['description'][:80]}"
                        )

        if cross_domain:
            return "[CROSS-DOMAIN SOLUTIONS]:\n" + "\n".join(cross_domain[:3])
    except Exception:
        pass

    return ""


# ══════════════════════════════════════════════════════════════════════════
# 1G. VISION-LOGIC CROSS-REFERENCE
# ══════════════════════════════════════════════════════════════════════════

_ERROR_KEYWORDS = ["error", "exception", "traceback", "crash", "not responding",
                   "fatal", "failed", "unhandled", "segfault", "blue screen",
                   "syntax error", "import error", "module not found"]

def vision_error_handler(vision_summary: str) -> Optional[Dict]:
    """
    Check vision summary for error keywords.
    If detected: trigger self_diagnose or code_self_repair.
    Returns action taken or None.
    """
    if not vision_summary:
        return None

    summary_lower = vision_summary.lower()
    detected = [kw for kw in _ERROR_KEYWORDS if kw in summary_lower]

    if not detected:
        return None

    print(f"  [VISION->LOGIC] Error detected in vision: {detected[:3]}")

    # Try internal monologue first (if reasoning module available)
    try:
        from modules.joi_reasoning import record_thought
        record_thought(
            f"Vision detected error on screen: {vision_summary[:200]}",
            thought_type="spatial"
        )
    except Exception:
        pass

    # Trigger self-diagnosis
    action_taken = {"action": "self_diagnose", "triggers": detected[:3]}
    try:
        executors = joi_companion.TOOL_EXECUTORS
        if "self_diagnose" in executors:
            result = executors["self_diagnose"]()
            action_taken["diagnosis_ok"] = result.get("ok", False) if isinstance(result, dict) else False
        elif "code_self_repair" in executors:
            # If it looks like a code error, try code repair
            issue_desc = f"Vision detected on screen: {vision_summary[:300]}"
            result = executors["code_self_repair"](issue=issue_desc)
            action_taken["action"] = "code_self_repair"
            action_taken["repair_ok"] = result.get("ok", False) if isinstance(result, dict) else False
    except Exception as e:
        action_taken["error"] = str(e)[:200]

    return action_taken


# ══════════════════════════════════════════════════════════════════════════
# 1H. AUTO-CAPTURE HOOK
# ══════════════════════════════════════════════════════════════════════════

_auto_capture_lock = threading.Lock()

def auto_capture_skill(tool_calls_log: List, user_message: str, joi_reply: str):
    """
    Called after /chat in a background thread.
    If 2+ successful tool calls in sequence: extract, name, save as skill.
    """
    def _do_capture():
        try:
            if not tool_calls_log or len(tool_calls_log) < 2:
                return

            # Filter to successful tool calls
            successful = [tc for tc in tool_calls_log if tc.get("result_ok", tc.get("success", False))]
            if len(successful) < 2:
                return

            # Build tool sequence
            tool_sequence = []
            for i, tc in enumerate(successful[:6]):  # cap at 6 steps
                tool_sequence.append({
                    "step": i + 1,
                    "tool": tc.get("name", ""),
                    "params_template": {},
                    "purpose": f"Step {i+1} of auto-captured workflow",
                })

            # Generate a name from the user message
            name = _generate_skill_name(user_message) if user_message else f"auto_skill_{int(time.time())}"
            description = user_message[:200] if user_message else "Auto-captured tool chain"
            tags = _extract_domain_tags(user_message or "", tool_sequence)

            with _auto_capture_lock:
                save_skill(
                    name=name,
                    description=description,
                    tool_sequence=tool_sequence,
                    domain_tags=tags,
                    source="auto_captured",
                    confidence=70,
                )
                print(f"  [SKILL] Auto-captured skill: {name} ({len(tool_sequence)} steps)")

        except Exception as e:
            print(f"  [SKILL] Auto-capture failed: {e}")

    threading.Thread(target=_do_capture, daemon=True).start()


# ══════════════════════════════════════════════════════════════════════════
# 1I. SYSTEM PROMPT BLOCK
# ══════════════════════════════════════════════════════════════════════════

def compile_skill_synthesis_block(user_message: str = "", max_chars: int = 550) -> str:
    """Returns context block for system prompt injection."""
    try:
        lib = _load_skill_library()
        goals = _load_goals()
        corr = _load_corrections()

        total_skills = len(lib.get("skills", {}))
        total_exec = lib.get("stats", {}).get("total_executions", 0)
        active_goals = len(goals.get("active_goals", []))
        patterns = len(corr.get("patterns_detected", []))

        parts = [f"\n[SKILL SYNTHESIS]: Library: {total_skills} skills, {total_exec} executions."]

        # Top relevant skills for current message (include prompt snippets so model "levels up")
        if user_message and total_skills > 0:
            relevant = find_skills(user_message, top_k=3)
            if relevant:
                skill_names = [s.get("name", "?") for s in relevant[:3]]
                parts.append(f"Relevant: {', '.join(skill_names)}.")
                for s in relevant[:3]:
                    snip = s.get("prompt_snippet", "").strip()
                    if snip:
                        parts.append(snip)

        if active_goals > 0:
            goal_areas = [g["skill_area"] for g in goals.get("active_goals", [])[:3]]
            parts.append(f"Goals: {', '.join(goal_areas)}.")

        if patterns > 0:
            parts.append(f"Self-corrections tracked: {patterns}.")

        parts.append(
            "Use `synthesize_skill` to compose multi-step workflows. "
            "Use `find_skill` to check for proven solutions.\n"
        )

        block = " ".join(parts)
        return block[:max_chars]

    except Exception as e:
        print(f"  [SKILL] Context block failed: {e}")
        return ""


# ══════════════════════════════════════════════════════════════════════════
# 1J. AUTONOMY CYCLE HOOK
# ══════════════════════════════════════════════════════════════════════════

def autonomy_cycle_hook(cycle_result: Dict) -> Dict:
    """
    Called during autonomy cycle between LEARN and RESEARCH steps.
    A. Run self-correction
    B. Generate practice goals
    C. If idle >30min: practice one goal (dry_run)
    D. Prune unused skills (0 uses + >30 days old)
    60-second timeout.
    """
    summary_parts = []
    hook_result = {"ok": True}

    try:
        # A. Self-correction
        corr_result = run_self_correction()
        hook_result["self_correction"] = {
            "patterns": corr_result.get("patterns_found", 0),
            "fixes": corr_result.get("fixes_proposed", 0),
        }
        summary_parts.append(f"corrections={corr_result.get('patterns_found', 0)}")
    except Exception as e:
        hook_result["self_correction"] = {"error": str(e)}

    try:
        # B. Practice goals
        goal_result = generate_practice_goals()
        hook_result["goals"] = {
            "new": goal_result.get("new_goals", 0),
            "active": goal_result.get("total_active", 0),
        }
        summary_parts.append(f"goals={goal_result.get('total_active', 0)}")
    except Exception as e:
        hook_result["goals"] = {"error": str(e)}

    try:
        # C. Practice a goal if idle
        goals = _load_goals()
        active = goals.get("active_goals", [])
        if active:
            goal = active[0]
            practice_result = _practice_goal(goal)
            hook_result["practice"] = practice_result
            # Move completed goals
            still_active = []
            for g in active:
                if g.get("status") == "completed":
                    goals["completed_goals"].append(g)
                else:
                    still_active.append(g)
            goals["active_goals"] = still_active
            _save_goals(goals)
    except Exception as e:
        hook_result["practice"] = {"error": str(e)}

    try:
        # D. Prune unused skills (0 uses + >30 days old)
        lib = _load_skill_library()
        cutoff = time.time() - (30 * 24 * 3600)
        to_prune = []
        for sid, skill in lib["skills"].items():
            if (skill.get("success_count", 0) + skill.get("fail_count", 0)) == 0:
                if skill.get("created", time.time()) < cutoff:
                    to_prune.append(sid)

        for sid in to_prune:
            del lib["skills"][sid]

        if to_prune:
            _save_skill_library(lib)
            summary_parts.append(f"pruned={len(to_prune)}")
            hook_result["pruned"] = len(to_prune)
    except Exception as e:
        hook_result["prune"] = {"error": str(e)}

    hook_result["summary"] = ", ".join(summary_parts) if summary_parts else "done"
    return hook_result


# ══════════════════════════════════════════════════════════════════════════
# 1K. TOOL: get_skill_stats
# ══════════════════════════════════════════════════════════════════════════

def get_skill_stats(**kwargs) -> Dict:
    """TOOL: Return skill library stats, active goals, and correction patterns."""
    lib = _load_skill_library()
    goals = _load_goals()
    corr = _load_corrections()

    # Top 5 most-used skills
    skills_sorted = sorted(
        lib.get("skills", {}).values(),
        key=lambda s: s.get("success_count", 0) + s.get("fail_count", 0),
        reverse=True,
    )
    top_skills = [{
        "name": s["name"],
        "uses": s.get("success_count", 0) + s.get("fail_count", 0),
        "success_rate": round(
            s.get("success_count", 0) / max(s.get("success_count", 0) + s.get("fail_count", 0), 1), 2
        ),
        "confidence": s.get("confidence", 0),
    } for s in skills_sorted[:5]]

    return {
        "ok": True,
        "library": {
            "total_skills": len(lib.get("skills", {})),
            "total_executions": lib.get("stats", {}).get("total_executions", 0),
            "total_successes": lib.get("stats", {}).get("total_successes", 0),
            "top_skills": top_skills,
        },
        "goals": {
            "active": len(goals.get("active_goals", [])),
            "completed": len(goals.get("completed_goals", [])),
            "active_list": [{"area": g["skill_area"], "priority": g.get("priority", "medium")}
                           for g in goals.get("active_goals", [])[:5]],
        },
        "self_correction": {
            "patterns_tracked": len(corr.get("patterns_detected", [])),
            "fixes_applied": len(corr.get("fixes_applied", [])),
            "last_review": corr.get("last_review"),
        },
    }


def find_skill_tool(**kwargs) -> Dict:
    """TOOL: Search skill library for proven solutions."""
    query = kwargs.get("query", "")
    top_k = kwargs.get("top_k", 5)
    if not query:
        return {"ok": False, "error": "No query provided"}

    results = find_skills(query, top_k=top_k)
    return {
        "ok": True,
        "results": [{
            "name": s.get("name", "?"),
            "description": s.get("description", ""),
            "confidence": s.get("confidence", 0),
            "tools": [step.get("tool") for step in s.get("tool_sequence", [])],
            "uses": s.get("success_count", 0) + s.get("fail_count", 0),
        } for s in results],
        "total_found": len(results),
    }


def manage_skills(**kwargs) -> Dict[str, Any]:
    """Unified tool for managing skills, self-correction, and practice goals."""
    action = kwargs.get("action")
    if not action:
        return {"ok": False, "error": "action parameter is required"}
        
    try:
        if action == "synthesize": return synthesize_skill(**kwargs)
        elif action == "find": return find_skill_tool(**kwargs)
        elif action == "self_correct": return run_self_correction(**kwargs)
        elif action == "generate_goals": return generate_practice_goals(**kwargs)
        elif action == "get_stats": return get_skill_stats(**kwargs)
        else: return {"ok": False, "error": f"Unknown action: {action}"}
    except Exception as exc:
        return {"ok": False, "error": f"Skill action {action} failed: {exc}"}

# ══════════════════════════════════════════════════════════════════════════
# TOOL REGISTRATION
# ══════════════════════════════════════════════════════════════════════════

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "manage_skills",
        "description": "Unified tool to manage skill synthesis, search, self-correction, goal generation, and stats.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["synthesize", "find", "self_correct", "generate_goals", "get_stats"]
                },
                "request": {
                    "type": "string",
                    "description": "What you want to accomplish (e.g. 'convert video to GIF') (for synthesize)"
                },
                "dry_run": {
                    "type": "boolean",
                    "description": "If true, plan only -- don't execute (for synthesize)"
                },
                "query": {
                    "type": "string",
                    "description": "What skill to search for (for find)"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Max results to return (for find)"
                }
            },
            "required": ["action"]
        },
    }},
    manage_skills
)


# ══════════════════════════════════════════════════════════════════════════
# FLASK ROUTES
# ══════════════════════════════════════════════════════════════════════════

def _skills_route():
    """GET=stats, POST action=search/synthesize/self_correct/goals"""
    from modules.joi_memory import require_user
    require_user()

    if flask_req.method == "GET":
        return jsonify(get_skill_stats())

    data = flask_req.get_json(silent=True) or {}
    action = data.get("action", "")

    if action == "search":
        query = data.get("query", "")
        return jsonify(find_skill_tool(query=query, top_k=data.get("top_k", 5)))
    elif action == "synthesize":
        return jsonify(synthesize_skill(
            request=data.get("request", ""),
            dry_run=data.get("dry_run", False),
        ))
    elif action == "self_correct":
        return jsonify(run_self_correction())
    elif action == "goals":
        return jsonify(generate_practice_goals())
    else:
        return jsonify({"ok": False, "error": "Unknown action. Use: search, synthesize, self_correct, goals"})


def _skills_library_route():
    """GET -- full skill library for UI."""
    from modules.joi_memory import require_user
    require_user()
    lib = _load_skill_library()
    return jsonify({"ok": True, **lib})


joi_companion.register_route("/skills", ["GET", "POST"], _skills_route, "skills_route")
joi_companion.register_route("/skills/library", ["GET"], _skills_library_route, "skills_library_route")


# ── Startup message ──────────────────────────────────────────────────────
_lib = _load_skill_library()
print(f"  [OK] Skill synthesis: {len(_lib.get('skills', {}))} skills in library")
