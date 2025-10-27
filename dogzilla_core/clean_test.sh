#!/bin/bash
# Modified Amy Test with Microphone Cleanup
echo "🎬 AMY TEST WITH MIC CLEANUP"
echo "=========================="

# Ensure clean audio state
echo "🔧 Cleaning audio processes..."
sudo fuser -k /dev/snd/* 2>/dev/null || true
sleep 2

# Ensure amplifier is on
echo "🔊 Turning on amplifier..."
/home/spencer/bin/amp_on.sh

echo "🎯 Starting Amy (press Ctrl+C when done)..."
cd /home/spencer/amy_core

# Set environment variables explicitly
export AUDIODEV="plughw:CARD=sndrpihifiberry,DEV=0"
export AREC_DEV="plughw:CARD=Device,DEV=0"
export PICOVOICE_ACCESS_KEY="$(</home/spencer/.config/picovoice.key)"

# Start Amy
bash astra_listen_loop.sh