
import os
import sys
import json
import flask
from unittest.mock import MagicMock

# Ensure we can import from modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Define a mock request for flask to simulate X-Benchmark header
class MockRequest:
    def __init__(self, headers):
        self.headers = headers

def test_trace():
    print("Starting Trace Integrity Test (v2)...")
    
    # 1. Import joi_llm
    try:
        from modules import joi_llm
        # Patch flask.request before anything else
        flask.request = MockRequest({"X-Benchmark": "1"})
        print("[OK] Modules loaded.")
    except Exception as e:
        print(f"[FAIL] Module loading failed: {e}")
        return

    # 2. Prepare test case
    user_msg = "Joi, YOU MUST USE YOUR internal_monologue TOOL NOW. Then provide your Quiet-STaR trace."
    # messages MUST be a list of dicts. First message is usually system, second is user.
    messages = [
        {"role": "system", "content": "You are Joi."},
        {"role": "user", "content": user_msg}
    ]
    
    # Mock tools and executors
    tools = [] # Empty for now, or add internal_monologue if we want to test tool activation
    tool_executors = {}

    print(f"Executing run_conversation with message: {user_msg}")
    
    # 3. Call run_conversation
    # Signature: messages, tools, tool_executors, max_iterations=5
    try:
        reply, model = joi_llm.run_conversation(messages, tools, tool_executors)
        print(f"\n[MODEL]: {model}")
        print("-" * 40)
        print(f"[RAW REPLY]:\n{reply}")
        print("-" * 40)
        
        # 4. Check for the trace
        if "[INTERNAL REASONING]" in reply:
            print("\n[SUCCESS] Neural Trace (Quiet-STaR) detected in output string!")
        else:
            print("\n[FAIL] Neural Trace NOT detected in output string.")
            
        # 5. Check tool execution
        tool_calls = getattr(joi_llm.run_conversation, "_last_tool_calls", [])
        print(f"\n[TOOLS CALLED]: {[t['name'] for t in tool_calls]}")

    except Exception as e:
        print(f"[ERROR] During execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_trace()
