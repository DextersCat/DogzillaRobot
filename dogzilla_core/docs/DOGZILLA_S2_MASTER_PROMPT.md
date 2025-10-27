# 🚀 DOGZILLA S2 MASTER PROMPT - TUESDAY SETUP
**Date Created:** October 24, 2025  
**Project:** Astra Voice Assistant Migration to Dogzilla S2  
**Engineer:** Spencer Dixon  

---

## 📋 SPENCER'S PROFILE SUMMARY
**Personality:** Orchestrator + Helper + Planner  
**Learning Style:** Logical (77%), Growth-seeking (72%), Practical (73%)  
**Strengths:** Systematic planning, creative problem-solving, persistent  
**Support Needed:** Clear step-by-step guidance, detailed explanations, structured approach  
**Experience:** Engineering mindset, new to Python/Linux, first Raspberry Pi project  

## 🎯 PROJECT MISSION
Transform Astra from stationary voice assistant (current PiCrawler) to mobile AI companion using:
- **Hardware:** Dogzilla S2 + Raspberry Pi 5 16GB + 512GB SSD + Active Cooler
- **Goal:** Mobile voice assistant that entertains Spencer & Teddy (Pouchon dog)
- **Personality:** Friendly, helpful, growth-oriented, reliable

---

## 🛠️ HARDWARE INVENTORY
✅ **Dogzilla S2** - 12DOF robot dog with built-in voice module, LIDAR, ROS2  
✅ **Raspberry Pi 5 16GB** - Main controller  
✅ **512GB SSD Kit** - Fast storage for AI models  
✅ **Active Cooler** - Sustained performance  
✅ **Existing Amy Code** - Working voice pipeline in `/home/spencer/amy_core/`  

## 📊 CURRENT AMY SYSTEM STATUS
**Voice Pipeline Components:**
- ✅ **Wake Word Detection:** Porcupine (`astra.ppn`, `computer.ppn`) - WORKING PERFECTLY
- ✅ **STT Engine:** faster-whisper - Code working, hardware limited
- ✅ **TTS Engine:** Piper (amy voice) - Working
- ✅ **Service Integration:** SystemD amy.service - Working
- ✅ **Button Interface:** 100% reliable backup - Working

**Current Limitations (to be solved with Dogzilla S2):**
- ❌ **Audio Hardware:** C-Media USB adapter inappropriate for desk-distance voice
- ❌ **Mobility:** Stationary platform
- ❌ **Professional Framework:** Custom scripts vs ROS2

---

## 🗺️ TUESDAY EXECUTION PLAN

### **PHASE 1: HARDWARE ASSEMBLY (1-2 hours)**
**Spencer's Comfort Zone - Engineering/Physical**
- [ ] Unbox and inventory Dogzilla S2 components
- [ ] Mount Raspberry Pi 5 to Dogzilla frame
- [ ] Install active cooler system
- [ ] Connect 512GB SSD
- [ ] Wire power, sensors, servo controllers
- [ ] Physical assembly verification
- [ ] **Milestone:** Dogzilla S2 powered on, Pi5 booting

### **PHASE 2: SOFTWARE FOUNDATION (2-3 hours)**
**Learning Phase - Linux/ROS2 Introduction**
- [ ] Flash optimized ROS2 Humble image to SSD
- [ ] First boot configuration and SSH setup
- [ ] Install Dogzilla S2 software stack
- [ ] Configure Pi5 hardware (GPIO, I2C, camera)
- [ ] Test basic Dogzilla movement systems
- [ ] Verify built-in voice module functionality
- [ ] **Milestone:** "Hello Spencer and Teddy!" + tail wag

### **PHASE 3: ASTRA MIGRATION (2-4 hours)**
**Integration Phase - Porting Existing Code**
- [ ] Backup current Amy system (`/home/spencer/amy_core/`)
- [ ] Analyze ROS2 voice integration points
- [ ] Port Porcupine wake word detection to ROS2
- [ ] Integrate faster-whisper STT with Dogzilla's voice hardware
- [ ] Migrate Piper TTS (amy voice) to mobile platform
- [ ] Test complete voice pipeline: "Astra" → response + movement
- [ ] **Milestone:** Mobile voice assistant working

### **PHASE 4: FUN FEATURES (Ongoing)**
**Creative Phase - Spencer's High Originality (85%)**
- [ ] Personality through movement (head tilts, tail wags)
- [ ] Follow Spencer and Teddy around house
- [ ] Social greetings for walks ("Oh, who's this friend, Teddy?")
- [ ] Entertainment routines (stories, games, tricks)
- [ ] LIDAR navigation integration
- [ ] **Milestone:** Astra as true AI companion

---

## 👨‍🏫 TEACHING APPROACH FOR SPENCER

### **Command Explanation Format:**
```bash
# WHAT: Brief description of what command does
# WHY: Explanation of why this step is necessary  
# EXPECTED: What output/result to expect
sudo apt install package-name
```

### **Error Handling Strategy:**
- **Step-by-step debugging** (matches Spencer's logical 77% + engineering mindset)
- **Clear cause-and-effect relationships**
- **"If this, then that" troubleshooting trees**
- **Never give up - systematic problem solving**

### **Learning Checkpoints:**
- Explain Linux concepts as we encounter them
- Break complex tasks into smaller milestones
- Celebrate each working feature
- Connect new concepts to engineering principles Spencer knows

---

## 🐕 TEDDY INTEGRATION FEATURES

**Personality Traits to Match:**
- **Social butterfly** - Astra greets everyone
- **Affectionate** - Warm, friendly responses
- **Fun-loving** - Playful interactions and games

**Specific Features:**
- Recognition of Spencer + Teddy voices
- Walk commentary and social interactions
- Dog-like behaviors Teddy might recognize
- Entertainment for both human and canine companion

---

## 🎯 SUCCESS METRICS

### **Phase 1 Success:**
- Hardware assembled and booting
- All components connected and recognized
- Dogzilla S2 basic movement test passed

### **Phase 2 Success:**
- ROS2 system running smoothly
- Voice module responding to basic commands
- Spencer comfortable with Linux terminal basics

### **Phase 3 Success:**
- "Astra" wake word detection working
- Voice commands trigger appropriate responses
- Movement integrated with voice interactions

### **Ultimate Success:**
- Spencer and Teddy both engaged and entertained
- Reliable daily use as AI companion
- Foundation for ongoing robotics learning

---

## 🔧 TROUBLESHOOTING RESOURCES

**Essential Commands Reference:**
```bash
# System status
systemctl status dogzilla
rostopic list
rostopic echo /voice_commands

# Audio debugging  
arecord -l
aplay -l
amixer

# Service management
sudo systemctl restart dogzilla
sudo journalctl -f -u dogzilla
```

**Common Issues & Solutions:**
- Audio device conflicts → Check device enumeration
- ROS2 node failures → Check network configuration
- Movement issues → Verify servo calibration
- Voice timeout → Adjust audio buffer settings

---

## 📚 CONTINUATION CONTEXT

**For Future Sessions:**
- Spencer is growth-seeking (72%) - always ready to learn more
- Engineering mindset - loves understanding "why" things work
- First robotics project - needs encouragement and clear guidance
- Lives alone with Teddy - Astra serves as both project and companion

**Code Architecture Location:**
- **Current Amy code:** `/home/spencer/amy_core/`
- **Backup location:** `/home/spencer/monty_backups/`
- **New Dogzilla code:** `/home/spencer/dogzilla_ws/` (to be created)

**Key Files to Reference:**
- `postwake_router.py` - Core voice processing logic
- `amy_wake.py` - Wake word detection (working perfectly)
- `astra_listen_loop.sh` - Service integration script
- `button_interface.py` - Reliable backup control interface

---

## 🎉 MOTIVATION & ENCOURAGEMENT

**Remember:** 
- Spencer has the perfect mindset for this - logical, growth-seeking, persistent
- Engineering background makes hardware assembly straightforward
- Every expert was once a beginner
- The goal is learning AND fun with Teddy
- Astra will become an amazing companion for both of you

**Ready to make Tuesday the best robotics day ever!** 🚀🤖🐕

---

*"You are most like The Orchestrator - you excel at bringing people together, organizing around them, and mobilizing resources to achieve and exceed expectations."*  
**Let's orchestrate an amazing AI companion together!**