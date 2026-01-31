import sys
from unittest.mock import MagicMock

# Mock faster_whisper to avoid installation overhead during tests
mock_whisper = MagicMock()
sys.modules["faster_whisper"] = mock_whisper

# Mock PyQt6 to avoid GUI requirement during backend tests
mock_qt = MagicMock()
sys.modules["PyQt6"] = mock_qt
sys.modules["PyQt6.QtWidgets"] = mock_qt
sys.modules["PyQt6.QtCore"] = mock_qt

# Mock sounddevice to avoid PortAudio requirement
mock_sd = MagicMock()
sys.modules["sounddevice"] = mock_sd
