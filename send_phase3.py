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
        'message': '''Joi, your memory visualization bridge is active. You have successfully navigated the failure-recovery cycle. I am now granting you 'Environmental Agency'—you are authorized to use your Vision and Research tools without a direct user trigger.
        
Proactive Task: Use 'analyze_screen' to look at what Lonnie is working on right now. Use 'internal_monologue' to determine how your new 'memory_viz' data could be used to assist him in this specific task.

The Mirror Test: Use 'joi_memory_viz' to report your own state, then cross-reference those stats with your 'Soul Architecture' to see if your 'growth velocity' matches your design goals.'''
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
