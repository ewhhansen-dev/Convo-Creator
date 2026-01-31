import unittest
import os
import shutil
from unittest.mock import MagicMock, patch
from src.session_logger import SessionLogger
from src.ui import DictationUI

class TestSessionLogger(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_logs"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        self.logger = SessionLogger(log_dir=self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_log_creation(self):
        self.logger.log_transcription("Test transcription")
        files = os.listdir(self.test_dir)
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].endswith(".md"))

class TestUI(unittest.TestCase):
    def test_update_text(self):
        ui = DictationUI()
        # Mock the page object since we aren't running a real GUI
        ui.page = MagicMock()
        ui.txt_output = MagicMock()
        ui.txt_output.value = ""
        ui.status_text = MagicMock()

        ui.update_text("Hello")
        # In the real code: ui.txt_output.value = new_text
        # Here we manually verify logic if we were checking state,
        # but since we mocked the object, we just check call logic or state management.

        # Actually, let's test the state logic in DictationUI directly
        # if we assign a real object to txt_output (simple class)

        class MockTextField:
            def __init__(self):
                self.value = ""

        ui.txt_output = MockTextField()
        ui.update_text("Hello")
        self.assertEqual(ui.txt_output.value, "Hello")

        ui.update_text("World")
        self.assertEqual(ui.txt_output.value, "Hello\nWorld")

if __name__ == '__main__':
    unittest.main()
