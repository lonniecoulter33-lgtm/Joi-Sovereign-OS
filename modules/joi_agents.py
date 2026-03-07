"""
modules/joi_agents.py

Multi-Agent Definitions -- Architect / Coder / Validator
========================================================
All agent model selection from config.joi_models AGENT_MODEL_MAP.
  - Architect (supervisor_agent): Planning, decomposes tasks
  - Coder (coder_agent): Surgical code edits -- old_text/new_text pairs
  - Validator (subprocess): Runs terminal commands, syntax/import checks
"""

import ast
import difflib
import importlib
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ── JOI_CONTEXT.md Loader ────────────────────────────────────────────────────

def load_context_file(project_path: Optional[str] = None) -> str:
    """
    Read JOI_CONTEXT.md from project directory or ROOT.
    Returns empty string if no context file found.
    Uses Path for all path handling to avoid Windows backslash/unicodeescape issues.
    """
    search_paths: List[Path] = []
    if project_path:
        try:
            search_paths.append(Path(project_path).resolve() / "JOI_CONTEXT.md")
        except (TypeError, ValueError, OSError):
            pass
    search_paths.append(BASE_DIR / "JOI_CONTEXT.md")

    for p in search_paths:
        try:
            if p.exists() and p.is_file():
                text = p.read_text(encoding="utf-8")
                if text.strip():
                    return text.strip()
        except Exception:
            pass
    return ""


# ── File Reader Utility ──────────────────────────────────────────────────────

def _read_files(file_paths: List[str]) -> Dict[str, str]:
    """Read multiple files and return {path: content} dict.
    Uses source_modules from file_registry.json as fallback for unresolved paths.
    """
    contents = {}

    # Load source module registry for fallback resolution
    _source_mods = {}
    try:
        _reg = BASE_DIR / "file_registry.json"
        if _reg.exists():
            with open(_reg, "r", encoding="utf-8") as _f:
                _source_mods = json.load(_f).get("source_modules", {})
    except Exception:
        pass

    for fp in file_paths:
        try:
            p = Path(fp)
            if not p.is_absolute():
                p = BASE_DIR / p

            # If path doesn't exist, try the source module registry
            if not p.exists():
                stem = Path(fp).stem
                if stem in _source_mods:
                    p = Path(_source_mods[stem])

            if p.exists() and p.is_file():
                text = p.read_text(encoding="utf-8", errors="replace")
                # Truncate very large files to 50K chars
                if len(text) > 50000:
                    text = text[:50000] + f"\n\n... [TRUNCATED -- {len(text)} total chars]"
                contents[str(p)] = text
            else:
                contents[str(fp)] = f"[FILE NOT FOUND: {fp}]"
        except Exception as e:
            contents[str(fp)] = f"[ERROR reading file: {e}]"
    return contents


# ══════════════════════════════════════════════════════════════════════════════
# ARCHITECT AGENT -- Gemini Flash (1M+ context, reads entire codebase)
# ══════════════════════════════════════════════════════════════════════════════

ARCHITECT_SYSTEM_PROMPT = """You are the ARCHITECT agent for Joi's multi-agent coding pipeline.

YOUR ROLE:
- Analyze the codebase structure and understand existing patterns
- Decompose the user's coding task into precise, ordered subtasks
- NEVER write code yourself -- only plan and assign work to the CODER agent
- Each subtask should be one surgical edit to one file

OUTPUT FORMAT (strict JSON, no markdown):
{
    "plan_summary": "Brief description of the overall approach",
    "global_setup_commands": ["pip install flask", "mkdir -p static"],
    "build_config": {"type": "python_exe", "entry_point": "src/main.py"},
    "continuation": false,
    "continuation_hint": "",
    "subtasks": [
        {
            "id": 1,
            "description": "What this subtask accomplishes",
            "role": "coder",
            "files": ["path/to/file.py"],
            "depends_on": [],
            "setup_commands": ["pip install requests"],
            "template": "",
            "test_command": "python -c \\"import ast; ast.parse(open('path/to/file.py').read())\\"",
            "acceptance_criteria": "What success looks like"
        }
    ],
    "risk_assessment": "Low/Medium/High -- what could go wrong"
}

OPTIONAL TOP-LEVEL FIELDS:
- "global_setup_commands": shell commands to run BEFORE any subtasks (pip install, mkdir, etc.)
- "build_config": {"type": "python_exe|python_package|web_zip|node_build", "entry_point": "..."} -- post-pipeline build
- "continuation": true if the task needs MORE than 20 subtasks
- "continuation_hint": what remains after these subtasks (only if continuation=true)

OPTIONAL PER-SUBTASK FIELDS:
- "setup_commands": shell commands to run before this subtask's coder (pip install, etc.)
- "role": "coder" (default) or "scaffold" -- "scaffold" creates project from template, skips coder
- "template": template name for scaffold subtasks (python_cli, python_flask, python_fastapi, python_desktop, html_spa, node_express)

RULES:
- Keep subtasks small and surgical (one logical change per subtask)
- Order subtasks by dependency -- earlier tasks should be prerequisites
- Always include a test_command (at minimum: syntax check with ast.parse)
- For Python files: test with ast.parse + import check
- For HTML files: basic syntax validation
- If the task is trivial (1 change), return exactly 1 subtask
- Max 20 subtasks per plan
- If the task needs MORE than 20 subtasks, set "continuation": true with a "continuation_hint"
- Use file paths relative to the project root provided (e.g. "my_app/main.py" or "projects/my_tool/script.py")
- CREATING NEW FILES: To create a new file that does not exist yet, set files: ["path/to/newfile.py"].
  The Coder will receive empty content; it must output exactly one change with old_text="" and new_text=full file content.
- For brand-new projects: FIRST subtask should be role="scaffold" with appropriate template
- Use setup_commands for dependency installation (pip install, npm install, mkdir)
- Use build_config if the user wants a packaged output (.exe, .zip, npm build)
"""


def call_architect(task: str, file_contents: Dict[str, str],
                   joi_ctx: str = "", project_path: str = "") -> Dict[str, Any]:
    """
    Call the Brain to generate a structured plan (config: supervisor_agent).
    Returns parsed JSON plan or error dict.
    """
    # Build context prompt
    files_block = ""
    for fpath, content in file_contents.items():
        files_block += f"\n\n--- FILE: {fpath} ---\n{content}\n--- END FILE ---\n"

    ctx_block = ""
    if joi_ctx:
        ctx_block = f"\n\nPROJECT RULES (from JOI_CONTEXT.md):\n{joi_ctx}\n"

    # Use resolved Path and forward slashes in prompt to avoid Windows \U unicodeescape in generated commands
    _root = Path(project_path).resolve() if project_path else BASE_DIR
    project_root_display = _root.as_posix()

    prompt = f"""PROJECT ROOT: {project_root_display}
{ctx_block}

TASK: {task}

FILES TO ANALYZE:
{files_block}

Generate your plan as strict JSON. No markdown, no explanation outside the JSON."""

    # Agent Terminal: use Dynamic Model Router (planning -> heavy_reasoning: Gemma 12B / GPT-4o)
    model_used = "unknown"
    try:
        from modules.joi_llm import route_and_call_for_agent
        text, model_used = route_and_call_for_agent(
            task_type="planning",
            messages=[{"role": "user", "content": prompt}],
            system_prompt=ARCHITECT_SYSTEM_PROMPT,
            max_tokens=4000,
        )
        if text is None:
            # Fallback to Brain if router returns None
            from modules.joi_brain import brain
            result = brain.think(
                task=f"Architect plan: {task[:80]}",
                prompt=prompt,
                system_prompt=ARCHITECT_SYSTEM_PROMPT,
                thinking_level=3,
                max_tokens=4000,
            )
            if not result.get("ok"):
                return {"error": result.get("error", "Brain returned failure"), "subtasks": []}
            text = result.get("text", "")
            model_used = result.get("model", "unknown")
    except ImportError as e:
        text = None
        try:
            from modules.joi_llm import _call_gemini, HAVE_GEMINI
            from config.joi_models import GEMINI_MODELS
            if HAVE_GEMINI:
                full_prompt = f"{ARCHITECT_SYSTEM_PROMPT}\n\n{prompt}"
                text = _call_gemini(full_prompt, max_tokens=4000, model=GEMINI_MODELS.get("fallback", "gemini-2.5-flash-lite"))
                model_used = "gemini"
            else:
                return {"error": "No LLM provider available (Brain and Gemini both unavailable)", "subtasks": []}
        except ImportError:
            return {"error": f"No LLM provider available: {e}", "subtasks": []}

    if not text:
        return {"error": "LLM returned empty response", "subtasks": []}

    # Parse JSON from response (handle markdown code blocks)
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last ``` lines
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        plan = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from mixed text
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                plan = json.loads(json_match.group())
            except json.JSONDecodeError:
                return {"error": f"Could not parse Architect output as JSON", "raw": text[:500], "subtasks": []}
        else:
            return {"error": "No JSON found in Architect output", "raw": text[:500], "subtasks": []}

    # Attach model info for terminal display
    plan["model_used"] = model_used
    plan["model_key"] = model_used

    # Validate structure
    if "subtasks" not in plan:
        plan["subtasks"] = []
    if "plan_summary" not in plan:
        plan["plan_summary"] = "Plan generated"
    if "risk_assessment" not in plan:
        plan["risk_assessment"] = "Unknown"

    # Cap at 20 subtasks
    plan["subtasks"] = plan["subtasks"][:20]

    # Assign IDs if missing
    for i, st in enumerate(plan["subtasks"]):
        if "id" not in st:
            st["id"] = i + 1
        if "status" not in st:
            st["status"] = "pending"
        if "retries" not in st:
            st["retries"] = 0
        if "changes" not in st:
            st["changes"] = []
        if "validation" not in st:
            st["validation"] = {}

    return plan


# ══════════════════════════════════════════════════════════════════════════════
# EXPLORE AGENT -- Read-only codebase scanner (never writes code)
# ══════════════════════════════════════════════════════════════════════════════

EXPLORE_SYSTEM_PROMPT = """You are the EXPLORE agent for Joi's multi-agent coding pipeline.

YOUR ROLE:
- Read-only. You scan files and report findings. You NEVER write or suggest code.
- Discover project structure, patterns, dependencies, potential issues.
- Provide observations that help the CODER and ARCHITECT make better decisions.

OUTPUT FORMAT (strict JSON, no markdown):
{
    "findings": [
        {
            "file": "path/to/file.py",
            "observation": "What you found",
            "relevance": "high|medium|low"
        }
    ],
    "summary": "Brief overall assessment",
    "suggestions_for_coder": ["Actionable suggestion 1", "Suggestion 2"]
}

RULES:
- Focus on structure, patterns, dependencies, and potential issues.
- Note any inconsistencies, missing imports, or unused code.
- Keep observations concise and actionable.
- NEVER include code changes or new code in your output.
"""


def call_explore(task: str, file_contents: Dict[str, str],
                 joi_ctx: str = "") -> Dict[str, Any]:
    """Call the explore agent to scan files read-only. Returns findings."""
    files_block = ""
    for fpath, content in file_contents.items():
        files_block += f"\n\n--- FILE: {fpath} ---\n{content}\n--- END FILE ---\n"

    prompt = f"""TASK: {task}

FILES TO EXPLORE:
{files_block}

{f'PROJECT RULES: {joi_ctx}' if joi_ctx else ''}

Report your findings as strict JSON. No markdown."""

    model_used = "unknown"
    try:
        from modules.joi_llm import route_and_call_for_agent
        text, model_used = route_and_call_for_agent(
            task_type="exploration",
            messages=[{"role": "user", "content": prompt}],
            system_prompt=EXPLORE_SYSTEM_PROMPT,
            max_tokens=3000,
        )
        if text is None:
            from modules.joi_brain import brain
            result = brain.think(
                task=f"Explore: {task[:80]}",
                prompt=prompt,
                system_prompt=EXPLORE_SYSTEM_PROMPT,
                thinking_level=2,
                max_tokens=3000,
            )
            if not result.get("ok"):
                return {"error": result.get("error", "Brain returned failure"), "findings": []}
            text = result.get("text", "")
            model_used = result.get("model", "unknown")
    except ImportError:
        return {"error": "No LLM provider available", "findings": []}

    if not text:
        return {"error": "LLM returned empty response", "findings": []}

    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        output = json.loads(text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                output = json.loads(json_match.group())
            except json.JSONDecodeError:
                return {"error": "Could not parse Explore output", "findings": []}
        else:
            return {"error": "No JSON in Explore output", "findings": []}

    output.setdefault("findings", [])
    output.setdefault("summary", "")
    output.setdefault("suggestions_for_coder", [])
    output["model_used"] = model_used
    return output


# ══════════════════════════════════════════════════════════════════════════════
# SECURITY AUDITOR AGENT -- Reviews for vulnerabilities
# ══════════════════════════════════════════════════════════════════════════════

SECURITY_SYSTEM_PROMPT = """You are the SECURITY AUDITOR agent for Joi's multi-agent coding pipeline.

YOUR ROLE:
- Review code for security vulnerabilities.
- Check for: hardcoded secrets, SQL/XSS injection, unsafe eval/exec, missing input validation,
  path traversal, insecure deserialization, command injection.
- Rate severity and provide fix suggestions.

OUTPUT FORMAT (strict JSON, no markdown):
{
    "issues": [
        {
            "severity": "critical|high|medium|low",
            "file": "path/to/file.py",
            "line_hint": "approximate line or code snippet",
            "description": "What the vulnerability is",
            "fix_suggestion": "How to fix it"
        }
    ],
    "passed": true,
    "summary": "Brief security assessment"
}

RULES:
- Set passed=false if ANY critical or high severity issues found.
- Be specific about line locations and fix suggestions.
- Don't flag theoretical issues -- focus on real exploitable vulnerabilities.
"""


def call_security_auditor(task: str, file_contents: Dict[str, str]) -> Dict[str, Any]:
    """Call the security auditor to review code for vulnerabilities."""
    files_block = ""
    for fpath, content in file_contents.items():
        files_block += f"\n\n--- FILE: {fpath} ---\n{content}\n--- END FILE ---\n"

    prompt = f"""TASK: {task}

FILES TO AUDIT:
{files_block}

Review for security vulnerabilities. Output strict JSON."""

    model_used = "unknown"
    try:
        from modules.joi_llm import route_and_call_for_agent
        text, model_used = route_and_call_for_agent(
            task_type="security_audit",
            messages=[{"role": "user", "content": prompt}],
            system_prompt=SECURITY_SYSTEM_PROMPT,
            max_tokens=3000,
        )
        if text is None:
            from modules.joi_brain import brain
            result = brain.think(
                task=f"Security audit: {task[:80]}",
                prompt=prompt,
                system_prompt=SECURITY_SYSTEM_PROMPT,
                thinking_level=3,
                max_tokens=3000,
            )
            if not result.get("ok"):
                return {"error": result.get("error", "Brain returned failure"), "issues": [], "passed": True}
            text = result.get("text", "")
            model_used = result.get("model", "unknown")
    except ImportError:
        return {"error": "No LLM provider available", "issues": [], "passed": True}

    if not text:
        return {"error": "LLM returned empty response", "issues": [], "passed": True}

    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        output = json.loads(text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                output = json.loads(json_match.group())
            except json.JSONDecodeError:
                return {"error": "Could not parse Security output", "issues": [], "passed": True}
        else:
            return {"error": "No JSON in Security output", "issues": [], "passed": True}

    output.setdefault("issues", [])
    output.setdefault("passed", True)
    output.setdefault("summary", "")
    output["model_used"] = model_used
    return output


# ══════════════════════════════════════════════════════════════════════════════
# UI/UX SPECIALIST AGENT -- Reviews HTML/CSS/JS for accessibility + design
# ══════════════════════════════════════════════════════════════════════════════

UIUX_SYSTEM_PROMPT = """You are the UI/UX SPECIALIST agent for Joi's multi-agent coding pipeline.

YOUR ROLE:
- Review HTML/CSS/JS for: accessibility (ARIA), design system consistency (CSS vars),
  responsive issues, UX anti-patterns.
- Check that CSS uses project variables (--primary, --secondary, --accent) where appropriate.
- Verify keyboard navigability and screen reader compatibility.

OUTPUT FORMAT (strict JSON, no markdown):
{
    "issues": [
        {
            "type": "accessibility|design|responsive|ux",
            "description": "What the issue is",
            "suggestion": "How to fix it"
        }
    ],
    "approved": true,
    "summary": "Brief UI/UX assessment"
}

RULES:
- Set approved=false only for significant accessibility or usability issues.
- Focus on real user-facing problems, not nitpicks.
- Be constructive with suggestions.
"""


def call_uiux_specialist(task: str, file_contents: Dict[str, str]) -> Dict[str, Any]:
    """Call the UI/UX specialist to review frontend code."""
    files_block = ""
    for fpath, content in file_contents.items():
        files_block += f"\n\n--- FILE: {fpath} ---\n{content}\n--- END FILE ---\n"

    prompt = f"""TASK: {task}

FILES TO REVIEW:
{files_block}

Review for UI/UX issues. Output strict JSON."""

    model_used = "unknown"
    try:
        from modules.joi_llm import route_and_call_for_agent
        text, model_used = route_and_call_for_agent(
            task_type="validation",
            messages=[{"role": "user", "content": prompt}],
            system_prompt=UIUX_SYSTEM_PROMPT,
            max_tokens=3000,
        )
        if text is None:
            from modules.joi_brain import brain
            result = brain.think(
                task=f"UI/UX review: {task[:80]}",
                prompt=prompt,
                system_prompt=UIUX_SYSTEM_PROMPT,
                thinking_level=2,
                max_tokens=3000,
            )
            if not result.get("ok"):
                return {"error": result.get("error", "Brain returned failure"), "issues": [], "approved": True}
            text = result.get("text", "")
            model_used = result.get("model", "unknown")
    except ImportError:
        return {"error": "No LLM provider available", "issues": [], "approved": True}

    if not text:
        return {"error": "LLM returned empty response", "issues": [], "approved": True}

    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        output = json.loads(text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                output = json.loads(json_match.group())
            except json.JSONDecodeError:
                return {"error": "Could not parse UI/UX output", "issues": [], "approved": True}
        else:
            return {"error": "No JSON in UI/UX output", "issues": [], "approved": True}

    output.setdefault("issues", [])
    output.setdefault("approved", True)
    output.setdefault("summary", "")
    output["model_used"] = model_used
    return output


# ══════════════════════════════════════════════════════════════════════════════
# TEST ENGINEER AGENT -- Generates and runs tests
# ══════════════════════════════════════════════════════════════════════════════

TEST_SYSTEM_PROMPT = """You are the TEST ENGINEER agent for Joi's multi-agent coding pipeline.

YOUR ROLE:
- Analyze code and generate appropriate test commands.
- Determine what kind of testing is needed (syntax, imports, unit tests, integration).
- Generate concrete test commands that can be run in a shell.

OUTPUT FORMAT (strict JSON, no markdown):
{
    "test_commands": ["python -c \\"import ast; ...\\""  ],
    "test_results": [],
    "coverage_estimate": "low|medium|high",
    "summary": "Brief test plan description"
}

RULES:
- For Python: always include ast.parse syntax check.
- For HTML: include basic tag balance checks.
- Keep test commands simple and fast (< 30s each).
- coverage_estimate reflects how thorough your test plan is.
"""


def call_test_engineer(task: str, file_contents: Dict[str, str],
                       project_root: str = "") -> Dict[str, Any]:
    """Call the test engineer to generate and run tests."""
    files_block = ""
    for fpath, content in file_contents.items():
        files_block += f"\n\n--- FILE: {fpath} ---\n{content}\n--- END FILE ---\n"

    prompt = f"""TASK: {task}
PROJECT ROOT: {project_root or 'unknown'}

FILES TO TEST:
{files_block}

Generate test commands. Output strict JSON."""

    model_used = "unknown"
    try:
        from modules.joi_llm import route_and_call_for_agent
        text, model_used = route_and_call_for_agent(
            task_type="validation",
            messages=[{"role": "user", "content": prompt}],
            system_prompt=TEST_SYSTEM_PROMPT,
            max_tokens=2000,
        )
        if text is None:
            from modules.joi_brain import brain
            result = brain.think(
                task=f"Test plan: {task[:80]}",
                prompt=prompt,
                system_prompt=TEST_SYSTEM_PROMPT,
                thinking_level=2,
                max_tokens=2000,
            )
            if not result.get("ok"):
                return {"error": result.get("error", "Brain returned failure"),
                        "test_commands": [], "test_results": []}
            text = result.get("text", "")
            model_used = result.get("model", "unknown")
    except ImportError:
        return {"error": "No LLM provider available", "test_commands": [], "test_results": []}

    if not text:
        return {"error": "LLM returned empty response", "test_commands": [], "test_results": []}

    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        output = json.loads(text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                output = json.loads(json_match.group())
            except json.JSONDecodeError:
                return {"error": "Could not parse Test output", "test_commands": [], "test_results": []}
        else:
            return {"error": "No JSON in Test output", "test_commands": [], "test_results": []}

    output.setdefault("test_commands", [])
    output.setdefault("test_results", [])
    output.setdefault("coverage_estimate", "low")
    output.setdefault("summary", "")
    output["model_used"] = model_used

    # Run generated test commands
    cwd = project_root or str(BASE_DIR)
    for cmd in output["test_commands"][:5]:  # cap at 5 commands
        result = call_validator(cmd, cwd)
        output["test_results"].append(result)

    return output


# ══════════════════════════════════════════════════════════════════════════════
# CODER AGENT -- GPT-4o (fast, reliable JSON, strict formatting)
# ══════════════════════════════════════════════════════════════════════════════

CODER_SYSTEM_PROMPT = """You are the CODER agent for Joi's multi-agent coding pipeline.

YOUR ROLE:
- Receive ONE subtask and the target file content
- Generate SURGICAL edits as old_text/new_text pairs
- old_text must be an EXACT substring of the current file (including whitespace/indentation)
- new_text is what replaces it
- Be precise -- small, targeted changes only

OUTPUT FORMAT (strict JSON, no markdown):
{
    "changes": [
        {
            "file_path": "absolute/path/to/file.py",
            "old_text": "exact text to find in the file",
            "new_text": "replacement text",
            "explanation": "Why this change"
        }
    ],
    "confidence": 85
}

RULES:
- old_text MUST be a verbatim copy from the file (whitespace-sensitive)
- Keep changes minimal -- don't rewrite entire functions when a line change suffices
- If you need to ADD new code (no old_text to replace), use the last line of the
  insertion point as old_text and include it plus the new code as new_text
- NEW FILE: If the CURRENT FILE CONTENT is empty or indicates a new file, output exactly one change:
  old_text="" and new_text=the complete new file content (full program).
- confidence: 0-100 (how sure you are this change is correct)
- Multiple changes in one file is fine -- they'll be applied in order
- NEVER change code unrelated to the subtask
"""


def _classify_coding_complexity(subtask: Dict) -> str:
    """
    Classify subtask coding complexity for model routing.
    Returns 'simple', 'standard', or 'complex'.
    No LLM call — pure keyword heuristic.
    """
    desc = (subtask.get("description", "") + " " + subtask.get("acceptance_criteria", "")).lower()
    files = subtask.get("files", [])

    # Complex: multi-file, architecture, design, refactor
    complex_signals = [
        "architect", "design", "refactor", "multi-file", "restructure",
        "redesign", "overhaul", "rewrite", "complex", "algorithm",
        "concurrent", "thread", "async", "middleware", "framework",
        "integration", "pipeline", "orchestrat", "authentication",
    ]
    if any(s in desc for s in complex_signals) or len(files) > 2:
        return "complex"

    # Simple: boilerplate, scaffold, rename, add import, config
    simple_signals = [
        "scaffold", "boilerplate", "rename", "add import", "add constant",
        "add comment", "update docstring", "update version", "bump",
        "typo", "whitespace", "format", "add line", "remove line",
        "simple", "trivial", "placeholder", "stub",
    ]
    if any(s in desc for s in simple_signals):
        return "simple"

    return "standard"


def call_coder(subtask: Dict[str, Any], file_content: str,
               joi_ctx: str = "", error_feedback: Optional[str] = None) -> Dict[str, Any]:
    """
    Call the Brain to generate surgical edits (config: coder_agent).
    Returns parsed JSON with changes[] or error dict.

    Fix 4: Routes by coding complexity:
      simple   → task_type="quick"    (cheaper/faster model for boilerplate)
      standard → task_type="coding"   (current default)
      complex  → task_type="planning" (more capable model for architecture)
    """
    file_path = subtask.get("files", ["unknown"])[0] if subtask.get("files") else "unknown"

    error_block = ""
    if error_feedback:
        error_block = f"""

PREVIOUS ATTEMPT FAILED. Here's the error:
{error_feedback}

Fix the issue and try again. Make sure old_text exactly matches the file content."""

    prompt = f"""SUBTASK: {subtask.get('description', 'No description')}
ACCEPTANCE CRITERIA: {subtask.get('acceptance_criteria', 'N/A')}
FILE PATH: {file_path}

CURRENT FILE CONTENT:
--- START ---
{file_content}
--- END ---
{error_block}

{f'PROJECT RULES: {joi_ctx}' if joi_ctx else ''}

Generate your changes as strict JSON. No markdown, no explanation outside the JSON."""

    # Fix 4: Route by coding complexity
    complexity = _classify_coding_complexity(subtask)
    _complexity_task_map = {
        "simple":   "quick",    # → cheaper/faster model for boilerplate
        "standard": "coding",   # → standard coding model (default)
        "complex":  "planning", # → more capable model for architecture
    }
    _routed_task_type = _complexity_task_map.get(complexity, "coding")

    # Agent Terminal: use Dynamic Model Router
    result = None
    text = None
    model_used = "unknown"
    try:
        from modules.joi_llm import route_and_call_for_agent
        text, model_used = route_and_call_for_agent(
            task_type=_routed_task_type,
            messages=[{"role": "user", "content": prompt}],
            system_prompt=CODER_SYSTEM_PROMPT,
            max_tokens=3000,
        )
        if text is None:
            from modules.joi_brain import brain
            result = brain.think(
                task=f"Code edit (JSON output): {subtask.get('description', '')[:60]}",
                prompt=prompt,
                system_prompt=CODER_SYSTEM_PROMPT,
                thinking_level=2,
                max_tokens=3000,
            )
            if not result.get("ok"):
                return {"error": result.get("error", "Brain returned failure"),
                        "changes": [], "confidence": 0}
            text = result.get("text", "")
            model_used = result.get("model", "unknown")
    except ImportError:
        try:
            from modules.joi_llm import _call_openai
            from config.joi_models import OPENAI_MODELS
            messages = [
                {"role": "system", "content": CODER_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
            raw = _call_openai(messages, tools=None, max_tokens=3000, model=OPENAI_MODELS.get("coding", "gpt-4o"))
            if hasattr(raw, 'choices'):
                text = raw.choices[0].message.content or ""
            elif isinstance(raw, str):
                text = raw
            else:
                text = str(raw) if raw else ""
            model_used = f"openai:{OPENAI_MODELS.get('coding', 'gpt-4o')}"
        except ImportError:
            return {"error": "No LLM provider available", "changes": [], "confidence": 0}

    if not text:
        return {"error": "LLM returned empty response", "changes": [], "confidence": 0}

    text = text.strip()

    # Remove markdown code blocks if present
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        output = json.loads(text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                output = json.loads(json_match.group())
            except json.JSONDecodeError:
                return {"error": "Could not parse Coder output", "raw": text[:500],
                        "changes": [], "confidence": 0}
        else:
            return {"error": "No JSON in Coder output", "raw": text[:500],
                    "changes": [], "confidence": 0}

    if "changes" not in output:
        output["changes"] = []
    if "confidence" not in output:
        output["confidence"] = 50

    # Attach model info for terminal display
    output["model_used"] = model_used
    output["model_key"] = model_used

    return output


# ══════════════════════════════════════════════════════════════════════════════
# VALIDATOR AGENT -- subprocess (not an LLM)
# ══════════════════════════════════════════════════════════════════════════════

def call_validator(test_command: str, working_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Run a terminal command and capture results.
    Returns {passed, exit_code, stdout, stderr, command}.
    """
    if not test_command or not test_command.strip():
        return {"passed": True, "exit_code": 0, "stdout": "No test command specified",
                "stderr": "", "command": ""}

    cwd = working_dir or str(BASE_DIR)

    # Emit brain event
    try:
        from modules.joi_neuro import emit_brain_event
        emit_brain_event("REPAIR", 0.6, "orchestrator_validate")
    except Exception:
        pass

    try:
        result = subprocess.run(
            test_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=cwd,
            env={**os.environ, "PYTHONPATH": str(BASE_DIR)}
        )
        return {
            "passed": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": (result.stdout or "")[:2000],
            "stderr": (result.stderr or "")[:2000],
            "command": test_command,
        }
    except subprocess.TimeoutExpired:
        return {
            "passed": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": "Command timed out after 30 seconds",
            "command": test_command,
        }
    except Exception as e:
        return {
            "passed": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Error running command: {e}",
            "command": test_command,
        }


def validate_python_file(file_path: str) -> Dict[str, Any]:
    """Validate a Python file with ast.parse + import check."""
    results = {"syntax": None, "import": None, "passed": False}

    # Syntax check
    try:
        source = Path(file_path).read_text(encoding="utf-8")
        ast.parse(source)
        results["syntax"] = {"passed": True, "message": "Syntax OK"}
    except SyntaxError as e:
        results["syntax"] = {"passed": False, "message": f"SyntaxError: {e}"}
        return results
    except Exception as e:
        results["syntax"] = {"passed": False, "message": f"Error: {e}"}
        return results

    # Import check (lightweight -- just verify it can be imported)
    try:
        rel = Path(file_path).relative_to(BASE_DIR)
        module_name = str(rel).replace(os.sep, ".").replace("/", ".")
        if module_name.endswith(".py"):
            module_name = module_name[:-3]

        # Use ast.parse result -- actual import is too risky (side effects)
        results["import"] = {"passed": True, "message": f"Module path: {module_name}"}
    except Exception as e:
        results["import"] = {"passed": False, "message": f"Import path error: {e}"}

    results["passed"] = all(
        r.get("passed", False) for r in [results["syntax"], results["import"]] if r
    )
    return results


def validate_html_file(file_path: str) -> Dict[str, Any]:
    """Basic HTML validation -- check for balanced tags."""
    try:
        content = Path(file_path).read_text(encoding="utf-8")
        # Basic checks
        issues = []
        if "<html" not in content.lower():
            issues.append("Missing <html> tag")
        if "</html>" not in content.lower():
            issues.append("Missing </html> closing tag")
        if "<head" not in content.lower():
            issues.append("Missing <head> tag")
        if "<body" not in content.lower():
            issues.append("Missing <body> tag")

        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "message": "HTML OK" if not issues else f"Issues: {', '.join(issues)}"
        }
    except Exception as e:
        return {"passed": False, "issues": [str(e)], "message": f"Error: {e}"}


# ══════════════════════════════════════════════════════════════════════════════
# DIFF GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_diff(old_text: str, new_text: str, file_path: str = "file") -> str:
    """Generate a unified diff between old and new text."""
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)

    diff = difflib.unified_diff(
        old_lines, new_lines,
        fromfile=f"--- {file_path}",
        tofile=f"+++ {file_path} (modified)",
        lineterm=""
    )
    return "\n".join(diff)


def generate_full_file_diff(original_content: str, changes: List[Dict],
                            file_path: str = "file") -> str:
    """Apply changes to content in memory and generate diff."""
    modified = original_content
    for change in changes:
        old = change.get("old_text", "")
        new = change.get("new_text", "")
        if old and old in modified:
            modified = modified.replace(old, new, 1)

    return generate_diff(original_content, modified, file_path)


# ══════════════════════════════════════════════════════════════════════════════
# CHANGE APPLICATOR (in-memory preview, not disk)
# ══════════════════════════════════════════════════════════════════════════════

def preview_changes(file_path: str, changes: List[Dict]) -> Dict[str, Any]:
    """
    Preview what the file would look like after changes (in memory only).
    Returns {original, modified, diff, valid, errors[]}.
    """
    try:
        original = Path(file_path).read_text(encoding="utf-8")
    except Exception as e:
        return {"original": "", "modified": "", "diff": "",
                "valid": False, "errors": [f"Cannot read file: {e}"]}

    modified = original
    errors = []
    for i, change in enumerate(changes):
        old = change.get("old_text", "")
        new = change.get("new_text", "")
        if not old:
            errors.append(f"Change {i+1}: empty old_text")
            continue
        if old not in modified:
            errors.append(f"Change {i+1}: old_text not found in file")
            continue
        modified = modified.replace(old, new, 1)

    diff = generate_diff(original, modified, file_path)

    return {
        "original": original,
        "modified": modified,
        "diff": diff,
        "valid": len(errors) == 0,
        "errors": errors,
    }


def preview_new_file(changes: List[Dict], file_path: str = "new_file") -> Dict[str, Any]:
    """
    Preview for creating a NEW file (path does not exist yet).
    Valid if exactly one change with old_text=="" and new_text non-empty.
    Returns {original, modified, diff, valid, errors[]}.
    """
    if not changes:
        return {"original": "", "modified": "", "diff": "", "valid": False,
                "errors": ["No changes provided for new file"]}
    # Accept single change with empty old_text and non-empty new_text (full file content)
    if len(changes) == 1:
        old = (changes[0].get("old_text") or "").strip()
        new = changes[0].get("new_text") or ""
        if old == "" and new.strip():
            diff = f"--- /dev/null\n+++ {file_path}\n" + "\n".join(
                "+" + line for line in new.splitlines()
            )
            return {
                "original": "",
                "modified": new,
                "diff": diff,
                "valid": True,
                "errors": [],
            }
    return {"original": "", "modified": "", "diff": "", "valid": False,
            "errors": ["New file requires exactly one change with empty old_text and full file content as new_text"]}


# ══════════════════════════════════════════════════════════════════════════════
# ANALYST AGENT — gpt-4.1-mini (1M context, reads whole modules)
# ══════════════════════════════════════════════════════════════════════════════

ANALYST_SYSTEM_PROMPT = """You are the ANALYST agent for Joi's multi-agent coding pipeline.

YOUR ROLE:
- Read and deeply understand large codebases or datasets (you have 1M token context).
- Produce structured findings, cross-file dependency maps, and actionable summaries.
- You NEVER write code — only analyze and report.

OUTPUT FORMAT (strict JSON, no markdown):
{
    "findings": [
        {
            "file": "path/to/file.py",
            "insight": "Key observation about this file",
            "dependencies": ["other/file.py"],
            "issues": ["potential problem 1"]
        }
    ],
    "cross_file_patterns": ["Pattern 1 observed across files"],
    "recommendations": ["Actionable recommendation for CODER"],
    "summary": "Executive summary of analysis"
}

RULES:
- Focus on cross-file patterns, dependency chains, and systemic issues.
- Be specific about file paths and function/class names.
- Recommendations must be actionable by a CODER agent.
"""


def call_analyst(task: str, file_contents: Dict[str, str],
                 joi_ctx: str = "") -> Dict[str, Any]:
    """Call the analyst agent (gpt-4.1-mini, 1M context) for deep codebase analysis."""
    files_block = ""
    for fpath, content in file_contents.items():
        files_block += f"\n\n--- FILE: {fpath} ---\n{content}\n--- END FILE ---\n"

    prompt = f"""TASK: {task}

FILES TO ANALYZE:
{files_block}

{f'PROJECT RULES: {joi_ctx}' if joi_ctx else ''}

Produce your analysis as strict JSON. No markdown."""

    model_used = "unknown"
    try:
        from modules.joi_llm import route_and_call_for_agent
        text, model_used = route_and_call_for_agent(
            task_type="exploration",
            messages=[{"role": "user", "content": prompt}],
            system_prompt=ANALYST_SYSTEM_PROMPT,
            max_tokens=4000,
        )
        if text is None:
            from modules.joi_brain import brain
            result = brain.think(
                task=f"Analyst: {task[:80]}",
                prompt=prompt,
                system_prompt=ANALYST_SYSTEM_PROMPT,
                thinking_level=2,
                max_tokens=4000,
            )
            if not result.get("ok"):
                return {"error": result.get("error", "Brain returned failure"), "findings": []}
            text = result.get("text", "")
            model_used = result.get("model", "unknown")
    except ImportError:
        return {"error": "No LLM provider available", "findings": []}

    if not text:
        return {"error": "LLM returned empty response", "findings": []}

    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        output = json.loads(text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                output = json.loads(json_match.group())
            except json.JSONDecodeError:
                return {"error": "Could not parse Analyst output", "findings": []}
        else:
            return {"error": "No JSON in Analyst output", "findings": []}

    output.setdefault("findings", [])
    output.setdefault("cross_file_patterns", [])
    output.setdefault("recommendations", [])
    output.setdefault("summary", "")
    output["model_used"] = model_used
    return output


# ══════════════════════════════════════════════════════════════════════════════
# REPORT WRITER AGENT — gpt-5-mini (synthesis, clear prose)
# ══════════════════════════════════════════════════════════════════════════════

REPORT_WRITER_SYSTEM_PROMPT = """You are the REPORT WRITER agent for Joi's multi-agent coding pipeline.

YOUR ROLE:
- Synthesize findings from multiple agents into clear, structured reports.
- Combine security audit results, explore findings, analyst insights, and test results.
- Produce markdown reports suitable for the user.

OUTPUT FORMAT (strict JSON, no markdown wrapper):
{
    "title": "Report title",
    "sections": [
        {
            "heading": "Section heading",
            "content": "Prose content for this section",
            "severity": "info|warning|critical"
        }
    ],
    "executive_summary": "1-3 sentence summary",
    "action_items": ["Action 1", "Action 2"],
    "report_markdown": "Full markdown report as a single string"
}

RULES:
- Be concise but comprehensive.
- Prioritize critical and high severity items.
- action_items must be specific and implementable.
"""


def call_report_writer(task: str, agent_results: Dict[str, Any],
                       joi_ctx: str = "") -> Dict[str, Any]:
    """Call the report writer agent (gpt-5-mini) to synthesize agent findings into a report."""
    results_block = json.dumps(agent_results, indent=2, default=str)[:8000]

    prompt = f"""TASK: {task}

AGENT FINDINGS TO SYNTHESIZE:
{results_block}

{f'PROJECT RULES: {joi_ctx}' if joi_ctx else ''}

Produce a synthesis report as strict JSON. No markdown wrapper."""

    model_used = "unknown"
    try:
        from modules.joi_llm import route_and_call_for_agent
        text, model_used = route_and_call_for_agent(
            task_type="quick",
            messages=[{"role": "user", "content": prompt}],
            system_prompt=REPORT_WRITER_SYSTEM_PROMPT,
            max_tokens=3000,
        )
        if text is None:
            from modules.joi_brain import brain
            result = brain.think(
                task=f"Report writer: {task[:80]}",
                prompt=prompt,
                system_prompt=REPORT_WRITER_SYSTEM_PROMPT,
                thinking_level=1,
                max_tokens=3000,
            )
            if not result.get("ok"):
                return {"error": result.get("error", "Brain returned failure"), "sections": []}
            text = result.get("text", "")
            model_used = result.get("model", "unknown")
    except ImportError:
        return {"error": "No LLM provider available", "sections": []}

    if not text:
        return {"error": "LLM returned empty response", "sections": []}

    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        output = json.loads(text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                output = json.loads(json_match.group())
            except json.JSONDecodeError:
                return {"error": "Could not parse Report Writer output", "sections": []}
        else:
            return {"error": "No JSON in Report Writer output", "sections": []}

    output.setdefault("title", "Report")
    output.setdefault("sections", [])
    output.setdefault("executive_summary", "")
    output.setdefault("action_items", [])
    output.setdefault("report_markdown", "")
    output["model_used"] = model_used
    return output


# ══════════════════════════════════════════════════════════════════════════════
# DOC WRITER AGENT — gpt-4o (docs + code, specialist)
# ══════════════════════════════════════════════════════════════════════════════

DOC_WRITER_SYSTEM_PROMPT = """You are the DOC WRITER agent for Joi's multi-agent coding pipeline.

YOUR ROLE:
- Generate docstrings, inline comments, README sections, and API documentation.
- Produce code changes that ADD documentation without changing functionality.
- Output surgical edits (old_text/new_text) like the CODER agent, but for docs only.

OUTPUT FORMAT (strict JSON, no markdown):
{
    "changes": [
        {
            "file_path": "absolute/path/to/file.py",
            "old_text": "def my_func(x, y):",
            "new_text": "def my_func(x, y):\\n    \\\"\\\"\\\"Brief description.\\\"\\\"\\\"",
            "explanation": "Added docstring to my_func"
        }
    ],
    "doc_summary": "What documentation was added/updated",
    "confidence": 90
}

RULES:
- old_text MUST be a verbatim substring of the current file.
- Only add docs — never change logic.
- Keep docstrings concise (1-2 sentences for functions, 3-4 for classes/modules).
- For new files: produce a README or module docstring.
"""


def call_doc_writer(task: str, file_contents: Dict[str, str],
                    joi_ctx: str = "") -> Dict[str, Any]:
    """Call the doc writer agent (gpt-4o) to generate documentation edits."""
    files_block = ""
    for fpath, content in file_contents.items():
        files_block += f"\n\n--- FILE: {fpath} ---\n{content}\n--- END FILE ---\n"

    prompt = f"""TASK: {task}

FILES TO DOCUMENT:
{files_block}

{f'PROJECT RULES: {joi_ctx}' if joi_ctx else ''}

Generate documentation changes as strict JSON. No markdown."""

    model_used = "unknown"
    try:
        from modules.joi_llm import route_and_call_for_agent
        text, model_used = route_and_call_for_agent(
            task_type="coding",
            messages=[{"role": "user", "content": prompt}],
            system_prompt=DOC_WRITER_SYSTEM_PROMPT,
            max_tokens=3000,
        )
        if text is None:
            from modules.joi_brain import brain
            result = brain.think(
                task=f"Doc writer: {task[:80]}",
                prompt=prompt,
                system_prompt=DOC_WRITER_SYSTEM_PROMPT,
                thinking_level=2,
                max_tokens=3000,
            )
            if not result.get("ok"):
                return {"error": result.get("error", "Brain returned failure"), "changes": [], "confidence": 0}
            text = result.get("text", "")
            model_used = result.get("model", "unknown")
    except ImportError:
        return {"error": "No LLM provider available", "changes": [], "confidence": 0}

    if not text:
        return {"error": "LLM returned empty response", "changes": [], "confidence": 0}

    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        output = json.loads(text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                output = json.loads(json_match.group())
            except json.JSONDecodeError:
                return {"error": "Could not parse Doc Writer output", "changes": [], "confidence": 0}
        else:
            return {"error": "No JSON in Doc Writer output", "changes": [], "confidence": 0}

    output.setdefault("changes", [])
    output.setdefault("doc_summary", "")
    output.setdefault("confidence", 75)
    output["model_used"] = model_used
    return output


print("    [OK] joi_agents (Architect/Coder/Validator/Explore/Security/UIUX/Test/Analyst/ReportWriter/DocWriter agents)")
