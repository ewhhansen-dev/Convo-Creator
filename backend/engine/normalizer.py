import subprocess
import os

class AudioNormalizer:
    """
    Handles audio normalization using ffmpeg.
    """
    @staticmethod
    def normalize(input_path: str, output_path: str) -> bool:
        """
        Normalizes audio to -16 LUFS (or similar standard) using ffmpeg.
        Returns True if successful.
        """
        # Minimal implementation: just converting to 16kHz mono wav for Whisper
        # In a full implementation, we'd add filter chains for loudness normalization.

        cmd = [
            "ffmpeg",
            "-y", # Overwrite
            "-i", input_path,
            "-ar", "16000",
            "-ac", "1",
            "-c:a", "pcm_s16le",
            output_path
        ]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Normalization failed: {e}")
            return False
