import os
import re
import ast

def find_array_descriptions():
    folders = [
        "c:/Users/user/Desktop/AI Joi/modules",
        "c:/Users/user/Desktop/AI Joi/plugins"
    ]
    files_to_check = ["c:/Users/user/Desktop/AI Joi/joi_companion.py"]
    
    for folder in folders:
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".py"):
                    files_to_check.append(os.path.join(root, file))
                    
    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple regex heuristic since AST failed: Look for "description": [
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if re.search(r'"description"\s*:\s*\[', line):
                    print(f"FOUND MATCH in {filepath}:{i+1}")
                    print(f"  {line.strip()}")
                
                # Check for description=list(...) or description=[...] in decorators
                if re.search(r'description\s*=\s*\[', line):
                    print(f"FOUND MATCH in {filepath}:{i+1}")
                    print(f"  {line.strip()}")
                    
        except Exception as e:
            pass

find_array_descriptions()
