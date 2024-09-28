import torch, clip, multiprocessing
from PIL import Image
from io import BytesIO

import litserve as ls


class CLIPAPI(ls.LitAPI):
    def setup(self, device):
        self.device = device
        self.model, self.preprocess = clip.load("ViT-B/32", device=device)
        
        # Load candidate captions
        with open('captions.txt', 'r') as file:
            self.candidate_captions = [line.strip() for line in file.readlines()]
        
        # Pre-tokenize and pre-encode text captions
        with torch.no_grad():
            self.text_tokens = clip.tokenize(self.candidate_captions).to(self.device)
            self.text_embeddings = self.model.encode_text(self.text_tokens)

    def decode_request(self, request):
        # Convert request to input tensor
        image_bytes = bytes.fromhex(request["image_bytes"])
        image = Image.open(BytesIO(image_bytes))
        return self.preprocess(image).unsqueeze(0).to(self.device)

    def predict(self, image_tensor):
        # Compare the image against the list of captions
        with torch.no_grad():
            image_embedding = self.model.encode_image(image_tensor)

            # Calculating similarities with pre-encoded text features
            similarities = (100.0 * image_embedding @ self.text_embeddings.T).softmax(dim=-1)
            max_indices = similarities.argmax(dim=-1)

            return [self.candidate_captions[idx] for idx in max_indices.cpu().numpy()]

    def encode_response(self, output):
        return {"description": output[0]}

if __name__ == "__main__":
    api = CLIPAPI()
    server = ls.LitServer(api, accelerator="auto")
    server.run(port=8000)