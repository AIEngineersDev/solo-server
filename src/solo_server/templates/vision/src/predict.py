import litserve as ls
from transformers import pipeline
from PIL import Image
import io

class VisionLitAPI(ls.LitAPI):
    def setup(self, device):
        model_name = "google/vit-base-patch16-224"
        self.pipeline = pipeline("image-classification", model=model_name, device=device)

    def decode_request(self, request):
        image_bytes = request["image"]
        return Image.open(io.BytesIO(image_bytes))

    def predict(self, image):
        return self.pipeline(image)

    def encode_response(self, output):
        return {"label": output[0]["label"], "score": output[0]["score"]}

def main():
    api = VisionLitAPI()
    server = ls.LitServer(api, accelerator="cuda")
    server.run(port=8000)

if __name__ == "__main__":
    main()