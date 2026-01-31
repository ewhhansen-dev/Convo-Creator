import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue

class AudioRecorder:
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_queue = queue.Queue()
        self._stream = None

    def _callback(self, indata, frames, time, status):
        """Callback for sounddevice."""
        if status:
            print(f"Audio status: {status}")
        if self.recording:
            self.audio_queue.put(indata.copy())

    def start_recording(self):
        """Starts the audio recording stream."""
        if self.recording:
            return

        self.recording = True
        self.audio_queue = queue.Queue() # Clear queue

        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self._callback
        )
        self._stream.start()
        print("Recording started...")

    def stop_recording(self, output_filename):
        """Stops recording and saves to file."""
        if not self.recording:
            return

        self.recording = False
        self._stream.stop()
        self._stream.close()

        # Collect all data from queue
        data_list = []
        while not self.audio_queue.empty():
            data_list.append(self.audio_queue.get())

        if not data_list:
            print("No audio recorded.")
            return

        # Concatenate and save
        full_recording = np.concatenate(data_list, axis=0)
        sf.write(output_filename, full_recording, self.sample_rate)
        print(f"Recording saved to {output_filename}")

if __name__ == "__main__":
    # Simple test
    import time
    recorder = AudioRecorder()
    recorder.start_recording()
    time.sleep(3)
    recorder.stop_recording("test_audio.wav")
