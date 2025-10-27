# Camera and LIDAR Hardware Installation Guide
## Quick Reference for Dogzilla S2 Migration (Tuesday)

---

## 📷 Camera Module Installation

### OV5647 Camera Module
**Connection Type**: CSI Ribbon Cable  
**Status**: ✅ Currently working on Pi 5

### Installation Steps
1. **Power Down** the Raspberry Pi completely
2. **Locate CSI Port** on Raspberry Pi 5 (between HDMI ports)
3. **Release Connector**: Gently pull up the plastic clip
4. **Insert Ribbon Cable**: 
   - Blue side faces away from Pi
   - Contacts face the board
   - Push firmly until seated
5. **Secure Connector**: Press down plastic clip
6. **Power Up** and test with: `rpicam-hello --list-cameras`

### Mounting on Dogzilla S2
- **Position**: Front-facing for navigation
- **Height**: Eye-level for optimal face detection
- **Protection**: Consider protective housing for mobile use
- **Cable Management**: Secure ribbon cable to prevent damage

### Verification Commands
```bash
# List available cameras
rpicam-hello --list-cameras

# Test photo capture
rpicam-still -o test.jpg --width 1280 --height 720

# Test web stream
python3 /home/spencer/amy_core/simple_camera_test.py
```

---

## 📡 Ultrasonic Sensor Installation

### HC-SR04 Ultrasonic Sensor
**Connection Type**: 4-wire to Robot HAT  
**Status**: ✅ Currently working on D2/D3

### Pin Connections
| Sensor Pin | Robot HAT Pin | GPIO | Color Suggestion |
|------------|---------------|------|------------------|
| VCC        | 5V            | -    | Red              |
| GND        | GND           | -    | Black            |
| Trig       | D2            | GPIO27 | Yellow         |
| Echo       | D3            | GPIO22 | Green          |

### Installation Steps
1. **Prepare Wires**: Cut 4 jumper wires to appropriate length
2. **Connect VCC**: Red wire from sensor VCC to Robot HAT 5V pin
3. **Connect GND**: Black wire from sensor GND to Robot HAT GND pin  
4. **Connect Trig**: Yellow wire from sensor Trig to Robot HAT D2
5. **Connect Echo**: Green wire from sensor Echo to Robot HAT D3
6. **Secure Connections**: Ensure all connections are tight
7. **Test**: Run ultrasonic test script

### Mounting on Dogzilla S2
- **Position**: Front-facing for obstacle detection
- **Height**: 10-20cm above ground level
- **Angle**: Slightly downward (10-15°) for floor detection
- **Protection**: Waterproof housing if outdoor use planned
- **Range**: Effective 2cm - 400cm (optimal 10cm - 200cm)

### Verification Commands
```bash
# Test ultrasonic sensor
python3 /home/spencer/amy_core/desk_ultrasonic_test.py

# Integrated test
python3 /home/spencer/amy_core/fixed_desk_test.py
```

---

## 🔧 Robot HAT Pin Reference

### Digital Pins (D0-D3)
```
D0 = GPIO17  (Available)
D1 = GPIO4   (Available)  
D2 = GPIO27  (ULTRASONIC TRIG) ← USED
D3 = GPIO22  (ULTRASONIC ECHO) ← USED
```

### Power Pins
```
5V   = 5V Supply     (ULTRASONIC VCC) ← USED
3.3V = 3.3V Supply   (Available)
GND  = Ground        (ULTRASONIC GND) ← USED
```

### Additional Available Pins
```
PWM: P0-P11 (12 channels available)
ADC: A0-A3  (4 analog inputs available)
I2C: SDA/SCL (For future sensors)
SPI: MOSI/MISO/SCLK (For future expansion)
```

---

## 🚀 Installation Checklist

### Pre-Installation
- [ ] Raspberry Pi powered down
- [ ] All cables and components ready
- [ ] Workspace clear and organized
- [ ] Anti-static precautions taken

### Camera Installation
- [ ] CSI connector opened
- [ ] Ribbon cable inserted correctly (blue side out)
- [ ] Connector secured
- [ ] Cable routed safely
- [ ] Camera mounted securely

### Ultrasonic Sensor Installation  
- [ ] VCC connected to 5V (red wire)
- [ ] GND connected to GND (black wire)
- [ ] Trig connected to D2 (yellow wire)
- [ ] Echo connected to D3 (green wire)
- [ ] All connections secured
- [ ] Sensor mounted facing forward

### Testing
- [ ] Power up system
- [ ] Camera detection: `rpicam-hello --list-cameras`
- [ ] Camera test: `python3 simple_camera_test.py`
- [ ] Ultrasonic test: `python3 desk_ultrasonic_test.py`
- [ ] Integrated test: `python3 fixed_desk_test.py`
- [ ] Web stream accessible: `http://pi_ip:9000/mjpg`

---

## ⚠️ Important Notes

### Camera Module
- **Fragile**: Handle ribbon cable carefully
- **Static Sensitive**: Use anti-static precautions
- **Orientation**: Blue side of cable faces away from Pi
- **Focus**: Some modules have adjustable focus ring

### Ultrasonic Sensor
- **Power Requirements**: Needs 5V (not 3.3V)
- **Timing Critical**: Ensure stable power supply
- **Range Limitations**: Dead zone under 2cm
- **Interference**: Can be affected by soft surfaces

### General
- **Battery Impact**: Camera and sensor will increase power consumption
- **Heat**: Monitor Pi temperature during extended operation
- **Backup**: Keep current working configuration before changes
- **Documentation**: Update system documentation after installation

---

## 🔍 Troubleshooting

### Camera Issues
| Problem | Solution |
|---------|----------|
| No camera detected | Check ribbon cable connection |
| Poor image quality | Adjust focus ring if available |
| Web stream fails | Verify vilib installation |
| Permission errors | Run tests with sudo |

### Ultrasonic Issues
| Problem | Solution |
|---------|----------|
| No distance readings | Check 5V power connection |
| Erratic readings | Verify D2/D3 pin connections |
| Timeout errors | Check for loose wires |
| Interference | Reposition sensor, avoid soft surfaces |

### System Integration
| Problem | Solution |
|---------|----------|
| High CPU usage | Lower camera resolution |
| Battery drain | Optimize sampling rates |
| Conflicts | Stop other camera applications |
| Network issues | Check IP address and port availability |

---

## 📅 Tuesday Migration Plan

### Phase 1: Hardware Transfer (30 min)
1. Document current Pi 5 setup
2. Power down and carefully remove components
3. Install camera and sensor on Dogzilla S2
4. Verify all connections

### Phase 2: Software Setup (30 min)
1. Copy mobile platform package to Dogzilla S2
2. Install dependencies if needed
3. Run hardware verification tests
4. Configure network settings

### Phase 3: Mobile Testing (60 min)
1. Stationary system test
2. Slow movement validation
3. Obstacle avoidance testing
4. Remote laptop access setup

### Phase 4: Integration (30 min)
1. Combine with existing Amy voice system
2. Test battery monitoring integration
3. Validate mobile app readiness
4. Document final configuration

**Total Estimated Time**: 2.5 hours  
**Success Criteria**: All systems operational on mobile platform

---

**Installation Guide Complete** ✅  
**Ready for Tuesday Dogzilla S2 Migration** 🚀