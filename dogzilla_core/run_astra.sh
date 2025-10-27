#!/usr/bin/env bash
set -euo pipefail
export AUDIODEV='plughw:2,0'
export AREC_DEV='plughw:3,0'
export GPIOZERO_PIN_FACTORY=lgpio
export PATH="$HOME/bin:$PATH"

FLAG="/tmp/amy_sleep"
LOGDIR="$HOME/logs"
mkdir -p "$LOGDIR"

if [[ -e "$FLAG" ]]; then
  echo "[run_astra] Sleep flag present: $FLAG — not starting."
  exit 0
fi

LOG="$LOGDIR/astra_run_$(date +%F_%H%M%S).log"
echo "[run_astra] Starting amy_wake.py | log: $LOG"
echo "$LOG" > "$LOGDIR/astra.logpath"

# launch and keep a pidfile for safe stop
python3 "$HOME/amy_core/amy_wake.py" >>"$LOG" 2>&1 & echo $! > "$LOGDIR/astra.pid"
wait "$(cat "$LOGDIR/astra.pid")" || true
