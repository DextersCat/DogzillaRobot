#!/usr/bin/env bash
set -euo pipefail
. "$HOME/amy_core/env/astra_audio.env"
"$HOME/amy_core/env/venv_guard.sh"
exec "$@"
