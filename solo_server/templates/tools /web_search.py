import litserve as ls
from fastapi import Request
import aiohttp
import os

class SerperLitAPI(ls.LitAPI):
    def setup(self):
        self.api_key = os.environ.get('SERPER_API_KEY')
        if not self.api_key:
            raise ValueError("SERPER_API_KEY environment variable is not set")
        self.base_url = "https://google.serper.dev/search"

    async def predict(self, data):
        query = data.get('query')
        if not query:
            raise ValueError("Query is required")

        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'q': query
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Serper API request failed with status {response.status}")

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
    api = SerperLitAPI()
    server = CustomLitServer(api)
    server.run(port=8000)
