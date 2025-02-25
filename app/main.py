from fastapi import FastAPI, BackgroundTasks, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import httpx
import asyncio
import json
from .config import validate_api_key

app = FastAPI()

class Setting(BaseModel):
    id: str  # Added
    label: str
    type: str
    required: bool
    default: str

class MonitorPayload(BaseModel):
    channel_id: str
    return_url: str
    settings: List[Setting]

@app.get("/integration.json")
def get_integration_json(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "descriptions": {
            "app_name": "Package Update Notifier",
            "app_description": "Tracks updates for dependencies in a project and sends changelogs to Telex.",
            "app_url": base_url,
            "app_logo": "https://i.imgur.com/lZqvffp.png"
        },
        "integration_type": "interval",
        "settings": [
            {
                "id": "tracked_packages",
                "label": "Packages to Track",
                "type": "json",
                "required": True,
                "default": json.dumps({"pip": [], "npm": [], "cargo": []})
            },
            {
                "id": "interval",
                "label": "Check Interval",
                "type": "cron",  # Changed from text
                "required": True,
                "default": "0 0 * * *"  # Daily at midnight
            }
        ],
        "tick_url": f"{base_url}/tick"
    }

@app.post("/tick", status_code=202)
def monitor(
    payload: MonitorPayload,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(validate_api_key)  # Added auth
):
    background_tasks.add_task(monitor_task, payload)
    return {"status": "accepted"}

async def monitor_task(payload: MonitorPayload):
    tracked_packages = {}
    for setting in payload.settings:
        if setting.id == "tracked_packages":
            try:
                tracked_packages = json.loads(setting.default)  # Fixed
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
                return

    results = {}
    for manager, packages in tracked_packages.items():
        results[manager] = await check_package_updates(manager, packages)

    updates = [
        f"{pkg}: {ver}" for manager in results.values() 
        for pkg, ver in manager.items() if "Error" not in ver
    ]
    
    data = {
        "text": "Package Updates:\n" + "\n".join(updates),  # Telex-compatible
        "username": "Package Notifier",
        "icon_url": "https://i.imgur.com/lZqvffp.png"
    }

    async with httpx.AsyncClient() as client:
        await client.post(payload.return_url, json=data)