#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
PID_FILE="$PROJECT_ROOT/.runtime/twinkle_webui.pid"

if [ ! -f "$PID_FILE" ]; then
  echo "No TwinkleBite AI WebUI PID file found: $PID_FILE"
  echo "The WebUI may not have been started by scripts/twinkle_webui_start.sh."
  exit 0
fi

PID="$(cat "$PID_FILE")"
if [ -z "$PID" ]; then
  echo "PID file is empty: $PID_FILE"
  rm -f "$PID_FILE"
  exit 0
fi

if ! kill -0 "$PID" 2>/dev/null; then
  echo "TwinkleBite AI WebUI process is not running. Removing stale PID file."
  rm -f "$PID_FILE"
  exit 0
fi

echo "Stopping TwinkleBite AI WebUI PID $PID ..."
kill "$PID"

for _ in 1 2 3 4 5; do
  if ! kill -0 "$PID" 2>/dev/null; then
    rm -f "$PID_FILE"
    echo "TwinkleBite AI WebUI stopped."
    exit 0
  fi
  sleep 1
done

echo "TwinkleBite AI WebUI did not stop within 5 seconds."
echo "PID $PID is still running. Please inspect it manually; this script does not use kill -9 by default."
exit 1
