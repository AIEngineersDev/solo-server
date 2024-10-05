import streamlit as st
import requests
import json

def generate_text(prompt):
    url = "http://localhost:8000/predict"
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        result = response.json()
        return result['generated_text']
    else:
        return f"Error: {response.status_code} - {response.text}"

st.title("Llama 3.2 1B Instruct Demo")

prompt = st.text_area("Enter your prompt:", height=100)
if st.button("Generate"):
    if prompt:
        with st.spinner("Generating response..."):
            response = generate_text(prompt)
        st.text_area("Generated Response:", value=response, height=300)
    else:
        st.warning("Please enter a prompt.")

st.markdown("---")
st.write("This demo uses the Llama 3.2 1B Instruct model. The model is running locally on your machine.")