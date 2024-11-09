import litserve as ls
from transformers import pipeline

class CompoundLitAPI(ls.LitAPI):
    def setup(self, device):
        self.text_pipeline = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english", device=device)
        self.image_pipeline = pipeline("image-classification", model="google/vit-base-patch16-224", device=device)
        self.audio_pipeline = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h", device=device)

    def decode_request(self, request):
        return request["type"], request["data"]

    def predict(self, type, data):
        if type == "text":
            return self.text_pipeline(data)
        elif type == "image":
            return self.image_pipeline(data)
        elif type == "audio":
            return self.audio_pipeline(data)
        else:
            return {"error": "Unsupported type"}

    def encode_response(self, output):
        if isinstance(output, list):
            return {"result": output[0]}
        return {"result": output}

def main():
    api = CompoundLitAPI()
    server = ls.LitServer(api, accelerator="cuda")
    server.run(port=8000)

if __name__ == "__main__":
    main()