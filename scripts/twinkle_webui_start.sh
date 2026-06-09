#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
PORT="${PORT:-8501}"
HOST="${HOST:-127.0.0.1}"
RUNTIME_DIR="$PROJECT_ROOT/.runtime"
PID_FILE="$RUNTIME_DIR/twinkle_webui.pid"
LOG_FILE="$RUNTIME_DIR/twinkle_webui.log"

is_port_in_use() {
  if command -v lsof >/dev/null 2>&1; then
    lsof -i :"$PORT" >/dev/null 2>&1
    return $?
  fi

  python3 - "$HOST" "$PORT" <<'PY'
import socket
import sys

host = sys.argv[1]
port = int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sys.exit(0 if sock.connect_ex((host, port)) == 0 else 1)
PY
}

if is_port_in_use; then
  echo "Port $PORT is already in use. Run scripts/twinkle_webui_status.sh to inspect."
  echo "Run scripts/twinkle_webui_stop.sh if it was started by this project."
  exit 1
fi

mkdir -p "$RUNTIME_DIR"

if [ -x "$PROJECT_ROOT/.venv/bin/python" ]; then
  STREAMLIT_CMD=("$PROJECT_ROOT/.venv/bin/python" -m streamlit)
elif command -v uv >/dev/null 2>&1; then
  STREAMLIT_CMD=(uv run streamlit)
elif command -v streamlit >/dev/null 2>&1; then
  STREAMLIT_CMD=(streamlit)
else
  echo "Neither project Python, uv, nor streamlit was found. Please install dependencies first."
  exit 1
fi

cd "$PROJECT_ROOT"
nohup "${STREAMLIT_CMD[@]}" run "$PROJECT_ROOT/webui/Main.py" \
  --server.address="$HOST" \
  --server.port="$PORT" \
  --browser.serverAddress="$HOST" \
  --browser.gatherUsageStats=False \
  --server.enableCORS=True \
  > "$LOG_FILE" 2>&1 &
PID="$!"
echo "$PID" > "$PID_FILE"
disown "$PID" 2>/dev/null || true

sleep 3
if ! kill -0 "$PID" 2>/dev/null; then
  echo "TwinkleBite AI WebUI failed to stay running."
  echo "Log: $LOG_FILE"
  tail -40 "$LOG_FILE" 2>/dev/null || true
  rm -f "$PID_FILE"
  exit 1
fi

if ! is_port_in_use; then
  echo "TwinkleBite AI WebUI process is running, but port $PORT is not listening yet."
  echo "PID: $PID"
  echo "Log: $LOG_FILE"
  tail -40 "$LOG_FILE" 2>/dev/null || true
  exit 1
fi

echo "TwinkleBite AI WebUI started."
echo "URL: http://$HOST:$PORT"
echo "PID: $PID"
echo "Log: $LOG_FILE"
