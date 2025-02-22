from fastapi import FastAPI, Depends
from apscheduler.schedulers.background import BackgroundScheduler
from .config import validate_api_key
from .notifier import check_pip, check_npm, check_cargo
import json
import os

app = FastAPI()
packages = json.loads(os.getenv("TRACKED_PACKAGES"))

def check_updates():
    for manager in ["pip", "npm", "cargo"]:
        for pkg in packages.get(manager, []):
            current_version = "0.0.0"  # Replace with real version check
            checker = globals()[f"check_{manager}"]
            latest_version = checker(pkg)
            
            if latest_version and latest_version != current_version:
                message = f"{pkg} update: {current_version} → {latest_version}"
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
    return {"status": "ok", "scheduled_jobs": len(scheduler.get_jobs())}

@app.get("/check/{manager}/{package}")
async def manual_check(
    manager: str,
    package: str,
    auth: str = Depends(validate_api_key)
):
    checker = globals().get(f"check_{manager}")
    if not checker:
        return {"error": "Invalid package manager"}
    return {"version": checker(package)}