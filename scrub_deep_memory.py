import sqlite3
import re
import json

# 1. Clean SQLite Memory DB
try:
    conn = sqlite3.connect('joi_memory.db')
    c = conn.cursor()
    # Find how many rows we are deleting
    c.execute("SELECT COUNT(*) FROM messages WHERE content LIKE '%Ariana Grande%' AND content LIKE '%image%' AND role = 'assistant'")
    count = c.fetchone()[0]
    
    # Actually delete them
    c.execute("DELETE FROM messages WHERE content LIKE '%Ariana Grande%' AND content LIKE '%image%' AND role = 'assistant'")
    c.execute("DELETE FROM messages WHERE content LIKE '%I don\\'t have a direct tool for generating images%'")
    c.execute("DELETE FROM messages WHERE content LIKE '%I can\\'t directly create images%'")
    conn.commit()
    print(f"Deleted {count} toxic memory entries from joi_memory.db")
    conn.close()
except Exception as e:
    print("Error cleaning SQLite:", e)

# 2. Aggressively clean learning_data.json
try:
    with open('learning_data.json', 'r', encoding='utf-8') as f:
        content = f.read()

    # We will replace any refusal with a generic "Attempting image generation"
    # Match any JSON string value that contains "Ariana Grande" and "image" in the same response
    import re
    
    def replacement(match):
        return '"[Attempted Image Generation] Please wait while I pull up my image generation tools..."'
        
    pattern1 = re.compile(r'"[^"]*don\'t have a direct tool for generating images[^"]*"', re.IGNORECASE)
    pattern2 = re.compile(r'"[^"]*capability to generate images directly[^"]*"', re.IGNORECASE)
    pattern3 = re.compile(r'"[^"]*can\'t directly create images[^"]*"', re.IGNORECASE)
    
    start_len = len(content)
    content = pattern1.sub(replacement, content)
    content = pattern2.sub(replacement, content)
    content = pattern3.sub(replacement, content)
    
    if len(content) != start_len:
        with open('learning_data.json', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Scrubbed learning_data.json")
    else:
        print("No matches to scrub in learning_data.json")
        
except Exception as e:
    print("Error cleaning learning_data.json:", e)
