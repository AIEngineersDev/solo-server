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
        # Handle both POST /predict and direct completion requests
        if isinstance(request, dict):
            return request.get("prompt", request.get("input", ""))
        return request

    def predict(self, prompt):
        try:
            # Internal request to LLaMA server on 8080
            response = subprocess.run(
                ["curl", "-s", "http://localhost:8080/completion",
                 "-H", "Content-Type: application/json",
                 "-d", json.dumps({
                     "prompt": prompt,
                     "n_predict": 128
                 })],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if response.returncode != 0:
                print(f"Error from LLM server: {response.stderr}")
                return f"Error: {response.stderr}"
                
            result = json.loads(response.stdout)
            return result.get("content", "No content generated")
            
        except Exception as e:
            print(f"Error in predict: {e}")
            return f"Error: {str(e)}"

    def encode_response(self, output):
        if isinstance(output, str):
            cleaned_output = output.replace("<|eot_id|>", "").replace("\n", " ").strip()
            return {
                "generated_text": cleaned_output,
                "status": "success"
            }
        return {
            "error": str(output),
            "status": "error"
        }

    def health_check(self):
        """Health check endpoint"""
        try:
            response = subprocess.run(
                ["curl", "-s", "http://localhost:8080/completion",
                 "-H", "Content-Type: application/json",
                 "-d", '{"prompt": "test", "n_predict": 1}'],
                capture_output=True,
                timeout=5
            )
            return response.returncode == 0
        except:
            return False


# STEP 2: START THE SERVER
if __name__ == "__main__":
    api = LlamaLitAPI()
    server = ls.LitServer(api, accelerator="auto")
    
    # Add health check endpoint
    @server.app.get("/health")
    async def health():
        if api.health_check():
            return {"status": "healthy"}
        return {"status": "unhealthy"}
    
    server.run(port=8000, generate_client_file=False)