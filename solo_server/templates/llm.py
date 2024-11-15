# server.py
import litserve as ls
import subprocess
import os
import json

# STEP 1: DEFINE YOUR MODEL API
class LlamaLitAPI(ls.LitAPI):
    def setup(self, device):
        # Get values from environment variables
        model_url = os.getenv("MODEL_URL")
        model_filename = os.getenv("MODEL_FILENAME")
        
        if not model_url or not model_filename:
            raise ValueError("MODEL_URL and MODEL_FILENAME environment variables must be set")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, model_filename)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Download model
        subprocess.run(["wget", "-O", model_path, model_url], check=True)
        
        os.chmod(model_path, 0o755)
        
        shell_script_path = os.path.join(current_dir, "run_llama.sh")
        with open(shell_script_path, "w") as f:
            f.write(f'''#!/bin/bash
DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" && pwd )"
"$DIR/{model_filename}" --server
''')
        os.chmod(shell_script_path, 0o755)
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.model_process = subprocess.Popen(["bash", shell_script_path], 
                                                    stdout=subprocess.PIPE, 
                                                    stderr=subprocess.PIPE)
                if self.model_process.poll() is None:
                    break
            except subprocess.SubprocessError as e:
                print(f"Error starting model server (attempt {retry_count + 1}/{max_retries}): {e}")
                retry_count += 1
                if retry_count == max_retries:
                    raise RuntimeError("Failed to start model server after multiple attempts")
        print("Llama model server started.")

    def decode_request(self, request):
        return request["prompt"]

    def predict(self, prompt):
        response = subprocess.run(["curl", "-X", "POST", "http://localhost:8080/completion", 
                                 "-H", "Content-Type: application/json", 
                                 "-d", f'{{"prompt": "{prompt}", "n_predict": 128}}'], 
                                capture_output=True, text=True)
        response_json = json.loads(response.stdout)
        return response_json["content"]

    def encode_response(self, output):
        # Clean up the output by removing system tokens, newlines, and redundant text
        cleaned_output = output.replace("<|eot_id|>", "")  # Remove system token
        cleaned_output = cleaned_output.replace("\n", " ")  # Replace newlines with spaces
        cleaned_output = " ".join(cleaned_output.split())  # Remove extra spaces
        return {"generated_text": cleaned_output}


# STEP 2: START THE SERVER
if __name__ == "__main__":
    api = LlamaLitAPI()
    server = ls.LitServer(api, accelerator="auto")
    server.run(port=8000, generate_client_file=False)