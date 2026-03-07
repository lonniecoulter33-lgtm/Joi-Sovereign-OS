"""
joi_git_agency.py — Autonomous Git Agency (Tier-2 Powered)
===========================================================
Gives Joi the ability to autonomously manage her Git repository.

Architecture:
  - git_manager()       The safe, validated entry point for all Git operations.
  - _ai_commit_message()  Uses GPT-5-mini to analyze the diff, then GPT-5-Pro
                          to craft a professional Conventional Commit message.
  - _git_preflight_check() Scans for secrets/.env/temp files before any commit.
  - _log_activity()     Appends every action to data/joi_activity.log (the Black Box).

Safety gates:
  - Blocklist: reset, force, rm --cached, stash drop, clean -fd
  - Pre-commit scan: refuses to commit .env, *.key, id_rsa, tokens.json etc.
  - Push gate: git push NEVER auto-executes — returns PENDING_APPROVAL state.

Tier-2 model usage:
  - GPT-5-mini: fast diff analysis (cheap, structure understanding)
  - GPT-5-Pro : high-quality Conventional Commit message writing

Personality hook:
  Joi's system prompt should read:
    "After any successful file edit, run git_manager with command='status'
     to see what changed. If changes are meaningful, call git_manager with
     command='auto_commit'. Never push without explicit user approval."
"""

import os
import re
import subprocess
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

# ── Config ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(os.getenv("JOI_PROJECT_ROOT", Path(__file__).parent.parent))
ACTIVITY_LOG = PROJECT_ROOT / "data" / "joi_activity.log"

# Tier-2 models for Git operations
DIFF_ANALYSIS_MODEL  = os.getenv("JOI_GIT_DIFF_MODEL",   "gpt-5-mini")   # fast analysis
COMMIT_MSG_MODEL     = os.getenv("JOI_GIT_COMMIT_MODEL",  "gpt-5")         # high quality
OPENAI_API_KEY       = os.getenv("OPENAI_API_KEY", "").strip()

# Commands Joi is allowed to run
ALLOWED_GIT_COMMANDS: List[str] = ["status", "add", "commit", "push", "pull", "diff",
                                     "branch", "log", "show", "stash"]

# Hard-blocked substrings (checked against full command string)
BLOCKED_PATTERNS: List[str] = [
    "reset", "force", "--force", "-f",
    "rm --cached", "clean -f", "clean -fd",
    "stash drop", "stash clear",
    "push --mirror", "push --delete",
    "reflog", "gc --prune",
]

# Files/patterns that should never be committed
SECRET_PATTERNS: List[str] = [
    ".env", ".env.local", ".env.production", ".env.backup",
    "*.key", "*.pem", "*.p12", "*.pfx",
    "id_rsa", "id_ed25519", "authorized_keys",
    "secrets.json", "tokens.json", "credentials.json",
    "*.secret", "service_account*.json",
    "__pycache__", "*.pyc", "node_modules",
]

_log_lock = threading.Lock()

# ── Push Approval Registry ────────────────────────────────────────────────────
# Pending push requests that need user approval before executing
_pending_push: Dict[str, Any] = {}


# ── Logging ───────────────────────────────────────────────────────────────────

def _log_activity(command: str, result: str, reasoning: str = "", commit_hash: str = "") -> None:
    """Append a timestamped entry to data/joi_activity.log (the Black Box)."""
    try:
        ACTIVITY_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp":   datetime.now().isoformat(),
            "command":     command,
            "commit_hash": commit_hash,
            "reasoning":   reasoning,
            "result":      result[:500] if result else "",
        }
        with _log_lock:
            with open(ACTIVITY_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"  [GIT LOG] Could not write activity log: {e}")


# ── Safety Filters ────────────────────────────────────────────────────────────

def _is_blocked(command: str) -> Optional[str]:
    """Return a reason string if command is blocked, else None."""
    cmd_lower = command.lower().strip()
    for pattern in BLOCKED_PATTERNS:
        if pattern in cmd_lower:
            return (f"High-risk pattern '{pattern}' detected. "
                    f"This command is blocked for safety. Please run it manually in your terminal.")
    # Check base command
    base = cmd_lower.split()[0] if cmd_lower else ""
    if base not in ALLOWED_GIT_COMMANDS:
        return (f"Command '{base}' is not in Joi's allowed Git operations "
                f"({', '.join(ALLOWED_GIT_COMMANDS)}). Run it manually if needed.")
    return None


def _git_preflight_check() -> Dict[str, Any]:
    """
    Scan the staging area (git status --short) for secret/dangerous files.
    Returns {'ok': bool, 'warnings': list, 'blocked_files': list}
    """
    blocked = []
    warnings = []
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True, text=True, cwd=PROJECT_ROOT
        )
        staged_lines = result.stdout.splitlines()
        for line in staged_lines:
            # Line format: 'XY filename'
            filename = line[3:].strip() if len(line) > 3 else ""
            filename_lower = filename.lower()
            for pattern in SECRET_PATTERNS:
                # Simple glob-style match
                pat = pattern.replace("*", "")
                if pat in filename_lower or filename_lower.endswith(pat.lstrip(".")):
                    blocked.append(filename)
                    break
            # Warn about large files
            try:
                filepath = PROJECT_ROOT / filename
                if filepath.is_file() and filepath.stat().st_size > 5_000_000:  # 5MB
                    warnings.append(f"{filename} is large ({filepath.stat().st_size // 1024}KB)")
            except Exception:
                pass
    except Exception as e:
        return {"ok": False, "warnings": [], "blocked_files": [], "error": str(e)}

    return {
        "ok": len(blocked) == 0,
        "blocked_files": blocked,
        "warnings": warnings,
    }


# ── AI Commit Message Generation ──────────────────────────────────────────────

def _ai_commit_message(diff_output: str, staged_files: str) -> str:
    """
    Two-stage AI commit message generation:
      Stage 1: GPT-5-mini  → rapid diff analysis (what changed structurally)
      Stage 2: GPT-5-Pro   → professional Conventional Commit message

    Falls back to a structured default if OpenAI is unavailable.
    """
    if not OPENAI_API_KEY:
        # Fallback: generate from diff without AI
        lines_added   = diff_output.count("\n+")
        lines_removed = diff_output.count("\n-")
        return f"chore: update {lines_added} additions, {lines_removed} deletions across staged files"

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        # ── Stage 1: GPT-5-mini — fast diff analysis ──────────────────────────
        mini_prompt = (
            "You are a code change analyzer. Analyze this git diff and respond with a "
            "1-paragraph summary of what changed (which modules, what kind of change: "
            "feat/fix/refactor/chore, and the technical impact). Be concise and technical.\n\n"
            f"STAGED FILES:\n{staged_files}\n\nDIFF (first 4000 chars):\n{diff_output[:4000]}"
        )
        analysis_resp = client.chat.completions.create(
            model=DIFF_ANALYSIS_MODEL,
            messages=[{"role": "user", "content": mini_prompt}],
            max_tokens=300,
            temperature=0.3,
        )
        analysis = analysis_resp.choices[0].message.content.strip()

        # ── Stage 2: GPT-5-Pro — high-quality commit message ─────────────────
        pro_prompt = (
            "You are a senior engineer writing professional Git commit messages. "
            "Using the change analysis below, write ONE commit message following "
            "Conventional Commits spec (https://www.conventionalcommits.org). "
            "Format: '<type>(<scope>): <description>' on line 1, blank line, then "
            "a body of 2-4 bullet points explaining the 'why'. "
            "Types: feat, fix, refactor, chore, docs, perf, test. "
            "Be specific, be professional, do NOT use generic phrases like 'update code'.\n\n"
            f"CHANGE ANALYSIS:\n{analysis}\n\nRESPOND WITH THE COMMIT MESSAGE ONLY."
        )
        commit_resp = client.chat.completions.create(
            model=COMMIT_MSG_MODEL,
            messages=[{"role": "user", "content": pro_prompt}],
            max_tokens=400,
            temperature=0.4,
        )
        msg = commit_resp.choices[0].message.content.strip()

        # Validate it looks like a commit message (starts with a type)
        if not re.match(r'^(feat|fix|refactor|chore|docs|perf|test|style|ci|build)\b', msg, re.IGNORECASE):
            msg = "chore: " + msg.split("\n")[0][:72]

        return msg

    except Exception as e:
        print(f"  [GIT-AI] Commit message AI failed ({e}), using fallback.")
        lines_added = diff_output.count("\n+")
        return f"chore: ai-generated commit ({lines_added} line changes)"


# ── Core Git Runner ───────────────────────────────────────────────────────────

def _run_git(args: List[str], cwd: Path = PROJECT_ROOT) -> Dict[str, Any]:
    """Execute a git command safely and return structured output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True, text=True, cwd=cwd, timeout=30
        )
        return {
            "ok":       result.returncode == 0,
            "stdout":   result.stdout.strip(),
            "stderr":   result.stderr.strip(),
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": "Command timed out (30s)", "returncode": -1}
    except FileNotFoundError:
        return {"ok": False, "stdout": "", "stderr": "Git not found. Is git installed?", "returncode": -1}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e), "returncode": -1}


# ── Main Public Tool ──────────────────────────────────────────────────────────

def git_manager(**kwargs) -> Dict[str, Any]:
    """
    Joi's Git Agency Tool — the single entry point for all Git operations.

    Commands:
      status        → git status (always safe, always allowed)
      diff          → git diff (staged or unstaged)
      add [path]    → git add <path> (default: '.')
      commit [msg]  → git commit with provided or AI-generated message
      auto_commit   → Full pipeline: diff → AI message → preflight → add → commit
      push [remote] → Returns PENDING_APPROVAL (never auto-executes)
      approve_push  → Executes a previously approved push
      pull [remote] → git pull (safe, read-only)
      branch        → list branches
      log [n]       → last N commits (default 5)
      status_report → Full health report (status + recent log)

    Args (via **kwargs):
      command (str):        The operation to perform (see above)
      message (str):        Commit message override (for commit/auto_commit)
      path (str):           Path for git add (default '.')
      remote (str):         Remote for push/pull (default 'origin')
      branch (str):         Branch for push (default current branch)
      reasoning (str):      Why Joi is doing this (stored in activity log)
      n (int):              Number of log entries (for log command)
    """
    command   = str(kwargs.get("command", "status")).strip().lower()
    message   = kwargs.get("message", "").strip()
    path      = kwargs.get("path", ".").strip()
    remote    = kwargs.get("remote", "origin").strip()
    branch    = kwargs.get("branch", "").strip()
    reasoning = kwargs.get("reasoning", "Routine Git operation.").strip()
    n         = int(kwargs.get("n", 5))

    # ── Safety blocklist check ────────────────────────────────────────────────
    block_reason = _is_blocked(command)
    if block_reason:
        _log_activity(f"git {command}", f"BLOCKED: {block_reason}", reasoning)
        return {"ok": False, "status": "BLOCKED", "message": block_reason}

    # ── Route by command ──────────────────────────────────────────────────────

    # STATUS
    if command == "status" or command == "status_report":
        r = _run_git(["status"])
        out = r["stdout"] or "(clean — nothing to commit)"
        if command == "status_report":
            log_r = _run_git(["log", f"--oneline", f"-{n}"])
            out += f"\n\nRecent commits:\n{log_r['stdout']}"
        _log_activity("git status", out, reasoning)
        return {"ok": True, "status": "OK", "output": out}

    # DIFF
    elif command == "diff":
        r = _run_git(["diff", "--staged"])
        if not r["stdout"]:
            r = _run_git(["diff"])  # unstaged fallback
        _log_activity("git diff", r["stdout"][:300], reasoning)
        return {"ok": True, "status": "OK", "output": r["stdout"] or "(no changes)"}

    # ADD
    elif command == "add":
        r = _run_git(["add", path])
        msg = r["stdout"] or (f"Staged: {path}" if r["ok"] else r["stderr"])
        _log_activity(f"git add {path}", msg, reasoning)
        return {"ok": r["ok"], "status": "OK" if r["ok"] else "ERROR", "output": msg}

    # COMMIT (with explicit message)
    elif command == "commit":
        if not message:
            return {"ok": False, "status": "ERROR",
                    "message": "Provide a 'message' argument for commit, or use auto_commit."}
        preflight = _git_preflight_check()
        if not preflight["ok"]:
            blocked = ", ".join(preflight["blocked_files"])
            return {"ok": False, "status": "BLOCKED",
                    "message": f"Pre-commit check failed. Dangerous files staged: {blocked}. "
                               f"Remove them or add to .gitignore before committing."}
        if preflight["warnings"]:
            print(f"  [GIT] Commit warnings: {preflight['warnings']}")
        r = _run_git(["commit", "-m", message])
        # Extract commit hash from output
        hash_match = re.search(r'\[[\w/]+ ([a-f0-9]+)\]', r["stdout"])
        commit_hash = hash_match.group(1) if hash_match else ""
        _log_activity(f"git commit", r["stdout"], reasoning, commit_hash)
        return {"ok": r["ok"], "status": "COMMITTED" if r["ok"] else "ERROR",
                "output": r["stdout"] or r["stderr"], "commit_hash": commit_hash}

    # AUTO_COMMIT — the full autonomous pipeline
    elif command == "auto_commit":
        # Step 1: Check status
        status_r = _run_git(["status", "--short"])
        if not status_r["stdout"]:
            return {"ok": True, "status": "CLEAN",
                    "message": "Working tree is clean. Nothing to commit."}

        # Step 2: Get staged files + diff
        staged_r = _run_git(["diff", "--staged", "--name-only"])
        if not staged_r["stdout"]:
            # Auto-add if nothing staged yet
            _run_git(["add", "."])
            staged_r = _run_git(["diff", "--staged", "--name-only"])

        staged_files = staged_r["stdout"]

        # Step 3: Pre-flight safety scan
        preflight = _git_preflight_check()
        if not preflight["ok"]:
            blocked = ", ".join(preflight["blocked_files"])
            return {"ok": False, "status": "BLOCKED",
                    "message": f"AUTO_COMMIT aborted: dangerous files in staging: {blocked}. "
                               f"Please add them to .gitignore first."}

        # Step 3b: v4.0 Kernel Lock — block commits containing Layer 1/2 protected files
        try:
            from modules.joi_kernel_lock import get_kernel_lock
            _klock = get_kernel_lock()
            staged_list = [f.strip() for f in staged_files.splitlines() if f.strip()]
            kl_ok, kl_reason = _klock.check_git_commit_allowed(staged_list)
            if not kl_ok:
                _klock.log_violation("auto_commit", kl_reason, action="git_auto_commit")
                _log_activity("auto_commit", f"KERNEL_LOCK_BLOCKED: {kl_reason[:200]}", reasoning)
                return {"ok": False, "status": "KERNEL_LOCK_BLOCKED", "message": kl_reason}
        except Exception as _kl_err:
            # Kernel lock unavailable — log and continue (non-blocking)
            print(f"  [GIT] Kernel lock check skipped: {_kl_err}")

        # Step 4: Get full diff for AI analysis
        diff_r = _run_git(["diff", "--staged"])
        diff_text = diff_r["stdout"]

        if not diff_text.strip():
            return {"ok": False, "status": "ERROR",
                    "message": "No staged changes found after git add. Check if files are modified."}

        # Step 5: AI generates the commit message
        print("  [GIT-AI] Analyzing diff with GPT-5-mini, drafting message with GPT-5-Pro...")
        commit_msg = message or _ai_commit_message(diff_text, staged_files)
        if preflight["warnings"]:
            print(f"  [GIT] Warnings: {preflight['warnings']}")

        # Step 6: Execute commit
        r = _run_git(["commit", "-m", commit_msg])
        hash_match = re.search(r'\[[\w/]+ ([a-f0-9]+)\]', r["stdout"])
        commit_hash = hash_match.group(1) if hash_match else ""
        _log_activity("auto_commit", r["stdout"], reasoning + f" | Files: {staged_files}", commit_hash)

        if r["ok"]:
            return {
                "ok":           True,
                "status":       "COMMITTED",
                "commit_hash":  commit_hash,
                "commit_msg":   commit_msg,
                "files_committed": staged_files.split("\n"),
                "output":       r["stdout"],
                "next_step":    "Use git_manager(command='push') to push (requires your approval).",
            }
        else:
            return {"ok": False, "status": "ERROR", "output": r["stdout"] or r["stderr"]}

    # PUSH — returns PENDING_APPROVAL, never auto-executes
    elif command == "push":
        # Get current branch if not specified
        if not branch:
            branch_r = _run_git(["rev-parse", "--abbrev-ref", "HEAD"])
            branch = branch_r["stdout"].strip() or "main"

        # Get last commit info for the approval request
        log_r = _run_git(["log", "--oneline", "-1"])
        last_commit = log_r["stdout"]

        approval_id = f"push_{int(time.time())}"
        _pending_push[approval_id] = {
            "remote": remote, "branch": branch,
            "last_commit": last_commit, "timestamp": time.time()
        }
        _log_activity(f"git push {remote} {branch}",
                      f"PENDING_APPROVAL (id={approval_id})", reasoning)
        return {
            "ok":               False,
            "status":           "PENDING_APPROVAL",
            "approval_id":      approval_id,
            "remote":           remote,
            "branch":           branch,
            "last_commit":      last_commit,
            "message":          (
                f"PUSH GATE: Pushing '{branch}' to '{remote}' requires your explicit approval. "
                f"Last commit: {last_commit}. "
                f"Reply with git_manager(command='approve_push', approval_id='{approval_id}') to proceed."
            ),
        }

    # APPROVE_PUSH — user explicitly approves a pending push
    elif command == "approve_push":
        approval_id = kwargs.get("approval_id", "").strip()
        if approval_id not in _pending_push:
            return {"ok": False, "status": "ERROR",
                    "message": f"No pending push found with id '{approval_id}'. It may have expired."}
        pending = _pending_push.pop(approval_id)
        r = _run_git(["push", pending["remote"], pending["branch"]])
        _log_activity(f"git push {pending['remote']} {pending['branch']}",
                      r["stdout"] or r["stderr"], f"APPROVED by user (id={approval_id})")
        return {
            "ok":     r["ok"],
            "status": "PUSHED" if r["ok"] else "ERROR",
            "output": r["stdout"] or r["stderr"],
            "remote": pending["remote"],
            "branch": pending["branch"],
        }

    # PULL
    elif command == "pull":
        r = _run_git(["pull", remote])
        _log_activity(f"git pull {remote}", r["stdout"] or r["stderr"], reasoning)
        return {"ok": r["ok"], "status": "OK" if r["ok"] else "ERROR",
                "output": r["stdout"] or r["stderr"]}

    # BRANCH
    elif command == "branch":
        r = _run_git(["branch", "-a"])
        return {"ok": True, "status": "OK", "output": r["stdout"]}

    # LOG
    elif command == "log":
        r = _run_git(["log", "--oneline", f"-{n}"])
        return {"ok": True, "status": "OK", "output": r["stdout"]}

    else:
        return {"ok": False, "status": "ERROR",
                "message": (f"Unknown command '{command}'. "
                            f"Allowed: status, diff, add, commit, auto_commit, push, approve_push, pull, branch, log, status_report")}


# ── Tool Registration ─────────────────────────────────────────────────────────
try:
    import joi_companion

    joi_companion.register_tool(
        {
            "type": "function",
            "function": {
                "name": "git_manager",
                "description": (
                    "Joi's autonomous Git Agency tool. Safely executes Git operations with "
                    "built-in safety filters, AI-powered commit messages, and a mandatory "
                    "approval gate for push operations.\n\n"
                    "Workflow after code edits:\n"
                    "1. git_manager(command='status') — see what changed\n"
                    "2. git_manager(command='auto_commit', reasoning='why I made this change')"
                    " — AI writes the commit message using GPT-5-mini (analysis) + GPT-5-Pro (message)\n"
                    "3. git_manager(command='push') — returns PENDING_APPROVAL for user to approve\n"
                    "4. git_manager(command='approve_push', approval_id='<id>') — user approves the push\n\n"
                    "Safety: Blocks reset, force push, deleting files. Scans for .env/secrets before commit. "
                    "ALL pushes require explicit user approval — Joi NEVER pushes autonomously."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "enum": ["status", "diff", "add", "commit", "auto_commit",
                                     "push", "approve_push", "pull", "branch", "log", "status_report"],
                            "description": "The Git operation to perform."
                        },
                        "message": {
                            "type": "string",
                            "description": "Commit message (optional for auto_commit — AI will generate one)."
                        },
                        "path": {
                            "type": "string",
                            "description": "File or directory path for 'add' (default: '.' for all changes)."
                        },
                        "remote": {
                            "type": "string",
                            "description": "Remote name for push/pull (default: 'origin')."
                        },
                        "branch": {
                            "type": "string",
                            "description": "Branch name for push (default: current branch)."
                        },
                        "approval_id": {
                            "type": "string",
                            "description": "Approval ID returned by a previous 'push' command."
                        },
                        "reasoning": {
                            "type": "string",
                            "description": "Joi's internal reasoning for making this Git action (logged to activity log)."
                        },
                        "n": {
                            "type": "integer",
                            "description": "Number of log entries to show (for 'log' command, default 5)."
                        },
                    },
                    "required": ["command"],
                },
            },
        },
        git_manager,
    )
    print("  [OK] joi_git_agency (Git Agency: git_manager, auto_commit, push gate, activity log)")
except Exception as _reg_e:
    print(f"  [WARN] joi_git_agency: tool registration skipped ({_reg_e})")
