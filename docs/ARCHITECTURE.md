# Architecture Design

## Overview

Convo-Creator follows a modular architecture to separate concerns between audio capture, transcription processing, data persistence, and the user interface.

## Modules

### 1. Audio Capture (`src/audio_capture.py`)
-   **Responsibility**: records audio from the default microphone.
-   **Libraries**: `sounddevice`, `soundfile`, `numpy`.
-   **Interface**:
    -   `start_recording()`: Starts a background thread or stream.
    -   `stop_recording()`: Stops the stream and returns the filename or byte stream.

### 2. Transcription Engine (`src/transcriber.py`)
-   **Responsibility**: Converts audio to text using `faster-whisper`.
-   **Libraries**: `faster-whisper`.
-   **Configuration**: Model size (tiny, base, small, medium, large), Device (cpu, cuda), Compute Type (int8, float16).
-   **Interface**:
    -   `transcribe(audio_path)`: Returns text string.

### 3. Session Manager (`src/session_manager.py`)
-   **Responsibility**: Handles data persistence.
-   **Functionality**:
    -   Appends transcribed text to a daily markdown file (e.g., `data/2023-10-27.md`).
    -   Manages storage paths.

### 4. User Interface (`src/gui.py`)
-   **Responsibility**: Interaction layer.
-   **Libraries**: `PyQt6`.
-   **Components**:
    -   Main Window.
    -   Record/Stop Toggle Button.
    -   Text Display Area (Editable).
    -   Action Buttons (Copy, Clear).

### 5. Application Entry (`src/main.py`)
-   **Responsibility**: Bootstraps the application, loads config, initializes modules, and launches the GUI.

## Data Flow

1.  User clicks **Record**.
2.  `GUI` calls `AudioCapture.start()`.
3.  User clicks **Stop**.
4.  `GUI` calls `AudioCapture.stop()` -> receives `temp_audio.wav`.
5.  `GUI` calls `Transcriber.transcribe('temp_audio.wav')` -> receives `"Hello world"`.
6.  `GUI` updates Text Area.
7.  `GUI` calls `SessionManager.save("Hello world")` -> appends to log.
8.  User clicks **Copy** -> text sent to Clipboard.

## Configuration

Settings are stored in `config/settings.yaml`.
