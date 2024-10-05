import unittest
from unittest.mock import patch, MagicMock
from src.predict import HuggingFaceLitAPI

class TestHuggingFaceLitAPI(unittest.TestCase):
    def setUp(self):
        self.api = HuggingFaceLitAPI()
        self.api.setup("cpu")  # Use CPU for testing

    def test_decode_request(self):
        request = {"text": "This is a test"}
        self.assertEqual(self.api.decode_request(request), "This is a test")

    @patch('src.predict.pipeline')
    def test_predict(self, mock_pipeline):
        mock_pipeline.return_value = [{"label": "POSITIVE", "score": 0.9}]
        self.api.pipeline = mock_pipeline
        result = self.api.predict("This is a great test")
        self.assertEqual(result, [{"label": "POSITIVE", "score": 0.9}])

    def test_encode_response(self):
        output = [{"label": "NEGATIVE", "score": 0.8}]
        expected = {"label": "NEGATIVE", "score": 0.8}
        self.assertEqual(self.api.encode_response(output), expected)

if __name__ == '__main__':
    unittest.main()