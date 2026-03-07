# NOTE: Fortress references found in this module. Proposals follow.
"""
modules/joi_fortress_simulator.py

Fortress Simulator for Joi v7/v8
================================
In-memory validation of proposed code extractions.
Uses joi_preflight for syntax and import validation.
Strictly non-destructive (no disk writes).
"""

import sys
import os
import json
import ast
import platform
from typing import List, Dict, Any, Optional

try:
    import pkg_resources
except ImportError:
    pkg_resources = None

try:
    from modules import joi_preflight
except ImportError:
    joi_preflight = None

def normalize_variants(obj: dict) -> List[dict]:
    """
    Safely normalize variants list. 
    Accepts missing 'variants' key and returns a list of dicts.
    """
    variants = obj.get("variants", [])
    if not isinstance(variants, list):
        return []
        
    normalized = []
    for v in variants:
        if isinstance(v, dict):
            normalized.append({
                "name": str(v.get("name", "unknown")),
                "description": str(v.get("description", "no description"))
            })
        elif isinstance(v, str):
            normalized.append({
                "name": v,
                "description": "no description"
            })
    return normalized

def check_circular_imports(file_path: str, new_content: str) -> List[str]:
    """
    Static analysis to detect potential circular imports.
    Simple check: does the file import its own module prefix or common core?
    """
    warnings = []
    try:
        tree = ast.parse(new_content)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        # Heuristic: if a module in 'modules/' imports 'modules.joi_orchestrator' 
        # and orchestrator imports it, it might be circular.
        # For now, we flag imports of core orchestration or itself.
        file_name = os.path.basename(file_path).replace(".py", "")
        for imp in imports:
            if imp.endswith(file_name):
                warnings.append(f"Potential self-import detected: {imp}")
            if imp in ["modules.joi_orchestrator", "joi_orchestrator"]:
                warnings.append(f"Import of core orchestrator ({imp}) may cause circularity if orchestrator uses this module.")
                
    except Exception as e:
        pass
    return warnings

def run_simulations(base_dir: str, proposals: List[dict]) -> dict:
    """
    Run in-memory simulations for a set of proposals.
    Each proposal should have: file_path, proposed_new_text.
    """
    report = {
        "results": [],
        "risk_summary": {
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "low_risk_count": 0
        },
        "environment": {
            "python_version": sys.version,
            "os": platform.platform(),
            "sys_path": sys.path[:5], # Limit for brevity
            "installed_packages": [f"{d.project_name}=={d.version}" for d in pkg_resources.working_set][:20] if pkg_resources else []
        }
    }

    for prop in proposals:
        file_path = prop.get("file_path", "unknown_file.py")
        new_text = prop.get("proposed_new_text", "")
        
        sim_result = {
            "file_path": file_path,
            "preflight_passed": True,
            "errors": [],
            "warnings": [],
            "risk_score": "Low"
        }

        # 1. Preflight validation
        if joi_preflight and file_path.endswith(".py"):
            try:
                pf_report = joi_preflight.preflight_validate_content(new_text, file_path)
                sim_result["preflight_passed"] = pf_report.get("passed", False)
                sim_result["errors"] = pf_report.get("errors", [])
                sim_result["warnings"] = pf_report.get("warnings", [])
            except Exception as e:
                sim_result["warnings"].append(f"Preflight internal error: {str(e)}")
        else:
            if not joi_preflight:
                sim_result["warnings"].append("joi_preflight module missing, skipping full validation.")

        # 2. Circular import check
        if file_path.endswith(".py"):
            circ_warns = check_circular_imports(file_path, new_text)
            sim_result["warnings"].extend(circ_warns)

        # 3. Import detection
        try:
            tree = ast.parse(new_text)
            imports_found = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports_found.append(ast.dump(node))
            sim_result["imports_detected"] = len(imports_found)
        except:
            sim_result["imports_detected"] = 0

        # 4. Risk Scoring
        if not sim_result["preflight_passed"] or sim_result["errors"]:
            sim_result["risk_score"] = "High"
            report["risk_summary"]["high_risk_count"] += 1
        elif sim_result["warnings"]:
            sim_result["risk_score"] = "Medium"
            report["risk_summary"]["medium_risk_count"] += 1
        else:
            sim_result["risk_score"] = "Low"
            report["risk_summary"]["low_risk_count"] += 1

        report["results"].append(sim_result)

    return report

if __name__ == "__main__":
    # Example usage / test
    test_proposals = [
        {
            "file_path": "test_module.py",
            "proposed_new_text": "import os\ndef test(): return 'ok'"
        }
    ]
    print(json.dumps(run_simulations(".", test_proposals), indent=2))