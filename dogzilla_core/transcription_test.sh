#!/bin/bash

echo "🎙️ TRANSCRIPTION FIX TEST"
echo "=========================="
echo ""
echo "This test will:"
echo "1. Clean up any audio processes"
echo "2. Start Amy with improved timing"
echo "3. Wait for wake word detection"
echo "4. Test the transcription with 1.0s settle time"
echo ""
echo "Instructions:"
echo "- Wait for Amy to say 'Amy is online'"
echo "- Say 'Astra' clearly to wake her"
echo "- Wait for 'Yes?' response"
echo "- Then say 'What's the time?' clearly"
echo ""
echo "Starting in 3 seconds..."
sleep 3

# Clean up any existing audio processes
sudo fuser -k /dev/snd/* 2>/dev/null || true

# Set environment variables
export AUDIODEV="plughw:CARD=sndrpihifiberry,DEV=0"
export AREC_DEV="plughw:CARD=Device,DEV=0"

# Start Amy
cd /home/spencer/amy_core
source /home/spencer/picrawler/my_venv/bin/activate
python3 amy_wake.py