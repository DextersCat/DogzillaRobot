#!/bin/bash
# Amy Voice Assistant Environment Activation Script
# Created: 2025-10-24
# Purpose: Standardize environment activation for Amy development

echo "🎤 Activating Amy Voice Assistant Environment..."

# Activate virtual environment
source /home/spencer/picrawler/my_venv/bin/activate

# Load audio environment variables
source /home/spencer/amy_core/env/astra_audio.env

# Set Picovoice API key
export PICOVOICE_ACCESS_KEY="$(</home/spencer/.config/picovoice.key)"

# Suppress ONNX Runtime warnings for cleaner output
export OMP_NUM_THREADS=1
export ORT_LOGGING_LEVEL=3

# Verify critical packages
python3 -c "
import pvporcupine, faster_whisper, picrawler
print('✅ Environment ready - All critical packages available')
print(f'🐍 Python: {__import__(\"sys\").version.split()[0]}')
print(f'🎯 Working Directory: {__import__(\"os\").getcwd()}')
print(f'🔊 Audio Output: {__import__(\"os\").environ.get(\"AUDIODEV\", \"Not set\")}')
print(f'🎙️  Audio Input: {__import__(\"os\").environ.get(\"AREC_DEV\", \"Not set\")}')
"

echo "🚀 Amy environment is ready!"
echo "💡 To test: python3 ~/amy_core/postwake_router.py"
echo "🔧 To debug: tail -f ~/logs/pipeline_*.log"