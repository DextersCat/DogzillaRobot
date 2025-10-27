#!/usr/bin/env bash
set -euo pipefail
export AUDIODEV='plughw:2,0'
export AREC_DEV='plughw:3,0'
export GPIOZERO_PIN_FACTORY=lgpio
export PATH="$HOME/bin:$PATH"
FLAG="/tmp/amy_sleep"
LOGDIR="$HOME/logs"

rm -f "$FLAG"

TMP=$(mktemp /tmp/amy_wake_XXXX.wav)
piper --model "$HOME/voices/en_US-amy-medium.onnx" --text "I am awake." --output_file "$TMP" || true
aplay -D "${AUDIODEV:-plughw:2,0}" "$TMP" >/dev/null 2>&1 || true
rm -f "$TMP"

# relaunch non-blocking
nohup "$HOME/amy_core/run_astra.sh" >/dev/null 2>&1 &

echo "[astra_wake] Cleared sleep flag and relaunched."
sleep 0.5
[[ -f "$LOGDIR/astra.logpath" ]] && echo "[astra_wake] Current log: $(cat "$LOGDIR/astra.logpath")"
