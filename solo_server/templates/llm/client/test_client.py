import requests
import json

def test_llama_api():
    url = "http://localhost:8000/predict"
    headers = {"Content-Type": "application/json"}
    
    prompts = [
        "What is the capital of France?",
        "Explain the concept of machine learning in simple terms.",
        "Write a short poem about a cat."
    ]
    
    for prompt in prompts:
        data = {"prompt": prompt}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            result = response.json()
            print(f"Prompt: {prompt}")
            print(f"Response: {result['generated_text']}")
            print("-" * 50)
        else:
            print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_llama_api()