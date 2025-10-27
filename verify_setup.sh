#!/bin/bash
# Dogzilla S2 Quick Setup Verification Script

echo "🐕🦖 DOGZILLA S2 SETUP VERIFICATION"
echo "=================================="

# Check if running on Pi 5
echo "📟 Checking hardware..."
if grep -q "Raspberry Pi 5" /proc/cpuinfo; then
    echo "✅ Running on Raspberry Pi 5"
else
    echo "⚠️ Not detected as Raspberry Pi 5"
fi

# Check memory
MEMORY=$(free -h | grep "Mem:" | awk '{print $2}')
echo "💾 Available RAM: $MEMORY"

# Check SSD mount
echo "💿 Checking storage..."
if lsblk | grep -q "sda"; then
    echo "✅ SSD detected"
    df -h / | grep -v "Filesystem"
else
    echo "⚠️ SSD not detected - using SD card"
fi

# Check temperature
echo "🌡️ Checking temperature..."
if [ -f "/sys/class/thermal/thermal_zone0/temp" ]; then
    TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
    TEMP_C=$((TEMP / 1000))
    echo "🌡️ CPU Temperature: ${TEMP_C}°C"
    if [ $TEMP_C -lt 60 ]; then
        echo "✅ Temperature normal"
    else
        echo "⚠️ Temperature high - check cooling"
    fi
fi

# Check required packages
echo "📦 Checking essential packages..."
packages=("python3" "pip3" "nodejs" "npm" "git")
for pkg in "${packages[@]}"; do
    if command -v $pkg &> /dev/null; then
        echo "✅ $pkg installed"
    else
        echo "❌ $pkg missing"
    fi
done

# Check Python libraries
echo "🐍 Checking Python libraries..."
python3 -c "
import sys
libraries = ['flask', 'numpy', 'cv2', 'requests']
for lib in libraries:
    try:
        __import__(lib)
        print(f'✅ {lib} available')
    except ImportError:
        print(f'❌ {lib} missing')
"

# Check hardware interfaces
echo "🔌 Checking hardware interfaces..."
if [ -d "/sys/class/gpio" ]; then
    echo "✅ GPIO available"
else
    echo "❌ GPIO not available"
fi

if [ -c "/dev/spidev0.0" ]; then
    echo "✅ SPI enabled"
else
    echo "⚠️ SPI not enabled - run sudo raspi-config"
fi

if [ -c "/dev/i2c-1" ]; then
    echo "✅ I2C enabled"
else
    echo "⚠️ I2C not enabled - run sudo raspi-config"
fi

# Check camera
echo "📷 Checking camera..."
if command -v rpicam-still &> /dev/null; then
    echo "✅ Camera apps installed"
else
    echo "❌ Camera apps missing - install rpicam-apps"
fi

# Check audio
echo "🔊 Checking audio..."
if command -v aplay &> /dev/null; then
    echo "✅ Audio system available"
else
    echo "❌ Audio system missing"
fi

# Check network
echo "🌐 Checking network..."
if ping -c 1 8.8.8.8 &> /dev/null; then
    echo "✅ Internet connectivity"
else
    echo "⚠️ No internet connection"
fi

# Check local IP
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo "🏠 Local IP: $LOCAL_IP"

# Check if Dogzilla repository exists
echo "📁 Checking Dogzilla repository..."
if [ -d "/home/spencer/DogzillaRobot" ]; then
    echo "✅ DogzillaRobot repository found"
    
    if [ -f "/home/spencer/DogzillaRobot/dogzilla_core/mobile_api_server.py" ]; then
        echo "✅ Flask backend ready"
    else
        echo "❌ Flask backend missing"
    fi
    
    if [ -d "/home/spencer/DogzillaRobot/DogzillaVoiceControl" ]; then
        echo "✅ React frontend ready"
    else
        echo "❌ React frontend missing"
    fi
else
    echo "❌ DogzillaRobot repository not found"
fi

echo ""
echo "🐕🦖 Setup verification complete!"
echo "Next steps:"
echo "1. If any items show ❌, address them first"
echo "2. Run: python3 /home/spencer/DogzillaRobot/dogzilla_core/test_hardware.py"
echo "3. Start services when ready!"