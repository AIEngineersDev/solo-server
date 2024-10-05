import unittest
from unittest.mock import patch
import requests
import streamlit as st
from src.predict import HuggingFaceLitAPI, main as api_main
import threading
import time

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the API server in a separate thread
        cls.server_thread = threading.Thread(target=api_main)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(2)  # Give the server some time to start

    def test_streamlit_client(self):
        # Mock Streamlit components
        with patch('streamlit.text_area') as mock_text_area, \
             patch('streamlit.button') as mock_button, \
             patch('streamlit.write') as mock_write, \
             patch('streamlit.error') as mock_error:

            mock_text_area.return_value = "This is a great test"
            mock_button.return_value = True

            # Import the Streamlit app
            import client.streamlit_app

            # Check if the correct API endpoint is used
            self.assertEqual(client.streamlit_app.api_endpoint, "http://localhost:8000/predict")

            # Verify that the API call was made and the result was displayed
            mock_write.assert_any_call("Prediction: POSITIVE")
            mock_write.assert_any_call("Confidence: 0.90")

    def test_api_directly(self):
        response = requests.post("http://localhost:8000/predict", json={"text": "This is a great test"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("label", data)
        self.assertIn("score", data)

if __name__ == '__main__':
    unittest.main()