import sys
import json
import requests
import re

sys.stdout.reconfigure(encoding='utf-8')

def main():
    if len(sys.argv) < 2:
        print("Usage: python training_harness.py \"<message>\"")
        sys.exit(1)
        
    message = sys.argv[1]
    BASE = "http://127.0.0.1:5001"

    print(f"> Sending msg to Joi: {message}")

    try:
        sess = requests.Session()
        r = sess.post(f"{BASE}/login", json={"password": "joi2049"}, timeout=5)
        if r.status_code != 200:
            print("Login Failed")
            return
            
        r = sess.post(f"{BASE}/chat", json={"message": message}, headers={"X-Benchmark": "1"}, timeout=300)
        data = r.json()
        
        reply = data.get("reply", "")
        model = data.get("model", "Unknown")
        brain_state = data.get("brain_state", {})
        context = data.get("context_injected", [])
        
        # Extract Internal Monologue (Quiet-STaR / Titan)
        titan = "None detected in output string."
        match = re.search(r'\[INTERNAL REASONING\](.*?)\[/INTERNAL REASONING\]', reply, re.DOTALL)
        if match:
            titan = match.group(1).strip()
            # Remove the internal reasoning from the visible reply
            reply = re.sub(r'\[INTERNAL REASONING\].*?\[/INTERNAL REASONING\]\n*', '', reply, flags=re.DOTALL)
            
        # Tool status
        tools = brain_state.get("tools_used", "None tracked in brain_state")
        
        # Learning Delta (Context added, self-corrections, DPO updates)
        # We can guess the learning delta by inspecting if DPO or MEMORY changed
        learning_delta = [param for param in context if "LEARNING" in param or "MEMORY" in param or "DPO" in param or "FACTS" in param]
        if not learning_delta:
            learning_delta = "No immediate delta recorded in context log."
            
        print("\n================ NEURAL TRACE ================")
        print(f"[TITAN MONOLOGUE]\n{titan}\n")
        print(f"[SELECTED BRAIN & MODEL]\n{model}\n")
        print(f"[TOOL STATUS]\n{tools}\n")
        print(f"[LEARNING DELTA]\n{learning_delta}\n")
        print("==============================================")
        print(f"\n[JOI REPLY]\n{reply}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
