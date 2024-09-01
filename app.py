import os
import json
import requests
from flask import Flask, request, Response, abort, jsonify
from typing import Dict, Any
import re

app = Flask(__name__)

llama_cpp_url = "http://127.0.0.1:50100"

SYSTEM_PROMPT = "You are Solo: an on-device AI."

def detect_intention(prompt: str) -> str:
    """
    Detect the intention of the user's prompt.
    """
    lower_prompt = prompt.lower()
    
    intent_keywords = {
        "text_classification": ["classify", "categorize", "label"],
        "token_classification": ["identify entities", "named entity", "pos tagging"],
        "summarization": ["summarize", "summary", "brief overview"],
        "text_generation": ["write", "create", "compose", "generate text"],
        "translation": ["translate", "convert language"],
        "question_answering": ["answer", "explain", "?"],
        "code_generation": ["code", "program", "function", "script"],
        "sentiment_analysis": ["sentiment", "emotion", "feeling"],
        "language_modeling": ["predict next word", "autocomplete"],
        "text_similarity": ["compare texts", "find similarity", "text matching"],
        "machine_translation": ["translate between languages"],
        "text_to_speech": ["convert text to speech", "text to audio"],
        "speech_to_text": ["transcribe", "convert speech to text"],
        "information_extraction": ["extract info", "pull data from text"],
        "text_clustering": ["group similar texts", "cluster documents"],
        "dialogue_generation": ["chatbot", "conversational ai"],
        "general_conversation": []  # Default case
    }
    
    for intent, keywords in intent_keywords.items():
        if any(keyword in lower_prompt for keyword in keywords):
            return intent
    
    return "general_conversation"

def sanitize_prompt(prompt: str) -> str:
    """
    Sanitize the prompt by removing potential harmful content.
    """
    # Remove any HTML or script tags
    prompt = re.sub(r'<[^>]*>', '', prompt)
    
    # Remove any potential SQL injection attempts
    prompt = re.sub(r'\b(UNION|SELECT|INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|TABLE|FROM|WHERE|AND|OR)\b', '', prompt, flags=re.IGNORECASE)
    
    # Limit the prompt length
    max_length = 1000
    if len(prompt) > max_length:
        prompt = prompt[:max_length] + "... (truncated)"
    
    return prompt

def adjust_parameters(intention: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Adjust model parameters based on the detected intention.
    """
    intention_params = {
        "text_classification": {"temperature": 0.3, "top_p": 0.9},
        "token_classification": {"temperature": 0.2, "top_p": 0.95},
        "summarization": {"temperature": 0.3, "top_p": 0.9},
        "text_generation": {"temperature": 0.7, "top_p": 0.95},
        "translation": {"temperature": 0.2, "top_k": 50},
        "question_answering": {"temperature": 0.5, "top_p": 0.95},
        "code_generation": {"temperature": 0.2, "top_p": 0.9, "repeat_penalty": 1.2},
        "sentiment_analysis": {"temperature": 0.3, "top_p": 0.9},
        "language_modeling": {"temperature": 0.6, "top_k": 40},
        "text_similarity": {"temperature": 0.4, "top_p": 0.95},
        "machine_translation": {"temperature": 0.3, "top_k": 50},
        "text_to_speech": {"temperature": 0.5, "top_p": 0.9},
        "speech_to_text": {"temperature": 0.3, "top_p": 0.95},
        "information_extraction": {"temperature": 0.2, "top_p": 0.9},
        "text_clustering": {"temperature": 0.4, "top_p": 0.95},
        "dialogue_generation": {"temperature": 0.6, "top_p": 0.9},
        "general_conversation": {"temperature": 0.6, "top_p": 0.9}
    }
    
    params.update(intention_params.get(intention, intention_params["general_conversation"]))
    return params

@app.route("/health-check")
def health_check():
    return "Get Solo!"

@app.route("/api/chat", methods=["POST"])
def stream():
    body = request.json
    original_prompt = body.get("prompt", "")
    
    # Detect intention
    intention = detect_intention(original_prompt)
    
    # Sanitize prompt
    sanitized_prompt = sanitize_prompt(original_prompt)
    
    # Prepare base parameters
    stream_params = {
        "stream": True,
        "n_predict": 400,
        "temperature": body.get("temperature", 0.4),
        "stop": [
            "</s>",
            "Llama:",
            "User:",
            "assistant:",
            "user:",
            "llama:",
            "<|eot_id|>",
        ],
        "repeat_last_n": 256,
        "repeat_penalty": 1.18,
        "top_k": 40,
        "top_p": 0.95,
        "min_p": 0.05,
        "tfs_z": 1,
        "typical_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "mirostat": 0,
        "mirostat_tau": 5,
        "mirostat_eta": 0.1,
        "grammar": "",
        "n_probs": 0,
        "min_keep": 0,
        "image_data": [],
        "cache_prompt": True,
        "api_key": "",
        "slot_id": 0,
        "prompt": sanitized_prompt,
    }
    
    # Adjust parameters based on intention
    adjusted_params = adjust_parameters(intention, stream_params)
    
    # Prepare the payload with system prompt
    payload = {k: v for k, v in adjusted_params.items() if k != "prompt"}
    payload["prompt"] = f"{SYSTEM_PROMPT}\n\n[Intention: {intention}]\nUser: {adjusted_params['prompt']}\nSolo:"

    try:
        response = requests.post(
            f"{llama_cpp_url}/completion",
            json=payload,
            headers={"Content-Type": "application/json"},
            stream=True,
        )
        response.raise_for_status()

        def generate():
            try:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        yield chunk.decode("utf-8")
            except Exception as e:
                app.logger.error(f"Error during streaming: {e}")

        return Response(generate(), content_type="text/event-stream")
    except requests.RequestException as e:
        app.logger.error(f"Error during request to llama server: {e}")
        return "Internal Server Error", 500

@app.route("/get-models", methods=["GET"])
def get_list():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FILENAME = "models.json"

    JSON_FILE_PATH = os.path.join(BASE_DIR, FILENAME)
    JSON_FILE_PATH_2 = os.path.join(BASE_DIR, "../assets", FILENAME)
    FILE_PATH = None

    if os.path.isfile(JSON_FILE_PATH):
        FILE_PATH = JSON_FILE_PATH
    elif os.path.isfile(JSON_FILE_PATH_2):
        FILE_PATH = JSON_FILE_PATH_2

    if not FILE_PATH:
        abort(404, description="Resource not found")

    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
        return jsonify({"models": data})
    except json.JSONDecodeError:
        abort(500, description="Error reading JSON file")
    except Exception as e:
        abort(500, description=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=55010)