# server.py
import litserve as ls
import subprocess
import os
import json
from llama_cpp import Llama
import json


# STEP 1: DEFINE YOUR MODEL API
class LlamaLitAPI(ls.LitAPI):
    def setup(self, device):
        # Get values from environment variables
        # model_url = "https://huggingface.co/lmstudio-community/Llama-3.2-1B-Instruct-GGUF/blob/main/Llama-3.2-1B-Instruct-Q6_K.gguf"
        model_filename = "Llama-3.2-1B-Instruct-Q4_K_M.gguf"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, model_filename)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        self.llm = Llama(model_path=model_path, chat_format="chatml")
 

    def decode_request(self, request):
        return request["prompt"]

    
    def predict(self, input_data):
        """
        Generate a prediction using the Llama GGUF model.

        Args:
            input_data (dict): Dictionary containing input messages.

        Returns:
            dict: JSON response from the Llama model.
        """
        try:
            # Prepare the chat completion request
            response = self.llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that outputs in JSON.",
        },
        {"role": "user", "content": input_data},
    ],
    response_format={
        "type": "json_object",
    },
    temperature=0.7,
)

            # Ensure the response is in the expected JSON format
            if not isinstance(response, dict):
                raise ValueError("Model response is not a valid JSON object.")

            return response

        except ValueError as e:
            print("Input validation error:", str(e))
            raise

        except json.JSONDecodeError as e:
            print("Failed to decode JSON response from the model.")
            raise

        except Exception as e:
            print("An unexpected error occurred:", str(e))
            raise


    def encode_response(self, output):
        return {"generated_text": output}


# STEP 2: START THE SERVER
if __name__ == "__main__":
    api = LlamaLitAPI()
    server = ls.LitServer(api, accelerator="auto")
    server.run(port=8000, generate_client_file=False)