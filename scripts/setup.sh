#!/bin/bash
set -e

echo ">>> Setting up Convo-Creator Environment..."

# 1. System Dependencies (Debian/Ubuntu/Crostini)
echo ">>> Installing System Dependencies (ffmpeg, portaudio)..."
sudo apt-get update
sudo apt-get install -y ffmpeg libportaudio2 libasound2-dev python3-venv librtmidi-dev

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
