import os
import ast

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)
            
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                for key, value in zip(node.keys, node.values):
                    if isinstance(key, ast.Constant) and key.value == 'description':
                        if isinstance(value, ast.List):
                            print(f"FOUND ARRAY DESCRIPTION IN {filepath} at line {node.lineno}")
                            # Print the list elements for context
                            elements = [e.value for e in value.elts if isinstance(e, ast.Constant)]
                            print(f"  Contents: {elements}")
    except Exception as e:
        pass

for root_dir in ['c:\\Users\\user\\Desktop\\AI Joi\\modules', 'c:\\Users\\user\\Desktop\\AI Joi\\plugins']:
    for dirpath, _, filenames in os.walk(root_dir):
        for name in filenames:
            if name.endswith('.py'):
                check_file(os.path.join(dirpath, name))
