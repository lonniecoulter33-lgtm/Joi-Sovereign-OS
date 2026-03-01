import os
import sys
import json
import pkgutil
import importlib

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
import joi_companion

app = Flask(__name__)

def main():
    tools_list = []
    
    with app.app_context():
        # Force load all modules to ensure tools are registered
        modules_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "modules")
        for _, name, is_pkg in pkgutil.iter_modules([modules_dir]):
            if name.startswith('joi_'):
                try:
                    importlib.import_module(f'modules.{name}')
                except Exception as e:
                    print(f"Skipping {name} due to error: {e}")
                    pass
        
        roles = set()
        from modules.core import registry
        
        # Combine both registries (legacy and modern)
        for tool in getattr(joi_companion, 'TOOLS', []):
            if tool not in tools_list:
                tools_list.append(tool)
                
        for tool in getattr(registry, 'TOOLS', []):
            if tool not in tools_list:
                tools_list.append(tool)
            
    # Dump to JSON
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tools_dump.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tools_list, f, indent=2)
        
    print(f"Dumped {len(tools_list)} tools to {out_path}")
    
    # Also generate the Chapter 5 Markdown
    md_content = "# Chapter 5: Tools & Capabilities Encyclopedia\n\n"
    md_content += "This chapter contains a comprehensive reference of all tools currently available to Joi, dynamically generated from her internal registry. The registry reflects her exact capabilities at the time of compilation.\n\n"
    
    # Sort tools alphabetically by name
    tools_list.sort(key=lambda t: t.get("function", {}).get("name", ""))
    
    for idx, tool in enumerate(tools_list, 1):
        func = tool.get("function", {})
        name = func.get("name", "Unknown Tool")
        desc = func.get("description", "No description provided.")
        
        md_content += f"## {idx}. `{name}`\n\n"
        md_content += f"**Description:**\n{desc}\n\n"
        
        params = func.get("parameters", {}).get("properties", {})
        req = func.get("parameters", {}).get("required", [])
        
        if params:
             md_content += "**Parameters:**\n"
             for p_name, p_info in params.items():
                 p_type = p_info.get("type", "any")
                 p_desc = p_info.get("description", "")
                 req_str = " (Required)" if p_name in req else " (Optional)"
                 md_content += f"- `{p_name}` ({p_type}){req_str}: {p_desc}\n"
             md_content += "\n"
        else:
             md_content += "**Parameters:** None required.\n\n"
             
        md_content += "---\n\n"
        
    # Write directly to artifact as Chapter 5
    artifact_path = os.path.expanduser(r"~/.gemini/antigravity/brain/fdf633c7-efe6-4f76-b7eb-cf4f2498f407/Chapter_5_Tools.md")
    if os.path.exists(os.path.dirname(artifact_path)):
        with open(artifact_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Generated Markdown at {artifact_path}")

if __name__ == "__main__":
    main()
