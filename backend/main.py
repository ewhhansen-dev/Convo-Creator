from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import routes
from backend.config.loader import load_settings
import os

app = FastAPI(title="The Dictator API")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

@app.on_event("startup")
async def startup_event():
    print(">>> Backend Starting...")

    # Load Config
    config = load_settings()
    print(f">>> Loaded Config: Host={config.host}, Port={config.port}")
    print(f">>> Whisper Settings: Model={config.whisper.model_size}, Device={config.whisper.device}")

    # Ensure log directory exists
    os.makedirs("transcripts", exist_ok=True)
