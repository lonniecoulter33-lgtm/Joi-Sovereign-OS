"""
modules/core/workers.py

Layer 1 --- Core Runtime: Worker Pool.
Manages specialized reasoning nodes (Local, Cloud, Sub-Agent).
Enables Joi to delegate heavy cognitive tasks.
"""
import threading
import time
from typing import List, Dict, Any, Optional
from modules.core.interfaces import JoiWorker
from modules.core.regulator import regulator

class WorkerRegistry:
    def __init__(self):
        self._workers: Dict[str, JoiWorker] = {}
        self._active_jobs = 0
        self._lock = threading.Lock()

    def register_worker(self, worker: JoiWorker):
        """Register a new specialized node."""
        with self._lock:
            self._workers[worker.name] = worker
        print(f"  [WORKER] Registered node: {worker.name} (caps={worker.capabilities})")

    def find_worker(self, capability: str) -> Optional[JoiWorker]:
        """Find a worker that matches the requested capability."""
        with self._lock:
            for worker in self._workers.values():
                if capability in worker.capabilities:
                    return worker
        return None

    def can_spawn(self) -> bool:
        """Check with regulator if we can handle more load."""
        limit = regulator.get_concurrency_limit()
        with self._lock:
            return self._active_jobs < limit

    def execute_async(self, worker_name: str, ctx: Any, task: Dict[str, Any], callback: Any):
        """Spawn a worker in a managed thread."""
        if not self.can_spawn():
            print(f"  [WORKER] Concurrency limit reached. Queuing task...")
            # Simple wait loop for this pilot
            while not self.can_spawn():
                time.sleep(1.0)

        def _run():
            with self._lock:
                self._active_jobs += 1
            
            try:
                worker = self._workers.get(worker_name)
                if worker:
                    result = worker.dispatch(ctx, task)
                    callback(result)
            finally:
                with self._lock:
                    self._active_jobs -= 1

        t = threading.Thread(target=_run, name=f"agent_{worker_name}", daemon=True)
        t.start()

class LocalSandboxWorker(JoiWorker):
    """
    Local Code Execution Sandbox.
    Runs Python code in an isolated subprocess with timeout.
    """
    def __init__(self):
        self.name = "local_sandbox"
        self.capabilities = ["code_execution", "unit_testing"]
        self.timeout = 30  # seconds

    def dispatch(self, ctx: Any, task: Dict[str, Any]) -> Any:
        import subprocess
        import sys

        task_type = task.get("type", "code_execution")
        code = task.get("code", "")

        if not code:
            return {"status": "error", "worker": self.name, "error": "No code provided"}

        print(f"  [WORKER] {self.name} executing: {task_type}")

        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=str(task.get("cwd", ".")),
            )
            return {
                "status": "completed",
                "worker": self.name,
                "exit_code": result.returncode,
                "stdout": result.stdout[:5000],
                "stderr": result.stderr[:2000],
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "worker": self.name, "error": f"Exceeded {self.timeout}s"}
        except Exception as e:
            return {"status": "error", "worker": self.name, "error": str(e)}

# Singleton Pool
pool = WorkerRegistry()
# Register Pilot
pool.register_worker(LocalSandboxWorker())
