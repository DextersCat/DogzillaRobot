#!/usr/bin/env python3
"""
Astra Battery Monitor
Monitors Robot HAT battery voltage and provides alerts
Date: October 25, 2025
"""

import sys
import os
import time
import subprocess
import logging

# Add robot_hat to path
sys.path.append('/home/spencer/robot-hat')

try:
    import robot_hat
    from robot_hat import Pin
except ImportError:
    print("Error: robot_hat library not found")
    print("Please install: cd /home/spencer/robot-hat && sudo python3 setup.py install")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/spencer/logs/battery_monitor.log'),
        logging.StreamHandler()
    ]
)

class AstraBatteryMonitor:
    def __init__(self):
        self.voltage_history = []
        self.last_alert_time = 0
        self.alert_interval = 300  # 5 minutes between alerts
        
        # Battery thresholds (from Robot HAT documentation)
        self.CRITICAL_VOLTAGE = 7.15
        self.WARNING_VOLTAGE = 7.6
        self.GOOD_VOLTAGE = 7.6
        
        # Initialize user LED for status indication
        try:
            self.status_led = Pin("LED")
        except:
            self.status_led = None
            logging.warning("Could not initialize status LED")
    
    def get_battery_voltage(self):
        """Get current battery voltage"""
        try:
            voltage = robot_hat.get_battery_voltage()
            logging.info(f"Battery voltage: {voltage:.2f}V")
            return voltage
        except Exception as e:
            logging.error(f"Error reading battery voltage: {e}")
            return None
    
    def get_battery_status(self, voltage):
        """Determine battery status from voltage"""
        if voltage is None:
            return "UNKNOWN", "gray", 0
        
        if voltage > self.GOOD_VOLTAGE:
            return "GOOD", "green", 2
        elif voltage > self.CRITICAL_VOLTAGE:
            return "WARNING", "yellow", 1
        else:
            return "CRITICAL", "red", 0
    
    def voltage_to_percentage(self, voltage):
        """Convert voltage to approximate percentage"""
        if voltage is None:
            return 0
        
        # Based on 2S Li-ion battery (6.0V - 8.4V range)
        min_voltage = 6.0   # 0%
        max_voltage = 8.4   # 100%
        
        percentage = ((voltage - min_voltage) / (max_voltage - min_voltage)) * 100
        return max(0, min(100, percentage))
    
    def speak_alert(self, message):
        """Use Astra's voice system for battery alerts"""
        try:
            # Try to use Amy's TTS system first
            if os.path.exists('/home/spencer/amy_core/postwake_router.py'):
                # Use Amy's TTS if available
                cmd = f'cd /home/spencer/amy_core && python3 -c "from postwake_router import speak_response; speak_response(\'{message}\')"'
                subprocess.run(cmd, shell=True, timeout=10)
            else:
                # Fallback to espeak-ng
                subprocess.run(['espeak-ng', message], timeout=10)
            
            logging.info(f"Battery alert spoken: {message}")
        except Exception as e:
            logging.error(f"Error speaking alert: {e}")
    
    def blink_status_led(self, pattern):
        """Blink status LED in different patterns"""
        if not self.status_led:
            return
        
        try:
            if pattern == "warning":
                # Slow blink for warning
                for _ in range(3):
                    self.status_led.on()
                    time.sleep(0.5)
                    self.status_led.off()
                    time.sleep(0.5)
            elif pattern == "critical":
                # Fast blink for critical
                for _ in range(6):
                    self.status_led.on()
                    time.sleep(0.2)
                    self.status_led.off()
                    time.sleep(0.2)
        except Exception as e:
            logging.error(f"Error blinking LED: {e}")
    
    def handle_battery_alert(self, voltage, status):
        """Handle battery alerts based on status"""
        current_time = time.time()
        
        # Check if enough time has passed since last alert
        if current_time - self.last_alert_time < self.alert_interval:
            return
        
        percentage = self.voltage_to_percentage(voltage)
        
        if status == "WARNING":
            message = f"Battery level is {percentage:.0f} percent at {voltage:.1f} volts. Please consider charging soon."
            self.speak_alert(message)
            self.blink_status_led("warning")
            self.last_alert_time = current_time
            
        elif status == "CRITICAL":
            message = f"Critical battery level! Only {percentage:.0f} percent remaining at {voltage:.1f} volts. Please plug in charger immediately!"
            self.speak_alert(message)
            self.blink_status_led("critical")
            self.last_alert_time = current_time
            
            # Log critical event
            logging.critical(f"CRITICAL BATTERY: {voltage:.2f}V ({percentage:.0f}%)")
            
            # Consider emergency actions
            self.emergency_power_save()
    
    def emergency_power_save(self):
        """Emergency power saving actions"""
        try:
            logging.warning("Initiating emergency power save mode")
            
            # Stop non-essential services (but keep monitoring)
            # subprocess.run(['sudo', 'systemctl', 'stop', 'amy'], timeout=30)
            
            # Reduce system performance
            subprocess.run(['sudo', 'cpufreq-set', '-g', 'powersave'], timeout=10)
            
            # Log emergency action
            logging.critical("Emergency power save mode activated")
            
        except Exception as e:
            logging.error(f"Error in emergency power save: {e}")
    
    def log_battery_data(self, voltage, status, percentage):
        """Log battery data for analysis"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Keep voltage history for trend analysis
        self.voltage_history.append({
            'timestamp': timestamp,
            'voltage': voltage,
            'percentage': percentage,
            'status': status
        })
        
        # Keep only last 100 readings
        if len(self.voltage_history) > 100:
            self.voltage_history.pop(0)
        
        # Log to file
        logging.info(f"Battery: {voltage:.2f}V ({percentage:.0f}%) - {status}")
    
    def get_status_for_api(self):
        """Get battery status formatted for mobile app API"""
        voltage = self.get_battery_voltage()
        status, color, led_count = self.get_battery_status(voltage)
        percentage = self.voltage_to_percentage(voltage)
        
        return {
            'voltage': round(voltage, 2) if voltage else 0,
            'percentage': round(percentage, 1),
            'status': status,
            'color': color,
            'led_count': led_count,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def monitor_loop(self, check_interval=60):
        """Main monitoring loop"""
        logging.info("Astra Battery Monitor started")
        
        while True:
            try:
                voltage = self.get_battery_voltage()
                status, color, led_count = self.get_battery_status(voltage)
                percentage = self.voltage_to_percentage(voltage)
                
                # Log battery data
                self.log_battery_data(voltage, status, percentage)
                
                # Handle alerts if needed
                if status in ["WARNING", "CRITICAL"]:
                    self.handle_battery_alert(voltage, status)
                
                # Sleep until next check
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logging.info("Battery monitor stopped by user")
                break
            except Exception as e:
                logging.error(f"Error in monitoring loop: {e}")
                time.sleep(check_interval)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Astra Battery Monitor')
    parser.add_argument('--interval', type=int, default=60, 
                        help='Check interval in seconds (default: 60)')
    parser.add_argument('--status', action='store_true',
                        help='Show current battery status and exit')
    
    args = parser.parse_args()
    
    monitor = AstraBatteryMonitor()
    
    if args.status:
        # Just show current status
        status_data = monitor.get_status_for_api()
        print(f"Battery Status:")
        print(f"  Voltage: {status_data['voltage']}V")
        print(f"  Percentage: {status_data['percentage']}%")
        print(f"  Status: {status_data['status']}")
        print(f"  LED Count: {status_data['led_count']}")
    else:
        # Start monitoring loop
        monitor.monitor_loop(args.interval)

if __name__ == "__main__":
    main()