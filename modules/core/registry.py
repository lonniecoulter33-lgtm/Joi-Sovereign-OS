"""
modules/core/registry.py

Central registry for tools, routes, and feature status.
Enables modules to self-register capabilities without importing the main app.
"""
from typing import Dict, Any, List, Optional

# OpenAI function-calling tool definitions
TOOLS = []

# {tool_name: function} mapping
TOOL_EXECUTORS = {}

# {tool_name: JoiTool} mapping for structured access
ACTIVE_TOOLS = {}

# Flask route registrations (for plugins)
ROUTES = []

# Context Providers (for system prompt construction)
CONTEXT_PROVIDERS = []

# Sensors (Environment monitors)
ACTIVE_SENSORS = {}

# Perception Buffer (Raw signals from sensors)
SIGNAL_QUEUE = []
MAX_SIGNAL_QUEUE = 100

def register_sensor(sensor_obj):
    """Register an active environment monitor."""
    # Basic validation
    if not hasattr(sensor_obj, 'name') or not hasattr(sensor_obj, 'poll'):
        raise TypeError(f"Object {type(sensor_obj).__name__} must implement JoiSensor interface")
    ACTIVE_SENSORS[sensor_obj.name] = sensor_obj
    print(f"  [REGISTRY] Sensor registered: {sensor_obj.name}")

def push_signal(source: str, data: Dict[str, Any]):
    """Sensors call this to push a signal to the buffer."""
    import time
    global SIGNAL_QUEUE
    SIGNAL_QUEUE.append({
        "source": source,
        "data": data,
        "timestamp": time.time()
    })
    if len(SIGNAL_QUEUE) > MAX_SIGNAL_QUEUE:
        SIGNAL_QUEUE.pop(0)

def audit_features():
    """Proactively scan modules and tools to enable high-level features."""
    global ENABLED_FEATURES, DISABLED_FEATURES
    import os
    import re
    from pathlib import Path
    
    # 1. Clear current status to prevent desync
    ENABLED_FEATURES.clear()
    
    # 2. Define feature mapping patterns (Keywords used to identify capabilities)
    feature_map = {
        "filesystem": [r"fs_", "read_file", "write_file", "search_files"],
        "desktop": [r"click_mouse", r"type_text", r"move_mouse", r"launch_app", r"window"],
        "camera": [r"analyze_camera", r"enroll_face", r"face"],
        "vision": [r"analyze_screen", r"screenshot"],
        "voice": [r"generate_tts", r"voice_id", r"transcribe"],
        "home_automation": [r"ha_"],
        "agent_swarms": [r"orchestrate", r"agent_"]
    }
    
    # 3. Aggregate all registered tools (Modern + Legacy)
    all_tool_names = set(TOOL_EXECUTORS.keys()) | set(ACTIVE_TOOLS.keys())
    
    # Backup check: If executors are empty, check the TOOLS list objects
    if not all_tool_names and TOOLS:
        all_tool_names = set(t.get("function", {}).get("name", "") for t in TOOLS if isinstance(t, dict))
    
    # 4. Proactive Scan: Look into modules/ and tools/ for potential tools
    # This catches tools even if their module failed to import fully
    base_dir = Path(__file__).resolve().parent.parent.parent
    scan_dirs = [base_dir / "modules", base_dir / "tools"]
    
    print(f"  [REGISTRY] Starting proactive scan of {scan_dirs}...")
    
    for s_dir in scan_dirs:
        if not s_dir.exists(): continue
        for py_file in s_dir.glob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                # Look for register_tool or register_joi_tool calls in the text
                if "register_tool" in content or "register_joi_tool" in content:
                    # Found tool definitions in file - use filename to guess feature
                    name = py_file.stem.lower()
                    for feat, keywords in feature_map.items():
                        if any(kw in name for kw in keywords):
                            ENABLED_FEATURES[feat] = True
                            # print(f"    [FOUND] Proactive match: {py_file.name} -> {feat}")
            except Exception: pass

    # 5. Map explicitly registered tools to features
    for tool in all_tool_names:
        if not tool: continue
        for feat, keywords in feature_map.items():
            if any(kw in tool for kw in keywords):
                ENABLED_FEATURES[feat] = True
                
    # 6. Core features are always enabled if registry is alive
    ENABLED_FEATURES["core_cognition"] = True
    ENABLED_FEATURES["memory_graph"] = True
    
    print(f"  [REGISTRY] Feature Audit Complete: {len(ENABLED_FEATURES)} features enabled.")
    print(f"  [REGISTRY] Total Tools: {len(TOOLS)} (Legacy) | {len(ACTIVE_TOOLS)} (Modern)")

# Feature Status Registry
# Populated at startup by _check_dependencies
DISABLED_FEATURES = {}   # {"feature_name": "reason string"}
ENABLED_FEATURES = {}    # {"feature_name": True}

def is_feature_enabled(feature_name: str) -> bool:
    """Check if a feature is available. Modules call this before registering tools."""
    return feature_name in ENABLED_FEATURES

def register_tool(tool_def: dict, executor_fn):
    """Modules call this to register a tool (Legacy dict-based)."""
    # Check if tool is already registered to avoid duplicates on reload
    tool_name = tool_def["function"]["name"]
    if tool_name in TOOL_EXECUTORS:
        # Update existing
        for i, t in enumerate(TOOLS):
            if t["function"]["name"] == tool_name:
                TOOLS[i] = tool_def
                break
    else:
        TOOLS.append(tool_def)
        # print(f"  [REGISTRY] Tool registered: {tool_name}")
    
    TOOL_EXECUTORS[tool_name] = executor_fn

def register_joi_tool(tool_obj):
    """Register a structured JoiTool object (Modern contract-based)."""
    from modules.core.interfaces import JoiTool
    if not isinstance(tool_obj, JoiTool):
        # Allow duck typing for protocols if necessary, but here we prefer formal inheritance
        pass
    
    # Store formal object
    ACTIVE_TOOLS[tool_obj.name] = tool_obj
    
    # Map to legacy format for LLM loop compatibility
    register_tool(tool_obj.to_openai_dict(), tool_obj.execute)

def register_route(rule: str, methods: list, handler_fn, name: str):
    """Plugins call this to register Flask routes."""
    # Check if route already exists
    for r in ROUTES:
        if r["rule"] == rule and r["name"] == name:
            r["methods"] = methods
            r["handler"] = handler_fn
            return
            
    ROUTES.append({
        "rule": rule, 
        "methods": methods, 
        "handler": handler_fn, 
        "name": name
    })

def register_context_provider(provider):
    """Register a context provider (must follow ContextProvider protocol)."""
    # Basic validation
    if not hasattr(provider, 'name') or not hasattr(provider, 'build'):
        raise TypeError(f"Provider {type(provider).__name__} does not implement ContextProvider interface")
    
    # Ensure importance and compress exist (Phase 6)
    if not hasattr(provider, 'importance'):
        provider.importance = 0.5
    if not hasattr(provider, 'compress'):
        def _default_compress(content):
            return content[:500] + "..." if len(content) > 500 else content
        provider.compress = _default_compress
        
    # Avoid duplicates
    for i, p in enumerate(CONTEXT_PROVIDERS):
        if p.name == provider.name:
            CONTEXT_PROVIDERS[i] = provider
            return
            
    CONTEXT_PROVIDERS.append(provider)
    # Keep sorted by order for building
    CONTEXT_PROVIDERS.sort(key=lambda x: getattr(x, 'order', 10.0))

# Context Cache: {provider_name: (timestamp, result_tuple)}
CONTEXT_CACHE = {}
CONTEXT_CACHE_TTL = 3600  # Default 1 hour for static blocks

# Runtime Telemetry
TELEMETRY = {
    "boot_time": 0,
    "tool_calls": 0,
    "errors": 0,
    "active_context_blocks": []
}

# Model Performance Matrix: {task_type: {model_id: success_rate}}
ROUTING_SCORES = {}

def update_routing_score(task_type: str, model_id: str, success_rate: float):
    """Update the expert score for a specific model/task combo."""
    if task_type not in ROUTING_SCORES:
        ROUTING_SCORES[task_type] = {}
    ROUTING_SCORES[task_type][model_id] = success_rate
    # print(f"  [REGISTRY] Updated Expert Score: {task_type} -> {model_id} ({success_rate:.2f})")

def log_telemetry(metric: str, value: Any = 1):
    """Update runtime health metrics."""
    if metric in TELEMETRY:
        if isinstance(value, int):
            TELEMETRY[metric] += value
        else:
            TELEMETRY[metric] = value

def get_cached_context(name: str):
    """Retrieve a cached context block if it exists and hasn't expired."""
    import time
    if name in CONTEXT_CACHE:
        ts, result = CONTEXT_CACHE[name]
        if time.time() - ts < CONTEXT_CACHE_TTL:
            return result
    return None

def set_cached_context(name: str, result: tuple):
    """Store a context block result in the cache."""
    import time
    CONTEXT_CACHE[name] = (time.time(), result)

def invalidate_context_cache(name: str = None):
    """Clear specific or all context cache."""
    global CONTEXT_CACHE
    if name:
        CONTEXT_CACHE.pop(name, None)
    else:
        CONTEXT_CACHE = {}



