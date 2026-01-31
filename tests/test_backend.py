import pytest
from unittest.mock import MagicMock, patch
import os
from src.session_manager import SessionManager
from src.transcriber import AudioTranscriber
from src.audio_capture import AudioRecorder

# --- Session Manager Tests ---
def test_session_manager_creates_file(tmp_path):
    """Test that SessionManager creates a file and appends text."""
    manager = SessionManager(storage_path=str(tmp_path))
    text = "Test transcription"
    filepath = manager.save_transcription(text)

    assert filepath is not None
    assert os.path.exists(filepath)

    with open(filepath, 'r') as f:
        content = f.read()
        assert text in content

def test_session_manager_handles_empty_text(tmp_path):
    """Test that SessionManager ignores empty text."""
    manager = SessionManager(storage_path=str(tmp_path))
    result = manager.save_transcription("")
    assert result is None

# --- Transcriber Tests ---
def test_transcriber_calls_model():
    """Test that AudioTranscriber initializes the model and calls transcribe."""
    with patch('src.transcriber.WhisperModel') as MockModel:
        # Setup mock return values
        mock_instance = MockModel.return_value

        # Mock segments generator
        Segment = MagicMock()
        Segment.text = "Hello world"
        mock_instance.transcribe.return_value = ([Segment], None)

        transcriber = AudioTranscriber(model_size="tiny")

        # Mock os.path.exists to bypass file check
        with patch('os.path.exists', return_value=True):
            result = transcriber.transcribe("fake_audio.wav")

        assert result == "Hello world"
        MockModel.assert_called_with("tiny", device="auto", compute_type="int8")
        mock_instance.transcribe.assert_called()

def test_transcriber_handles_file_not_found():
    """Test that AudioTranscriber raises error for missing file."""
    transcriber = AudioTranscriber()
    with pytest.raises(FileNotFoundError):
        transcriber.transcribe("non_existent_file.wav")

# --- Audio Capture Tests ---
def test_audio_recorder_init():
    """Test AudioRecorder initialization."""
    recorder = AudioRecorder(sample_rate=44100, channels=2)
    assert recorder.sample_rate == 44100
    assert recorder.channels == 2
    assert recorder.recording is False

def test_audio_recorder_start_stop():
    """Test start and stop logic (mocking sounddevice)."""
    with patch('src.audio_capture.sd.InputStream') as MockStream:
        with patch('src.audio_capture.sf.write') as MockWrite:
            recorder = AudioRecorder()

            # Start
            recorder.start_recording()
            assert recorder.recording is True
            MockStream.assert_called()
            mock_stream_instance = MockStream.return_value
            mock_stream_instance.start.assert_called()

            # Simulate data in queue
            import numpy as np
            recorder.audio_queue.put(np.array([0.1, 0.2]))

            # Stop
            recorder.stop_recording("output.wav")
            assert recorder.recording is False
            mock_stream_instance.stop.assert_called()
            MockWrite.assert_called()
