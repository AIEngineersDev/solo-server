from haystack import Pipeline
from haystack.dataclasses import ChatMessage
from haystack.utils import Secret
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage, ChatRole
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
from typing import List
from typing import AsyncIterator

app = FastAPI()

origins = ["*"]  # Adjust as needed for CORS policy
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET", "POST"], allow_headers=["*"])

generator = OpenAIChatGenerator(
    api_key=Secret.from_token("sk-no-key-required"), 
    model="LLaMA_CPP",
    api_base_url="http://localhost:8081/v1",
    generation_kwargs = {"max_tokens": 100},
    streaming_callback=lambda chunk: print(chunk.content, end="", flush=True)
)

class ChatRequest(BaseModel):
    chat_data: str

async def generate_stream(chat_data: str) -> AsyncIterator[str]:
    chat_message = ChatMessage(content=chat_data, role=ChatRole.USER, name="solo")
    response = generator.run([chat_message])
    for item in response:
        yield item 


@app.post("/completion")
async def completion(request: ChatRequest):
    async def event_stream():
        async for chunk in generate_stream(request.chat_data):
            yield chunk
    return StreamingResponse(event_stream(), media_type="text/event-stream")

