import os
import httpx
import logging
import pickle
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from llama_index.core import Settings
from llama_index.llms.llamafile import Llamafile
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.llamafile import LlamafileEmbedding
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage

import re
import requests
import json
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings.base import Embeddings


logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

origins = ["*"]  # Adjust as needed for CORS policy
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET", "POST"], allow_headers=["*"])


index = None
stored_docs = {}

index_name = "./saved_index"
pkl_name = "stored_documents.pkl"
llama_cpp_url = 'http://llmaserver:8080'


class LocalEmbeddings(Embeddings):
    def __init__(self, url=f"{llama_cpp_url}/embedding"):
        self.url = url

    def embed_documents(self, texts):
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text):
        response = requests.post(
            self.url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'content': text})
        )
        embedding_dict = response.json()
        return embedding_dict['embedding'] 

embeddings = LocalEmbeddings()

def safe_load_file(file_path):
    try:
        with open(file_path, 'r', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return f"[Error reading file: {str(e)}]"

def load_documents(file_path):
    if os.path.isfile(file_path):
        return [safe_load_file(file_path)]
    elif os.path.isdir(file_path):
        documents = []
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file.endswith('.txt'):
                    full_path = os.path.join(root, file)
                    documents.append(safe_load_file(full_path))
        return documents
    else:
        raise ValueError("Invalid path")

def create_vector_store(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text("\n\n".join(documents))
    return Chroma.from_texts(texts, embeddings)


def load_web_data(urls):
    web_reader = SimpleWebPageReader(html_to_text=True)
    return web_reader.load_data(urls)

def initialize_index():
    """Create a new global index, or load one from the pre-set path."""
    global index, stored_docs
    print('initialize_index()')

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

    if os.path.exists(index_name):
        index = load_index_from_storage(StorageContext.from_defaults(persist_dir=index_name), Settings=Settings)
    # else:
    #     local_doc_reader = SimpleDirectoryReader(input_dir='./data')
    #     local_docs = local_doc_reader.load_data(show_progress=True)
    #     web_docs = load_web_data([
    #         'https://en.wikipedia.org/wiki/Homing_pigeon',
    #         # 'https://en.wikipedia.org/wiki/Magnetoreception'
    #     ])
    #     all_docs = local_docs + web_docs
    #     index = VectorStoreIndex.from_documents(all_docs, show_progress=True, Settings=Settings)
    #     index.storage_context.persist(persist_dir=index_name)
    if os.path.exists(pkl_name):
        with open(pkl_name, "rb") as f:
            stored_docs = pickle.load(f)
    return index


@app.post("/completion")
async def completion(request: Request):
    user_input = await request.json.get('message')
    context = ""
    
    file_paths = re.findall(r'/\S+', user_input)
    if file_paths:
        file_path = file_paths[0]
        print(f"Processing file path: {file_path}")
        query = user_input.replace(file_path, '').strip()
        
        try:
            # if not os.path.exists(file_path):
            #     return Response(f"Error: The path '{file_path}' does not exist.", status=400, content_type='application/json')
            
            if os.path.isfile(file_path):
                context = f"The path '{file_path}' is a file. Contents:\n"
                context += safe_load_file(file_path)
            elif os.path.isdir(file_path):
                contents = os.listdir(file_path)
                context = f"Contents of directory '{file_path}':\n" + "\n".join(contents)
                
                documents = load_documents(file_path)
                if documents:
                    vector_store = create_vector_store(documents)
                    relevant_docs = vector_store.similarity_search(query, k=2)
                    context += "\n\nRelevant content:\n" + "\n".join([doc.page_content for doc in relevant_docs])
            # else:
            #     return Response(f"Error: '{file_path}' is neither a file nor a directory.", status=400, content_type='application/json')
            
        except Exception as e:
            print(f"Error processing file or directory: {str(e)}")
            # return Response(f"Error processing file or directory: {str(e)}", status=400, content_type='application/json')
    
    print(f"Context: {context[:500]}...")  # Print first 500 characters of context for debugging
    

    client_request_data = await request.body()
    #TO-DO: have to add context variable to the request.body()'s message 
    logging.info('/completion', client_request_data)
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
        async with client.stream("POST", f"{llama_cpp_url}/completion", content=b"test") as response:
            headers = {key: value for key, value in response.headers.items() if key.lower() != "content-length"}

    return StreamingResponse(event_generator(), media_type="text/event-stream", headers=headers)


@app.get("/query")
async def query_index(request: Request):
    global index

    query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)
    try:
        async def event_generator(text = request.query_params.get('text')):
            try:
                response_stream = query_engine.query(text)

                for line in response_stream.response_gen:
                    if await request.is_disconnected():
                        break
                    yield line
            except Exception as e:
                print(f"Error in event_generator: {e}")

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying index: {str(e)}")


initialize_index()

if __name__ == "__main__":
    # init the global index
    print("server started...")