#!/bin/bash
# Full End-to-End Amy Test Script
# Complete interaction test: Startup → Wake → Command → Response + Wave

echo "🎬 AMY FULL END-TO-END TEST"
echo "=========================="
echo ""
echo "🎯 TEST SEQUENCE:"
echo "1. Amy announces: 'Astra is awake and listening'"
echo "2. YOU SAY: 'Astra'"
echo "3. Amy responds: 'Yes?' + wave gesture"
echo "4. YOU SAY: 'What's the time?'"
echo "5. Amy responds: 'The time is [current time]' + wave gesture"
echo ""
echo "🚀 Starting Amy..."
echo "   (Amplifier will be turned on automatically)"
echo "   (Press Ctrl+C to stop when done testing)"
echo ""

# Ensure amplifier is on
/home/spencer/bin/amp_on.sh

# Start Amy with full verbose output
cd /home/spencer/amy_core
bash astra_listen_loop.sh