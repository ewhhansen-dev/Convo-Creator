#!/bin/bash
set -e

MODEL_SIZE=${1:-"base.en"}
echo ">>> Downloading Whisper Model: $MODEL_SIZE"

source .venv/bin/activate

# We use a python one-liner to trigger the download via faster_whisper
python -c "from faster_whisper import download_model; download_model('$MODEL_SIZE')"

echo ">>> Model download complete."
