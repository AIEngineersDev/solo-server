from locust import HttpUser, task, between
import json

class SoloServerUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def test_llm(self):
        """Test LLM completions endpoint"""
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": "What is AI?",
            "n_predict": 128
        }

        with self.client.post(
            "/predict",
            json=payload,
            headers=headers,
            catch_response=True
        ) as response:
            try:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed with status code: {response.status_code}")
            except json.JSONDecodeError:
                response.failure("Response could not be decoded as JSON")
            except Exception as e:
                response.failure(f"Error: {str(e)}")
