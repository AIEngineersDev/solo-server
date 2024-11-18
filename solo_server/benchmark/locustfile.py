from locust import HttpUser, task

class SoloServerUser(HttpUser):
    wait_time = lambda self: 0  # No wait between tasks

    @task
    def generate_text(self):
        """Simulates text generation requests."""
        payload = {
            "prompt": "Generate a Solo app with load tests.",
            "max_tokens": 100,
        }
        self.client.post("/v1/completions", json=payload)
