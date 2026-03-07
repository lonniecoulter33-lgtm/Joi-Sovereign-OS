"""
modules/joi_fortress_scanner.py

Fortress Reference Scanner for Joi v7/v8
========================================
Recursively searches the repository for "fortress" related strings, 
imports, and configurations. Provides a classification for each match.

Strictly read-only.
"""

import os
import re
import json
import hashlib
import time
from pathlib import Path
from typing import List, Dict, Any

# Classification patterns
PATTERNS = {
    "module": re.compile(r"import\s+.*fortress|from\s+.*fortress", re.IGNORECASE),
    "config": re.compile(r"\"fortress\"\s*:", re.IGNORECASE),
    "learning_data": re.compile(r"digital\s+fortress", re.IGNORECASE),
    "manual": re.compile(r"Operations\s+Manual|Fortress\s+Upgrades", re.IGNORECASE),
}

def get_file_hash(file_path: str) -> str:
    """Generate SHA-256 hash for a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return "unknown"

def classify_match(file_path: str, line_text: str) -> str:
    """Classify a match based on file path and content."""
    path_lower = file_path.lower()
    
    if "manual" in path_lower or file_path.endswith(".md"):
        return "manual"
    if "learning_data.json" in path_lower:
        return "learning_data"
    if "config" in path_lower or file_path.endswith(".json"):
        return "config"
    if line_text:
        if PATTERNS["module"].search(line_text):
            return "import"
    if file_path.endswith(".py"):
        return "module"
    
    return "other"

def find_files_by_pattern(patterns: List[str], base_dir: str) -> List[str]:
    """Find files that match naming patterns recursively."""
    matches = []
    regexes = [re.compile(p, re.IGNORECASE) for p in patterns]
    
    for root, dirs, files in os.walk(base_dir):
        # Skip some directories to be safe and efficient
        if any(d in root for d in [".git", "__pycache__", "node_modules", "venv", "myenv"]):
            continue
            
        for file in files:
            if any(r.search(file) for r in regexes):
                matches.append(os.path.join(root, file))
    return matches

# FORTRESS NOTE: This function is a candidate for extraction to fortress_core.py
def scan_fortress_references(base_dir: str) -> Dict[str, Any]:
    """
    Recursively search repository for fortress references.
    Returns a JSON-serializable report.
    """
    report = {
        "matches": [],
        "summary": {
            "total_files_scanned": 0,
            "total_matches": 0,
            "matches_by_tag": {}
        }
    }
    
    keyword_regex = re.compile(r"fortress|digital\s+fortress", re.IGNORECASE)
    
    for root, dirs, files in os.walk(base_dir):
        if any(d in root for d in [".git", "__pycache__", "node_modules", "venv", "myenv", ".claude"]):
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            report["summary"]["total_files_scanned"] += 1
            
            try:
                file_size = os.path.getsize(file_path)
                # Read file for content matches
                # Limit size to prevent memory issues with binaries
                if file_size > 10 * 1024 * 1024: # 10MB
                    continue
                    
                matches_in_file = []
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        if keyword_regex.search(line):
                            tag = classify_match(file_path, line)
                            matches_in_file.append({
                                "file_path": os.path.abspath(file_path),
                                "line_number": line_num,
                                "match_text_snippet": line.strip()[:200], # Context window snippet
                                "classification_tag": tag
                            })
                            report["summary"]["matches_by_tag"][tag] = report["summary"]["matches_by_tag"].get(tag, 0) + 1
                
                if matches_in_file:
                    file_info = {
                        "file_path": os.path.abspath(file_path),
                        "file_hash": get_file_hash(file_path),
                        "file_size": file_size,
                        "last_modified": time.ctime(os.path.getmtime(file_path)),
                        "occurrences": matches_in_file
                    }
                    report["matches"].append(file_info)
                    report["summary"]["total_matches"] += len(matches_in_file)
                    
            except Exception:
                # Skip files that can't be read
                continue
                
    return report

if __name__ == "__main__":
    import sys
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    results = scan_fortress_references(base)
    print(json.dumps(results, indent=2))