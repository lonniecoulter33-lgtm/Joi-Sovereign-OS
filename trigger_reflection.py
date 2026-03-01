import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.core.meta_cognition import meta
print("Triggering meta-cognition reflection loop...")
meta.run_analysis_cycle()
print("Done.")
