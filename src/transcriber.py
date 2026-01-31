from faster_whisper import WhisperModel
import os

class AudioTranscriber:
    def __init__(self, model_size="base", device="auto", compute_type="int8"):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None

    def load_model(self):
        """Loads the Whisper model if not already loaded."""
        if self.model is None:
            print(f"Loading Whisper model: {self.model_size} on {self.device}...")
            try:
                self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
                print("Model loaded successfully.")
            except Exception as e:
                print(f"Error loading model: {e}")
                raise e

    def transcribe(self, audio_path):
        """
        Transcribes the audio file at the given path.
        Returns the transcribed text string.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        self.load_model()

        print(f"Transcribing {audio_path}...")
        try:
            segments, info = self.model.transcribe(audio_path, beam_size=5)

            full_text = []
            for segment in segments:
                full_text.append(segment.text)

            return " ".join(full_text).strip()
        except Exception as e:
            print(f"Transcription failed: {e}")
            return ""

if __name__ == "__main__":
    # Test stub (requires a file)
    pass
