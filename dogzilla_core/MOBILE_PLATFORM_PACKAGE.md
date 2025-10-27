# Amy Mobile Platform Package
## Complete Camera and LIDAR Integration for PiCrawler

**Package Date**: October 25, 2025  
**Status**: Desk testing completed ✅ - Ready for mobile deployment  
**Next Phase**: Downstairs laptop testing + Dogzilla S2 migration (Tuesday)

---

## 📋 System Status Summary

### ✅ Verified Working Components
- **Camera System**: OV5647 camera module with web streaming
- **Ultrasonic Sensor**: HC-SR04 connected to D2/D3 pins
- **Face Detection**: Real-time detection with vilib
- **TTS System**: Voice announcements via espeak
- **Web Stream**: Live camera feed at `http://192.168.1.4:9000/mjpg`

### 📊 Desk Test Results
- **Camera Resolution**: 640x480 (scalable to 1280x720)
- **Ultrasonic Range**: 16-240cm (tested, desk environment: ~68cm avg)
- **Face Detection**: Active and responsive
- **Web Stream**: Stable at 30 FPS
- **System Integration**: All components working together

---

## 📁 Package Contents

### Core Integration Scripts
1. **`mobile_platform_integration.py`** - Complete mobile platform with autonomous features
2. **`fixed_desk_test.py`** - Comprehensive testing script (desk-verified ✅)
3. **`simple_camera_test.py`** - Basic camera functionality test
4. **`desk_ultrasonic_test.py`** - Ultrasonic sensor testing with desk interpretation

### Test Results
- Camera web stream: `http://192.168.1.4:9000/mjpg` ✅
- Ultrasonic readings: 16-240cm range ✅  
- Face detection: Active monitoring ✅
- TTS announcements: Working ✅

---

## 🔌 Hardware Connections

### Camera Module (OV5647)
- **Connection**: CSI ribbon cable to Raspberry Pi 5 camera port
- **Status**: ✅ Connected and functional
- **Test Command**: `rpicam-hello --list-cameras`

### Ultrasonic Sensor (HC-SR04)
- **Trig Pin**: D2 (GPIO27) on Robot HAT
- **Echo Pin**: D3 (GPIO22) on Robot HAT  
- **Power**: VCC → 5V, GND → GND
- **Status**: ✅ Connected and functional
- **Test Range**: 16-240cm verified

### PiCrawler Base
- **Platform**: SunFounder PiCrawler with Robot HAT
- **Movement**: Ready for autonomous navigation
- **Power**: Battery monitoring system operational (8.27V, 94.5%)

---

## 🚀 Quick Start Guide

### 1. Verify Hardware
```bash
# Test camera
rpicam-hello --list-cameras

# Check video devices
ls /dev/video*
```

### 2. Run Comprehensive Test
```bash
cd /home/spencer/amy_core
python3 fixed_desk_test.py
```

### 3. Start Mobile Platform
```bash
cd /home/spencer/amy_core  
python3 mobile_platform_integration.py
```

### 4. Access Web Stream
- Open browser: `http://192.168.1.4:9000/mjpg`
- Live camera feed with face detection overlay

---

## 📱 Mobile App Integration Ready

### Available APIs
- **Camera Stream**: HTTP MJPEG at port 9000
- **Sensor Data**: Real-time distance and face detection
- **Photo Capture**: Triggered by events or manual command
- **Voice Feedback**: TTS announcements for status updates
- **Battery Monitoring**: Voltage and percentage status

### iPhone App Architecture (Ready to Implement)
```javascript
// Camera feed integration
const cameraURL = 'http://pi_ip:9000/mjpg';

// Sensor data endpoint (to be implemented)
const sensorAPI = 'http://pi_ip:5000/sensors';

// Voice command endpoint (existing Amy integration)
const voiceAPI = 'http://pi_ip:5000/voice';
```

---

## 🔧 Troubleshooting

### Camera Issues
- **No camera detected**: Check CSI cable connection
- **Web stream fails**: Restart with `python3 simple_camera_test.py`
- **Permission errors**: Run with `sudo` if needed

### Ultrasonic Sensor Issues  
- **No readings**: Verify D2/D3 connections and 5V power
- **Inconsistent readings**: Normal in desk environment
- **Timeout errors**: Check wiring, sensor positioning

### System Integration
- **Face detection not working**: Ensure vilib is properly installed
- **TTS silent**: Check espeak installation and audio output
- **Web stream port conflict**: Kill existing processes on port 9000

---

## 📅 Next Steps for Tuesday (Dogzilla S2 Migration)

### Hardware Preparation
1. **Camera Mount**: Secure camera module to Dogzilla S2 chassis
2. **Sensor Position**: Mount ultrasonic sensor for forward-looking detection  
3. **Cable Management**: Organize connections for mobile operation
4. **Power Validation**: Verify battery capacity for extended operation

### Software Deployment
1. **Transfer Package**: Copy all scripts to Dogzilla S2 system
2. **Test Mobile Platform**: Run `mobile_platform_integration.py`
3. **Calibrate Sensors**: Adjust thresholds for floor-based operation
4. **Web Stream Setup**: Configure for laptop remote access

### Testing Protocol
1. **Stationary Test**: Verify all systems before movement
2. **Slow Movement**: Test camera stability during motion
3. **Obstacle Avoidance**: Validate ultrasonic sensor performance
4. **Remote Control**: Test laptop-based monitoring and control

---

## 🎯 Success Metrics

### Desk Testing (Completed ✅)
- [x] Camera web stream active
- [x] Ultrasonic sensor responsive  
- [x] Face detection functional
- [x] TTS announcements working
- [x] System integration stable

### Mobile Testing (Tuesday Goals)
- [ ] Stable camera during movement
- [ ] Effective obstacle avoidance  
- [ ] Laptop remote access working
- [ ] Battery performance validated
- [ ] iPhone app development ready

---

## 📞 Support Information

### Documentation Links
- **PiCrawler**: https://docs.sunfounder.com/projects/pi-crawler/en/latest/
- **Robot HAT**: https://docs.sunfounder.com/projects/robot-hat-v4/en/latest/  
- **vilib Camera**: https://docs.sunfounder.com/projects/vilib-rpi/en/latest/

### Key Code Locations
- **Amy Core**: `/home/spencer/amy_core/`
- **PiCrawler Examples**: `/home/spencer/picrawler/examples/`
- **vilib Examples**: `/home/spencer/vilib/examples/`
- **Robot HAT Docs**: `/home/spencer/robot-hat/docs/`

---

**Package Ready for Mobile Deployment** 🚀  
**Next: Downstairs laptop testing + Tuesday Dogzilla S2 integration**