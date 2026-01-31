from faster_whisper import WhisperModel
import os

class Transcriber:
    """
    Wraps faster-whisper for transcription.
    """
    def __init__(self, model_size="base.en", device="cpu", compute_type="int8"):
        print(f">>> Loading Whisper Model: {model_size} on {device} ({compute_type})...")
        # In a real scenario, we might want to allow GPU (device="cuda")
        # but defaulting to CPU/INT8 is safest for broad compatibility.
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print(">>> Model Loaded.")

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribes the given WAV file.
        Returns the text string.
        """
        if not os.path.exists(audio_path):
            return ""

        segments, info = self.model.transcribe(audio_path, beam_size=5)

        full_text = []
        for segment in segments:
            full_text.append(segment.text)

        return " ".join(full_text).strip()
