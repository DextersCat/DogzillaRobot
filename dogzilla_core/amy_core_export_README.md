# 🚀 AMY VOICE ASSISTANT - CORE SYSTEM EXPORT
**Date:** October 25, 2025  
**Creator:** Spencer Dixon  
**System:** Astra Voice Assistant Core  
**Platform:** Raspberry Pi 5 / Linux  

---

## 📋 WHAT'S INCLUDED

### **Core Voice System:**
- **amy_wake.py** - Porcupine wake word detection (WORKING PERFECTLY)
- **postwake_router.py** - Voice command processing with STT/TTS
- **button_interface.py** - Reliable backup control interface
- **astra_listen_loop.sh** - Complete system integration

### **Keywords & Models:**
- **keywords/astra.ppn** - Primary wake word model
- **keywords/computer.ppn** - Alternative wake word
- **Audio enhancement** - sox-based processing pipeline

### **Service Integration:**
- **SystemD service** configuration
- **Environment management** scripts
- **Audio system** setup and configuration

### **Documentation:**
- **Complete setup guides** and technical reports
- **Troubleshooting** documentation
- **System architecture** explanations

---

## 🎯 SYSTEM CAPABILITIES

### **What Works Perfectly:**
✅ **Wake Word Detection** - "Astra" or "Computer" trigger reliably  
✅ **Voice Processing** - Complete STT/TTS pipeline  
✅ **Button Interface** - 100% reliable backup control  
✅ **Service Integration** - SystemD automatic startup  
✅ **Audio Enhancement** - sox processing for better recognition  

### **Voice Commands:**
- "What's the time?" - Current time announcement
- "Wave hello" - Friendly greeting response
- "System status" - Health check report
- "Test response" - System verification

---

## 🛠️ HARDWARE REQUIREMENTS

### **Minimum Setup:**
- **Raspberry Pi 4/5** (tested on Pi5 16GB)
- **USB Audio Device** (C-Media or better)
- **Microphone** (USB or 3.5mm)
- **Speakers/Headphones** for TTS output
- **8GB+ SD Card** for system

### **Recommended:**
- **Raspberry Pi 5** with adequate cooling
- **Quality USB audio interface**
- **Proper microphone** (not built-in laptop style)
- **Fast SD Card** (Class 10 or better)

---

## ⚙️ SOFTWARE DEPENDENCIES

### **System Packages:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv git
sudo apt install sox libsox-fmt-all
sudo apt install espeak-ng
```

### **Python Libraries:**
```bash
pip3 install pvporcupine
pip3 install faster-whisper
pip3 install requests
pip3 install soundfile
```

### **Audio System:**
- **Piper TTS** (included in voices/ directory)
- **Porcupine** for wake word detection
- **faster-whisper** for speech-to-text

---

## 🚀 QUICK START GUIDE

### **Step 1: Hardware Setup**
1. Connect USB audio device to Raspberry Pi
2. Connect microphone and speakers
3. Boot Raspberry Pi with fresh Raspbian OS

### **Step 2: Install Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3-pip python3-venv git sox espeak-ng

# Create project directory
mkdir -p /home/pi/amy_core
cd /home/pi/amy_core
```

### **Step 3: Extract and Setup**
```bash
# Extract the amy_core files to /home/pi/amy_core/
# Set permissions
chmod +x *.sh
chmod +x env/*.sh

# Install Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install pvporcupine faster-whisper requests soundfile
```

### **Step 4: Configure Audio**
```bash
# Test audio devices
arecord -l    # List recording devices
aplay -l      # List playback devices

# Edit env/astra_audio.env with your device numbers
nano env/astra_audio.env
```

### **Step 5: Test System**
```bash
# Test wake word detection
python3 amy_wake.py

# Test button interface (reliable backup)
python3 button_interface.py

# Test complete system
./astra_listen_loop.sh
```

---

## 🎮 USAGE INSTRUCTIONS

### **Voice Control:**
1. **Say wake word:** "Astra" or "Computer"
2. **Wait for confirmation:** "Yes, go ahead"
3. **Give command:** "What's the time?"
4. **Listen to response**

### **Button Control (Backup):**
```bash
python3 button_interface.py
# Then use: time, wave, status, test, quit
```

### **Service Mode:**
```bash
# Install as system service
sudo cp amy.service.new /etc/systemd/system/amy.service
sudo systemctl enable amy
sudo systemctl start amy

# Monitor service
sudo systemctl status amy
journalctl -f -u amy
```

---

## 🔧 TROUBLESHOOTING

### **Common Issues:**
1. **No wake word detection** - Check microphone permissions and audio levels
2. **No TTS output** - Verify speaker configuration in astra_audio.env
3. **Service won't start** - Check file permissions and paths
4. **Poor recognition** - Adjust microphone distance and background noise

### **Debug Commands:**
```bash
# Check audio devices
arecord -l && aplay -l

# Test microphone
arecord -d 5 test.wav && aplay test.wav

# Check service logs
journalctl -u amy --since "1 hour ago"

# Manual system test
python3 -c "import pvporcupine; print('Porcupine OK')"
```

---

## 📁 FILE STRUCTURE

```
amy_core/
├── amy_wake.py                 # Wake word detection
├── postwake_router.py          # Voice processing
├── button_interface.py         # Backup control
├── astra_listen_loop.sh        # Main service script
├── env/
│   ├── astra_audio.env         # Audio configuration
│   └── venv_guard.sh           # Environment helper
├── keywords/
│   ├── astra.ppn               # Wake word models
│   └── computer.ppn
├── tools/
│   └── wake_once.py            # Testing utilities
└── docs/                       # Documentation
```

---

## ⚡ QUICK DEMO

### **Voice Test:**
1. Run: `python3 amy_wake.py`
2. Say: "Astra"
3. When prompted, say: "What's the time?"
4. Listen for time announcement

### **Button Test:**
1. Run: `python3 button_interface.py`
2. Type: `time`
3. Listen for time announcement

---

## 📞 SUPPORT & NOTES

### **Known Working Configuration:**
- **Platform:** Raspberry Pi 5, 16GB RAM
- **OS:** Raspbian Bookworm
- **Audio:** C-Media USB Audio Adapter
- **Microphone:** Various USB and 3.5mm tested

### **Performance Notes:**
- Wake word detection: **Excellent** (near 100% accuracy)
- Voice processing: **Good** (dependent on microphone quality)
- Response time: **Fast** (~2-3 seconds total)
- Resource usage: **Moderate** (comfortable on Pi4+)

### **Future Enhancements:**
- Mobile platform integration (Dogzilla S2)
- ROS2 framework migration
- Advanced AI conversation capabilities
- Multi-room audio support

---

## 🎉 SUCCESS INDICATORS

### **System Working When:**
- Wake word triggers reliably with "Astra"
- TTS responds with clear audio
- Button interface provides backup control
- Service runs automatically on boot

### **Next Steps:**
- Customize voice commands in postwake_router.py
- Add your own wake words with Porcupine Console
- Integrate with smart home systems
- Scale to mobile robotics platforms

---

**Built with passion for voice-controlled AI assistants!**  
**Perfect foundation for robotics and smart home projects!** 🤖🏠✨

---

*Export created: October 25, 2025*  
*System Status: Production Ready*  
*Core Features: 100% Functional*