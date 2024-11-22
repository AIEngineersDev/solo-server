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
        # ... (Add the rest of the models in this category)
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
        # ... (Add the rest of the models)
    ],
    # ... (Add the rest of the categories and their models)
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
