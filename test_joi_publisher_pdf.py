import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Mock joi_companion to prevent Flask crash during CLI test
class MockCompanion:
    def register_tool(self, *args, **kwargs): pass
    def register_route(self, *args, **kwargs): pass

sys.modules["joi_companion"] = MockCompanion()

from modules.joi_publisher import publisher_generate_cover_script, publisher_format_interior_script

print("1. Testing Cover Script Generation")
res1 = publisher_generate_cover_script(project_name="The_AI_Publisher")
print(res1)

print("\n2. Testing Interior Script Generation")
res2 = publisher_format_interior_script(project_name="The_AI_Publisher")
print(res2)
