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

# Model selection
models = ["ResNet50", "InceptionV3", "MobileNetV2", "EfficientNetB0"]
selected_model = st.selectbox("Select a model:", models)

# Generate CLI command based on selection
cli_command = f"python run_model.py --model {selected_model}"
st.text_input("CLI Command:", value=cli_command, disabled=True)

# Initialize session state
if 'status' not in st.session_state:
    st.session_state['status'] = ''

def start_model():
    st.session_state['status'] = f"Starting {selected_model}..."
    # Add code to start the model here

def stop_model():
    st.session_state['status'] = f"Stopping {selected_model}..."
    # Add code to stop the model here

def benchmark_model():
    st.session_state['status'] = f"Benchmarking {selected_model}..."
    # Add code to benchmark the model here

# Buttons stacked on top of each other with bigger size
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

