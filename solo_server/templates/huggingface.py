import litserve as ls
from transformers import pipeline

class HuggingFaceLitAPI(ls.LitAPI):
    def setup(self, device):
        # Load the model and tokenizer from Hugging Face Hub
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.pipeline = pipeline("text-classification", model=model_name, device=device)

    def decode_request(self, request):
        # Extract text from request, with error handling
        if "input" in request:
            return request["input"]
        elif "text" in request:
            return request["text"]
        raise ValueError("Request must contain either 'input' or 'text' field")

    def predict(self, text):
        # Use the loaded pipeline to perform inference
        return self.pipeline(text)

    def encode_response(self, output):
        # Format the output to send as a response
        return {"label": output[0]["label"], "score": output[0]["score"]}

if __name__ == "__main__":
    api = HuggingFaceLitAPI()
    server = ls.LitServer(api, accelerator="auto")  # Use CPU in Docker
    server.run(port=8000, generate_client_file=False)