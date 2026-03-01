import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

try:
    # Set headless mode/prevent server start
    os.environ["JOI_NO_SERVER"] = "1"
    
    import joi_companion
    
    # 1. Dump tools
    tools = joi_companion.TOOLS
    with open(BASE_DIR / "tools_dump.json", "w") as f:
        json.dump(tools, f, indent=2)
        
    # 2. Dump orphans
    loaded = set()
    for name in sys.modules:
        if name.startswith("modules."):
            loaded.add(name.split(".")[-1] + ".py")
            
    all_files = set()
    modules_dir = BASE_DIR / "modules"
    for f in modules_dir.glob("*.py"):
        if f.is_file() and not f.name.startswith("__"):
            all_files.add(f.name)
            
    orphans = list(all_files - loaded)
    with open(BASE_DIR / "orphans_dump.json", "w") as f:
        json.dump(orphans, f, indent=2)
        
    print(f"SUCCESS: {len(tools)} tools, {len(orphans)} orphans")
except Exception as e:
    print(f"ERROR: {e}")
