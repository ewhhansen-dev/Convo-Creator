# AGENTS.md - Protocol & Guidelines

## 1. Project Context
This repository hosts the **Convo-Creator** (working title: Dictation Station), a robust dictation and AI-interaction tool designed for a Chromebook (Linux/Crostini) environment.
The user ("The Architect") utilizes multiple coding agents. This file serves as the coordination point.

## 2. Core Principles

### "Lead-Lined" Architecture (Security & Isolation)
- **Minimization:** Use minimal dependencies.
- **Isolation:** Where possible, separate "processing" (parsing, transcoding) from "host access" (hardware).
- **Immutability:** Code should be robust. If using Docker (future), containers must be Read-Only root with dropped capabilities (`cap_drop: [ALL]`).
- **Clean Room:** Prefer workflows that do not require constant internet access. Offline-first where possible (e.g., local `faster-whisper` models).

### Code Quality ("Best Version Wins")
- **Modular:** Keep UI, Audio Capture, and Transcription logic in separate modules (`src/`).
- **Documented:** Every major function must have a docstring.
- **Tested:** Write unit tests for logic that doesn't strictly depend on hardware. Mock hardware where necessary.

## 3. Tech Stack
- **Language:** Python 3.12+
- **UI:** Flet (Flutter for Python) - chosen for modern look + potential web portability.
- **Audio:** `sounddevice` (PortAudio wrapper).
- **Transcription:** `faster-whisper` (CTranslate2).
- **Environment:** Ubuntu 24.04 (Crostini) compatible.
- **Dependency Management:** PEP 668 compliant (use `venv` or `pipx`, do not run `pip install` globally as root).

## 4. Operational Guidelines
- **Git:** Commit messages should be descriptive.
- **Hardware:**
    - **Microphone:** Requires ChromeOS "Allow Linux to access microphone" setting.
    - **MIDI:** Requires ChromeOS USB device pass-through.
    - **GPU:** Faster Whisper should default to `int8` on CPU if CUDA is unavailable, but support CUDA if present.

## 5. File Structure
- `src/`: Source code.
- `tests/`: Unit tests.
- `docs/`: Architecture and design notes.
- `scripts/`: Setup and utility scripts.
