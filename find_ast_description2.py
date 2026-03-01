import os
import ast

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)
            
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                # Look for a dict that has 'name', 'description', 'parameters'
                keys = [k.value for k in node.keys if isinstance(k, ast.Constant)]
                if 'name' in keys and 'description' in keys:
                    desc_idx = keys.index('description')
                    desc_val = node.values[desc_idx]
                    if not isinstance(desc_val, ast.Constant):
                        print(f"SUSPICIOUS description in {filepath}:{node.lineno} - {type(desc_val)}")
                        if hasattr(desc_val, 'elts'):
                            print(f"  It's an array/sequence! Elements: {[e.value if hasattr(e, 'value') else type(e) for e in desc_val.elts]}")
    except Exception as e:
        pass

p1 = os.path.abspath('modules')
p2 = os.path.abspath('plugins')
for base in [p1, p2]:
    for r, d, f in os.walk(base):
        for file in f:
            if file.endswith('.py'):
                check_file(os.path.join(r, file))

check_file(os.path.abspath('joi_companion.py'))
check_file(os.path.abspath('joi_harness.py'))
print("Scan complete.")
