import os
import sys
import glob

def find_tools_in_dir(directory):
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    for i, line in enumerate(lines):
                        if 'description' in line:
                            if '[' in line and ']' in line:
                                print(f"Possible match in {filepath}:{i+1}")
                                print(f"  {line.strip()}")
                except Exception:
                    pass

print("Searching modules...")
find_tools_in_dir("c:/Users/user/Desktop/AI Joi/modules")
print("Searching plugins...")
find_tools_in_dir("c:/Users/user/Desktop/AI Joi/plugins")
print("Searching root...")
find_tools_in_dir("c:/Users/user/Desktop/AI Joi")
