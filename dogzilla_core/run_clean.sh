#!/usr/bin/env bash
set -euo pipefail
source "$HOME/amy_core/env.sh"
exec python "$HOME/amy_core/amy_wake.py" \
  --arec-dev "$AREC_DEV" \
  --sensitivity 0.25 \
  --duration 30 \
  --on-detect-cmd "python /tmp/wave_once.py" \
  --log /tmp/amy_wake_current.log
