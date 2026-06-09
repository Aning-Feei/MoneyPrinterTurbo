#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
PORT="${PORT:-8501}"
HOST="${HOST:-127.0.0.1}"
RUNTIME_DIR="$PROJECT_ROOT/.runtime"
PID_FILE="$RUNTIME_DIR/twinkle_webui.pid"
LOG_FILE="$RUNTIME_DIR/twinkle_webui.log"

echo "TwinkleBite AI WebUI status"
echo "Project: $PROJECT_ROOT"
echo "URL: http://$HOST:$PORT"
echo "PID file: $PID_FILE"

if [ -f "$PID_FILE" ]; then
  PID="$(cat "$PID_FILE")"
  echo "PID file exists: yes"
  echo "PID: $PID"
  if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
    echo "PID running: yes"
  else
    echo "PID running: no"
  fi
else
  echo "PID file exists: no"
fi

echo ""
echo "Port $PORT listener:"
if command -v lsof >/dev/null 2>&1; then
  lsof -i :"$PORT" || true
else
  echo "lsof is not available."
fi

echo ""
echo "Recent log: $LOG_FILE"
if [ -f "$LOG_FILE" ]; then
  tail -40 "$LOG_FILE"
else
  echo "Log file not found."
fi
