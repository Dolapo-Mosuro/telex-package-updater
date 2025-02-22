import subprocess
import re
import requests
import os
from typing import Optional

def check_pip(package: str) -> Optional[str]:
    try:
        response = requests.get(f"https://pypi.org/pypi/{package}/json")
        return response.json()["info"]["version"]
    except Exception:
        return None

def check_npm(package: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["npm", "view", package, "version"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception:
        return None

def check_cargo(package: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["cargo", "search", package],
            capture_output=True, text=True
        )
        match = re.search(rf'"{package}" = "(.*)"', result.stdout)
        return match.group(1) if match else None
    except Exception:
        return None