import requests
import json
import typer

def serve(
    model: str = typer.Option("llama3.2", "--model", "-m", help="Model to use"),
    input: str = typer.Option("Hello", "--input", "-i", help="Input text for inference"),
    stream: bool = typer.Option(False, "--stream", "-s", help="Enable streaming mode")
):
    # API Endpoint
    url = "http://localhost:11434/api/chat"

    # Chat request payload
    data = {
        "model": model, 
        "messages": [
            {
                "role": "user",
                "content": input
            }
        ],
        "stream": stream  # Set to True for streaming
    }

    if data["stream"] == False:
        # Sending POST request
        response = requests.post(url, json=data)
        # Check if response is valid JSON
        try:
            response_json = response.json()
            if "message" in response_json and "content" in response_json["message"]:
                print("Assistant Response:", response_json["message"]["content"])
            else:
                print("Unexpected Response:", json.dumps(response_json, indent=2))
        except json.JSONDecodeError:
            print("Error: API did not return valid JSON.")
            print("Raw Response:", response.text)


    else:
        with requests.post(url, json=data, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    json_obj = json.loads(line)
                    if "message" in json_obj and "content" in json_obj["message"]:
                        print(json_obj["message"]["content"], end="", flush=True)  # Streaming output
