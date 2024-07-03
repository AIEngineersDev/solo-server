from fastapi import FastAPI, Request, Response
import httpx
from starlette.responses import StreamingResponse
from llama_index.core import Settings
from llama_index.embeddings.llamafile import LlamafileEmbedding
from llama_index.llms.llamafile import Llamafile
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.readers.web import SimpleWebPageReader

app = FastAPI()

llama_cpp_url = "http://localhost:8080"

# Based on https://www.llamaindex.ai/blog/using-llamaindex-and-llamafile-to-build-a-local-private-research-assistant
# Configure LlamaIndex

def load_local_data(input_dir='./data'):
    local_doc_reader = SimpleDirectoryReader(input_dir=input_dir)
    return local_doc_reader.load_data(show_progress=True)

def load_web_data(urls):
    web_reader = SimpleWebPageReader(html_to_text=True)
    return web_reader.load_data(urls)

def build_index(docs, persist_dir="./storage"):
    index = VectorStoreIndex.from_documents(docs, show_progress=True)
    index.storage_context.persist(persist_dir=persist_dir)
    return index

def configure_llama_index():
    Settings.embed_model = LlamafileEmbedding(base_url=llama_cpp_url)
    Settings.llm = Llamafile(
        base_url=llama_cpp_url,
        temperature=0,
        seed=0
    )
    Settings.transformations = [
        SentenceSplitter(
            chunk_size=256,
            chunk_overlap=5
        )
    ]

def query_rag(index, question):
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return response

# TODO: add mongo store: https://docs.llamaindex.ai/en/stable/examples/vector_stores/MongoDBAtlasVectorSearch/

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
    # Load data and build index
    local_docs = load_local_data()
    web_docs = load_web_data([
        'https://en.wikipedia.org/wiki/Homing_pigeon',
        'https://en.wikipedia.org/wiki/Magnetoreception'
    ])
    all_docs = local_docs + web_docs
    build_index(all_docs)
    
    # Configure LlamaIndex
    configure_llama_index()
    uvicorn.run(app, host="0.0.0.0", port=8000)
