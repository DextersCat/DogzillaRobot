# 🐕🦖 DOGZILLA S2 COMPLETE SETUP GUIDE
**Hardware Arrival: 27 October 2025**

## 📦 Hardware Inventory Checklist
- [ ] **Raspberry Pi 5 (16GB RAM)** - Main brain
- [ ] **Raspberry Pi 5 Active Cooler** - Thermal management  
- [ ] **Raspberry Pi 5 512GB SSD Kit** - High-speed storage
- [ ] **Dogzilla S2 Robot Kit** - Chassis and servos
- [ ] **MicroSD Card** (if not using SSD for initial setup)
- [ ] **Power Supply** (USB-C for Pi 5)
- [ ] **HDMI Cable** (for initial setup)
- [ ] **USB Keyboard/Mouse** (for initial setup)

## 🎯 **PHASE 1: HARDWARE ASSEMBLY (30-45 minutes)**

### Step 1.1: Raspberry Pi 5 Preparation
```bash
# Priority Order:
1. Install Active Cooler on Raspberry Pi 5
2. Connect 512GB SSD to Pi 5 via USB 3.0
3. Prepare microSD for initial boot (if needed)
4. Test Pi 5 boot with monitor/keyboard
```

### Step 1.2: Dogzilla S2 Chassis Assembly
```bash
# Follow SunFounder documentation:
1. Assemble main chassis frame
2. Install servo motors (12x servos for quadruped)
3. Connect servo control board
4. Mount Raspberry Pi 5 on chassis
5. Connect Pi 5 to servo control board
6. Install camera module (if included)
7. Connect power distribution
```

### Step 1.3: Initial Power Test
```bash
# Verify all connections:
1. Pi 5 boots successfully
2. Servo control board powered
3. No loose connections
4. Active cooler functioning
```

## 🔧 **PHASE 2: SOFTWARE FOUNDATION (45-60 minutes)**

### Step 2.1: Raspberry Pi OS Setup
```bash
# Flash latest Raspberry Pi OS to SSD
sudo rpi-imager
# Select: Raspberry Pi OS (64-bit) Desktop
# Target: 512GB SSD
# Enable SSH, WiFi, username: spencer

# First boot checklist:
1. Connect to WiFi: Your home network
2. Update system: sudo apt update && sudo apt upgrade -y
3. Enable SSH: sudo systemctl enable ssh
4. Install Git: sudo apt install git -y
5. Configure timezone: sudo raspi-config
```

### Step 2.2: Essential Dependencies
```bash
# Python and development tools
sudo apt install -y python3-pip python3-venv nodejs npm
sudo apt install -y build-essential cmake pkg-config
sudo apt install -y libjpeg-dev libtiff5-dev libpng-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev
sudo apt install -y libgtk-3-dev libcanberra-gtk3-dev
sudo apt install -y libxvidcore-dev libx264-dev libgtk-3-dev
sudo apt install -y libopenexr-dev libatlas-base-dev python3-dev

# Audio system
sudo apt install -y alsa-utils pulseaudio espeak espeak-data
sudo apt install -y portaudio19-dev python3-pyaudio

# Camera support
sudo apt install -y rpicam-apps
```

### Step 2.3: Hardware-Specific Libraries
```bash
# Install SunFounder libraries
pip3 install sunfounder-robot-hat
pip3 install picrawler

# Install additional robot libraries
pip3 install opencv-python numpy
pip3 install flask requests
pip3 install picovoice porcupine
pip3 install piper-tts
```

## 🚀 **PHASE 3: DOGZILLA SOFTWARE DEPLOYMENT (30 minutes)**

### Step 3.1: Clone Dogzilla Repository
```bash
# Navigate to home directory
cd /home/spencer

# Clone the ready-made repository
git clone https://github.com/Dexterscat/DogzillaRobot.git
cd DogzillaRobot

# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # We'll create this
```

### Step 3.2: Install React Dependencies
```bash
# Install frontend dependencies
cd DogzillaVoiceControl
npm install

# Verify build works
npm run build
```

### Step 3.3: Hardware Configuration
```bash
# Enable necessary interfaces
sudo raspi-config
# Enable: Camera, SPI, I2C, GPIO

# Test servo control
cd /home/spencer/DogzillaRobot/dogzilla_core
python3 -c "
from picrawler import Picrawler
dog = Picrawler()
print('Dogzilla hardware initialized!')
dog.do_step('stand', 50)
print('Stand test complete!')
"
```

## 🎮 **PHASE 4: SYSTEM INTEGRATION & TESTING (45 minutes)**

### Step 4.1: Basic Movement Tests
```bash
# Test individual components
cd /home/spencer/DogzillaRobot/dogzilla_core

# 1. Test servo control
python3 test_servos.py

# 2. Test camera
python3 test_camera.py

# 3. Test audio output
espeak "Dogzilla is online"

# 4. Test sensors
python3 test_sensors.py
```

### Step 4.2: Start Dogzilla Services
```bash
# Terminal 1: Start Flask API (port 5011)
cd /home/spencer/DogzillaRobot/dogzilla_core
python3 mobile_api_server.py

# Terminal 2: Start React Interface (port 5010)
cd /home/spencer/DogzillaRobot/DogzillaVoiceControl
npm run dev

# Access interface at: http://192.168.1.4:5010/
```

### Step 4.3: Voice System Integration
```bash
# Configure wake word for "Dogzilla"
# Edit wake word configuration
cd /home/spencer/DogzillaRobot/dogzilla_core
cp keywords/computer.ppn keywords/dogzilla.ppn  # Temporarily use computer wake word

# Test voice recognition
python3 test_voice.py
```

## 🔍 **PHASE 5: CALIBRATION & OPTIMIZATION (30 minutes)**

### Step 5.1: Movement Calibration
```bash
# Fine-tune servo positions
1. Test stand position: [45, 45, -50] for all legs
2. Verify walk gait patterns
3. Adjust speed parameters
4. Test emergency stop function
```

### Step 5.2: Camera Setup
```bash
# Position camera for optimal view
1. Test camera feed: http://192.168.1.4:9010/mjpg
2. Adjust camera angle
3. Test photo capture
4. Verify streaming performance
```

### Step 5.3: Audio Calibration
```bash
# Test audio input/output
1. Microphone sensitivity
2. Speaker volume levels
3. Wake word detection range
4. Text-to-speech clarity
```

## 🎯 **PHASE 6: PERSONALITY DEVELOPMENT (Optional - Day 2)**

### Step 6.1: Kaiju Voice Personality
```bash
# Implement monster responses
1. Change TTS voice to deeper tone
2. Add "ROAR" sound effects
3. Aggressive movement patterns
4. Threatening gesture poses
```

### Step 6.2: UI Theme Updates
```bash
# Update React interface
1. Dark kaiju color scheme
2. Monster-themed icons
3. Aggressive animations
4. "Dogzilla Mode" branding
```

## 🚨 **TROUBLESHOOTING GUIDE**

### Common Issues & Solutions

#### 🔴 **Pi 5 Won't Boot**
```bash
# Check:
1. Proper power supply (USB-C, 5V 5A)
2. SSD properly connected
3. Boot from SSD enabled in config
4. Active cooler connected properly
```

#### 🔴 **Servos Not Responding**
```bash
# Check:
1. Servo power supply adequate
2. Control board connections
3. GPIO permissions: sudo usermod -a -G gpio spencer
4. SPI/I2C enabled in raspi-config
```

#### 🔴 **Camera Not Working**
```bash
# Check:
1. Camera enabled: sudo raspi-config
2. Ribbon cable connections
3. Camera permissions
4. rpicam-apps installed
```

#### 🔴 **Network Issues**
```bash
# Check:
1. WiFi credentials correct
2. SSH enabled
3. Firewall settings
4. Network interface up
```

## 📊 **SUCCESS CRITERIA CHECKLIST**

### ✅ **Hardware Integration Complete**
- [ ] Pi 5 boots from 512GB SSD
- [ ] Active cooler functioning (check temps)
- [ ] All 12 servos responding
- [ ] Camera feed working
- [ ] Audio input/output functional

### ✅ **Software Integration Complete**
- [ ] DogzillaVoiceControl UI accessible: http://192.168.1.4:5010/
- [ ] Flask API responding: http://192.168.1.4:5011/
- [ ] Basic movements: stand, sit, walk
- [ ] Emergency stop working
- [ ] Voice commands responding

### ✅ **System Performance**
- [ ] No overheating (Pi 5 temps < 60°C)
- [ ] Smooth movement execution
- [ ] Responsive web interface
- [ ] Stable voice recognition
- [ ] Reliable camera stream

## 🎊 **CELEBRATION MILESTONES**

### 🥳 **First Boot Success**
```bash
echo "🐕🦖 Dogzilla Pi 5 is ALIVE!"
```

### 🥳 **First Movement**
```bash
echo "🦵 Dogzilla takes first steps!"
```

### 🥳 **First Voice Command**
```bash
echo "🗣️ Dogzilla responds to voice!"
```

### 🥳 **Full Integration**
```bash
echo "🚀 Dogzilla S2 is FULLY OPERATIONAL!"
```

## 🔄 **PARALLEL ASTRA OPERATION**

### Ensuring No Conflicts
```bash
# Astra continues on:
- React Interface: http://192.168.1.4:5000/
- Flask API: http://192.168.1.4:5001/

# Dogzilla operates on:
- React Interface: http://192.168.1.4:5010/
- Flask API: http://192.168.1.4:5011/

# Both can run simultaneously!
```

## 📞 **SUPPORT CONTACTS**

### Technical Issues
- **SunFounder Support**: For hardware-specific problems
- **Raspberry Pi Foundation**: For Pi 5 specific issues
- **GitHub Repository**: https://github.com/Dexterscat/DogzillaRobot

### Emergency Procedures
```bash
# If something goes wrong:
1. Emergency stop: Press red button in UI
2. Power cycle: Unplug and reconnect power
3. Safe mode: Boot with keyboard attached
4. Recovery: Flash fresh OS to backup SD card
```

---

## 🎯 **ESTIMATED TIMELINE**

| Phase | Duration | Description |
|-------|----------|-------------|
| **Phase 1** | 30-45 min | Hardware assembly |
| **Phase 2** | 45-60 min | Software foundation |
| **Phase 3** | 30 min | Dogzilla deployment |
| **Phase 4** | 45 min | Integration & testing |
| **Phase 5** | 30 min | Calibration |
| **Phase 6** | Optional | Personality development |

**Total Setup Time**: ~3-4 hours for full integration

## 🏁 **FINAL SUCCESS STATE**

When complete, you'll have:
- 🤖 **Astra**: Running and working (original system)
- 🐕🦖 **Dogzilla**: Fully operational (new system)  
- 🌐 **Dual Interfaces**: Both accessible via web
- 🎮 **Independent Control**: No interference between robots
- 🚀 **Future Ready**: Foundation for advanced behaviors

**Dogzilla will be ready to ROAR! 🐕🦖**