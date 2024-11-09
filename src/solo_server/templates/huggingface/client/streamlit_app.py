import streamlit as st
import requests

# Streamlit UI setup
st.title("Hugging Face Sentiment Analysis")
st.write("Enter text to analyze sentiment:")

# Text input for the user
input_text = st.text_area("Text Input", value="I love this new project!")

# Define the API endpoint (replace with your actual server's IP/port if needed)
api_endpoint = "http://localhost:8000/predict"

# When the user presses the "Analyze" button, make a request to the server
if st.button("Analyze"):
    if input_text:
        # Prepare the request payload
        payload = {"text": input_text}
        
        # Send the request to the Hugging Face API
        try:
            response = requests.post(api_endpoint, json=payload)
            response_data = response.json()

            # Display the result in Streamlit
            if "label" in response_data and "score" in response_data:
                st.write(f"Prediction: {response_data['label']}")
                st.write(f"Confidence: {response_data['score']:.2f}")
            else:
                st.error("Unexpected response format.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter some text for analysis.")