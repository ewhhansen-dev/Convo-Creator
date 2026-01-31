import os
import datetime

class SessionLogger:
    """
    Appends transcriptions to a daily markdown file.
    """
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def log_transcription(self, text: str):
        if not text:
            return

        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        filename = os.path.join(self.log_dir, f"{date_str}.md")

        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"\n## {time_str}\n{text}\n")

        print(f">>> Logged to {filename}")
