import litserve as ls
import subprocess
import os

class LlamaLitAPI(ls.LitAPI):
    def setup(self, device):
        model_url = "https://huggingface.co/Mozilla/Llama-3.2-1B-Instruct-llamafile/resolve/main/Llama-3.2-1B-Instruct.Q6_K.llamafile"
        model_filename = "Llama-3.2-1B-Instruct.Q6_K.llamafile"
        
        if not os.path.exists(model_filename):
            print(f"Downloading {model_filename}...")
            subprocess.run(["wget", model_url], check=True)
        
        os.chmod(model_filename, 0o755)
        
        self.model_process = subprocess.Popen([f"./{model_filename}", "--server"], 
                                              stdout=subprocess.PIPE, 
                                              stderr=subprocess.PIPE)
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
    server.run(port=8000)

if __name__ == "__main__":
    main()