#!/bin/bash
set -e

echo ">>> Setting up The-Dictator Environment..."

# 1. System Dependencies
# ffmpeg is needed for faster-whisper/audio processing
echo ">>> Installing System Dependencies (ffmpeg)..."
sudo apt-get update
sudo apt-get install -y ffmpeg

# 2. Python Virtual Environment
if [ ! -d ".venv" ]; then
    echo ">>> Creating .venv..."
    python3 -m venv .venv
else
    echo ">>> .venv exists, skipping creation."
fi

# 3. Install Python Dependencies
echo ">>> Installing Python packages..."
source .venv/bin/activate
pip install --upgrade pip
pip install -e .

echo ">>> Setup Complete. Activate with: source .venv/bin/activate"
