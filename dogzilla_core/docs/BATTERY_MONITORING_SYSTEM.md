# 🔋 ASTRA BATTERY MONITORING SYSTEM
**Date:** October 25, 2025  
**Purpose:** Prevent unexpected Raspberry Pi shutdown by monitoring battery levels  
**Hardware:** Robot HAT LED indicators + voltage monitoring  

---

## 🔍 BATTERY MONITORING RESEARCH FINDINGS

### **Robot HAT Battery Indicators:**
- **2 LEDs on:** > 7.6V (Good battery level)
- **1 LED on:** > 7.15V (Low battery warning)  
- **Both LEDs off:** < 7.15V (Critical - shutdown imminent)

### **Voltage Monitoring Available:**
- **Function:** `robot_hat.get_battery_voltage()`
- **Method:** ADC A4 channel with voltage divider
- **Formula:** `Battery voltage = ADC_value / 4095.0 * 3.3 * 3`
- **Range:** 6.0V - 8.4V input voltage

---

## 🚨 BATTERY ALERT SYSTEM DESIGN

### **Alert Levels:**
- **GOOD:** > 7.6V - Green status
- **WARNING:** 7.15V - 7.6V - Yellow alert  
- **CRITICAL:** < 7.15V - Red alert + emergency actions

### **Emergency Actions:**
1. **Voice Alert:** "Battery low, please plug in charger"
2. **Service Shutdown:** Graceful stop of non-essential services
3. **Status Logging:** Record battery level before shutdown
4. **LED Indication:** Use user LED for status blinking

---

## 📱 MOBILE APP INTEGRATION

### **Battery Status in App:**
```
┌─────────────────────────┐
│ 🤖 ASTRA CONTROL       │
├─────────────────────────┤
│ 🔋 Battery: 7.8V ●Good  │
│ 📍 Location: Living Room│
│ 🎤 Status: Listening    │
├─────────────────────────┤
│ [Voice Command Button]  │
└─────────────────────────┘
```

### **Alert Notifications:**
- **Push notifications** when battery drops to warning level
- **Visual indicators** in app interface
- **Automatic mode switching** to power-saving operations

---

## 🛠️ IMPLEMENTATION PLAN

### **Phase 1: Basic Monitoring**
```python
#!/usr/bin/env python3
# Battery monitoring for Astra
import robot_hat
import time
import subprocess

def get_battery_status():
    """Get current battery voltage and status"""
    voltage = robot_hat.get_battery_voltage()
    
    if voltage > 7.6:
        status = "GOOD"
        color = "green"
    elif voltage > 7.15:
        status = "WARNING" 
        color = "yellow"
    else:
        status = "CRITICAL"
        color = "red"
    
    return voltage, status, color

def battery_alert(voltage, status):
    """Voice alert for low battery"""
    if status == "WARNING":
        message = f"Battery level is {voltage:.1f} volts. Please consider charging soon."
    elif status == "CRITICAL":
        message = f"Critical battery level {voltage:.1f} volts! Please plug in charger immediately!"
    
    # Use existing TTS system
    subprocess.run(["espeak-ng", message])

def main():
    while True:
        voltage, status, color = get_battery_status()
        print(f"Battery: {voltage:.2f}V - {status}")
        
        if status in ["WARNING", "CRITICAL"]:
            battery_alert(voltage, status)
            
        if status == "CRITICAL":
            # Emergency shutdown sequence
            print("Initiating emergency power save mode...")
            subprocess.run(["sudo", "systemctl", "stop", "amy"])
            
        time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    main()
```

### **Phase 2: Integration with Amy Service**
```python
# Add to postwake_router.py
import robot_hat

def check_battery_before_response():
    """Check battery before energy-intensive operations"""
    voltage = robot_hat.get_battery_voltage()
    
    if voltage < 7.15:
        return "Battery critically low. Please charge me before we continue."
    elif voltage < 7.6:
        return f"Battery at {voltage:.1f} volts. I may need charging soon."
    
    return None  # Battery OK, proceed normally
```

### **Phase 3: Mobile App Integration**
```python
# Web API endpoint for mobile app
from flask import jsonify

@app.route('/battery')
def battery_status():
    voltage, status, color = get_battery_status()
    return jsonify({
        'voltage': round(voltage, 2),
        'status': status,
        'color': color,
        'led_count': 2 if voltage > 7.6 else (1 if voltage > 7.15 else 0)
    })
```

---

## 🎯 MOBILE APP ENHANCED FEATURES

### **Battery-Aware Commands:**
- **Power-saving mode** when battery < 7.6V
- **Essential commands only** when battery < 7.15V  
- **Automatic sleep** after periods of inactivity
- **Charging reminders** via push notifications

### **Visual Battery Indicator:**
```css
.battery-indicator {
    width: 50px;
    height: 25px;
    border: 2px solid #333;
    border-radius: 3px;
}

.battery-good { background: linear-gradient(90deg, #4CAF50 80%, #fff 80%); }
.battery-warning { background: linear-gradient(90deg, #FFC107 50%, #fff 50%); }
.battery-critical { background: linear-gradient(90deg, #F44336 20%, #fff 20%); }
```

### **Smart Power Management:**
- **Reduce servo movements** when battery low
- **Lower audio volume** to save power
- **Disable LED effects** in power-save mode
- **Cache responses** to reduce processing

---

## 🔧 INSTALLATION STEPS

### **Step 1: Add Battery Monitor Service**
```bash
# Create battery monitoring service
sudo nano /etc/systemd/system/astra-battery.service

[Unit]
Description=Astra Battery Monitor
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/spencer/amy_core/battery_monitor.py
Restart=always
User=spencer

[Install]
WantedBy=multi-user.target
```

### **Step 2: Enable Service**
```bash
sudo systemctl enable astra-battery.service
sudo systemctl start astra-battery.service
```

### **Step 3: Test Battery Reading**
```bash
cd /home/spencer/amy_core
python3 -c "import robot_hat; print(f'Battery: {robot_hat.get_battery_voltage():.2f}V')"
```

---

## 📊 BATTERY LEVEL MAPPING

### **Voltage to Percentage Estimation:**
```python
def voltage_to_percentage(voltage):
    """Convert voltage to approximate percentage"""
    # Based on typical 2S Li-ion battery (6.0V - 8.4V range)
    min_voltage = 6.0   # 0%
    max_voltage = 8.4   # 100%
    
    percentage = ((voltage - min_voltage) / (max_voltage - min_voltage)) * 100
    return max(0, min(100, percentage))

# Examples:
# 8.4V = 100%
# 7.6V = 67% (LED threshold)
# 7.15V = 48% (Warning threshold)  
# 6.0V = 0%
```

### **Smart Alerts:**
- **80%+:** "Battery excellent"
- **50-80%:** "Battery good"  
- **30-50%:** "Battery moderate - charging recommended"
- **15-30%:** "Battery low - please charge soon"
- **<15%:** "Critical battery level - emergency charging needed!"

---

## 🎉 BENEFITS FOR DOGZILLA S2

### **Enhanced Mobile Platform:**
- **Predictive charging** - Know when to charge before missions
- **Route planning** - Factor battery level into movement decisions
- **Safe operation** - Never get stuck with dead battery mid-task
- **Performance optimization** - Adjust capabilities based on power

### **Mobile App Advantages:**
- **Remote monitoring** - Check battery from anywhere
- **Charging notifications** - Get alerts on your phone
- **Power-aware control** - App adjusts features based on battery
- **Usage analytics** - Track power consumption patterns

---

**Your overnight insight was BRILLIANT!** 🧠✨ Battery monitoring is absolutely critical for mobile robotics, and the Robot HAT provides perfect hardware support for this!

**Ready to implement this battery monitoring system?** 🔋🤖