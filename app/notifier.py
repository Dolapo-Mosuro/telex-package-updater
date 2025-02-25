from locust import HttpUser, task, between
import json

class TelexUser(HttpUser):
    wait_time = between(5, 15)
    
    @task
    def trigger_check(self):
        payload = {
            "channel_id": "test-channel",
            "return_url": "https://your-telex-webhook-url",
            "settings": [
                {
                    "id": "tracked_packages",
                    "label": "Packages to Track",
                    "type": "json",
                    "required": True,
                    "default": json.dumps({"pip": ["requests"], "npm": ["react"]})
                },
                {
                    "id": "interval",
                    "label": "Check Interval",
                    "type": "cron",
                    "required": True,
                    "default": "0 0 * * *"
                }
            ]
        }
        self.client.post(
            "/tick",
            json=payload,
            headers={"X-API-Key": "your-test-key"}
        )