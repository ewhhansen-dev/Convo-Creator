from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.engine.transcriber import Transcriber
from backend.engine.normalizer import AudioNormalizer
from backend.output.session_logger import SessionLogger
from backend.config.loader import load_settings
import shutil
import tempfile
import os

router = APIRouter()

_transcriber = None
_logger = SessionLogger(log_dir="transcripts")

def get_transcriber():
    global _transcriber
    if _transcriber is None:
        cfg = load_settings()
        _transcriber = Transcriber(
            model_size=cfg.whisper.model_size,
            device=cfg.whisper.device,
            compute_type=cfg.whisper.compute_type
        )
    return _transcriber

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Save raw upload
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            shutil.copyfileobj(file.file, tmp)
            raw_path = tmp.name

        # Normalize (optional but good practice)
        normalized_path = raw_path + "_norm.wav"
        if AudioNormalizer.normalize(raw_path, normalized_path):
            process_path = normalized_path
        else:
            process_path = raw_path # Fallback

        # Transcribe
        transcriber = get_transcriber()
        text = transcriber.transcribe(process_path)

        # Cleanup
        try:
            os.remove(raw_path)
            if os.path.exists(normalized_path):
                os.remove(normalized_path)
        except:
            pass

        # Log
        if text:
            _logger.log_transcription(text)

        return {"text": text}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    return {"status": "ok"}
