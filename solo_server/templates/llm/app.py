# server.py
import litserve as ls
from litgpt import LLM
import os 


# STEP 1: DEFINE YOUR MODEL API
class BasicLLMAPI(ls.LitAPI):
    def setup(self, device):
        # setup is called once at startup. 
        os.environ["HF_ACCESS_TOKEN"] = "hf_token"
        self.model = LLM.load("microsoft/phi-2")

    def decode_request(self, request):
        # Convert the request payload to model input.
        return request["prompt"]

    def predict(self, prompt):
        # Run llm inference
        return self.model.generate(prompt, max_new_tokens=333)

    def encode_response(self, output):
        # Convert the model output to a response payload.
        return {"output": output}

# STEP 2: START THE SERVER
if __name__ == "__main__":
    api = BasicLLMAPI()
    server = ls.LitServer(api, accelerator="auto", max_batch_size=1)
    server.run(port=50100)