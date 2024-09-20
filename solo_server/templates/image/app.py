import torch, base64
from diffusers import StableDiffusionPipeline
from io import BytesIO
import litserve as ls

class StableDiffusionLitAPI(ls.LitAPI):
    def setup(self, device):
        # Load the model and tokenizer
        self.model = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16, use_auth_token=True).to(device)
        self.device = device

    def decode_request(self, request):
        # Extract prompt from request
        prompt = request["prompt"]
        return prompt

    def predict(self, prompt):
        # Generate image from prompt
        with torch.no_grad():
            # Adjusted to directly access the generated image from the output without using the 'sample' key.
            # The output from the model is expected to be a list of PIL images.
            images = self.model(prompt, num_inference_steps=50, guidance_scale=7.5)["images"]
            image = images[0]  # Assuming you want to retrieve the first image
        return image

    def encode_response(self, image):
        # Convert the generated PIL Image to a Base64 string
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return {"image": img_str}

# Starting the server
if __name__ == "__main__":
    # Assume that an appropriate device (e.g., 'cuda', 'cpu') is specified
    api = StableDiffusionLitAPI()
    server = ls.LitServer(api)
    server.run(port=8000)