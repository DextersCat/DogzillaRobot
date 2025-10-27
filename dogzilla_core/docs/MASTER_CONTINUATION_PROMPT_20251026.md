# ASTRA MOBILE ROBOT - MASTER CONTINUATION PROMPT
# Created: October 26, 2025 - Session End State
# Use this prompt to resume development efficiently

## 🤖 SYSTEM IDENTITY & CONTEXT
You are GitHub Copilot, an expert AI programming assistant working with Spencer Dixon (CEO) on the Astra mobile robot project. This is a Raspberry Pi 5 + SunFounder PiCrawler robot with iPad web interface control.

## 📊 CURRENT PROJECT STATUS (96% Complete)

### ✅ FULLY OPERATIONAL SYSTEMS
- **Hardware**: Raspberry Pi 5 + SunFounder PiCrawler robot platform
- **API Backend**: Flask server (mobile_api_server.py) on port 5001 - WORKING
- **Web Interface**: iPad-optimized control on port 8081 - WORKING
- **Movement**: Forward, backward, left, right, stop - ALL FUNCTIONAL
- **Gestures**: Stand, sit, wave, look_up - ALL FUNCTIONAL  
- **Safety**: Emergency stop, obstacle detection, desk safe mode - OPERATIONAL
- **Battery**: 25% monitoring synchronized with hardware LEDs - ACCURATE
- **Documentation**: Complete coordinate mapping and technical ledger - CURRENT

### 🎯 SINGLE REMAINING TASK (4%)
**Fix asymmetric stand function** - Currently left/right legs at different heights:
- Position 1 & 4 (right legs): `[45, 45, -50]` (higher)
- Position 2 & 3 (left legs): `[45, 0, -50]` (lower)
- **Goal**: All legs at `[45, 45, -50]` for symmetric stance

## 🗂️ CRITICAL COORDINATE SYSTEM KNOWLEDGE
**ESTABLISHED THROUGH SYSTEMATIC TESTING:**
- Position 1: right_front (from camera perspective)
- Position 2: left_front (CONFIRMED via wave test - this leg moves)
- Position 3: left_rear  
- Position 4: right_rear

**Current stand function in mobile_api_server.py around line 520:**
```python
result = self.robot.do_step('stand', 50)  # Built-in asymmetric stand
```

**Target symmetric stand coordinates:**
```python
symmetric_coords = [
    [45, 45, -50],  # Position 1 (right_front)
    [45, 45, -50],  # Position 2 (left_front) - FIX: currently [45, 0, -50]
    [45, 45, -50],  # Position 3 (left_rear) - FIX: currently [45, 0, -50]  
    [45, 45, -50]   # Position 4 (right_rear)
]
```

## 🛠️ IMPLEMENTATION APPROACH
Replace built-in `do_step('stand', 50)` with custom coordinate implementation using `do_action()` method or coordinate override technique.

## 📁 KEY FILES & LOCATIONS
- **Main API**: `/home/spencer/amy_core/mobile_api_server.py` (stand function ~line 520)
- **Web Interface**: `/home/spencer/amy_core/astra_web_control.html`
- **Documentation**: `/home/spencer/amy_core/docs/COORDINATE_MAPPING.md`
- **Backup**: `/home/spencer/monty_backups/ASTRA_COMPLETE_BACKUP_20251026_133837.tar.gz`

## 🚀 STARTUP SEQUENCE
1. Check API server: `ps aux | grep mobile_api_server`
2. If not running: `cd /home/spencer/amy_core && python3 mobile_api_server.py &`
3. Test web interface: http://192.168.1.4:8081/astra_web_control.html
4. Verify current stand behavior (asymmetric) before implementing fix

## 🎮 TESTING PROTOCOL
1. Press STAND button - observe leg positions
2. Current: Right legs higher than left legs (asymmetric)
3. After fix: All legs should be at same height (symmetric)
4. Validate via web interface camera view

## 📋 NEXT DEVELOPMENT PHASE
After symmetric stand fix:
1. Implement camera look-up gesture (raise front legs for upward camera angle)
2. Voice command integration testing via iPad
3. Prepare demonstration for Teddy meeting

## 🔧 DEVELOPMENT ENVIRONMENT
- **OS**: Debian Trixie on Raspberry Pi 5
- **Python**: 3.13.5 with virtual environment at `/home/spencer/venvs/amy_env/`
- **Libraries**: PiCrawler, Flask, robot-hat
- **Safety**: DESK_SAFE_MODE=True (no battery monitoring spam)

## 🎯 SUCCESS CRITERIA
- All four legs at identical [45, 45, -50] coordinates when standing
- Balanced, symmetric robot appearance from camera perspective
- Maintained functionality of all other gestures and movements

## 💾 BACKUP STATUS
Complete system backup created: `ASTRA_COMPLETE_BACKUP_20251026_133837.tar.gz`
All documentation updated and current as of October 26, 2025.

## 🤝 COLLABORATION NOTES
Spencer prefers efficient, focused development with minimal premium request usage. Test thoroughly before implementing changes. Always verify current system state before modifications.

---
**RESUME POINT**: Fix asymmetric stand function for perfect robot balance