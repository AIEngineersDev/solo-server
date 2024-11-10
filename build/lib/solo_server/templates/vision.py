import litserve as ls
from transformers import pipeline
from PIL import Image
import io
import base64

class VisionLitAPI(ls.LitAPI):
    def setup(self, device):
        model_name = "google/vit-base-patch16-224"
        self.pipeline = pipeline("image-classification", model=model_name, device=device)

    def decode_request(self, request):
        if isinstance(request, dict):
            request = request['request']  # Extract the base64 string from the request dict
        if isinstance(request, str):
            request = base64.b64decode(request)
        return Image.open(io.BytesIO(request))

    def predict(self, image):
        return self.pipeline(image)

    def encode_response(self, output):
        return {"label": output[0]["label"], "score": output[0]["score"]}


if __name__ == "__main__":
    api = VisionLitAPI()
    server = ls.LitServer(api, accelerator="auto")
    server.run(port=8000, generate_client_file=False)