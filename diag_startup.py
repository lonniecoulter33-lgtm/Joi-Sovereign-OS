
import traceback
import importlib
import sys
import os
from pathlib import Path

# Add project root and modules to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "modules"))

mods = ['joi_exports', 'joi_llm', 'joi_memory']

for m in mods:
    print(f"\n--- Attempting to import {m} ---")
    try:
        importlib.import_module(f"modules.{m}")
        print(f"  [OK] {m} imported successfully.")
    except Exception:
        print(f"  [FAIL] {m} failed to import:")
        traceback.print_exc()
