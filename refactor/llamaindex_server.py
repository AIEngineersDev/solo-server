from fastapi import FastAPI, Request, Response
import httpx
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import json

app = FastAPI()

# Initialize the llama index
def initialize_llama_index():
    # Load documents from the 'data' directory
    documents = SimpleDirectoryReader('data').load_data()

    # Set up embedding model
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
    
    # Set up LLM with Ollama
    Settings.llm = Ollama(model="llama3", request_timeout=360.0)

    # Create the index
    index = GPTSimpleVectorIndex.from_documents(documents)
    return index

index = initialize_llama_index()

@app.post("/stream")
async def stream_to_llama_cpp(request: Request):
    data = await request.json()
    query = data.get('query', '')

    # Get the response from the index
    response = index.as_query_engine().query(query)
    response_text = str(response)

    return Response(content=json.dumps({"response": response_text}), media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
