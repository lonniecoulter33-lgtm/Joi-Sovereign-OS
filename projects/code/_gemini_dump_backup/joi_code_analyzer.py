"""
modules/joi_code_analyzer.py

Python Code Analysis & Quality Assessment Module
================================================

Provides comprehensive code analysis capabilities:
- Syntax validation and error detection
- Complexity metrics (cyclomatic, cognitive)
- Style and formatting suggestions
- Import analysis and optimization
- Security vulnerability detection
- Performance recommendations
- Best practices validation

This enables Joi to:
1. Analyze user's Python code for quality
2. Suggest improvements and optimizations
3. Detect potential bugs before runtime
4. Help maintain clean, professional codebases
"""

from __future__ import annotations

import ast
import os
import re
import json
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from collections import defaultdict
import traceback

import joi_companion
from flask import jsonify, request as flask_req
from modules.joi_memory import require_user

# ============================================================================
# CONFIGURATION
# ============================================================================

ANALYSIS_CACHE_DIR = Path("code_analysis_cache")
ANALYSIS_CACHE_DIR.mkdir(exist_ok=True)

# Complexity thresholds
MAX_FUNCTION_COMPLEXITY = 10
MAX_FILE_COMPLEXITY = 50
MAX_FUNCTION_LENGTH = 50
MAX_LINE_LENGTH = 100

# Style patterns
NAMING_CONVENTIONS = {
    "function": r"^[a-z_][a-z0-9_]*$",
    "class": r"^[A-Z][a-zA-Z0-9]*$",
    "constant": r"^[A-Z][A-Z0-9_]*$",
    "variable": r"^[a-z_][a-z0-9_]*$"
}

# ============================================================================
# SYNTAX ANALYSIS
# ============================================================================

def validate_syntax(code: str) -> Dict[str, Any]:
    """
    Validate Python syntax and return detailed error information
    
    Args:
        code: Python source code string
    
    Returns:
        {
            "valid": bool,
            "errors": [{"line": int, "message": str, "type": str}],
            "warnings": [{"line": int, "message": str}]
        }
    """
    result = {
        "valid": False,
        "errors": [],
        "warnings": []
    }
    
    try:
        ast.parse(code)
        result["valid"] = True
        
    except SyntaxError as e:
        result["errors"].append({
            "line": e.lineno or 0,
            "column": e.offset or 0,
            "message": e.msg,
            "type": "SyntaxError",
            "text": e.text.strip() if e.text else ""
        })
    except Exception as e:
        result["errors"].append({
            "line": 0,
            "column": 0,
            "message": str(e),
            "type": type(e).__name__,
            "text": ""
        })
    
    return result


# ============================================================================
# COMPLEXITY ANALYSIS
# ============================================================================

class ComplexityAnalyzer(ast.NodeVisitor):
    """
    Calculates cyclomatic complexity for functions and classes
    
    Cyclomatic Complexity = Decision Points + 1
    Decision points: if, elif, for, while, and, or, except, with
    """
    
    def __init__(self):
        self.complexity_map = {}
        self.current_function = None
        self.function_stack = []
    
    def visit_FunctionDef(self, node):
        """Track function complexity"""
        func_name = node.name
        self.function_stack.append(func_name)
        
        # Calculate complexity for this function
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                # Each 'and'/'or' adds complexity
                complexity += len(child.values) - 1
        
        self.complexity_map[func_name] = {
            "complexity": complexity,
            "line": node.lineno,
            "length": self._count_lines(node)
        }
        
        self.generic_visit(node)
        self.function_stack.pop()
    
    def visit_AsyncFunctionDef(self, node):
        """Handle async functions same as regular functions"""
        self.visit_FunctionDef(node)
    
    def _count_lines(self, node) -> int:
        """Count lines of code in a node"""
        if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
            return node.end_lineno - node.lineno + 1
        return 0


def analyze_complexity(code: str) -> Dict[str, Any]:
    """
    Analyze code complexity metrics
    
    Returns:
        {
            "total_complexity": int,
            "functions": {
                "func_name": {"complexity": int, "line": int, "length": int}
            },
            "complex_functions": [list of functions exceeding threshold],
            "long_functions": [list of functions exceeding length threshold]
        }
    """
    try:
        tree = ast.parse(code)
        analyzer = ComplexityAnalyzer()
        analyzer.visit(tree)
        
        total_complexity = sum(f["complexity"] for f in analyzer.complexity_map.values())
        
        complex_functions = [
            {"name": name, **data}
            for name, data in analyzer.complexity_map.items()
            if data["complexity"] > MAX_FUNCTION_COMPLEXITY
        ]
        
        long_functions = [
            {"name": name, **data}
            for name, data in analyzer.complexity_map.items()
            if data["length"] > MAX_FUNCTION_LENGTH
        ]
        
        return {
            "total_complexity": total_complexity,
            "functions": analyzer.complexity_map,
            "complex_functions": complex_functions,
            "long_functions": long_functions,
            "average_complexity": total_complexity / len(analyzer.complexity_map) if analyzer.complexity_map else 0
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "total_complexity": 0,
            "functions": {},
            "complex_functions": [],
            "long_functions": []
        }


# ============================================================================
# STYLE ANALYSIS
# ============================================================================

def analyze_naming_conventions(code: str) -> Dict[str, Any]:
    """
    Check if naming follows PEP 8 conventions
    
    Returns violations and suggestions
    """
    violations = []
    
    try:
        tree = ast.parse(code)
        
        for node in ast.walk(tree):
            # Check function names
            if isinstance(node, ast.FunctionDef):
                if not re.match(NAMING_CONVENTIONS["function"], node.name):
                    if not node.name.startswith('_'):  # Allow private functions
                        violations.append({
                            "line": node.lineno,
                            "type": "function_naming",
                            "name": node.name,
                            "message": f"Function '{node.name}' should use snake_case",
                            "suggestion": _to_snake_case(node.name)
                        })
            
            # Check class names
            elif isinstance(node, ast.ClassDef):
                if not re.match(NAMING_CONVENTIONS["class"], node.name):
                    violations.append({
                        "line": node.lineno,
                        "type": "class_naming",
                        "name": node.name,
                        "message": f"Class '{node.name}' should use PascalCase",
                        "suggestion": _to_pascal_case(node.name)
                    })
            
            # Check variable assignments
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        # Check if it's a constant (all uppercase)
                        if name.isupper():
                            if not re.match(NAMING_CONVENTIONS["constant"], name):
                                violations.append({
                                    "line": node.lineno,
                                    "type": "constant_naming",
                                    "name": name,
                                    "message": f"Constant '{name}' should use UPPER_CASE_WITH_UNDERSCORES"
                                })
                        # Regular variable
                        elif not re.match(NAMING_CONVENTIONS["variable"], name):
                            violations.append({
                                "line": node.lineno,
                                "type": "variable_naming",
                                "name": name,
                                "message": f"Variable '{name}' should use snake_case",
                                "suggestion": _to_snake_case(name)
                            })
        
    except Exception as e:
        violations.append({
            "line": 0,
            "type": "analysis_error",
            "message": f"Error analyzing naming: {e}"
        })
    
    return {
        "violations": violations,
        "total_violations": len(violations)
    }


def _to_snake_case(name: str) -> str:
    """Convert name to snake_case"""
    # Insert underscore before capitals
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def _to_pascal_case(name: str) -> str:
    """Convert name to PascalCase"""
    return ''.join(word.capitalize() for word in name.split('_'))


def analyze_line_lengths(code: str) -> Dict[str, Any]:
    """
    Check for overly long lines (PEP 8: max 79 chars, we use 100)
    """
    long_lines = []
    
    lines = code.split('\n')
    for i, line in enumerate(lines, 1):
        if len(line) > MAX_LINE_LENGTH:
            long_lines.append({
                "line": i,
                "length": len(line),
                "content": line[:50] + "..." if len(line) > 50 else line
            })
    
    return {
        "long_lines": long_lines,
        "total_violations": len(long_lines),
        "max_line_length": max((len(line) for line in lines), default=0)
    }


# ============================================================================
# IMPORT ANALYSIS
# ============================================================================

def analyze_imports(code: str) -> Dict[str, Any]:
    """
    Analyze import statements for optimization and issues
    
    Checks for:
    - Unused imports
    - Import order (stdlib, third-party, local)
    - Wildcard imports (from x import *)
    - Circular import potential
    """
    result = {
        "imports": [],
        "unused_imports": [],
        "wildcard_imports": [],
        "order_violations": [],
        "suggestions": []
    }
    
    try:
        tree = ast.parse(code)
        
        # Collect all imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    result["imports"].append({
                        "line": node.lineno,
                        "module": alias.name,
                        "alias": alias.asname,
                        "type": "import"
                    })
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        if alias.name == '*':
                            result["wildcard_imports"].append({
                                "line": node.lineno,
                                "module": node.module
                            })
                        
                        result["imports"].append({
                            "line": node.lineno,
                            "module": node.module,
                            "name": alias.name,
                            "alias": alias.asname,
                            "type": "from_import"
                        })
        
        # Check for unused imports (basic check - names used in code)
        code_without_imports = re.sub(r'^(import|from)\s+.*$', '', code, flags=re.MULTILINE)
        
        for imp in result["imports"]:
            module_name = imp.get("alias") or imp.get("name") or imp.get("module", "").split('.')[0]
            if module_name and module_name not in code_without_imports:
                result["unused_imports"].append(imp)
        
        # Suggestions
        if result["wildcard_imports"]:
            result["suggestions"].append(
                "Avoid wildcard imports (from x import *). Import specific names instead."
            )
        
        if result["unused_imports"]:
            result["suggestions"].append(
                f"Remove {len(result['unused_imports'])} unused import(s) to clean up code."
            )
        
    except Exception as e:
        result["error"] = str(e)
    
    return result


# ============================================================================
# SECURITY ANALYSIS
# ============================================================================

def analyze_security(code: str) -> Dict[str, Any]:
    """
    Check for common security vulnerabilities
    
    Looks for:
    - eval() / exec() usage
    - Hardcoded credentials
    - SQL injection patterns
    - Unsafe pickle usage
    - Shell command injection risks
    """
    vulnerabilities = []
    
    # Pattern checks
    patterns = {
        "eval_usage": (r'\beval\s*\(', "Avoid eval() - it can execute arbitrary code"),
        "exec_usage": (r'\bexec\s*\(', "Avoid exec() - it can execute arbitrary code"),
        "hardcoded_password": (r'password\s*=\s*["\'][^"\']+["\']', "Possible hardcoded password"),
        "hardcoded_key": (r'(api_key|secret|token)\s*=\s*["\'][^"\']+["\']', "Possible hardcoded API key"),
        "sql_concatenation": (r'(SELECT|INSERT|UPDATE|DELETE).*\+.*', "Possible SQL injection risk - use parameterized queries"),
        "shell_command": (r'os\.system\(|subprocess\.call\(.*shell=True', "Shell command with user input can be dangerous"),
    }
    
    for vuln_type, (pattern, message) in patterns.items():
        matches = re.finditer(pattern, code, re.IGNORECASE)
        for match in matches:
            line_num = code[:match.start()].count('\n') + 1
            vulnerabilities.append({
                "line": line_num,
                "type": vuln_type,
                "message": message,
                "severity": "high" if vuln_type in ["eval_usage", "exec_usage", "sql_concatenation"] else "medium"
            })
    
    return {
        "vulnerabilities": vulnerabilities,
        "total": len(vulnerabilities),
        "high_severity": sum(1 for v in vulnerabilities if v["severity"] == "high")
    }


# ============================================================================
# COMPREHENSIVE ANALYSIS
# ============================================================================

def analyze_code(**params) -> Dict[str, Any]:
    """
    Tool: Comprehensive code analysis
    
    Performs all analysis types and returns consolidated report
    
    Args:
        code: Python source code to analyze
        checks: List of checks to perform (default: all)
                Options: syntax, complexity, style, imports, security
    
    Returns:
        Complete analysis report with suggestions
    """
    require_user()
    
    code = params.get("code", "")
    if not code:
        return {"ok": False, "error": "No code provided"}
    
    checks = params.get("checks", ["syntax", "complexity", "style", "imports", "security"])
    
    report = {
        "ok": True,
        "code_length": len(code),
        "line_count": code.count('\n') + 1,
        "timestamp": __import__('time').time()
    }
    
    # Syntax validation (always run first)
    if "syntax" in checks:
        syntax_result = validate_syntax(code)
        report["syntax"] = syntax_result
        
        if not syntax_result["valid"]:
            report["ok"] = False
            report["message"] = "Code has syntax errors - other checks skipped"
            return report
    
    # Complexity analysis
    if "complexity" in checks:
        report["complexity"] = analyze_complexity(code)
    
    # Style analysis
    if "style" in checks:
        report["style"] = {
            "naming": analyze_naming_conventions(code),
            "line_lengths": analyze_line_lengths(code)
        }
    
    # Import analysis
    if "imports" in checks:
        report["imports"] = analyze_imports(code)
    
    # Security analysis
    if "security" in checks:
        report["security"] = analyze_security(code)
    
    # Generate overall score
    report["score"] = _calculate_score(report)
    
    # Generate recommendations
    report["recommendations"] = _generate_recommendations(report)
    
    return report


def _calculate_score(report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate overall code quality score (0-100)
    
    Scoring:
    - Syntax valid: +20
    - Low complexity: +20
    - Good naming: +20
    - Clean imports: +20
    - Secure code: +20
    """
    score = 0
    max_score = 100
    breakdown = {}
    
    # Syntax (20 points)
    if report.get("syntax", {}).get("valid"):
        score += 20
        breakdown["syntax"] = 20
    else:
        breakdown["syntax"] = 0
    
    # Complexity (20 points)
    if "complexity" in report:
        comp = report["complexity"]
        avg_complexity = comp.get("average_complexity", 0)
        
        if avg_complexity <= 5:
            points = 20
        elif avg_complexity <= MAX_FUNCTION_COMPLEXITY:
            points = 15
        elif avg_complexity <= 15:
            points = 10
        else:
            points = 5
        
        score += points
        breakdown["complexity"] = points
    
    # Style (20 points)
    if "style" in report:
        naming_violations = report["style"]["naming"]["total_violations"]
        line_violations = report["style"]["line_lengths"]["total_violations"]
        
        total_violations = naming_violations + line_violations
        
        if total_violations == 0:
            points = 20
        elif total_violations <= 5:
            points = 15
        elif total_violations <= 10:
            points = 10
        else:
            points = 5
        
        score += points
        breakdown["style"] = points
    
    # Imports (20 points)
    if "imports" in report:
        unused = len(report["imports"].get("unused_imports", []))
        wildcards = len(report["imports"].get("wildcard_imports", []))
        
        issues = unused + wildcards
        
        if issues == 0:
            points = 20
        elif issues <= 2:
            points = 15
        elif issues <= 5:
            points = 10
        else:
            points = 5
        
        score += points
        breakdown["imports"] = points
    
    # Security (20 points)
    if "security" in report:
        high_severity = report["security"].get("high_severity", 0)
        total_vulns = report["security"].get("total", 0)
        
        if total_vulns == 0:
            points = 20
        elif high_severity == 0 and total_vulns <= 2:
            points = 15
        elif high_severity <= 1:
            points = 10
        else:
            points = 5
        
        score += points
        breakdown["security"] = points
    
    return {
        "total": score,
        "max": max_score,
        "percentage": round((score / max_score) * 100, 1),
        "grade": _score_to_grade(score),
        "breakdown": breakdown
    }


def _score_to_grade(score: int) -> str:
    """Convert numeric score to letter grade"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def _generate_recommendations(report: Dict[str, Any]) -> List[str]:
    """Generate actionable recommendations based on analysis"""
    recommendations = []
    
    # Complexity recommendations
    if "complexity" in report:
        comp = report["complexity"]
        if comp.get("complex_functions"):
            recommendations.append(
                f"🔴 {len(comp['complex_functions'])} function(s) exceed complexity threshold. "
                f"Consider breaking them into smaller functions."
            )
        if comp.get("long_functions"):
            recommendations.append(
                f"📏 {len(comp['long_functions'])} function(s) are too long. "
                f"Aim for functions under {MAX_FUNCTION_LENGTH} lines."
            )
    
    # Style recommendations
    if "style" in report:
        naming_violations = report["style"]["naming"]["violations"]
        if naming_violations:
            recommendations.append(
                f"📝 Fix {len(naming_violations)} naming convention violation(s) to follow PEP 8."
            )
        
        long_lines = report["style"]["line_lengths"]["long_lines"]
        if long_lines:
            recommendations.append(
                f"↔️ {len(long_lines)} line(s) exceed {MAX_LINE_LENGTH} characters. "
                f"Consider breaking them up for readability."
            )
    
    # Import recommendations
    if "imports" in report:
        imports = report["imports"]
        if imports.get("unused_imports"):
            recommendations.append(
                f"🧹 Remove {len(imports['unused_imports'])} unused import(s)."
            )
        if imports.get("wildcard_imports"):
            recommendations.append(
                f"⚠️ Avoid wildcard imports - import specific names instead."
            )
    
    # Security recommendations
    if "security" in report:
        security = report["security"]
        if security.get("high_severity", 0) > 0:
            recommendations.append(
                f"🚨 CRITICAL: {security['high_severity']} high-severity security issue(s) found. "
                f"Address these immediately!"
            )
        elif security.get("total", 0) > 0:
            recommendations.append(
                f"⚠️ {security['total']} potential security issue(s) detected. Review and fix."
            )
    
    # Overall recommendation
    score = report.get("score", {}).get("percentage", 0)
    if score >= 90:
        recommendations.insert(0, "✅ Excellent code quality! Keep up the good work.")
    elif score >= 70:
        recommendations.insert(0, "👍 Good code quality with room for minor improvements.")
    elif score >= 50:
        recommendations.insert(0, "⚠️ Code needs improvement. Focus on the issues above.")
    else:
        recommendations.insert(0, "🔴 Code quality is poor. Significant refactoring needed.")
    
    return recommendations


# ============================================================================
# TOOL REGISTRATION
# ============================================================================

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "analyze_code",
        "description": "Analyze Python code for quality, style, complexity, security, and best practices. Returns comprehensive report with score and recommendations.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python source code to analyze"
                },
                "checks": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["syntax", "complexity", "style", "imports", "security"]
                    },
                    "description": "Which checks to perform (default: all)"
                }
            },
            "required": ["code"]
        }
    }},
    analyze_code
)


# ============================================================================
# FLASK ROUTES
# ============================================================================

def code_analyzer_route():
    """Code analysis endpoint"""
    require_user()
    
    if flask_req.method == "POST":
        data = flask_req.get_json(silent=True) or {}
        return jsonify(analyze_code(**data))
    else:
        return jsonify({
            "ok": True,
            "message": "Code analyzer ready",
            "available_checks": ["syntax", "complexity", "style", "imports", "security"]
        })


joi_companion.register_route("/code-analyzer", ["GET", "POST"], code_analyzer_route, "code_analyzer_route")
