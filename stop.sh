#!/usr/bin/env bash
# Stops the backend and frontend processes started by start.sh.
cd "$(dirname "$0")"

stop_pid_file() {
    local pid_file="$1"
    local name="$2"
    if [ -f "$pid_file" ]; then
        local pid
        pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
            echo "Stopped $name (PID $pid)"
        else
            echo "$name not running (stale PID file)"
        fi
        rm -f "$pid_file"
    else
        echo "$name: no PID file, nothing to stop"
    fi
}

stop_pid_file .backend.pid "backend"
stop_pid_file .frontend.pid "frontend"

# Fallback: in case a service was started outside start.sh and left orphaned.
pkill -f "uvicorn app.main:app" 2>/dev/null && echo "Killed stray uvicorn process(es)"
pkill -f "vite.*--port 5173" 2>/dev/null || true

echo "Done."
