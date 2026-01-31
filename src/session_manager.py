import os
from datetime import datetime

class SessionManager:
    def __init__(self, storage_path="data"):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def save_transcription(self, text):
        """
        Appends the transcription text to the daily markdown file.
        Returns the path of the file modified.
        """
        if not text:
            return None

        now = datetime.now()
        filename = now.strftime("%Y-%m-%d.md")
        filepath = os.path.join(self.storage_path, filename)

        timestamp = now.strftime("%H:%M:%S")

        entry = f"\n## {timestamp}\n\n{text}\n"

        try:
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(entry)
            print(f"Saved to {filepath}")
            return filepath
        except IOError as e:
            print(f"Failed to save session: {e}")
            return None
