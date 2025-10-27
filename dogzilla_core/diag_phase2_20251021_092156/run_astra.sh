#!/usr/bin/env bash
set -euo pipefail

# Devices per Golden v2
export APLAY_DEV='plughw:2,0'
export AREC_DEV='plughw:3,0'

# Use the venv we prepared for Porcupine + Piper
export PY_WAKE="$HOME/venvs/amy/bin/python3"
export PATH="$HOME/venvs/amy/bin:$PATH"

# Say helper: Piper if present+model, else espeak
say(){ 
  if command -v piper >/dev/null 2>&1 && [ -f "$HOME/voices/en_US-amy-medium.onnx" ]; then
    T=$(mktemp /tmp/amy_tts_XXXX.wav)
    printf "%s\n" "$*" | piper -m "$HOME/voices/en_US-amy-medium.onnx" -f "$T"
    aplay -D "$APLAY_DEV" "$T"
    rm -f "$T"
  else
    espeak-ng -v en-gb -s 175 "$*" --stdout | aplay -D "$APLAY_DEV"
  fi
}

# Sanity: Porcupine import with this interpreter
"$PY_WAKE" -c 'import pvporcupine, sys; print("Porcupine OK:", sys.executable)'

# 2) Run wake on your custom Astra .ppn for 25s; on detect say "Yes?"
"$PY_WAKE" "$HOME/amy_core/amy_wake.py" \
  --keyword "$HOME/amy_core/keywords/astra.ppn" \
  --arec-dev "$AREC_DEV" \
  --sensitivity 0.25 \
  --duration 25 \
  --on-detect-cmd 'bash -lc '\''say "Yes?"'\''' \
  --log /tmp/amy_wake_astra_say.log
