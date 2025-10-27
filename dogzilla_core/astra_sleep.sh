#!/usr/bin/env bash
set -euo pipefail
export AUDIODEV='plughw:2,0'
export PATH="$HOME/bin:$PATH"
FLAG="/tmp/amy_sleep"
LOGDIR="$HOME/logs"

touch "$FLAG"

# stop if running
if [[ -f "$LOGDIR/astra.pid" ]]; then
  PID=$(cat "$LOGDIR/astra.pid" || true)
  if [[ -n "${PID:-}" ]] && ps -p "$PID" >/dev/null 2>&1; then
    kill "$PID" 2>/dev/null || true
  fi
fi

# polite confirmation
TMP=$(mktemp /tmp/amy_sleep_XXXX.wav)
piper --model "$HOME/voices/en_US-amy-medium.onnx" --text "Going to sleep." --output_file "$TMP" || true
aplay -D "${AUDIODEV:-plughw:2,0}" "$TMP" >/dev/null 2>&1 || true
rm -f "$TMP"

echo "[astra_sleep] Sleep flag set at $FLAG"
[[ -f "$LOGDIR/astra.logpath" ]] && echo "[astra_sleep] Last log: $(cat "$LOGDIR/astra.logpath")"
