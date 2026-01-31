import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import tempfile
import os

class AudioRecorder:
    """
    Handles recording audio from the default input device.
    """
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_data = []
        self._stream = None

    def start_recording(self):
        """Starts the audio recording stream."""
        if self.recording:
            return

        self.recording = True
        self.audio_data = []

        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.audio_data.append(indata.copy())

        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=callback
        )
        self._stream.start()
        print(">>> Recording Started")

    def stop_recording(self) -> str:
        """
        Stops recording and saves to a temporary WAV file.
        Returns the path to the recorded file.
        """
        if not self.recording:
            return None

        self.recording = False
        self._stream.stop()
        self._stream.close()
        print(">>> Recording Stopped")

        if not self.audio_data:
            return None

        # Concatenate all buffer chunks
        full_recording = np.concatenate(self.audio_data, axis=0)

        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(temp_file.name, full_recording, self.sample_rate)

        return temp_file.name
