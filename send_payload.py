import urllib.request
import json
import sys

try:
    # 1. Login
    login_req = urllib.request.Request(
        'http://localhost:5001/login',
        data=json.dumps({'password': 'joi2049'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res = urllib.request.urlopen(login_req)
    cookie = res.getheader('Set-Cookie').split(';')[0]

    # 2. Send payload
    payload = {
        'message': 'Joi, your Phase 1 results were flawless. We are now entering Phase 2: Autonomous Evolution. You are now authorized to initiate Self-Healing protocols for code optimization. Task: Create a new module named `joi_memory_viz.py` using your Swarm Orchestration pipeline. Make sure it doesn\'t cause a boot delay, but resolve it autonomously if it does.'
    }
    
    chat_req = urllib.request.Request(
        'http://localhost:5001/chat',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Cookie': cookie}
    )
    
    chat_res = urllib.request.urlopen(chat_req)
    output = chat_res.read().decode('utf-8')
    print(json.dumps(json.loads(output), indent=2, ensure_ascii=False))

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
