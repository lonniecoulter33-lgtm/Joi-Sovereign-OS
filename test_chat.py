"""
Test Joi's actual /chat endpoint.
Run WHILE Joi's Flask server is running.

  venv311\Scripts\python.exe -X utf8 test_chat.py
"""
import json, sys
try:
    import requests
except ImportError:
    print("ERROR: requests not installed")
    sys.exit(1)

BASE = "http://127.0.0.1:5001"

print(f"\n{'='*60}")
print(f"  JOI LIVE CHAT DIAGNOSTIC")
print(f"{'='*60}\n")

# ── 1. Check server is up ────────────────────────────────────────
print("1. Checking server...")
try:
    r = requests.get(f"{BASE}/status/features", timeout=5)
    data = r.json()
    print(f"   Server UP. Enabled features: {data.get('enabled', [])}")
    print(f"   Disabled features: {list(data.get('disabled', {}).keys())}")
except Exception as e:
    print(f"   Server NOT reachable: {e}")
    print("   Make sure joi_companion.py is running first!")
    sys.exit(1)


# ── 2. Get a session cookie ──────────────────────────────────────
print("\n2. Getting session...")
sess = requests.Session()
try:
    r = sess.post(f"{BASE}/login", json={"password": "joi2049"}, timeout=5)
    print(f"   Login response: {r.status_code} {r.text[:100]}")
    if r.status_code != 200:
        print(f"   ERROR: Login failed! Check password.")
        sys.exit(1)
    print(f"   Login OK")
except Exception as e:
    print(f"   Login failed: {e}")
    sys.exit(1)

# Try without auth too (some setups don't require it)
# ── 3. Send a simple tool-requiring message ──────────────────────
test_messages = [
    "remember that my favorite color is blue",
    "open Chrome",
    "search the web for today's weather",
]

for msg in test_messages:
    print(f"\n3. Sending: '{msg}'")
    try:
        r = sess.post(f"{BASE}/chat",
                      json={"message": msg},
                      headers={"X-Benchmark": "1"},
                      timeout=30)
        if r.status_code != 200:
            print(f"   HTTP {r.status_code}: {r.text[:200]}")
            continue

        data = r.json()
        print(f"   ok:    {data.get('ok')}")
        print(f"   model: {data.get('model', 'NOT SET')}")
        print(f"   reply: {str(data.get('reply', ''))[:120]}")

        context = data.get('context_injected', [])
        print(f"   context_injected: {context}")

        if 'routing' in data:
            print(f"   routing:          {data['routing']}")
        if 'brain_state' in data:
            bs = data['brain_state']
            print(f"   brain_state tools_used: {bs.get('tools_used_this_session', 'N/A')}")

        print()
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback; traceback.print_exc()

print(f"\n{'='*60}\n")
print("KEY: look at 'model:' field above.")
print("  If model says 'brain:gemini*' -> fell back to Gemini (NO tools)")
print("  If model says 'openai:gpt-4o-mini' -> OpenAI path (tools work)")
print("  If model says 'direct-launch' -> bypassed LLM entirely")
print(f"{'='*60}\n")
