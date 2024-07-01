from fastapi import FastAPI, Request, Response
import httpx
from starlette.responses import StreamingResponse

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
    
@app.post("/completion")
async def completion(request: Request):
    client_request_data = await request.body()
    print("something happen")
    async def event_generator():
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", f"{llama_cpp_url}/completion", content=client_request_data) as response:
                    async for line in response.aiter_lines():
                        if await request.is_disconnected():
                            break
                        yield line + "\n"
        except Exception as e:
            print(f"Error in event_generator: {e}")

    # Create a StreamingResponse with headers from the external API response
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", "http://localhost:8080/completion", content=b"test") as response:
            headers = {key: value for key, value in response.headers.items() if key.lower() != "content-length"}

    return StreamingResponse(event_generator(), media_type="text/event-stream", headers=headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
