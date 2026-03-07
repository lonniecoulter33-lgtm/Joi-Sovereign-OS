# NOTE: Fortress references found in this module. Proposals follow.
"""
scripts/generate_fortress_proposal.py

Fortress Proposal Orchestrator for Joi v7/v8
===========================================
1. Runs joi_fortress_scanner.
2. Identifies fortress-related Python modules.
3. Generates conservative surgical extraction proposals.
4. Calls joi_fortress_simulator for validation.
5. Assembles final proposal JSON.

Strictly non-destructive.
"""

import sys
import os
import json
import time
import difflib
from datetime import datetime
from typing import List, Dict, Any

# Ensure modules are importable
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

try:
    from modules import joi_fortress_scanner
    from modules import joi_fortress_simulator
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def generate_extraction_proposal(file_path: str, occurrences: List[dict]) -> str:
    """
    Generate a conservative proposal for extraction.
    For this prototype, it will suggest moving identified functions/classes 
    into a fortress_core.py module while leaving the original file intact (suggested diff).
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        lines = content.splitlines()
        extracted_lines = []
        modified_lines = list(lines)
        
        # Heuristic extraction: if a line contains 'fortress' and is a def/class, extract it.
        # This is strictly a suggestion for review.
        for occ in occurrences:
            ln = occ["line_number"] - 1
            if ln < len(lines):
                line = lines[ln]
                if "def " in line or "class " in line:
                    # Very simple extraction logic: copy the line
                    extracted_lines.append(line)
                    modified_lines[ln] = f"# PROPOSED EXTRACTION TO fortress_core.py: {line}"
                    
        if not extracted_lines:
            # If no functions found, just add a placeholder comment
            modified_lines.insert(0, "# NOTE: Fortress references found in this module. Proposals follow.")
            
        return "\n".join(modified_lines)
    except Exception as e:
        return f"# Error generating proposal for {file_path}: {e}"

def main():
    try:
        print(f"[*] Starting Fortress Scanner in {BASE_DIR}...")
        results = joi_fortress_scanner.scan_fortress_references(BASE_DIR)
        
        matches = results.get("matches", [])
        print(f"[*] Found {results['summary']['total_matches']} matches in {len(matches)} files.")
        
        proposals = []
        unified_diffs = []
        files_touched = []
        
        for file_info in matches:
            fpath = file_info["file_path"]
            if not fpath.endswith(".py"):
                continue
                
            print(f"[*] Generating extraction proposal for {os.path.basename(fpath)}...")
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    old_text = f.read()
                    
                new_text = generate_extraction_proposal(fpath, file_info["occurrences"])
                
                # Create diff
                diff = list(difflib.unified_diff(
                    old_text.splitlines(),
                    new_text.splitlines(),
                    fromfile=f"a/{os.path.relpath(fpath, BASE_DIR)}",
                    tofile=f"b/{os.path.relpath(fpath, BASE_DIR)}",
                    lineterm=""
                ))
                
                proposals.append({
                    "file_path": fpath,
                    "old_text": old_text,
                    "proposed_new_text": new_text,
                    "diff": "\n".join(diff)
                })
                unified_diffs.append("\n".join(diff))
                files_touched.append(os.path.relpath(fpath, BASE_DIR))
                
            except Exception as e:
                print(f"[!] Error processing {fpath}: {e}")

        print(f"[*] Running Simulation on {len(proposals)} proposals...")
        sim_results = joi_fortress_simulator.run_simulations(BASE_DIR, proposals)
        
        # Assemble final JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        proposal_filename = f"fortress_proposal_{timestamp}.json"
        proposal_dir = os.path.join(BASE_DIR, "proposals")
        
        if not os.path.exists(proposal_dir):
            os.makedirs(proposal_dir)
            
        proposal_path = os.path.join(proposal_dir, proposal_filename)
        
        final_proposal = {
            "do_not_apply": True,
            "timestamp": timestamp,
            "files_touched": files_touched,
            "proposals": proposals,
            "unified_diffs": unified_diffs,
            "preflight_results": {p["file_path"]: sim_results["results"][i] for i, p in enumerate(proposals)},
            "risk_analysis": sim_results["risk_summary"],
            "environment_snapshot": sim_results["environment"],
            "backup_instructions": [
                f"# Recommended backup command for {f}" 
                for f in files_touched
            ],
            "reconciliation_notes": [
                "References found in learning_data.json and operations manual must be manually validated."
            ],
            "scanner_summary": results["summary"]
        }
        
        with open(proposal_path, "w", encoding="utf-8") as f:
            json.dump(final_proposal, f, indent=2)
            
        print("\n" + "="*60)
        print(f"SUCCESS: Fortress proposal generated.")
        print(f"File: {os.path.abspath(proposal_path)}")
        print("="*60)
        sys.exit(0)
        
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()