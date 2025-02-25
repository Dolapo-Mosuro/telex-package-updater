from typing import Optional, Dict, Any
import subprocess
import re
import json
import logging

def parse_version(output: str, pattern: str) -> Optional[str]:
    """Universal version parser"""
    try:
        match = re.search(pattern, output)
        return match.group(1) if match else None
    except Exception as e:
        logging.error(f"Version parsing failed: {str(e)}")
        return None

def get_installed_version(pkg: str, manager: str) -> Optional[str]:
    """Improved version check with common parser"""
    commands = {
        "pip": ["pip", "show", pkg],
        "npm": ["npm", "list", pkg, "--depth=0", "--json"],
        "cargo": ["cargo", "tree", "--quiet", "--package", pkg, "--depth", "0"]
    }
    
    patterns = {
        "pip": r"Version: (.*)",
        "npm": rf'"dependencies": {{"{pkg}": {{"version": "(.*?)"}}}}',
        "cargo": rf"{pkg} v(.*)"
    }
    
    try:
        result = subprocess.run(
            commands[manager],
            capture_output=True,
            text=True,
            check=True
        )
        return parse_version(result.stdout, patterns[manager])
    except Exception as e:
        logging.error(f"Version check failed for {pkg}: {str(e)}")
        return None
