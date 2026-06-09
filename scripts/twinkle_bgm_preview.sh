#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SONG_DIR="$PROJECT_ROOT/resource/songs"

usage() {
  cat <<'USAGE'
Usage:
  scripts/twinkle_bgm_preview.sh list
  scripts/twinkle_bgm_preview.sh output000.mp3 [seconds]

Examples:
  scripts/twinkle_bgm_preview.sh list
  scripts/twinkle_bgm_preview.sh output000.mp3
  scripts/twinkle_bgm_preview.sh output000.mp3 20
USAGE
}

bgm_id_for_file() {
  local filename="$1"
  local base number
  base="$(basename "$filename")"
  number="${base#output}"
  number="${number%.mp3}"
  printf "BGM-%03d" "$((10#$number + 1))"
}

list_files() {
  if [ ! -d "$SONG_DIR" ]; then
    echo "BGM directory not found: $SONG_DIR" >&2
    exit 1
  fi

  echo "Available BGM files:"
  find "$SONG_DIR" -maxdepth 1 -type f -name "output*.mp3" -print | sort | while read -r file; do
    printf "%s  %s\n" "$(bgm_id_for_file "$file")" "$(basename "$file")"
  done

  if [ ! -f "$SONG_DIR/output026.mp3" ]; then
    echo ""
    echo "Missing: BGM-027  output026.mp3"
  fi
}

play_file() {
  local filename="$1"
  local seconds="${2:-20}"
  local file player_pid

  if ! command -v afplay >/dev/null 2>&1; then
    echo "afplay not found. This preview script requires macOS afplay." >&2
    exit 1
  fi

  if [[ ! "$seconds" =~ ^[0-9]+$ ]] || [ "$seconds" -le 0 ]; then
    echo "seconds must be a positive integer." >&2
    exit 1
  fi

  file="$SONG_DIR/$filename"
  if [ ! -f "$file" ]; then
    echo "BGM file not found: $file" >&2
    exit 1
  fi

  echo "Playing resource/songs/$filename for $seconds seconds..."
  afplay "$file" &
  player_pid=$!
  sleep "$seconds"
  if kill -0 "$player_pid" 2>/dev/null; then
    kill "$player_pid" 2>/dev/null || true
    wait "$player_pid" 2>/dev/null || true
  fi
}

main() {
  if [ "$#" -lt 1 ]; then
    usage
    exit 1
  fi

  case "$1" in
    list)
      list_files
      ;;
    -h|--help|help)
      usage
      ;;
    *)
      play_file "$@"
      ;;
  esac
}

main "$@"
