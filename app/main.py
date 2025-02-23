from fastapi import FastAPI, Depends, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from .config import validate_api_key
from .notifier import check_pip, check_npm, check_cargo
from .utils import get_installed_version
from app.config import validate_api_key

import json
import os

app = FastAPI()
packages = json.loads(os.getenv("TRACKED_PACKAGES", "{}"))

# Manager to function mapping
CHECKERS = {
    "pip": check_pip,
    "npm": check_npm,
    "cargo": check_cargo
}

def check_updates():
    """Scheduled update checker with proper version tracking"""
    for manager in ["pip", "npm", "cargo"]:
        for pkg in packages.get(manager, []):
            current = get_installed_version(pkg, manager)
            latest = CHECKERS[manager](pkg)
            
            if current and latest and current != latest:
                message = f"{pkg} update: {current} → {latest}"
                requests.post(
                    os.getenv("TELEX_WEBHOOK_URL"),
                    json={"text": message},
                    headers={"X-API-Key": os.getenv("TELEX_API_KEY")}
                )

scheduler = BackgroundScheduler()
scheduler.add_job(check_updates, 'interval', hours=24)
scheduler.start()

@app.get("/health")
async def health_check():
    return {"status": "ok", "jobs": scheduler.get_jobs()}

@app.get("/check/{manager}/{package}")
async def manual_check(
    manager: str,
    package: str,
    auth: str = Depends(validate_api_key)
):
    """Endpoint with proper manager validation"""
    if manager not in CHECKERS:
        raise HTTPException(status_code=400, detail="Invalid package manager")
    
    current = get_installed_version(package, manager)
    latest = CHECKERS[manager](package)
    
    return {
        "package": package,
        "current": current,
        "latest": latest,
        "update_available": current != latest if all([current, latest]) else None
    }