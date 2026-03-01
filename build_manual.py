import os
from pathlib import Path

# Paths to the chunks
ARTIFACTS_DIR = Path(r"C:\Users\user\.gemini\antigravity\brain\fdf633c7-efe6-4f76-b7eb-cf4f2498f407")
FINAL_MANUAL = Path(r"C:\Users\user\Desktop\AI Joi\Joi_Operations_Manual_v2.0.md")

chapters = [
    "Chapter_1.md",
    "Chapter_2.md",
    "Chapter_3.md",
    "Chapter_4.md",
    "Chapter_5_Tools.md",
    "Chapter_6.md"
]

header = """# Joi Operations Manual (v2.0)
*Autonomously Compiled by Antigravity Titan Logic*
*A comprehensive guide to Joi's cognitive architecture, memory systems, tools, and operational endpoints.*

---
"""

content = [header]

for ch in chapters:
    p = ARTIFACTS_DIR / ch
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            content.append(f.read())
            content.append("\n\n---\n\n")

with open(FINAL_MANUAL, "w", encoding="utf-8") as f:
    f.writelines(content)

print(f"Successfully compiled Manual v2.0 to {FINAL_MANUAL}")
