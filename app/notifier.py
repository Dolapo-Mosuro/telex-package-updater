import subprocess
import re
import requests
import os
import logging
from typing import Optional
from .utils import log_errors

logger = logging.getLogger(__name__)

@log_errors
def check_pip(package: str) -> Optional[str]:
    """Check PyPI for package version with timeout"""
    try:
        response = requests.get(
            f"https://pypi.org/pypi/{package}/json",
            timeout=5  # Added timeout
        )
        return response.json()["info"]["version"]
    except Exception as e:
        logger.error(f"PyPI check failed for {package}: {str(e)}")
        return None

@log_errors
def check_npm(package: str) -> Optional[str]:
    """Check npm registry with error logging"""
    try:
        result = subprocess.run(
            ["npm", "view", package, "version"],
            capture_output=True, 
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"npm check failed: {e.stderr}")
        return None

@log_errors
def check_cargo(package: str) -> Optional[str]:
    """Check Cargo.io with quiet flag"""
    try:
        result = subprocess.run(
            ["cargo", "search", "--quiet", package],  # Added --quiet
            capture_output=True,
            text=True,
            check=True
        )
        match = re.search(rf'"{package}" = "(.*)"', result.stdout)
        return match.group(1) if match else None
    except subprocess.CalledProcessError as e:
        logger.error(f"Cargo check failed: {e.stderr}")
        return None