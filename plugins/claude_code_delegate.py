"""
plugins/claude_code_delegate.py

Claude Code Delegation Plugin
Allows Joi to delegate coding tasks to Claude Code CLI tool.

Adapted for Joi's self-registering module architecture:
- Tools registered via joi_companion.register_tool()
- Functions accept **kwargs (matching joi_llm.py tool executor)
- Auto-initializes on import
"""

import os
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

import joi_companion

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_PATH = BASE_DIR / "config" / "claude_code.json"

# ============================================================================
# CONFIGURATION
# ============================================================================

def _load_config() -> Dict[str, Any]:
    """Load config from config/claude_code.json"""
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

_raw_config = _load_config()
CONFIG = _raw_config.get("claude_code", {})


# ============================================================================
# CLAUDE CODE DELEGATE CLASS
# ============================================================================

class ClaudeCodeDelegate:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.task_history: List[Dict[str, Any]] = []
        self.lock_file = DATA_DIR / "claude_code.lock"
        self.task_queue = DATA_DIR / "claude_code_queue.json"

    def is_claude_code_running(self) -> bool:
        """Check if Claude Code is currently active"""
        return self.lock_file.exists()

    def create_lock(self) -> None:
        """Create lock file to prevent conflicts"""
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        self.lock_file.write_text(json.dumps({
            "created_at": datetime.now().isoformat(),
            "pid": os.getpid()
        }, indent=2))

    def release_lock(self) -> None:
        """Release lock file"""
        try:
            if self.lock_file.exists():
                self.lock_file.unlink()
        except OSError:
            pass

    def delegate_task(self, task_description: str,
                      files: Optional[List[str]] = None,
                      context: Optional[str] = None) -> Dict[str, Any]:
        """
        Delegate a coding task to Claude Code.

        Args:
            task_description: Natural language description of the task
            files: Optional list of specific files to work on
            context: Additional context or constraints

        Returns:
            dict with task status and information
        """
        if self.is_claude_code_running():
            return {
                "ok": True,
                "status": "queued",
                "message": "Claude Code is already running. Task added to queue.",
                "task_id": self._queue_task(task_description, files, context)
            }

        task_id = f"task_{int(time.time())}"

        # Build the command
        cmd = self._build_command(task_description, files, context)

        # Create lock
        self.create_lock()

        # Log the task
        self.active_tasks[task_id] = {
            "description": task_description,
            "files": files,
            "started_at": datetime.now().isoformat(),
            "status": "running"
        }

        try:
            timeout = self.config.get("max_timeout", 300)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(BASE_DIR)
            )

            task_result = {
                "ok": True,
                "task_id": task_id,
                "status": "completed" if result.returncode == 0 else "failed",
                "stdout": result.stdout[-2000:] if result.stdout else "",
                "stderr": result.stderr[-1000:] if result.stderr else "",
                "return_code": result.returncode
            }

        except subprocess.TimeoutExpired:
            task_result = {
                "ok": False,
                "task_id": task_id,
                "status": "timeout",
                "error": f"Task exceeded {timeout}s timeout"
            }
        except FileNotFoundError:
            task_result = {
                "ok": False,
                "task_id": task_id,
                "status": "error",
                "error": "Claude Code CLI not found. Ensure 'claude' is installed and on PATH."
            }
        except Exception as e:
            task_result = {
                "ok": False,
                "task_id": task_id,
                "status": "error",
                "error": str(e)
            }
        finally:
            self.release_lock()

            # Update task history
            if task_id in self.active_tasks:
                self.active_tasks[task_id]["completed_at"] = datetime.now().isoformat()
                self.active_tasks[task_id]["status"] = task_result.get("status", "unknown")
                self.task_history.append(self.active_tasks[task_id])
                del self.active_tasks[task_id]

        # Notify monitor if available
        try:
            from plugins.system_monitor_dashboard import monitor
            monitor.log_activity("claude_code", f"Task {task_result['status']}: {task_description[:80]}", {
                "task_id": task_id,
                "status": task_result["status"]
            })
        except Exception:
            pass

        return task_result

    def _build_command(self, task_description: str,
                       files: Optional[List[str]] = None,
                       context: Optional[str] = None) -> List[str]:
        """Build Claude Code CLI command"""
        cli = self.config.get("cli_command", "claude")
        cmd = [cli]

        prompt = task_description

        if context:
            prompt += f"\n\nAdditional context: {context}"

        if files:
            prompt += f"\n\nFocus on these files: {', '.join(files)}"

        cmd.extend(["--print", "--message", prompt])

        if self.config.get("auto_approve"):
            cmd.append("--dangerously-skip-permissions")

        return cmd

    def _queue_task(self, task_description: str,
                    files: Optional[List[str]],
                    context: Optional[str]) -> str:
        """Add task to queue for later execution"""
        task_id = f"queued_{int(time.time())}"

        queue: List[Dict[str, Any]] = []
        if self.task_queue.exists():
            try:
                queue = json.loads(self.task_queue.read_text(encoding="utf-8"))
            except Exception:
                queue = []

        queue.append({
            "task_id": task_id,
            "description": task_description,
            "files": files,
            "context": context,
            "queued_at": datetime.now().isoformat()
        })

        self.task_queue.parent.mkdir(parents=True, exist_ok=True)
        self.task_queue.write_text(json.dumps(queue, indent=2))

        return task_id

    def process_queue(self) -> Dict[str, Any]:
        """Process next queued task"""
        if not self.task_queue.exists():
            return {"ok": True, "status": "no_queue", "message": "No tasks in queue"}

        try:
            queue = json.loads(self.task_queue.read_text(encoding="utf-8"))
        except Exception:
            return {"ok": False, "error": "Failed to read task queue"}

        if not queue:
            return {"ok": True, "status": "empty", "message": "Queue is empty"}

        # Pop first task
        task = queue.pop(0)

        # Update queue file
        self.task_queue.write_text(json.dumps(queue, indent=2))

        # Delegate it
        return self.delegate_task(
            task["description"],
            task.get("files"),
            task.get("context")
        )

    def get_status(self) -> Dict[str, Any]:
        """Get current status of Claude Code tasks"""
        queue_size = 0
        if self.task_queue.exists():
            try:
                queue_size = len(json.loads(self.task_queue.read_text(encoding="utf-8")))
            except Exception:
                pass

        return {
            "is_running": self.is_claude_code_running(),
            "active_tasks": len(self.active_tasks),
            "queued_tasks": queue_size,
            "completed_tasks": len(self.task_history),
            "recent_history": self.task_history[-10:]
        }


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

delegate = ClaudeCodeDelegate(CONFIG)


# ============================================================================
# TOOL FUNCTIONS (called by LLM via **kwargs)
# ============================================================================

def delegate_to_claude_code(**kwargs) -> Dict[str, Any]:
    """Tool: Delegate a coding task to Claude Code CLI"""
    task_description = kwargs.get("task_description", "")
    if not task_description:
        return {"ok": False, "error": "task_description is required"}

    files = kwargs.get("files")
    context = kwargs.get("context")
    return delegate.delegate_task(task_description, files, context)


def check_claude_code_status(**kwargs) -> Dict[str, Any]:
    """Tool: Check Claude Code status and queue"""
    return {"ok": True, **delegate.get_status()}


def process_claude_code_queue(**kwargs) -> Dict[str, Any]:
    """Tool: Process next task in the Claude Code queue"""
    return delegate.process_queue()


# ============================================================================
# TOOL REGISTRATION (Joi's self-registering pattern)
# ============================================================================

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "delegate_to_claude_code",
        "description": "Delegate a coding task to Claude Code CLI. Use this when Lonnie asks you to create new functions, fix bugs, refactor code, or make file changes. Claude Code will autonomously edit files.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_description": {
                    "type": "string",
                    "description": "Clear description of what needs to be coded/fixed"
                },
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of specific files to modify"
                },
                "context": {
                    "type": "string",
                    "description": "Additional context, constraints, or requirements"
                }
            },
            "required": ["task_description"]
        }
    }},
    delegate_to_claude_code
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "check_claude_code_status",
        "description": "Check if Claude Code is currently running and view task queue status",
        "parameters": {"type": "object", "properties": {}}
    }},
    check_claude_code_status
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "process_claude_code_queue",
        "description": "Process the next task in the Claude Code queue",
        "parameters": {"type": "object", "properties": {}}
    }},
    process_claude_code_queue
)

print("    + Claude Code delegation tools registered")
