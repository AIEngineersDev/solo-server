from flask import Flask, request, Response
from flask_restful import Api, Resource
from datasets import load_dataset
from haystack import Document, Pipeline
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.retrievers import InMemoryEmbeddingRetriever
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack_integrations.components.generators.llama_cpp import LlamaCppGenerator
import json

app = Flask(__name__)
api = Api(app)

# Load dataset and initialize components
dataset = load_dataset("pszemraj/simple_wikipedia", split="validation[:100]")
docs = [Document(content=doc["text"], meta={"title": doc["title"], "url": doc["url"]}) for doc in dataset]

doc_store = InMemoryDocumentStore(embedding_similarity_function="cosine")
doc_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")

indexing_pipeline = Pipeline()
indexing_pipeline.add_component(instance=doc_embedder, name="doc_embedder")
indexing_pipeline.add_component(instance=DocumentWriter(document_store=doc_store), name="doc_writer")
indexing_pipeline.connect("doc_embedder", "doc_writer")
indexing_pipeline.run({"doc_embedder": {"documents": docs}})

prompt_template = """GPT4 Correct User: Answer the question using the provided context.
Question: {{question}}
Context:
{% for doc in documents %}
    {{ doc.content }}
{% endfor %}

GPT4 Correct Assistant:
"""
rag_pipeline = Pipeline()
text_embedder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
model_path = "/Users/dhruvdiddi/Downloads/qwen2-0_5b-instruct-q5_0.gguf"
generator = LlamaCppGenerator(model=model_path, n_ctx=4096, n_batch=128)

rag_pipeline.add_component(instance=text_embedder, name="text_embedder")
rag_pipeline.add_component(instance=InMemoryEmbeddingRetriever(document_store=doc_store, top_k=3), name="retriever")
rag_pipeline.add_component(instance=PromptBuilder(template=prompt_template), name="prompt_builder")
rag_pipeline.add_component(instance=generator, name="llm")
rag_pipeline.add_component(instance=AnswerBuilder(), name="answer_builder")

rag_pipeline.connect("text_embedder", "retriever")
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")
rag_pipeline.connect("llm.replies", "answer_builder.replies")
rag_pipeline.connect("retriever", "answer_builder.documents")

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    if not question:
        return Response("No question provided", status=400)
    
    def generate_response():
        result = rag_pipeline.run(
            {
                "text_embedder": {"text": question},
                "prompt_builder": {"question": question},
                "llm": {"generation_kwargs": {"max_tokens": 128, "temperature": 0.1}},
                "answer_builder": {"query": question},
            }
        )
        answers = result["answer_builder"]["answers"]
        if not answers:
            yield json.dumps({"error": "No answer found"})
        else:
            yield json.dumps({"answer": answers[0].data})

    return Response(generate_response(), content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)
