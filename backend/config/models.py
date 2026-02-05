from pydantic import BaseModel
from typing import Dict, List, Optional

class AudioSettings(BaseModel):
    device_id: int = -1  # Default device
    sample_rate: int = 16000

class WhisperSettings(BaseModel):
    model_size: str = "base.en"
    device: str = "cpu"
    compute_type: str = "int8"

class AppConfig(BaseModel):
    audio: AudioSettings = AudioSettings()
    whisper: WhisperSettings = WhisperSettings()
    host: str = "127.0.0.1"
    port: int = 8000

class ButtonAction(BaseModel):
    note: int
    action: str
    payload: Optional[str] = None

class ButtonMap(BaseModel):
    buttons: List[ButtonAction] = []
