import sys
import os
import json
from pathlib import Path

# Add current dir to path
sys.path.append(os.getcwd())

def run_definitive_test():
    print("--- JOI DEFINITIVE DIAGNOSTIC START ---")
    
    try:
        from modules.core.kernel import kernel
        kernel.boot()
        
        from joi_companion import app
        from modules.joi_memory import create_session
        
        # Create a valid admin token
        token = create_session(is_admin=True)
        
        with app.test_client() as client:
            client.set_cookie('joi_session', token)
            
            print("\nTEST 1: Casual Greeting")
            r1 = client.post('/chat', json={'message': 'Hello Joi, are you there?'})
            print(f"Status: {r1.status_code}")
            try:
                data = r1.get_json()
                if data and data.get('ok'):
                    print("Result: SUCCESS (Valid JSON)")
                else:
                    print(f"Result: FAILED (JSON ok:false or missing).")
                    print(f"Body: {r1.get_data(as_text=True)[:200]}")
            except Exception as e:
                print(f"Result: CRITICAL FAILURE (Body is not JSON). Error: {e}")
                print(f"Raw Body Preview: {r1.get_data(as_text=True)[:500]}")

            print("\nTEST 2: Tool Intent (Filesystem)")
            r2 = client.post('/chat', json={'message': 'List the files in the project root.'})
            print(f"Status: {r2.status_code}")
            try:
                data = r2.get_json()
                if data and data.get('ok'):
                    print("Result: SUCCESS (Valid JSON + Tool Path)")
                else:
                    print(f"Result: FAILED.")
                    print(f"Body: {r2.get_data(as_text=True)[:200]}")
            except Exception as e:
                print(f"Result: CRITICAL FAILURE. Raw Body: {r2.get_data(as_text=True)[:500]}")

    except Exception as e:
        print(f"\nDIAGNOSTIC CRASHED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_definitive_test()
