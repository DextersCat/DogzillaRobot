#!/usr/bin/env bash
if [ -n "${VIRTUAL_ENV:-}" ]; then
  echo "[ASTRA GUARD] A Python virtualenv is active at: $VIRTUAL_ENV"
  echo "[ASTRA GUARD] Our policy is System Python 3.13 only. Deactivate with: 'deactivate'"
  exit 42
fi
