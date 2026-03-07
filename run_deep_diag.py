import json
import sqlite3

try:
    with open('usage_log.json', 'r', encoding='utf-8') as f:
        log = json.load(f)
        last = log[-1] if log else {}
        
    tools = last.get('tools', [])
    tool_names = [t.get('function', {}).get('name') for t in tools if 'function' in t]
    image_tools = [n for n in tool_names if 'image' in n or 'publisher' in n]
    
    diagnostic = {
        'total_tools': len(tools),
        'tool_names': tool_names,
        'image_tools_in_payload': image_tools,
        'system_prompt_start': last.get('messages', [])[0]['content'][:500] if last.get('messages') else None,
        'last_messages': last.get('messages', [])[-3:] if last.get('messages') else []
    }
    
    with open('diagnostic_payload.json', 'w', encoding='utf-8') as f:
        json.dump(diagnostic, f, indent=2)
        
    print(f"Diagnostic saved. Total tools: {len(tools)}. Image tools: {image_tools}")
except Exception as e:
    print(f"Error checking usage_log: {e}")

try:
    conn = sqlite3.connect('joi_memory.db')
    c = conn.cursor()
    c.execute('SELECT role, content FROM messages ORDER BY id DESC LIMIT 5')
    rows = c.fetchall()
    
    with open('diagnostic_memory.txt', 'w', encoding='utf-8') as f:
        for r in reversed(rows):
            f.write(f"ROLE: {r[0]}\nCONTENT:\n{r[1]}\n{'-'*40}\n")
    print("Memory diagnostic saved.")
except Exception as e:
    print(f"Error checking memory: {e}")
