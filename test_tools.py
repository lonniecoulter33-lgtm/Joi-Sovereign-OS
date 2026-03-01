"""
Quick diagnostic - run this directly in your terminal:
  venv312\Scripts\python.exe -X utf8 test_tools.py

It tests whether OpenAI actually accepts and responds to tool calls.
"""
import os, sys, json
from pathlib import Path

# Load the same .env as Joi
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=False)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
TOOL_MODEL = os.getenv("JOI_OPENAI_TOOL_MODEL", "gpt-4o-mini").strip()

print(f"\n{'='*60}")
print(f"  JOI TOOL DIAGNOSTIC")
print(f"{'='*60}")
print(f"  Model:   {TOOL_MODEL}")
print(f"  API key: {OPENAI_API_KEY[:12]}...{OPENAI_API_KEY[-4:] if OPENAI_API_KEY else 'MISSING'}")
print()

if not OPENAI_API_KEY:
    print("  ERROR: OPENAI_API_KEY is empty in .env")
    sys.exit(1)

try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY, max_retries=0)
    print("  [OK] OpenAI client created")
except Exception as e:
    print(f"  [FAIL] OpenAI client: {e}")
    sys.exit(1)

# One simple test tool
TEST_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Open an application",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "Name of the app to open"}
                },
                "required": ["app_name"]
            }
        }
    }
]

MESSAGES = [
    {"role": "system", "content": "You are Joi, an AI assistant. You have tools available. Use them."},
    {"role": "user", "content": "Open Chrome"}
]

print(f"\n  Sending to OpenAI ({TOOL_MODEL}) with 1 tool and message: 'Open Chrome'")
print(f"  (This is a real API call - may cost a tiny amount)")
print()

try:
    kwargs = {
        "model": TOOL_MODEL,
        "messages": MESSAGES,
        "tools": TEST_TOOLS,
        "tool_choice": "auto",
    }

    # Only add temperature/top_p if NOT a reasoning model
    is_reasoning = (
        TOOL_MODEL.startswith("o1") or TOOL_MODEL.startswith("o3") or
        TOOL_MODEL.startswith("o4") or TOOL_MODEL.startswith("gpt-5")
    )
    if not is_reasoning:
        kwargs["temperature"] = 0.7
        kwargs["top_p"] = 0.9
        kwargs["max_tokens"] = 500
    else:
        kwargs["max_completion_tokens"] = 500

    print(f"  kwargs sent to OpenAI:")
    debug_kwargs = dict(kwargs)
    debug_kwargs["messages"] = f"[{len(MESSAGES)} messages]"
    debug_kwargs["tools"] = f"[{len(TEST_TOOLS)} tools]"
    for k, v in debug_kwargs.items():
        print(f"    {k}: {v}")
    print()

    response = client.chat.completions.create(**kwargs)

    msg = response.choices[0].message
    print(f"  RESULT:")
    print(f"    finish_reason: {response.choices[0].finish_reason}")
    print(f"    content:       {msg.content!r}")
    print(f"    tool_calls:    {msg.tool_calls}")

    if msg.tool_calls:
        print(f"\n  SUCCESS: Model called a tool!")
        for tc in msg.tool_calls:
            print(f"    Tool: {tc.function.name}")
            print(f"    Args: {tc.function.arguments}")
    else:
        print(f"\n  NOTE: Model returned text only (no tool call).")
        print(f"  finish_reason={response.choices[0].finish_reason!r}")
        print(f"  This means tools were SENT but the model chose not to call one.")
        print(f"  Try adding tool_choice='required' to force a call.")

except Exception as e:
    print(f"  ERROR: {type(e).__name__}: {e}")
    print()
    print(f"  Full error:")
    import traceback
    traceback.print_exc()

print(f"\n{'='*60}\n")
