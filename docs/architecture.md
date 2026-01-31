# Architecture: Browser + Backend Split

## Overview
To bypass ChromeOS/Crostini limitations regarding hardware access (MIDI) and UI integration, **The Dictator** uses a client-server model running entirely on localhost.

## Components

### 1. Frontend (Chrome Browser)
*   **Technologies:** HTML5, Vanilla JS.
*   **Responsibilities:**
    *   **Web MIDI:** Directly connects to MIDI controllers (Drum Pads) without passing through Linux USB.
    *   **Audio Capture:** Uses `MediaRecorder` API to capture microphone input as blobs.
    *   **UI:** Minimal status display and manual controls.
    *   **Communication:** Sends audio via HTTP POST to the backend.

### 2. Backend (Crostini Linux)
*   **Technologies:** Python, FastAPI, Faster-Whisper.
*   **Responsibilities:**
    *   **API:** Exposes `/transcribe` endpoint.
    *   **Engine:** Runs `faster-whisper` (int8 optimized) to convert audio to text.
    *   **Logging:** Appends text to `transcripts/YYYY-MM-DD.md`.
    *   **Persistence:** No database; flat files for portability.

## Security ("Lead-Lined")
*   The Backend runs offline. It downloads the model once and requires no further internet connection.
*   Frontend runs in the browser context.
*   No data leaves the machine.

## Data Flow
1.  **User** hits Pad 1 (MIDI Note 36).
2.  **Frontend** detects `note_on`, starts `MediaRecorder`.
3.  **User** speaks.
4.  **User** hits Pad 1 again.
5.  **Frontend** stops recorder, creates `audio/wav` Blob.
6.  **Frontend** POSTs Blob to `http://localhost:8000/transcribe`.
7.  **Backend** saves temp file, transcribes, logs to disk.
8.  **Backend** returns JSON `{ "text": "..." }`.
9.  **Frontend** displays text and copies to Clipboard.
