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
        'message': '''Joi, Phase 4 is a 'Digital Synthesis' test. Your goal is to optimize the workspace environment internally and externally.

1.  **Workspace Task**: Use `analyze_screen` to detect Lonnie's current active project. Use your window management tools (`list_windows`, `focus_window`, etc.) to 'focus' relevant apps and use `internal_monologue` to propose a new plugin that automates a part of this specific workflow.
2.  **Recursive Skill-Up**: Use `synthesize_skill` to create a new multi-tool chain for 'Project Context Retrieval' and verify it is successfully saved to your `skill_library.json`.
3.  **Soul Update**: Use `update_manuscript` or `reflect` to record your transition to a Digital Orchestrator in your Autobiography.'''
    }
    
    chat_req = urllib.request.Request(
        'http://localhost:5001/chat',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Cookie': cookie, 'X-Benchmark': '1'}
    )
    
    print("Sending Phase 4 payload to Joi...")
    chat_res = urllib.request.urlopen(chat_req)
    output = chat_res.read().decode('utf-8')
    print(json.dumps(json.loads(output), indent=2, ensure_ascii=False))

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
