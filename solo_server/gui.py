import streamlit as st

# Set page config
st.set_page_config(page_title="Solo-Server x Ambarella GUI Demo", layout="centered")

# Display image at the top
st.image(
    "../assets/SoloServerBanner.png",
    use_column_width=True
)

# Title
st.title("Solo-Server x Ambarella GUI Demo")

# Inject CSS to make buttons bigger
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 3em;
        font-size: 1.2em;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'status' not in st.session_state:
    st.session_state['status'] = ''
if 'service_message' not in st.session_state:
    st.session_state['service_message'] = ''

# Data structure for models
categories = {
    "Language Models": [
        {
            "Model": "LLaMA 3.2 3B Instruct",
            "Tagged Template": "Llama-3.2-3B.Q6_K",
            "Model Size": "2.62 GB",
            "Info Link": "See HF repo",
            "Tags": "Instruct, LLaMA, 3B, multilingual"
        },
        {
            "Model": "LLaMA 3.2 1B Instruct",
            "Tagged Template": "Llama-3.2-1B.Q6_K",
            "Model Size": "1.11 GB",
            "Info Link": "See HF repo",
            "Tags": "Instruct, LLaMA, 1B, lightweight"
        },
        {
            "Model": "Gemma 2 2B Instruct",
            "Tagged Template": "Gemma-2-2B.Q6_K",
            "Model Size": "2.32 GB",
            "Info Link": "See HF repo",
            "Tags": "Instruct, Gemma, 2B, Italian"
        },
        {
            "Model": "Gemma 2 9B Instruct",
            "Tagged Template": "Gemma-2-9B.Q6_K",
            "Model Size": "7.76 GB",
            "Info Link": "See HF repo",
            "Tags": "Instruct, Gemma, 9B, high performance"
        },
        {
            "Model": "Gemma 2 27B Instruct",
            "Tagged Template": "Gemma-2-27B.Q6_K",
            "Model Size": "22.5 GB",
            "Info Link": "See HF repo",
            "Tags": "Instruct, Gemma, 27B, high power"
        },
        {
            "Model": "LLaVA 1.5",
            "Tagged Template": "LLaVA-7B.Q4",
            "Model Size": "3.97 GB",
            "Info Link": "See HF repo",
            "Tags": "LLaVA, vision, 7B, visual capabilities"
        },
        {
            "Model": "TinyLlama-1.1B",
            "Tagged Template": "TinyLlama-1.1B.F16",
            "Model Size": "2.05 GB",
            "Info Link": "See HF repo",
            "Tags": "Chat, TinyLlama, 1.1B, efficient"
        },
        {
            "Model": "Mistral-7B-Instruct",
            "Tagged Template": "Mistral-7B.Q4",
            "Model Size": "3.85 GB",
            "Info Link": "See HF repo",
            "Tags": "Instruct, Mistral, 7B, versatile"
        },
        {
            "Model": "Phi-3-mini-4k-instruct",
            "Tagged Template": "Phi-3-4k.F16",
            "Model Size": "7.67 GB",
            "Info Link": "See HF repo",
            "Tags": "Instruct, Phi, 4k context, flexible"
        },
        {
            "Model": "Mixtral-8x7B-Instruct",
            "Tagged Template": "Mixtral-8x7B.Q5_K_M",
            "Model Size": "30.03 GB",
            "Info Link": "See HF repo",
            "Tags": "Instruct, Mixtral, 8x7B, multitask"
        },
        {
            "Model": "WizardCoder-34B",
            "Tagged Template": "WizardCoder-34B.Q5_K_M",
            "Model Size": "22.23 GB",
            "Info Link": "See HF repo",
            "Tags": "Code, WizardCoder, 34B, programming"
        },
        {
            "Model": "WizardCoder-13B",
            "Tagged Template": "WizardCoder-13B",
            "Model Size": "7.33 GB",
            "Info Link": "See HF repo",
            "Tags": "Code, WizardCoder, 13B, programming"
        },
        {
            "Model": "LLaMA-3-Instruct-70B",
            "Tagged Template": "LLaMA-3-70B.Q4",
            "Model Size": "37.25 GB",
            "Info Link": "See HF repo",
            "Tags": "Instruct, LLaMA, 70B, high power"
        },
        {
            "Model": "LLaMA-3-Instruct-8B",
            "Tagged Template": "LLaMA-3-8B.Q5_K_M",
            "Model Size": "5.37 GB",
            "Info Link": "See HF repo",
            "Tags": "Instruct, LLaMA, 8B, high efficiency"
        },
        {
            "Model": "Rocket-3B",
            "Tagged Template": "Rocket-3B.Q5_K_M",
            "Model Size": "1.89 GB",
            "Info Link": "See HF repo",
            "Tags": "Rocket, 3B, lightweight, efficient"
        },
        {
            "Model": "OLMo-7B",
            "Tagged Template": "OLMo-7B.Q6_K",
            "Model Size": "5.68 GB",
            "Info Link": "See HF repo",
            "Tags": "OLMo, 7B, optimized, versatile"
        },
    ],
    "Text Embedding Models": [
        {
            "Model": "E5-Mistral-7B",
            "Tagged Template": "E5-Mistral-7B.Q5_K_M",
            "Model Size": "5.16 GB",
            "Info Link": "See HF repo",
            "Tags": "Embedding, Mistral, 7B, NLP"
        },
        {
            "Model": "mxbai-embed-large-v1",
            "Tagged Template": "mxbai-embed-large-v1.F16",
            "Model Size": "0.7 GB",
            "Info Link": "See HF repo",
            "Tags": "Embedding, mxbai, NLP, compact"
        },
    ],
    "Audio": [
        {
            "Model": "Wav2Vec 2.0 Large",
            "Tagged Template": "Wav2Vec2-Large.F16",
            "Model Size": "1.04 GB",
            "Info Link": "See HF repo",
            "Tags": "Speech Recognition, ASR, Wav2Vec"
        },
        {
            "Model": "Whisper-Tiny",
            "Tagged Template": "Whisper-Tiny.Q4",
            "Model Size": "0.17 GB",
            "Info Link": "See HF repo",
            "Tags": "Transcription, Whisper, Tiny"
        },
        {
            "Model": "SpeechT5",
            "Tagged Template": "SpeechT5-Q4",
            "Model Size": "1.25 GB",
            "Info Link": "See HF repo",
            "Tags": "ASR, Speech, Text-to-Speech"
        },
        {
            "Model": "Hubert-Large",
            "Tagged Template": "Hubert-Large.F16",
            "Model Size": "0.95 GB",
            "Info Link": "See HF repo",
            "Tags": "Speech Embedding, Hubert, ASR"
        },
        {
            "Model": "SEW-D-Tiny",
            "Tagged Template": "SEW-D-Tiny.Q4",
            "Model Size": "0.12 GB",
            "Info Link": "See HF repo",
            "Tags": "Speech Processing, SEW-D, Tiny"
        },
    ],
    "Vision": [
        {
            "Model": "ViT-Base",
            "Tagged Template": "ViT-Base-16-Q4",
            "Model Size": "0.33 GB",
            "Info Link": "See HF repo",
            "Tags": "Vision, Transformer, ViT"
        },
        {
            "Model": "Swin-Tiny",
            "Tagged Template": "Swin-Tiny.F16",
            "Model Size": "0.14 GB",
            "Info Link": "See HF repo",
            "Tags": "Image Classification, Swin, Tiny"
        },
        {
            "Model": "ConvNeXT-Base",
            "Tagged Template": "ConvNeXT-Base.F16",
            "Model Size": "0.34 GB",
            "Info Link": "See HF repo",
            "Tags": "Image Recognition, ConvNeXT, Base"
        },
        {
            "Model": "YOLOv5-Small",
            "Tagged Template": "YOLOv5-Small.Q4",
            "Model Size": "0.05 GB",
            "Info Link": "See HF repo",
            "Tags": "Object Detection, YOLOv5, Small"
        },
        {
            "Model": "DINO-Small",
            "Tagged Template": "DINO-Small.F16",
            "Model Size": "0.11 GB",
            "Info Link": "See HF repo",
            "Tags": "Self-Supervised, DINO, Vision"
        },
    ],
    "Tabular": [
        {
            "Model": "TabNet",
            "Tagged Template": "TabNet-Base.F16",
            "Model Size": "0.02 GB",
            "Info Link": "See HF repo",
            "Tags": "Tabular, Feature Learning, TabNet"
        },
        {
            "Model": "SAINT",
            "Tagged Template": "SAINT-Tabular.F16",
            "Model Size": "0.03 GB",
            "Info Link": "See HF repo",
            "Tags": "Tabular, SAINT, Self-Attention"
        },
        {
            "Model": "XGBoost",
            "Tagged Template": "XGBoost-Q4",
            "Model Size": "0.05 GB",
            "Info Link": "See HF repo",
            "Tags": "Tabular, Gradient Boosting, Efficient"
        },
        {
            "Model": "TabTransformer",
            "Tagged Template": "TabTransformer-F16",
            "Model Size": "0.04 GB",
            "Info Link": "See HF repo",
            "Tags": "Tabular, Transformer, TabTransformer"
        },
        {
            "Model": "Node",
            "Tagged Template": "Node-Tabular-Q4",
            "Model Size": "0.03 GB",
            "Info Link": "See HF repo",
            "Tags": "Tabular, Neural Oblivious Decision Ensemble"
        },
    ],
    "Compound AI": [
        {
            "Model": "Flamingo-3B",
            "Tagged Template": "Flamingo-3B-Q5",
            "Model Size": "3.12 GB",
            "Info Link": "See HF repo",
            "Tags": "Vision, Language, Multimodal, Flamingo"
        },
        {
            "Model": "BLIP-2 Base",
            "Tagged Template": "BLIP-2-Base.F16",
            "Model Size": "2.45 GB",
            "Info Link": "See HF repo",
            "Tags": "Image Captioning, Language, Multimodal"
        },
        {
            "Model": "LayoutLMv3",
            "Tagged Template": "LayoutLMv3-F16",
            "Model Size": "0.98 GB",
            "Info Link": "See HF repo",
            "Tags": "Document Understanding, OCR, Multimodal"
        },
        {
            "Model": "GIT-2",
            "Tagged Template": "GIT-2.Q6",
            "Model Size": "4.20 GB",
            "Info Link": "See HF repo",
            "Tags": "Generative, Language + Vision, Multimodal"
        },
        {
            "Model": "UnifiedQA-v2",
            "Tagged Template": "UnifiedQA-v2-Q4",
            "Model Size": "1.34 GB",
            "Info Link": "See HF repo",
            "Tags": "Question Answering, Multitask, QA"
        },
    ],
    "Miscellaneous": [
        {
            "Model": "BigGAN",
            "Tagged Template": "BigGAN-512x512.Q4",
            "Model Size": "1.67 GB",
            "Info Link": "See HF repo",
            "Tags": "Image Generation, GAN, BigGAN"
        },
        {
            "Model": "T5-11B",
            "Tagged Template": "T5-11B-Q4",
            "Model Size": "42.00 GB",
            "Info Link": "See HF repo",
            "Tags": "Text Generation, Translation, Large Model"
        },
        {
            "Model": "DistilBERT",
            "Tagged Template": "DistilBERT-Base.F16",
            "Model Size": "0.26 GB",
            "Info Link": "See HF repo",
            "Tags": "NLP, Lightweight, Distilled, BERT"
        },
        {
            "Model": "StyleGAN3",
            "Tagged Template": "StyleGAN3-FHQ-Q4",
            "Model Size": "2.05 GB",
            "Info Link": "See HF repo",
            "Tags": "Image Synthesis, GAN, StyleGAN"
        },
        {
            "Model": "MiniGPT-4",
            "Tagged Template": "MiniGPT-4.Q5",
            "Model Size": "2.89 GB",
            "Info Link": "See HF repo",
            "Tags": "Vision + Language, Multimodal, Lightweight"
        },
    ],
}

# Create options list and model info dictionary
options = []
model_info_dict = {}

for category in categories:
    for model in categories[category]:
        option_name = f"{category} - {model['Model']}"
        options.append(option_name)
        # Store model info with option name as key
        model_info_dict[option_name] = model

# Model selection
selected_option = st.selectbox("Select a model:", options)

# Get selected model info
selected_model_info = model_info_dict[selected_option]

# Generate CLI command based on selection
cli_command = f"python run_model.py --model {selected_model_info['Tagged Template']}"
st.text_input("CLI Command:", value=cli_command, disabled=True)

# Display model information
st.subheader("Model Information")
st.write(f"**Model:** {selected_model_info['Model']}")
st.write(f"**Category:** {selected_option.split(' - ')[0]}")
st.write(f"**Tagged Template:** {selected_model_info['Tagged Template']}")
st.write(f"**Model Size:** {selected_model_info['Model Size']}")
st.write(f"**Info Link:** {selected_model_info['Info Link']}")
st.write(f"**Tags:** {selected_model_info['Tags']}")

def start_model():
    st.session_state['status'] = f"Starting {selected_model_info['Model']}..."
    st.session_state['service_message'] = f"{selected_model_info['Model']} is running."
    # Add code to start the model here

def stop_model():
    st.session_state['status'] = f"Stopping {selected_model_info['Model']}..."
    st.session_state['service_message'] = ''
    # Add code to stop the model here

def benchmark_model():
    st.session_state['status'] = f"Benchmarking {selected_model_info['Model']}..."
    # Add code to benchmark the model here

# Buttons
if st.button("Start", key='start_button'):
    start_model()

if st.button("Stop", key='stop_button'):
    stop_model()

if st.button("Benchmark", key='benchmark_button'):
    benchmark_model()

# Display status
if st.session_state['status']:
    st.write(st.session_state['status'])

# Create sidebar with service message
st.sidebar.title("Model Status")
st.sidebar.write("Model running on:")
if st.session_state['service_message']:
    st.sidebar.write(st.session_state['service_message'])
else:
    st.sidebar.write("No model is currently running.")
