# Convo-Creator

A lightweight, local dictation and transcription application designed for power users on Linux (Chromebook/Crostini).

## Features

-   **Local Transcription**: Uses `faster-whisper` for high-speed, privacy-focused transcription without cloud dependencies.
-   **Dictation Mode**: Record voice notes and immediately transcribe them.
-   **Clipboard Integration**: Automatically copy transcriptions to the clipboard for easy pasting into any application.
-   **Session Logging**: Archives all transcriptions into a daily Markdown file for easy retrieval.
-   **GUI**: A clean, "premium" feel interface built with PyQt6.
-   **Extensible**: Architecture designed to support future AI "Action" plugins (e.g., "Refine this text", "Draft email").

## Installation

1.  **System Dependencies** (Debian/Ubuntu/Chromebook):
    ```bash
    sudo apt-get update
    sudo apt-get install python3-pip python3-venv portaudio19-dev ffmpeg libxcb-cursor0
    ```

2.  **Python Setup**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

Run the main application:

```bash
python src/main.py
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design documentation.
