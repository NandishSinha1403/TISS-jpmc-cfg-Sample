#!/usr/bin/env bash
# Starts backend (FastAPI, :8000) and frontend (Vite, :5173) in the background.
# Logs go to logs/backend.log and logs/frontend.log; PIDs go to .backend.pid / .frontend.pid.
set -euo pipefail
cd "$(dirname "$0")"

mkdir -p logs

if [ -f .backend.pid ] && kill -0 "$(cat .backend.pid)" 2>/dev/null; then
    echo "Backend already running (PID $(cat .backend.pid))"
else
    echo "Starting backend..."
    cd backend
    if [ ! -d venv ]; then
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    else
        source venv/bin/activate
    fi
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "Created backend/.env from .env.example — add your OPENROUTER_API_KEY if you want practice questions to work."
    fi
    if [ ! -f tiss.db ]; then
        python -m scripts.seed_admin
    fi
    nohup uvicorn app.main:app --port 8000 > ../logs/backend.log 2>&1 &
    echo $! > ../.backend.pid
    cd ..
    echo "Backend starting on http://localhost:8000 (PID $(cat .backend.pid))"
fi

if [ -f .frontend.pid ] && kill -0 "$(cat .frontend.pid)" 2>/dev/null; then
    echo "Frontend already running (PID $(cat .frontend.pid))"
else
    echo "Starting frontend..."
    cd frontend
    if [ ! -d node_modules ]; then
        npm install
    fi
    if [ ! -f .env ]; then
        cp .env.example .env
    fi
    nohup npm run dev > ../logs/frontend.log 2>&1 &
    echo $! > ../.frontend.pid
    cd ..
    echo "Frontend starting on http://localhost:5173 (PID $(cat .frontend.pid))"
fi

echo ""
echo "Waiting for services to come up..."
sleep 6
curl -s http://localhost:8000/health > /dev/null && echo "Backend: OK  (http://localhost:8000, docs at /docs)" || echo "Backend: not responding yet — check logs/backend.log"
curl -s -o /dev/null http://localhost:5173 && echo "Frontend: OK (http://localhost:5173)" || echo "Frontend: not responding yet — check logs/frontend.log"
echo ""
echo "Admin login: nandish@tiss.edu / admin101"
echo "Run ./stop.sh to stop both."
