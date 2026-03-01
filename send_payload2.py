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
        'message': 'Can you re-run Swarm Orchestration to create the `joi_memory_viz.py` module? Ensure that the generated code is completely free of syntax errors and uses the correct `joi_companion` imports so it does not fail the watchdog sanity check.'
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
