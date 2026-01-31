# Architecture Design

## Overview
Convo-Creator is designed as a modular Python application using a "Core-Shell" pattern. The Core handles hardware I/O and Logic, while the Shell handles the UI.

## Components

### 1. Frontend (UI)
*   **Library:** Flet (Python wrapper for Flutter).
*   **Responsibility:** Display status, provide manual record buttons, show live transcription preview, and manage settings.
*   **Reasoning:** Flet allows creating a "app-like" experience on Linux without the heaviness of Electron or the dated look of Tkinter. It also supports web-view deployment if we move to a remote-container model later.

### 2. Audio Capture (Input)
*   **Library:** `sounddevice` (PortAudio).
*   **Format:** 16kHz Mono Float32 (Optimal for Whisper).
*   **VAD:** (Future) Silero VAD or WebRTC VAD to auto-trim silence.
*   **ChromeOS Note:** Relies on PulseAudio/PipeWire pass-through from ChromeOS.

### 3. Transcription Engine (Processing)
*   **Library:** `faster-whisper`.
*   **Model:** `tiny.en` or `base.en` (default) for speed; user configurable.
*   **Execution:** Runs in a separate thread to prevent UI freezing.
*   **Hardware:** Checks for CUDA; falls back to CPU INT8.

### 4. MIDI Controller (Trigger)
*   **Library:** `mido` + `python-rtmidi`.
*   **Function:** Listens for "Note On" events from specific MIDI devices to toggle recording state.

### 5. Data Flow
1.  **User** hits Drum Pad (MIDI Note On).
2.  **MIDI Handler** signals **Audio Capture** to start buffer.
3.  **User** speaks.
4.  **User** hits Drum Pad again (or Silence Detected).
5.  **Audio Capture** stops, saves temporary WAV (or passes in-memory buffer).
6.  **Transcriber** processes audio -> Text.
7.  **Output Handler**:
    *   Copies to **Clipboard**.
    *   Appends to **Session Log** (`YYYY-MM-DD.md`).
    *   Updates **UI** text area.

## "Lead-Lined" Security Considerations
*   **Network:** The core transcription engine requires NO internet access once the model is downloaded.
*   **Dependencies:** All Python deps are pinned in `pyproject.toml`.
*   **Isolation:** Future versions can move the `Transcriber` to a dedicated Docker container exposing a REST API, keeping the host lightweight.
