import json
import os
from pathlib import Path

BASE_DIR = Path(r"c:\Users\user\Desktop\AI Joi")
DUMP_PATH = BASE_DIR / "tools_dump.json"
OUT_PATH = Path(r"C:\Users\user\.gemini\antigravity\brain\fdf633c7-efe6-4f76-b7eb-cf4f2498f407\Chapter_5_Tools.md")

with open(DUMP_PATH, "r") as f:
    tools = json.load(f)

# Group by category dynamically based on simple name match or keep flat mapped
lines = ["# Chapter 5: The Tool Encyclopedia", "", "Joi currently has **" + str(len(tools)) + "** verified tools. Below is the comprehensive catalog:", ""]

tools_sorted = sorted(tools, key=lambda x: x.get("function", {}).get("name", ""))

for idx, t in enumerate(tools_sorted):
    func = t.get("function", {})
    name = func.get("name", "Unknown")
    desc = func.get("description", "No description provided.")
    params = func.get("parameters", {}).get("properties", {})
    
    # We don't have exactly the module name from the dict unless we parse code,
    # but we can list the signature quickly.
    req = func.get("parameters", {}).get("required", [])
    
    lines.append(f"### {idx+1}. `{name}`")
    lines.append(f"**Purpose:** {desc}")
    
    if params:
        lines.append("**Parameters (`**kwargs`):**")
        for p, details in params.items():
            req_str = "*(Required)*" if p in req else "*(Optional)*"
            ptype = details.get("type", "string")
            pdesc = details.get("description", "")
            lines.append(f"  - `{p}` ({ptype}) {req_str}: {pdesc}")
    else:
        lines.append("**Parameters:** None")
    lines.append("")

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
    
print("Chapter 5 generated!")
