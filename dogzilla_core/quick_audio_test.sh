#!/bin/bash
# Quick Audio Test - Verify Amy can speak responses

echo "🔊 AUDIO CHAIN TEST"
echo "=================="
echo ""

# Ensure amp is on
echo "1. Turning on amplifier..."
/home/spencer/bin/amp_on.sh

echo "2. Testing robot HAT speaker with system sound..."
aplay -D plughw:CARD=sndrpihifiberry,DEV=0 /usr/share/sounds/alsa/Front_Right.wav

echo "3. Testing Amy's voice with Piper..."
cd /home/spencer/amy_core
python3 -c "
from postwake_router import say
print('   Generating Amy voice...')
say('Audio test successful. Amy can speak clearly.')
print('   ✅ Amy voice test completed')
"

echo ""
echo "🎯 If you heard Amy say 'Audio test successful', the fix worked!"
echo "   Ready to test full voice pipeline again."