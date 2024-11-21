from locust import HttpUser, task, between
import json
import time


class SoloServerUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def test_llm(self):
        """Test LLM completions endpoint with additional metrics"""
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": "What is AI?",
            "n_predict": 128
        }

        start_time = time.time()

        with self.client.post(
            "/predict",
            json=payload,
            headers=headers,
            catch_response=True,
            stream=True
        ) as response:
            try:
                if response.status_code == 200:
                    total_latency = time.time() - start_time
                    data = response.json()

                    # Extract metrics
                    generated_text = data.get("generated_text", "")
                    tokens_generated = len(generated_text.split())
                    qps = 1 / total_latency if total_latency > 0 else 0

                    # Calculate streaming metrics
                    streaming_times = []
                    first_token_time = None

                    for token_event in data.get("streaming_events", []):
                        token_time = token_event.get("timestamp")
                        if first_token_time is None:
                            first_token_time = token_time
                        else:
                            streaming_times.append(token_time - first_token_time)

                    ttft = first_token_time - start_time if first_token_time else None
                    per_token_latencies = streaming_times

                    # Log metrics
                    response.success()
                    self.environment.events.request_success.fire(
                        request_type="POST",
                        name="/predict",
                        response_time=total_latency * 1000,  # ms
                        response_length=len(response.content),
                    )
                    print(f"Metrics: Total Latency = {total_latency:.3f}s, "
                          f"Tokens Generated = {tokens_generated}, QPS = {qps:.2f}, "
                          f"TTFT = {ttft:.3f}s, Per Token Latency = {per_token_latencies}")

                else:
                    response.failure(f"Failed with status code: {response.status_code}")
            except json.JSONDecodeError:
                response.failure("Response could not be decoded as JSON")
            except Exception as e:
                response.failure(f"Error: {str(e)}")
