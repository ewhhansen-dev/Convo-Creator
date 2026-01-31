# The Dictator

Local-first dictation that behaves like a tool — not a platform.

**Goal (MVP):** hit a MIDI pad → talk → stop → get clean text → copy/paste anywhere → every take appends to a running session .md.

## Architecture

**Browser + Backend Split**

ChromeOS + Crostini is a sandbox with two pain points:
1. USB MIDI into the Linux container is unreliable.
2. Cross-app keystroke injection is blocked.

**Solution:**
- **Frontend (Chrome):** Web MIDI API (Pads) + MediaRecorder (Audio) -> Sends WAV to Backend.
- **Backend (Python/Crostini):** FastAPI server -> `faster-whisper` -> Logs to Markdown -> Returns text.

## Directory Structure

```
The-Dictator/
├── backend/             # Python API (FastAPI)
│   ├── main.py          # Entry point
│   ├── api/             # Routes
│   ├── engine/          # Transcription logic
│   └── output/          # Session logging
├── frontend/            # HTML/JS Client
│   ├── index.html
│   └── app.js           # Web MIDI & Fetch logic
├── scripts/             # Setup utilities
└── transcripts/         # Session logs
```

## Quick Start

1. **Setup Backend:**
   ```bash
   ./scripts/setup.sh
   source .venv/bin/activate
   ```

2. **Run Backend:**
   ```bash
   uvicorn backend.main:app --reload
   ```

3. **Open Frontend:**
   Open `frontend/index.html` in Chrome.
   *(Note: For microphone access, you may need to serve it via a local server, e.g., `python -m http.server` in the frontend dir, or configure Chrome to allow file:// access to mic)*

## MIDI Mapping (Default)
- **Pad 1 (Note 36):** Toggle Record
- **Pad 2 (Note 37):** Copy to Clipboard
