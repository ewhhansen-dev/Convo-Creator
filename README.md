# Convo-Creator (Dictation Station)

A lightweight, robust, and "lead-lined" dictation application designed for ChromeOS (Crostini) but portable to any Linux environment.

## Features

- **Local Transcription:** Uses `faster-whisper` for high-speed, offline-capable speech-to-text.
- **MIDI Trigger:** Supports 16-key MIDI drum pads to trigger recording, start AI workflows, or insert macros.
- **Session Logging:** Automatically appends all dictations to a daily Markdown (`.md`) journal.
- **Clipboard Integration:** Instantly copies transcription to clipboard for pasting into any app.
- **Modern UI:** Built with Flet for a clean, responsive interface.
- **AI Ready:** Designed to easily plug in local LLMs or external APIs for text refinement.

## Requirements

- Linux (Ubuntu 24.04+ recommended) or ChromeOS Crostini.
- Python 3.12+
- `ffmpeg` installed on the system.

## Quick Start

1. **Setup:**
   ```bash
   ./scripts/setup.sh
   source .venv/bin/activate
   ```

2. **Run:**
   ```bash
   python main.py
   ```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design info.
