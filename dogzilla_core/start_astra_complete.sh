#!/bin/bash
#
# Astra Complete System Startup Script
# Starts all services needed for full Astra functionality
#

echo "🤖 Starting Astra Complete System..."
echo "========================================"

# Change to amy_core directory
cd /home/spencer/amy_core

# Kill any existing services
echo "🧹 Cleaning up existing services..."
pkill -f mobile_api_server 2>/dev/null
pkill -f vilib 2>/dev/null
pkill -f web_server 2>/dev/null
sleep 3

# Start API Server
echo "🚀 Starting API Server (port 5001)..."
nohup python3 mobile_api_server.py > api_server.log 2>&1 &
API_PID=$!
echo "   API Server PID: $API_PID"

# Wait for API server to initialize
sleep 5

# Start Camera Stream
echo "📹 Starting Camera Stream (port 9000)..."
cd /home/spencer
nohup python3 -c "
import sys
sys.path.append('/home/spencer/vilib')
from vilib import Vilib
import time
import signal

def signal_handler(sig, frame):
    print('� Stopping camera...')
    Vilib.camera_close()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

print('�📹 Starting camera stream...')
Vilib.camera_start(vflip=False, hflip=False)
Vilib.display(local=False, web=True)
print('✅ Camera stream: http://192.168.1.4:9000/mjpg')

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    signal_handler(None, None)
" > /home/spencer/amy_core/camera.log 2>&1 &
CAMERA_PID=$!
echo "   Camera Stream PID: $CAMERA_PID"

# Start Web Control Panel
echo "🌐 Starting Web Control Panel (port 8080)..."
cd /home/spencer/amy_core
nohup python3 web_server.py > web_server.log 2>&1 &
WEB_PID=$!
echo "   Web Server PID: $WEB_PID"

# Wait for services to start
echo "⏳ Waiting for services to initialize..."
sleep 10

# Test connections
echo "🔍 Testing service connections..."

# Test API
if curl -s http://192.168.1.4:5001/api/status > /dev/null; then
    echo "   ✅ API Server: Online"
else
    echo "   ❌ API Server: Failed"
fi

# Test Camera
if curl -s -I http://192.168.1.4:9000/mjpg > /dev/null; then
    echo "   ✅ Camera Stream: Online"
else
    echo "   ❌ Camera Stream: Failed"
fi

# Test Web Interface
if curl -s http://192.168.1.4:8080/astra_web_control.html > /dev/null; then
    echo "   ✅ Web Control Panel: Online"
else
    echo "   ❌ Web Control Panel: Failed"
fi

echo ""
echo "🎯 Astra System Status:"
echo "========================================"
echo "📱 Mobile App:       exp://192.168.1.4:8083"
echo "🌐 Web Control:      http://192.168.1.4:8080/astra_web_control.html"
echo "📹 Camera Stream:    http://192.168.1.4:9000/mjpg"
echo "🔧 API Endpoints:    http://192.168.1.4:5001/api/"
echo ""
echo "📋 Process IDs:"
echo "   API Server: $API_PID"
echo "   Camera:     $CAMERA_PID"
echo "   Web Server: $WEB_PID"
echo ""
echo "🔗 BOOKMARK THESE URLS:"
echo "   💻 Desktop/Laptop: http://192.168.1.4:8080/astra_web_control.html"
echo "   📱 Mobile App:     exp://192.168.1.4:8083"
echo ""
echo "✅ Astra system ready for operation!"