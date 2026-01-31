from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.engine.transcriber import Transcriber
from backend.output.session_logger import SessionLogger
import shutil
import tempfile
import os

router = APIRouter()

# Global instances (lazy loaded in real app, but initialized here for simplicity)
# Note: Transcriber loading is heavy, so we might want to do it on startup or lazy.
# For this MVP, we instantiate it once at module level or lazily.
_transcriber = None
_logger = SessionLogger(log_dir="transcripts")

def get_transcriber():
    global _transcriber
    if _transcriber is None:
        _transcriber = Transcriber()
    return _transcriber

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Receives an audio file (blob), saves it temp, transcribes it,
    logs it, and returns the text.
    """
    try:
        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        # Transcribe
        transcriber = get_transcriber()
        text = transcriber.transcribe(tmp_path)

        # Cleanup
        os.remove(tmp_path)

        # Log
        if text:
            _logger.log_transcription(text)

        return {"text": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    return {"status": "ok"}
