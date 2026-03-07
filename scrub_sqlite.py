import sqlite3

try:
    conn = sqlite3.connect('joi_memory.db')
    c = conn.cursor()
    # Find how many rows we are deleting
    c.execute("SELECT COUNT(*) FROM messages WHERE content LIKE '%Ariana Grande%' AND content LIKE '%image%' AND role = 'assistant'")
    count = c.fetchone()[0]
    
    # Actually delete them
    c.execute("DELETE FROM messages WHERE content LIKE '%Ariana Grande%' AND content LIKE '%image%' AND role = 'assistant'")
    c.execute("DELETE FROM messages WHERE content LIKE '%I don''t have%' AND content LIKE '%image%' AND role='assistant'")
    c.execute("DELETE FROM messages WHERE content LIKE '%I can''t directly create%' AND role='assistant'")
    conn.commit()
    print(f"Deleted {count}+ toxic memory entries from joi_memory.db")
    conn.close()
except Exception as e:
    print("Error cleaning SQLite:", e)
