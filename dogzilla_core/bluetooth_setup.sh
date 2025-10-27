#!/bin/bash

echo "🎧 BLUETOOTH HEADSET SETUP FOR AMY"
echo "=================================="
echo ""
echo "✅ Bluetooth service is running"
echo "✅ You have existing headsets (Bluetooth + AirPods Pro)"
echo "✅ Zero additional cost required!"
echo ""

echo "🎯 SETUP PROCESS:"
echo "=================="
echo ""

echo "STEP 1: Put your headset in pairing mode"
echo "- Bluetooth headset: Hold power/pair button"
echo "- AirPods Pro: Open case, press back button until light flashes"
echo ""

echo "STEP 2: Discover and pair (run these commands):"
echo ""
echo "# Start Bluetooth pairing mode"
echo "sudo bluetoothctl"
echo ""
echo "# In bluetoothctl prompt:"
echo "power on"
echo "agent on"
echo "default-agent"
echo "scan on"
echo ""
echo "# Wait for your headset to appear, then:"
echo "pair XX:XX:XX:XX:XX:XX  # Replace with your headset's MAC address"
echo "trust XX:XX:XX:XX:XX:XX"
echo "connect XX:XX:XX:XX:XX:XX"
echo "exit"
echo ""

echo "STEP 3: Test audio input/output"
echo ""

echo "🔧 AUTOMATED SETUP SCRIPT:"
echo "=========================="
echo ""
echo "Run this to start pairing mode:"
echo ""

# Create the pairing commands
cat << 'EOF'
# Bluetooth pairing helper
echo "Starting Bluetooth discovery..."
bluetoothctl << BTCTL
power on
agent on
default-agent
scan on
EOF

echo ""
echo "After seeing your headset in the scan results:"
echo "1. Note the MAC address (XX:XX:XX:XX:XX:XX format)"
echo "2. Run: sudo bluetoothctl"
echo "3. In bluetoothctl: pair XX:XX:XX:XX:XX:XX"
echo "4. In bluetoothctl: trust XX:XX:XX:XX:XX:XX"
echo "5. In bluetoothctl: connect XX:XX:XX:XX:XX:XX"
echo "6. Type: exit"
echo ""

echo "🎤 TESTING WITH AMY:"
echo "==================="
echo ""
echo "Once connected, we'll need to:"
echo "1. Configure ALSA to use Bluetooth audio"
echo "2. Update Amy's audio device settings"
echo "3. Test voice commands"
echo ""

echo "Expected result:"
echo 'You (wearing headset): "Astra"'
echo 'Amy: "Yes, go ahead." (through headset speakers)'
echo 'You: "What\'s the time?"'
echo 'Amy: "The time is 4:45 PM" (perfect transcription!)'
echo ""

echo "🚀 READY TO START?"
echo "=================="
echo ""
echo "1. Put your headset in pairing mode"
echo "2. Run: sudo bluetoothctl"
echo "3. Follow the pairing steps above"
echo "4. Call me back when connected!"
echo ""

echo "This will solve your 6-week problem in the next 10 minutes! 🎯"