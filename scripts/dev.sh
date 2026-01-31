#!/bin/bash
set -e

# Activate venv
source .venv/bin/activate

# Start Backend
echo ">>> Starting Backend on localhost:8000..."
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Start Frontend (simple python http server for now to bypass CORS/file protocol issues if needed)
echo ">>> Serving Frontend on localhost:5500..."
cd frontend
python -m http.server 5500 &
FRONTEND_PID=$!

echo ">>> The Dictator is running!"
echo "    Frontend: http://localhost:5500"
echo "    Backend:  http://localhost:8000/docs"
echo ">>> Press Ctrl+C to stop."

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
