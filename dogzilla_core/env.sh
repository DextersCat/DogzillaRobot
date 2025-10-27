export AUDIODEV='plughw:2,0'            # DAC
export AREC_DEV='plughw:3,0'            # USB mic
export GPIOZERO_PIN_FACTORY=lgpio       # Pi 5 GPIO backend
export PICOVOICE_ACCESS_KEY="$(<"$HOME/.config/picovoice.key")"
# Ensure venv path (edit if your venv differs)
[ -d "$HOME/venvs/amy/bin" ] && export PATH="$HOME/venvs/amy/bin:$PATH"
