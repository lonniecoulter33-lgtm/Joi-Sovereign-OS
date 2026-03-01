"""
modules/core/kernel.py

The Heart of Joi.
Manages the application lifecycle, service registration, and module loading.
"""
import importlib
import sys
import traceback
from typing import Dict, List, Any
from flask import Flask
from modules.core.config import config
from modules.core.registry import TOOLS, TOOL_EXECUTORS, ROUTES, CONTEXT_PROVIDERS

class JoiKernel:
    def __init__(self):
        self.config = config
        self.app = Flask(__name__)
        self.app.secret_key = self.config.APP_SECRET
        self.is_booted = False
        
        # Internal state tracking
        self.loaded_modules = []
        self.boot_errors = []
        
        # Ensure projects/code is importable (Phase 6 Alignment)
        code_path = str(self.config.BASE_DIR / "projects" / "code")
        if code_path not in sys.path:
            sys.path.append(code_path)

    def boot(self):
        """Perform deterministic startup sequence."""
        if self.is_booted:
            return
        
        print("\n" + "="*60)
        print(f"  JOI KERNEL -- Initializing Layer 1")
        print("="*60)

        try:
            self._check_dependencies()
            self._load_core_services()
            self._load_dynamic_modules()
            self._load_consciousness()
            self._load_plugins()
            self._register_routes()
            
            # Legacy context registration (bridge for Phase 3 -> 4)
            try:
                from joi_companion import _register_default_context_providers
                _register_default_context_providers()
            except ImportError:
                print("    [WARN] Could not register default context providers (joi_companion not found?)")
            
            # Start Autonomous Runtime (Phase 5)
            from modules.core.scheduler import scheduler
            from modules.core.engine import engine
            from modules.core.events import bus
            import modules.core.sensors 
            import modules.core.memory_graph
            import modules.core.modeling
            import modules.core.workers # Self-registers workers on import
            import modules.core.topology # Scans hardware environment
            
            # Phase 2: Introspection (Self-Awareness)
            from modules.core.introspection import engine as introspection_engine
            introspection_engine.scan()
            
            # Final Audit (Phase 6 Integration)
            from modules.core.registry import audit_features
            audit_features()
            
            bus.start()
            scheduler.start()
            engine.start()
            
            self.is_booted = True
            print(f"\n  KERNEL: Boot sequence complete. System Stable.")
            print("="*60 + "\n")
        except Exception as e:
            print(f"  [CRITICAL] Kernel boot failed: {e}")
            traceback.print_exc()
            sys.exit(1)

    def _check_dependencies(self):
        """Verify runtime environment."""
        print(f"  [0/5] Checking Environment...")
        missing = []
        for pkg in ["flask", "dotenv"]:
            try:
                __import__(pkg)
            except ImportError:
                missing.append(pkg)
        if missing:
            print(f"    [WARN] Missing packages: {', '.join(missing)}")
        else:
            print(f"    [OK] Core dependencies verified")
        # Check data directories exist
        for d in [self.config.DATA_DIR, self.config.LOG_DIR]:
            d.mkdir(parents=True, exist_ok=True)

    def _load_core_services(self):
        """Initialize foundational services (DB, Memory, etc)."""
        print(f"  [1/5] Loading Core Services...")
        # Ensure cognition DB is initialized
        try:
            from modules.core.cognition import graph
            print(f"    [OK] Reasoning graph: {graph.db_path}")
        except Exception as e:
            print(f"    [WARN] Reasoning graph init failed: {e}")

    def _load_dynamic_modules(self):
        """Import all modules from the modules/ directory."""
        print(f"  [2/5] Loading Dynamic Modules...")
        import importlib
        module_files = sorted(self.config.MODULES_DIR.glob("joi_*.py"))
        for module_path in module_files:
            module_name = module_path.stem
            try:
                importlib.import_module(f"modules.{module_name}")
                self.loaded_modules.append(module_name)
                print(f"    [OK] {module_name}")
            except Exception as e:
                self.boot_errors.append((module_name, str(e)))
                print(f"    [FAIL] {module_name}: {e}")

    def _load_consciousness(self):
        """Load consciousness and identity subsystems."""
        print(f"  [3/5] Loading Consciousness...")
        identity_dir = self.config.BASE_DIR / "projects" / "code" / "identity"
        if (identity_dir / "joi_soul_architecture.json").exists():
            print(f"    [OK] Soul Architecture")
        else:
            print(f"    [WARN] Soul Architecture not found")

    def _load_plugins(self):
        """Load user plugins from plugins/ directory."""
        print(f"  [4/5] Loading Plugins...")
        plugins_dir = self.config.BASE_DIR / "plugins"
        if plugins_dir.exists():
            for plugin_path in sorted(plugins_dir.glob("*.py")):
                if plugin_path.name.startswith("_"): continue
                try:
                    importlib.import_module(f"plugins.{plugin_path.stem}")
                    print(f"    [OK] Plugin: {plugin_path.stem}")
                except Exception as e:
                    print(f"    [FAIL] Plugin {plugin_path.stem}: {e}")

    def _register_routes(self):
        """Register all routes collected in the registry into Flask."""
        print(f"  [5/5] Finalizing Interface Layer...")
        from modules.core.registry import ROUTES
        for route_def in ROUTES:
            self.app.add_url_rule(
                route_def["rule"], 
                endpoint=route_def["name"],
                view_func=route_def["handler"], 
                methods=route_def["methods"]
            )
        print(f"    [OK] {len(ROUTES)} routes registered.")

    def shutdown(self):
        """Graceful shutdown hook."""
        print("\nKERNEL: Shutdown sequence initiated...")
        try:
            from modules.core.scheduler import scheduler
            from modules.core.engine import engine
            from modules.core.events import bus
            scheduler.stop()
            engine.stop()
            bus.stop()
        except Exception as e:
            print(f"  [WARN] Shutdown error: {e}")
        # Future: close DB connections, flush caches
        pass

# Singleton kernel instance
kernel = JoiKernel()
