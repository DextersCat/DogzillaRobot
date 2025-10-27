# 🐕🦖 Dogzilla Deployment Guide

## Quick Start (When Dogzilla Arrives!)

### 1. Install Dependencies
```bash
cd /home/spencer/DogzillaRobot/DogzillaVoiceControl
npm install
```

### 2. Start Dogzilla System
```bash
# Terminal 1: Start React Interface (port 5010)
cd /home/spencer/DogzillaRobot/DogzillaVoiceControl
npm run dev

# Terminal 2: Start Flask API (port 5011)
cd /home/spencer/DogzillaRobot/dogzilla_core
python mobile_api_server.py
```

### 3. Access Dogzilla Interface
- **Primary Interface**: http://192.168.1.4:5010/
- **API Server**: http://192.168.1.4:5011/
- **Camera Stream**: http://192.168.1.4:9010/mjpg

## Port Configuration

### Dogzilla Ports (Different from Astra)
- React Interface: 5010 (vs Astra's 5000)
- Flask API: 5011 (vs Astra's 5001)
- Camera Stream: 9010 (vs Astra's 9000)
- Patch API: 5012 (vs Astra's 5002)

### Benefits of Different Ports
- ✅ Run both Astra and Dogzilla simultaneously
- ✅ No port conflicts between robots
- ✅ Easy A/B testing and comparison
- ✅ Independent development environments

## Voice System Integration

### Wake Words
- Change from "Computer" to "Dogzilla"
- Update voice recognition patterns
- Add kaiju-themed responses

### Voice Personality
- Replace calm computer voice with monster growls
- Add threatening sound effects
- Implement aggressive response patterns

## UI Customization ToDo

### Theme Changes
1. **Colors**: Purple/red/black kaiju theme
2. **Icons**: Monster-themed replacing Star Trek
3. **Animations**: Aggressive vs smooth
4. **Sounds**: Roars vs beeps

### Branding Updates
1. Replace "Astra" with "Dogzilla" throughout interface
2. Update logo and favicon
3. Add kaiju animations and effects
4. Implement pack behavior modes

## Hardware Differences

### Expected Dogzilla Features
- Enhanced mobility (dog-like movement)
- Advanced camera system
- Larger battery capacity
- More aggressive sound system
- Additional sensors

### Calibration Required
1. **Movement Parameters**: Adjust for Dogzilla chassis
2. **Sensor Positioning**: Recalibrate distance sensors  
3. **Camera Angles**: Update look up/down coordinates
4. **Audio Levels**: Tune for Dogzilla's speaker system

## Testing Plan

### Phase 1: Basic Connectivity
- [ ] Flask API responds on port 5011
- [ ] React interface loads on port 5010
- [ ] API endpoints return test data
- [ ] Emergency stop functionality

### Phase 2: Hardware Integration
- [ ] Servo movement controls
- [ ] Camera feed operational
- [ ] Sensor data readings
- [ ] Audio/TTS system

### Phase 3: Advanced Features
- [ ] Voice recognition tuning
- [ ] Gesture calibration
- [ ] Autonomous behaviors
- [ ] Pack coordination

## Development Notes

### Inherited from Astra (WORKING ✅)
- Complete React TypeScript interface
- Express proxy server with fallbacks
- Flask API with all endpoints
- Voice command processing
- Emergency safety systems
- Real-time sensor monitoring
- Camera integration framework

### Dogzilla Adaptations Required
- Port configuration (DONE ✅)
- Branding updates (TODO 📝)
- Voice personality (TODO 📝)
- Hardware calibration (PENDING ⏳)
- Kaiju UI theme (TODO 📝)

## Repository Status
- ✅ DogzillaVoiceControl React interface ready
- ✅ dogzilla_core Flask backend configured
- ✅ Port conflicts resolved
- ✅ Git repository initialized
- ⏳ Awaiting Dogzilla hardware for testing

## Commands for Spencer

### Start Dogzilla Development
```bash
cd /home/spencer/DogzillaRobot/DogzillaVoiceControl
npm run dev  # React on 5010
```

### Start Dogzilla API
```bash
cd /home/spencer/DogzillaRobot/dogzilla_core  
python mobile_api_server.py  # Flask on 5011
```

### Check Both Systems
```bash
# Astra (should still work)
curl http://192.168.1.4:5000/
curl http://192.168.1.4:5001/

# Dogzilla (ready for hardware)
curl http://192.168.1.4:5010/
curl http://192.168.1.4:5011/
```

---

**Ready for Dogzilla arrival! 🐕🦖**
*All systems prepared for hardware integration*