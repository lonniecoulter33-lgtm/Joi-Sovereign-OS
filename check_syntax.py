import re
import subprocess

with open('c:/Users/user/Desktop/AI Joi/joi_ui.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
print(f"Found {len(scripts)} script blocks.")
for i, s in enumerate(scripts):
    filename = f'script_{i}.js'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(s)
    try:
        subprocess.run(["node", "-c", filename], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error in {filename}:")
        print(e.stderr)

