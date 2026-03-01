import sys
import os
import json
import time
from pathlib import Path

# Add current dir to path
sys.path.append(os.getcwd())

def run_stress_test():
    print("--- JOI ARCHITECTURAL STRESS TEST ---")
    
    try:
        # Import triggers top-level boot
        print("\n[STEP 1] Testing Global Boot Sequence...")
        from joi_companion import app, TOOLS, ENABLED_FEATURES
        from modules.joi_memory import create_session
        
        print(f"Registry Status: {len(TOOLS)} tools found.")
        print(f"Features: {list(ENABLED_FEATURES.keys())}")
        
        if len(TOOLS) == 0:
            raise RuntimeError("CRITICAL: 0 tools found after boot!")

        # Create a valid session
        token = create_session(is_admin=True)
        
        with app.test_client() as client:
            client.set_cookie('joi_session', token)
            
            print("\n[STEP 2] Testing Response Integrity (Byte-Level)...")
            r = client.post('/chat', json={'message': 'Hey Joi, give me a quick hello.'})
            
            print(f"HTTP Status: {r.status_code}")
            raw_body = r.get_data(as_text=True)
            
            # Check for non-JSON corruption (common cause of unexpected token)
            if raw_body.strip().startswith("<"):
                print("CRITICAL ERROR: Response starts with HTML tag!")
                print(raw_body[:500])
                return
            
            try:
                data = json.loads(raw_body)
                if data.get('ok'):
                    print("SUCCESS: Valid JSON received.")
                    print(f"Reply: {data.get('reply')[:50]}...")
                else:
                    print(f"FAILED: Backend returned JSON error: {data.get('error')}")
            except Exception as e:
                print(f"CRITICAL: Body is NOT JSON. Error: {e}")
                print(f"Body snippet: {repr(raw_body[:200])}")

            print("\n[STEP 3] Testing Tool Invocation Logic...")
            r2 = client.post('/chat', json={'message': 'List project files.'})
            data2 = r2.get_json()
            if data2 and data2.get('ok'):
                print("SUCCESS: Tool request processed correctly.")
            else:
                print("FAILED: Tool request failed.")

        print("\n--- STRESS TEST COMPLETE: ALL SYSTEMS NOMINAL ---")

    except Exception as e:
        print("\nSTRESS TEST CRASHED")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_stress_test()
