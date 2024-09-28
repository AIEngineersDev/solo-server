# server.py
import litserve as ls

# STEP 1: DEFINE YOUR MODEL API
class BasicLitAPI(ls.LitAPI):
    def setup(self, device):
        # setup is called once at startup. 
        self.model = lambda x: x**3

    def decode_request(self, request):
        # Convert the request payload to model input.
        return request["input"]

    def predict(self, x):
        # Run inference and return the output.
        return self.model(x)

    def encode_response(self, output):
        # Convert the model output to a response payload.
        return {"output": output}

# STEP 2: START THE SERVER
if __name__ == "__main__":
    api = BasicLitAPI()
    server = ls.LitServer(api, accelerator="auto", max_batch_size=1)
    server.run(port=50100)