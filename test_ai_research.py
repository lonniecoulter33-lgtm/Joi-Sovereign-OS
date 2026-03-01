import sys
import traceback
sys.path.insert(0, '.')
try:
    from modules import joi_evolution
    print("Running monitor_ai_research...")
    res = joi_evolution.monitor_ai_research(force=False)
    print("Result:", res)
except Exception as e:
    traceback.print_exc()
