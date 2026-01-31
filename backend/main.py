from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import routes
import os

app = FastAPI(title="The Dictator API")

# Allow CORS for frontend dev (usually port 5500 or 8000)
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
    # Ensure log directory exists
    os.makedirs("transcripts", exist_ok=True)
