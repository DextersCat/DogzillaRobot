# 💻 LAPTOP VS CODE SETUP - REMOTE ASTRA CONTROL
**Date Created:** October 24, 2025  
**Purpose:** Duplicate VS Code environment on laptop for remote Amy/Astra control  
**Amy IP Address:** 192.168.1.4  
**Connection:** SSH with VS Code Remote-SSH extension  

---

## 🎯 SETUP OBJECTIVES
- **Remote Control:** Connect laptop to Amy/Astra via SSH
- **Code Editing:** Full VS Code environment mirroring desktop setup
- **Testing Freedom:** Control Astra from anywhere in house (perfect for movement testing)
- **Development:** Continue coding on Astra while mobile

---

## 📋 LAPTOP REQUIREMENTS CHECKLIST

### **Software to Install on Laptop:**
- [ ] **Visual Studio Code** (latest version)
- [ ] **Git** (for version control)
- [ ] **SSH Client** (usually pre-installed on Windows 10+/Mac/Linux)
- [ ] **Python** (for local development/testing)

### **VS Code Extensions to Install:**
- [ ] **Remote - SSH** (ms-vscode-remote.remote-ssh)
- [ ] **Remote - SSH: Editing Configuration Files** (ms-vscode-remote.remote-ssh-edit)
- [ ] **Python** (ms-python.python)
- [ ] **Pylance** (ms-python.vscode-pylance)
- [ ] **Git Extension Pack** (donjayamanne.git-extension-pack)
- [ ] **Markdown Preview Enhanced** (shd101wyy.markdown-preview-enhanced)

---

## 🔧 STEP-BY-STEP SETUP GUIDE

### **Step 1: Install Visual Studio Code on Laptop**
1. **Download VS Code:** https://code.visualstudio.com/
2. **Install with default settings**
3. **Launch VS Code**

### **Step 2: Install Remote-SSH Extension**
1. **Open Extensions panel** (Ctrl+Shift+X)
2. **Search for:** "Remote - SSH"
3. **Install:** Microsoft's Remote - SSH extension
4. **Also install:** Remote - SSH: Editing Configuration Files

### **Step 3: Configure SSH Connection to Amy**
1. **Open Command Palette** (Ctrl+Shift+P)
2. **Type:** "Remote-SSH: Open SSH Configuration File"
3. **Select:** User configuration file (usually `~/.ssh/config`)
4. **Add this configuration:**

```ssh
Host amy
    HostName 192.168.1.4
    User spencer
    Port 22
    ForwardAgent yes
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host amy.local
    HostName amy.local
    User spencer
    Port 22
    ForwardAgent yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### **Step 4: Set Up SSH Key Authentication (Recommended)**
**On your laptop, run these commands:**

```bash
# Generate SSH key pair (if you don't have one)
ssh-keygen -t rsa -b 4096 -C "laptop-to-amy"

# Copy public key to Amy (replace with your laptop's username)
ssh-copy-id spencer@192.168.1.4

# Test connection
ssh spencer@192.168.1.4
```

### **Step 5: Connect VS Code to Amy**
1. **Open Command Palette** (Ctrl+Shift+P)
2. **Type:** "Remote-SSH: Connect to Host"
3. **Select:** "amy" from the list
4. **VS Code will install VS Code Server on Amy automatically**
5. **Select platform:** Linux
6. **Wait for connection to establish**

### **Step 6: Open Amy's Workspace**
1. **Once connected, click:** File → Open Folder
2. **Navigate to:** `/home/spencer/amy_core`
3. **Click:** OK
4. **VS Code now shows Amy's file system**

---

## 🚀 TESTING YOUR SETUP

### **Test 1: Basic Connection**
```bash
# In VS Code terminal (connected to Amy)
pwd                    # Should show: /home/spencer/amy_core
ls -la                # Should show Amy's files
systemctl status amy   # Check Astra service status
```

### **Test 2: Run Amy Commands**
```bash
# Test voice pipeline components
cd /home/spencer/amy_core
source env/venv_guard.sh
python3 amy_wake.py    # Should show Porcupine loading
```

### **Test 3: Control Interface**
```bash
# Test button interface for reliable control
python3 button_interface.py
# Try commands: time, wave, status, test
```

---

## 📁 RECOMMENDED WORKSPACE STRUCTURE

**On your laptop, create a local folder structure:**
```
C:/AstraProjects/          (Windows)
~/AstraProjects/           (Mac/Linux)
├── amy_backup/            # Local backup copies
├── dogzilla_prep/         # Tuesday preparation files
├── documentation/         # Project notes and guides
└── development/           # Local testing and development
```

---

## 🔄 SYNCHRONIZATION STRATEGY

### **Option 1: Direct Remote Editing (Recommended)**
- **Edit files directly on Amy via VS Code Remote-SSH**
- **All changes happen in real-time on Amy**
- **No sync issues, always up-to-date**

### **Option 2: Git-Based Workflow**
```bash
# On Amy (set up git repository)
cd /home/spencer/amy_core
git init
git add .
git commit -m "Initial Amy core backup"

# Create backup branch before major changes
git checkout -b pre-dogzilla-backup
```

### **Option 3: Periodic Backups**
```bash
# From laptop, backup Amy's files
rsync -avz spencer@192.168.1.4:/home/spencer/amy_core/ ./amy_backup/
```

---

## 🎮 REMOTE CONTROL FEATURES

### **What You Can Do Remotely:**
- **Edit all Amy/Astra code** via VS Code
- **Run terminal commands** on Amy
- **Monitor service status** (systemctl status amy)
- **Test voice commands** via button interface
- **View logs** in real-time
- **Prepare for Dogzilla S2 migration**

### **Perfect for Movement Testing:**
- **Sit downstairs with laptop**
- **Send movement commands to Astra upstairs**
- **Monitor via button interface or voice commands**
- **Debug issues without being tied to desktop**

---

## 🔧 TROUBLESHOOTING COMMON ISSUES

### **Connection Problems:**
```bash
# Test basic SSH connection
ssh spencer@192.168.1.4

# Check Amy's IP hasn't changed
ping amy.local

# Restart SSH service on Amy if needed
sudo systemctl restart ssh
```

### **VS Code Remote Issues:**
1. **Reload window:** Ctrl+Shift+P → "Developer: Reload Window"
2. **Reconnect:** Ctrl+Shift+P → "Remote-SSH: Connect to Host"
3. **Clear VS Code Server:** Delete `~/.vscode-server` on Amy and reconnect

### **Authentication Issues:**
```bash
# Re-copy SSH key
ssh-copy-id spencer@192.168.1.4

# Check SSH key permissions on laptop
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

---

## 📱 MOBILE DEVELOPMENT WORKFLOW

### **Typical Session:**
1. **Connect laptop to Amy** via VS Code Remote-SSH
2. **Open amy_core workspace**
3. **Edit code** (postwake_router.py, button_interface.py, etc.)
4. **Test changes** via terminal
5. **Control Astra remotely** using button interface
6. **Monitor logs** and debug

### **For Movement Testing:**
1. **Position yourself downstairs** with laptop
2. **Connect to Amy upstairs**
3. **Run movement commands** via code
4. **Observe Astra's behavior** from different room
5. **Adjust code** based on observations

---

## 🎯 PREPARING FOR DOGZILLA S2

### **Remote Preparation Tasks:**
- **Review current Amy code** from comfort of laptop
- **Test existing functionality** remotely
- **Plan migration strategy** with mobility
- **Document current system** before Tuesday
- **Backup everything** to laptop for safety

### **Tuesday Advantages:**
- **Two development environments:** Desktop for heavy work, laptop for testing
- **Remote monitoring:** Watch Dogzilla S2 from anywhere in house
- **Mobility:** Move around while robot moves around
- **Backup access:** Always have laptop connection if desktop issues

---

## ✅ SETUP COMPLETION CHECKLIST

### **Laptop Setup:**
- [ ] VS Code installed and configured
- [ ] Remote-SSH extension installed
- [ ] SSH key authentication working
- [ ] Connection to Amy established
- [ ] Amy workspace opened successfully

### **Testing Complete:**
- [ ] Can edit Amy files remotely
- [ ] Terminal commands work on Amy
- [ ] Button interface accessible
- [ ] Service status monitoring working
- [ ] File synchronization method chosen

### **Ready for Use:**
- [ ] Local project folders created
- [ ] Backup strategy implemented
- [ ] Troubleshooting guide accessible
- [ ] Remote development workflow tested

---

## 🎉 SUCCESS!

**You now have:**
- **Full remote access** to Amy/Astra from laptop
- **Complete development environment** anywhere in house
- **Perfect setup** for Dogzilla S2 testing Tuesday
- **Mobile coding** capability for robotics projects

**Perfect for testing Astra with movement - you can be downstairs controlling the robot upstairs, or move around the house while Astra moves around too!**

---

*"Code from anywhere, control from everywhere - your laptop is now Astra's remote control center!"* 🚀💻🤖