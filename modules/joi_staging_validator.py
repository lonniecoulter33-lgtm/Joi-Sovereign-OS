"""
modules/joi_staging_validator.py

Static Analysis Validator for Joi's Staging Area.
Checks for syntax errors and NameErrors (missing imports).
Provides explicit suggestions for missing common imports (re, os, json).
"""

import ast
import os
import sys
import json
from typing import Dict, List, Any, Set

class NameErrorVisitor(ast.NodeVisitor):
    """
    Visitor to detect unbound names in Python code.
    Tracks imports, definitions, and usage.
    """
    def __init__(self):
        self.defined: Set[str] = set()
        self.used: Set[str] = set()
        # Expanded built-in names
        self.builtins = {
            'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes',
            'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir',
            'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset',
            'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int',
            'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max',
            'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print',
            'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
            'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip',
            'ImportError', 'RuntimeError', 'Exception', 'BaseException', 'ValueError', 
            'KeyError', 'TypeError', 'AttributeError', 'StopIteration', 'True', 'False', 'None',
            '__name__', '__file__', '__doc__', '__package__', '__loader__', '__spec__',
            'GeneratorExit', 'KeyboardInterrupt', 'SystemExit', 'StopAsyncIteration',
            'ArithmeticError', 'AssertionError', 'BufferError', 'EOFError', 'LookupError',
            'MemoryError', 'NameError', 'ReferenceError', 'SyntaxError', 'SystemError',
            'Warning', 'UserWarning', 'DeprecationWarning', 'PendingDeprecationWarning',
            'SyntaxWarning', 'RuntimeWarning', 'FutureWarning', 'ImportWarning', 'UnicodeWarning',
            'BytesWarning', 'ResourceWarning'
        }

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name.split('.')[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.defined.add(node.name)
        # Add arguments to defined set for the scope of this function
        # Note: This is a shallow check (doesn't handle nested scopes perfectly)
        # but prevents false positives for common patterns like 'def foo(**kwargs)'
        old_defined = self.defined.copy()
        for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
            self.defined.add(arg.arg)
        if node.args.vararg:
            self.defined.add(node.args.vararg.arg)
        if node.args.kwarg:
            self.defined.add(node.args.kwarg.arg)
        self.generic_visit(node)
        # Restore definitions after leaving function (simplified scope management)
        # self.defined = old_defined  # Commented out to avoid complex scope tracking for now

    def visit_ClassDef(self, node: ast.ClassDef):
        self.defined.add(node.name)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Store):
            self.defined.add(node.id)
        elif isinstance(node.ctx, (ast.Load, ast.Del)):
            self.used.add(node.id)
        self.generic_visit(node)

    def visit_arg(self, node: ast.arg):
        self.defined.add(node.arg)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.name:
            self.defined.add(node.name)
        self.generic_visit(node)

def validate_staging_file(file_path: str) -> Dict[str, Any]:
    """
    Validates a Python file in staging.
    Returns {passed: bool, errors: List[str], suggestions: List[str]}
    """
    if not file_path.endswith(".py"):
        return {"passed": True, "errors": [], "suggestions": []}

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()
    except Exception as e:
        return {"passed": False, "errors": [f"Read error: {e}"], "suggestions": []}

    # 1. Syntax Check
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return {
            "passed": False, 
            "errors": [f"SyntaxError at line {e.lineno}, col {e.offset}: {e.msg}"],
            "suggestions": []
        }

    # 2. NameError Check (missing imports)
    visitor = NameErrorVisitor()
    visitor.visit(tree)

    undefined = (visitor.used - visitor.defined - visitor.builtins)
    
    errors = []
    suggestions = []
    
    # Common core modules we want to explicitly suggest
    CORE_MODULES = ["re", "os", "json", "time", "sys", "pathlib", "shutil"]
    
    for name in undefined:
        if name in CORE_MODULES:
            errors.append(f"Missing import for module: '{name}'")
            suggestions.append(f"Missing import detected: please add 'import {name}' to the top of the file")
        else:
            # General warning for other undefined names
            errors.append(f"Name '{name}' is used but not defined or imported")

    return {
        "passed": len(errors) == 0,
        "errors": errors,
        "suggestions": suggestions
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = validate_staging_file(sys.argv[1])
        print(json.dumps(result, indent=2))
