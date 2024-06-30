from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()

llama_cpp_url = "http://localhost:8080"

@app.post("/stream")
async def stream_to_llama_cpp(request: Request):
    async with httpx.AsyncClient() as client:
        # Forward the request body and headers to the llama.cpp server
        llama_response = await client.post(
            llama_cpp_url,
            content=await request.body(),
            headers=request.headers
        )

        # Stream the response from llama.cpp server back to the client
        return Response(
            content=llama_response.content,
            status_code=llama_response.status_code,
            headers=llama_response.headers
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
