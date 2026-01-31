# AGENTS.md

Welcome to the Convo-Creator repository. This project is a collaborative effort between multiple agents and the user. To ensure stability and progress, please adhere to the following guidelines.

## Core Directives

1.  **Read Before Write**: Always explore the existing codebase (`list_files`, `read_file`) before creating new files to avoid duplication or overwriting work.
2.  **Architecture Adherence**: Follow the modular structure defined in `docs/ARCHITECTURE.md`.
    -   `src/`: Source code.
    -   `config/`: Configuration files (YAML/JSON). **Do not hardcode constants** in the source code; use the config file.
    -   `tests/`: Unit and integration tests.
3.  **Testing**: Every new feature or logic change must be accompanied by a test case in `tests/`. Run `pytest` to ensure no regressions.
4.  **Verification**: After writing a file, verify its content. After implementing logic, run it or test it.
5.  **Environment**: Assume a Linux environment (specifically Chromebook Crostini compatibility). Use standard Python libraries compatible with Linux.

## Code Style

-   Use Python 3.10+ conventions.
-   Add docstrings to functions and classes.
-   Keep functions small and focused (Single Responsibility Principle).

## Specific Feature Guidelines

-   **Audio**: Use `sounddevice` for capture.
-   **Transcription**: Use `faster-whisper`. Ensure the model path is configurable.
-   **GUI**: Use `PyQt6`. Keep the UI logic separate from business logic as much as possible.
