import litserve as ls
import subprocess
import os

class LlamaLitAPI(ls.LitAPI):
    def setup(self, device):
        model_url = "https://huggingface.co/Mozilla/Llama-3.2-1B-Instruct-llamafile/resolve/main/Llama-3.2-1B-Instruct.Q6_K.llamafile"
        model_filename = "Llama-3.2-1B-Instruct.Q6_K.llamafile"
        
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, model_filename)
        
        if not os.path.exists(model_path):
            print(f"Downloading {model_filename}...")
            subprocess.run(["wget", "-O", model_path, model_url], check=True)
        
        os.chmod(model_path, 0o755)
        
        # Create and make the shell script executable
        shell_script_path = os.path.join(current_dir, "run_llama.sh")
        with open(shell_script_path, "w") as f:
            f.write('''#!/bin/bash

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the Llama model
"$DIR/Llama-3.2-1B-Instruct.Q6_K.llamafile" --server
''')
        os.chmod(shell_script_path, 0o755)
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.model_process = subprocess.Popen(["bash", shell_script_path], 
                                                      stdout=subprocess.PIPE, 
                                                      stderr=subprocess.PIPE)
                if self.model_process.poll() is None:  # Check if process is running
                    break  # Success, exit the loop
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
        return response.stdout

    def encode_response(self, output):
        return {"generated_text": output}

def main():
    api = LlamaLitAPI()
    server = ls.LitServer(api)
    print("Starting Llama 3.2 1B Instruct API server...")
    print("You can now use the client code in the 'client' folder to interact with this API.")
    print("To run the Streamlit demo, use: streamlit run src/client/streamlit_demo.py")
    server.run(port=8000)

if __name__ == "__main__":
    main()