"""
Diagnose why _call_openai fails inside Joi's context.
Run: venv311\Scripts\python.exe -X utf8 test_tools_live.py
(No Flask server needed -- just loads the modules directly)
"""
import os, sys, json
sys.path.insert(0, '.')
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path('.env'), override=False)

print("Loading joi_companion (this loads all modules)...")
import joi_companion
TOOLS = joi_companion.TOOLS
print(f"Tools registered: {len(TOOLS)}")
print()

# --- Validate all tool schemas ---
print("Validating tool schemas...")
errors = []
for t in TOOLS:
    fn = t.get('function', {})
    name = fn.get('name', '?')
    params = fn.get('parameters', {})
    if not fn.get('name'):
        errors.append(f"MISSING NAME in: {t}")
    if not fn.get('description'):
        errors.append(f"{name}: missing description")
    if params:
        ptype = params.get('type')
        if ptype != 'object':
            errors.append(f"{name}: parameters.type={repr(ptype)} (must be 'object')")
        props = params.get('properties', {})
        for pname, pdef in props.items():
            if not isinstance(pdef, dict):
                errors.append(f"{name}.{pname}: property is not a dict")

if errors:
    print(f"FOUND {len(errors)} SCHEMA ERRORS:")
    for e in errors[:30]:
        print(f"  ERROR: {e}")
else:
    print("All schemas valid.")
print()

# --- Test OpenAI with ALL registered tools ---
from openai import OpenAI
key = os.getenv('OPENAI_API_KEY', '').strip()
model = os.getenv('JOI_OPENAI_TOOL_MODEL', 'gpt-4o-mini').strip()
print(f"Testing OpenAI ({model}) with ALL {len(TOOLS)} tools...")
client = OpenAI(api_key=key, max_retries=0)

try:
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': 'You are Joi. You have tools. Use them.'},
            {'role': 'user', 'content': "Analyze your capabilities and give me a report on the hardware and software you are running."}
        ],
        tools=TOOLS,
        tool_choice='auto',
        temperature=0.7,
        max_tokens=100,
    )
    msg = resp.choices[0].message
    print(f"SUCCESS: finish_reason={resp.choices[0].finish_reason}")
    if msg.tool_calls:
        print(f"  Tool called: {msg.tool_calls[0].function.name}({msg.tool_calls[0].function.arguments})")
    else:
        print(f"  No tool call (text only): {msg.content}")
except Exception as e:
    print(f"FAILED: {type(e).__name__}: {e}")
    print()
    # Try to find which tool is bad by binary search
    print("Finding bad tool via binary search...")
    def test_subset(tools_subset):
        try:
            client.chat.completions.create(
                model=model,
                messages=[{'role': 'system', 'content': 'You are Joi.'}, {'role': 'user', 'content': 'hi'}],
                tools=tools_subset,
                tool_choice='auto',
                max_tokens=10,
            )
            return True
        except Exception:
            return False

    bad_tools = []
    # Test in groups of 10
    for i in range(0, len(TOOLS), 10):
        chunk = TOOLS[i:i+10]
        if not test_subset(chunk):
            # Find which tool in this chunk is bad
            for j, t in enumerate(chunk):
                if not test_subset([t]):
                    bad_tools.append(t.get('function', {}).get('name', f'tool_{i+j}'))
                    print(f"  BAD TOOL: {bad_tools[-1]}")

    if bad_tools:
        print(f"\nBAD TOOLS FOUND: {bad_tools}")
    else:
        print("  No single bad tool found -- might be a combination issue")

print()
print("Done.")
