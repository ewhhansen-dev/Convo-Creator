import unittest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from backend.main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("backend.api.routes.Transcriber")
    def test_transcribe_endpoint(self, MockTranscriber):
        # Mock the transcriber instance and its method
        mock_instance = MockTranscriber.return_value
        mock_instance.transcribe.return_value = "Hello World"

        # Create a dummy wav file
        files = {'file': ('test.wav', b'fake audio data', 'audio/wav')}

        response = self.client.post("/transcribe", files=files)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"text": "Hello World"})
        mock_instance.transcribe.assert_called_once()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

if __name__ == '__main__':
    unittest.main()
