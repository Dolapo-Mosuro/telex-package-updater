import subprocess
import re
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)

def log_errors(func):
    """Decorator for consistent error logging"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

def get_installed_version(pkg: str, manager: str) -> Optional[str]:
    """Get currently installed version"""
    try:
        if manager == "pip":
            result = subprocess.run(
                ["pip", "show", pkg],
                capture_output=True,
                text=True
            )
            return re.search(r"Version: (.*)", result.stdout).group(1)
        
        elif manager == "npm":
            result = subprocess.run(
                ["npm", "list", pkg, "--depth=0", "--json"],
                capture_output=True,
                text=True
            )
            return json.loads(result.stdout)["dependencies"][pkg]["version"]
        
        elif manager == "cargo":
            result = subprocess.run(
                ["cargo", "tree", "--quiet", "--package", pkg, "--depth", "0"],
                capture_output=True,
                text=True
            )
            return re.search(rf"{pkg} v(.*)", result.stdout).group(1)
            
    except Exception as e:
        logging.error(f"Version check failed for {pkg}: {str(e)}")
        return None