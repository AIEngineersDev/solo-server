import os, logging, qdrant_client
from llama_index.llms.ollama import Ollama
from llama_index.core import StorageContext, Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
import litserve as ls

class DocumentChatAPI(ls.LitAPI):
    def setup(self, device):
        Settings.llm = Ollama(model="llama3.1:latest", request_timeout=120.0)
        Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-large-en-v1.5")
        client = qdrant_client.QdrantClient(host="localhost", port=6333)
        vector_store = QdrantVectorStore(client=client, collection_name="doc_search_collection")
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        documents = SimpleDirectoryReader("./docs").load_data()
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
        self.query_engine = index.as_query_engine()

    def decode_request(self, request):
        return request["query"]

    def predict(self, query):
        return self.query_engine.query(query)

    def encode_response(self, output):
        return {"output": output}

if __name__ == "__main__":
    api = DocumentChatAPI()
    server = ls.LitServer(api)
    server.run(port=8000)
