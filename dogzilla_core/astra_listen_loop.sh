#!/usr/bin/env bash
set -Eeuo pipefail

export AUDIODEV="${AUDIODEV:-plughw:CARD=sndrpihifiberry,DEV=0}"
export AREC_DEV="${AREC_DEV:-plughw:CARD=Device,DEV=0}"
export PATH="$HOME/bin:$PATH"
export ASTRA_SENS="${ASTRA_SENS:-0.90}"
export ORT_LOGGING_LEVEL=ERROR   # hush onnxruntime GPU warnings

KEYPPN="$HOME/amy_core/keywords/astra.ppn"
LOGDIR="$HOME/logs"; mkdir -p "$LOGDIR"
LOG="$LOGDIR/astra_listen_$(date +%F_%H%M%S).log"
echo "$LOG" > "$LOGDIR/astra_listen.logpath"

# Clean shutdown on Ctrl+C / kill
cleanup() {
  echo "[listen] exiting" | tee -a "$LOG"
  pkill -f 'arecord -D' 2>/dev/null || true
  pkill -f /tmp/wake_once.py 2>/dev/null || true
  exit 0
}
trap 'echo "[listen] exiting" | tee -a "$LOG"; kill -- -$$ 2>/dev/null || true; exit 0' INT TERM

# Pre-render "online" and "Yes?" once for snappier prompts
pre_say() {  # $1 text  $2 file
  local text="$1" file="$2"
  [[ -s "$file" ]] && return 0
  piper --model "$HOME/voices/en_US-amy-medium.onnx" --text "$text" --output_file "$file" >>"$LOG" 2>&1 || true
}
ONLINE=/tmp/astra_online.wav
YES=/tmp/astra_yes.wav
pre_say "Astra is awake and listening." "$ONLINE"
pre_say "Yes, go ahead." "$YES"

say(){ aplay -D "$AUDIODEV" "$1" >>"$LOG" 2>&1 || true; }

echo "[listen] log: $LOG" | tee -a "$LOG"
say "$ONLINE"

WINDOW=20
while true; do
  [[ -e /tmp/amy_sleep ]] && { echo "[listen] sleep flag; pause" >>"$LOG"; sleep 2; continue; }

  # mic preflight (RAW)
  if ! arecord -D "$AREC_DEV" -r 16000 -c 1 -f S16_LE -t raw -d 1 -q >/dev/null 2>&1; then
    echo "[listen] mic busy: $AREC_DEV; retry 2s" >>"$LOG"; sleep 2; continue
  fi

  echo "[listen] waiting for wake word (Astra)..." >>"$LOG"
  if timeout "${WINDOW}s" bash -c '
    arecord -D "'"$AREC_DEV"'" -r 16000 -c 1 -f S16_LE -t raw -q 2>>"'"$LOG"'" | \
    ASTRA_SENS="'"${ASTRA_SENS}"'" python3 /tmp/wake_once.py >>"'"$LOG"'" 2>&1
  '; then
    echo "[listen] wake detected" >>"$LOG"
    say "$YES"
    # settle time increased per Fault-Tree v1.0: 0.15s → 0.35s to reduce wake word tail bleed
    echo "[listen] applying settle=0.35s (Fault-Tree v1.0 corrective action)" >>"$LOG"
    sleep 0.35
    python3 "$HOME/amy_core/postwake_router.py" >>"$LOG" 2>&1 || true
    sleep 0.5
  else
    echo "[listen] (no wake in window)" >>"$LOG"; sleep 0.4
  fi
done
