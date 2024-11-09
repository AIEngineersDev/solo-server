import unittest
import requests
from src.predict import main as api_main
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

    def test_api_directly(self):
        response = requests.post("http://localhost:8000/predict", json={"text": "This is a great test"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("label", data)
        self.assertIn("score", data)

if __name__ == '__main__':
    unittest.main()