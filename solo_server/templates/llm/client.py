import requests
import json
import argparse

SERVER_URL = 'http://127.0.0.1:50100'

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Send a prompt to the LitServe Litgpt server.")
    parser.add_argument("--prompt", type=str, required=True, help="The prompt text to generate text from.")
    
    # Parse command line arguments
    args = parser.parse_args()
    
    # Use the provided prompt from the command line
    prompt_text = args.prompt
    
    # Define the server's URL and the endpoint
    predict_endpoint = "/predict"
    
    # Prepare the request data as a dictionary
    request_data = {
        "prompt": prompt_text
    }
    
    # Send a POST request to the server and receive the response
    response = requests.post(f"{SERVER_URL}{predict_endpoint}", json=request_data)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_data = json.loads(response.text)
        
        # Print the output from the response
        print("Response:", response_data["output"])
    else:
        print(f"Error: Received response code {response.status_code}")

if __name__ == "__main__":
    main()