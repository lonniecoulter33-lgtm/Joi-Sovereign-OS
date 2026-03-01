import json
import urllib.request
import urllib.error
import sys

PAYLOAD = {
    "message": "Antigravity reports a 'Context-Interface Mismatch'. You are claiming you have no tools in the browser, despite the previous 'all-clear' report.\n\n### THE FORCED AWAKENING\n1. Tool Audit: Run 'list_capabilities' and 'check_registry' immediately. Do NOT report success based on file existence; report success based on a 'LIVE EXECUTION' of 'fs_read' on 'modules/core/registry.py'.\n2. Quiet-STaR Reflection: Initiate a Quiet-STaR loop. Thought: \"Lonnie says I have tools I cannot see. Why does my internal registry differ from my browser-facing tool_map?\"\n3. Self-Healing: If 'analyze_screen' is missing from your browser context, use 'update_tool_config' to force-inject the priority-1 tool group into the UI session.\n4. Mirror Test: Report back exactly: \"I found [X] tools in my registry. I have successfully pushed [Y] tools to the UI bridge.\"\n\nWe need an admission of the disconnect, not a blanket 'all is well'. Execute these directives now.",
    "session_id": "auditor_terminal_emergency"
}

def send_prompt():
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
        url = 'http://127.0.0.1:5001/chat'
        data = json.dumps(PAYLOAD).encode('utf-8')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': cookie,
            'X-Benchmark': '1'
        }

        req = urllib.request.Request(url, data=data, headers=headers, method='POST')

        print(f"Sending Emergency Calibration payload to Joi...")
        print("-" * 50)
        print(PAYLOAD["message"])
        print("-" * 50)
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("\n[SUCCESS]")
            print("Response:")
            if "response" in result:
                print(result["response"])
            else:
                print(json.dumps(result, indent=2))
                
    except urllib.error.HTTPError as e:
        print(f"\n[HTTP Error]: {e.code} - {e.reason}")
        error_body = e.read().decode('utf-8')
        print(f"Details: {error_body}")
    except urllib.error.URLError as e:
        print(f"\n[Connection Error]: Failed to reach Joi server. Is it running on port 5001?")
        print(f"Reason: {e.reason}")
    except Exception as e:
        print(f"\n[Unexpected Error]: {str(e)}")

if __name__ == "__main__":
    send_prompt()
