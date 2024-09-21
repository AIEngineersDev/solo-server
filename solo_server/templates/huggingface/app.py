import litserve as ls
from transformers import pipeline
import logging
from fastapi import Request

logging.basicConfig(level=logging.INFO)

class HuggingFaceLitAPI(ls.LitAPI):
    def setup(self, device):
        # Load the model and tokenizer from Hugging Face Hub
        # For example, using the `distilbert-base-uncased-finetuned-sst-2-english` model for sentiment analysis
        # You can replace the model name with any model from the Hugging Face Hub
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.pipeline = pipeline("text-classification", model=model_name, device=0 if device=="gpu" else -1)

    def decode_request(self, request):
        # Extract text from request
        # This assumes the request payload is of the form: {'text': 'Your input text here'}
        return request["text"]

    def predict(self, text):
        # Use the loaded pipeline to perform inference
        return self.pipeline(text)

    def encode_response(self, output):
        # Format the output from the model to send as a response
        # This example sends back the label and score of the prediction
        return {"label": output[0]["label"], "score": output[0]["score"]}

class CustomLitServer(ls.LitServer):
    async def predict(self, request: Request):
        content_type = request.headers.get("Content-Type", "")
        
        if content_type == "application/x-www-form-urlencoded":
            form_data = await request.form()
            data = dict(form_data)
        elif content_type == "application/json":
            data = await request.json()
        else:
            try:
                data = await request.json()
            except:
                try:
                    form_data = await request.form()
                    data = dict(form_data)
                except:
                    raise ValueError("Unable to parse request data. Please specify a valid Content-Type.")

        return await self.api.predict(data)

if __name__ == "__main__":
    try:
        # Create an instance of your API
        api = HuggingFaceLitAPI()
        # Start the server, specifying the port
        server = CustomLitServer(api, accelerator="cuda")
        server.run(port=8000)
    except Exception as e:
        logging.error(f"An error occurred: {e}")