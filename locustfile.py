from locust import HttpUser, task, between

class TelexUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def check_health(self):
        self.client.get("/health")
    
    @task
    def check_package(self):
        self.client.get(
            "/check/pip/requests",
            headers={"X-API-Key": "test-key-123"}
        )
if __name__ == "__main__":
    import locust
    locust.run()