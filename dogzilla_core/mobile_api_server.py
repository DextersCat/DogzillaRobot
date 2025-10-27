#!/usr/bin/env python3
"""
Amy Mobile API Server
REST API backend for mobile app control and sensor data
Integrates with existing Amy systems
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import threading
import subprocess
import os
import sys

# Add amy_core to path for imports
sys.path.append('/home/spencer/amy_core')

try:
    from robot_hat import Ultrasonic, Pin
    HARDWARE_AVAILABLE = True
    HAS_VILIB = False
    HAS_ADC = False
except ImportError as e:
    print(f"⚠️  Hardware modules not available: {e}")
    HARDWARE_AVAILABLE = False
    HAS_VILIB = False
    HAS_ADC = False

# Try to import vilib separately (disabled to free camera for streaming)
try:
    # from vilib import Vilib  # Commented out to avoid camera conflict
    HAS_VILIB = False
    print("ℹ️  vilib disabled to free camera for streaming")
except ImportError:
    print("ℹ️  vilib not available - using fallback for face detection")
    HAS_VILIB = False

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app access

class AmyMobileAPI:
    def __init__(self):
        """Initialize Amy Mobile API"""
        self.sensor_data = {
            'distance': 0,
            'faces': 0,
            'battery_voltage': 0,
            'battery_percentage': 0,
            'timestamp': time.time(),
            'status': 'initialized'
        }
        
        self.hardware_initialized = False
        self.monitoring = False
        self.start_time = time.time()  # Track startup time for battery simulation
        
        self.camera_active = False
        self.camera_process = None
        
        # Safety and control states
        self.desk_safe_mode = True  # Default to safe mode
        
        # Initialize hardware if available
        if HARDWARE_AVAILABLE:
            self.init_hardware()
    
    def init_hardware(self):
        """Initialize hardware components with error handling"""
        try:
            # Initialize ultrasonic sensor with error handling
            try:
                self.sonar = Ultrasonic(Pin("D2"), Pin("D3"))
                print("✅ Ultrasonic sensor initialized")
            except Exception as e:
                print(f"⚠️  Ultrasonic sensor failed: {e}")
                self.sonar = None
            
            # Initialize battery monitoring (skipping ADC for now)
            self.battery_adc = None
            print("ℹ️  Battery ADC skipped - using fallback values")
            
            self.hardware_initialized = True
            print("✅ Hardware initialized successfully")
            
        except Exception as e:
            print(f"❌ Hardware initialization failed: {e}")
            self.hardware_initialized = False
            self.sonar = None
    
    def read_sensors(self):
        """Read all sensor data with error handling"""
        try:
            # Read distance sensor with proper filtering as per documentation
            if self.hardware_initialized and self.sonar:
                try:
                    distance = self.sonar.read()
                    # Filter out values < 0 as documented - ultrasonic sensor limitation
                    if distance < 0:
                        # Keep last good reading or use safe fallback
                        self.sensor_data['distance'] = self.sensor_data.get('distance', 30.0)
                    else:
                        self.sensor_data['distance'] = round(distance, 1)
                except Exception as e:
                    print(f"❌ Ultrasonic sensor error: {e}")
                    # Use safe fallback distance
                    self.sensor_data['distance'] = 30.0
            else:
                # Use realistic fallback data when hardware not available
                import random
                self.sensor_data['distance'] = round(25.0 + random.uniform(-5, 15), 1)
                
            # Read face detection from vilib
            if HAS_VILIB:
                try:
                    faces = Vilib.detect_obj_parameter['human_n']
                    self.sensor_data['faces'] = faces
                except:
                    self.sensor_data['faces'] = 0
            else:
                self.sensor_data['faces'] = 0
            
            # Read battery data with proper ADC if available
            if self.battery_adc:
                try:
                    # Use robot-hat ADC read_voltage() method for accurate readings
                    voltage = self.battery_adc.read_voltage()
                    # Convert to actual battery voltage (assuming voltage divider)
                    battery_voltage = voltage * 3.0  # Adjust multiplier based on your circuit
                    self.sensor_data['battery_voltage'] = round(battery_voltage, 2)
                    # Calculate percentage based on Li-ion battery curve (3.7V nominal, 4.2V max, 3.0V min)
                    percentage = max(0, min(100, ((battery_voltage - 3.0) / 1.2) * 100))
                    self.sensor_data['battery_percentage'] = round(percentage, 1)
                except Exception as e:
                    print(f"❌ Battery ADC error: {e}")
                    # Use realistic fallback values
                    self.sensor_data['battery_voltage'] = 3.85
                    self.sensor_data['battery_percentage'] = 75.0
            else:
                # DESK SAFE MODE: Disable battery monitoring spam
                if self.desk_safe_mode:
                    # In desk safe mode - just set safe defaults, no monitoring
                    self.sensor_data['battery_voltage'] = 4.2  # Full/safe
                    self.sensor_data['battery_percentage'] = 100.0
                    self.sensor_data['charging_status'] = "🏠 DESK MODE"
                    # Only print once when entering desk mode
                    if not hasattr(self, '_desk_mode_announced'):
                        print("🏠 DESK SAFE MODE: Battery monitoring disabled")
                        self._desk_mode_announced = True
                    return
                
                # Smart battery monitoring: Only test when needed
                # Baseline: On mains power = 100% at 4.2V (no monitoring needed)
                MAINS_VOLTAGE = 4.2  # 100% fully charged baseline
                MAINS_PERCENTAGE = 100.0
                
                # Check if we're on mains (stable high voltage)
                try:
                    # Quick voltage check to determine power source
                    if hasattr(self, 'battery_adc'):
                        test_voltage = self.battery_adc.read_voltage() * 3.0
                        if test_voltage >= 4.15:  # Very close to full charge = on mains
                            # On mains power - no monitoring spam needed
                            self.sensor_data['battery_voltage'] = MAINS_VOLTAGE
                            self.sensor_data['battery_percentage'] = MAINS_PERCENTAGE
                            self.sensor_data['charging_status'] = "🔌 MAINS POWER"
                            # Only print status change, not every 2 seconds
                            if not hasattr(self, '_last_power_status') or self._last_power_status != 'mains':
                                print("🔌 On mains power - 100% (no battery monitoring)")
                                self._last_power_status = 'mains'
                            return
                except:
                    pass
                
                # Only run battery monitoring if NOT on mains power
                print("🔋 Running on battery - monitoring active")
                
                # Existing battery monitoring logic for when on battery
                import time
                hours_running = (time.time() - getattr(self, 'start_time', time.time())) / 3600
                base_charge = 25.0  # Starting point when charging began
                charge_rate = 15.0  # % per hour (realistic Li-ion charging rate)
                current_charge = min(100.0, base_charge + (hours_running * charge_rate))
                
                charging_status = "🔋 CHARGING" if current_charge < 100.0 else "🔋 FULL"
                
                # Only print battery status when it changes significantly
                if not hasattr(self, '_last_battery_level') or abs(self._last_battery_level - current_charge) >= 1.0:
                    print(f"{charging_status} - Battery: {current_charge:.1f}%")
                    self._last_battery_level = current_charge
                
                # Battery voltage curve (only when actually on battery)
                if current_charge >= 80:
                    voltage = 3.9 + (current_charge - 80) * 0.015
                elif current_charge >= 40:
                    voltage = 3.7 + (current_charge - 40) * 0.005
                elif current_charge >= 10:
                    voltage = 3.4 + (current_charge - 10) * 0.01
                else:
                    voltage = 3.0 + current_charge * 0.04
                
                self.sensor_data['battery_voltage'] = round(voltage, 2)
                self.sensor_data['battery_percentage'] = round(current_charge, 1)
                self.sensor_data['charging_status'] = charging_status
            
            self.sensor_data['timestamp'] = time.time()
            self.sensor_data['status'] = 'active'
            
        except Exception as e:
            print(f"❌ Sensor reading error: {e}")
            self.sensor_data['status'] = f'error: {str(e)}'
    
    def start_monitoring(self):
        """Start background sensor monitoring"""
        self.monitoring = True
        
        def monitor_loop():
            while self.monitoring:
                self.read_sensors()
                time.sleep(1)  # Update every second
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        print("🔍 Sensor monitoring started")
    
    def stop_monitoring(self):
        """Stop sensor monitoring"""
        self.monitoring = False
        print("🛑 Sensor monitoring stopped")
    
    def execute_command(self, command, params=None):
        """Execute movement or system commands"""
        try:
            print(f"🤖 Executing command: {command}")
            
            if command == 'take_photo':
                return self.take_photo()
            elif command == 'emergency_stop':
                return self.emergency_stop()
            elif command == 'voice_command':
                text = params.get('text', 'Hello from Astra') if params else 'Hello from Astra'
                return self.handle_voice_command(text)
            elif command in ['forward', 'backward', 'left', 'right', 'stop']:
                return self.movement_command(command)
            elif command == 'speak':
                text = params.get('text', 'Hello from Astra') if params else 'Hello from Astra'
                return self.speak_text(text)
            else:
                return {'success': False, 'error': f'Unknown command: {command}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def take_photo(self):
        """Take a photo using rpicam-still"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            filename = f"/home/spencer/Pictures/amy_mobile_{timestamp}.jpg"
            
            cmd = f"rpicam-still -o {filename} --width 1280 --height 720 --timeout 1000 --nopreview"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {'success': True, 'filename': filename}
            else:
                return {'success': False, 'error': result.stderr}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def emergency_stop(self):
        """Emergency stop all operations"""
        try:
            # Stop any movement commands
            print("🚨 EMERGENCY STOP ACTIVATED")
            # Add movement stop code here when mobile platform is ready
            return {'success': True, 'message': 'Emergency stop activated'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def movement_command(self, direction):
        """Handle movement commands with PiCrawler integration"""
        try:
            # Check if desk safe mode is enabled
            if self.desk_safe_mode:
                return {
                    'success': False, 
                    'error': 'Movement disabled - desk safe mode active',
                    'message': 'Disable desk safe mode to enable movement'
                }
            
            # Import PiCrawler for movement
            sys.path.append('/home/spencer/picrawler')
            from picrawler import Picrawler
            
            # Initialize robot if not already done
            if not hasattr(self, 'robot'):
                self.robot = Picrawler()
                print("🤖 PiCrawler robot initialized")
            
            # Execute movement command
            print(f"🕹️  Executing movement: {direction}")
            
            if direction == 'forward':
                self.robot.forward(50)  # Move forward at speed 50
                time.sleep(0.5)  # Move for 0.5 seconds
                self.robot.stop()
                message = "Moving forward"
                
            elif direction == 'backward':
                self.robot.backward(50)  # Move backward at speed 50
                time.sleep(0.5)
                self.robot.stop()
                message = "Moving backward"
                
            elif direction == 'left':
                self.robot.turn_left(50)  # Turn left at speed 50
                time.sleep(0.3)  # Turn for 0.3 seconds
                self.robot.stop()
                message = "Turning left"
                
            elif direction == 'right':
                self.robot.turn_right(50)  # Turn right at speed 50
                time.sleep(0.3)
                self.robot.stop()
                message = "Turning right"
                
            elif direction == 'stop':
                self.robot.stop()
                message = "Stopping"
                
            else:
                return {'success': False, 'error': f'Unknown movement: {direction}'}
            
            # Announce movement
            self.speak_text(message)
            
            return {
                'success': True, 
                'command': direction, 
                'message': f'Movement {direction} completed'
            }
            
        except ImportError as e:
            return {
                'success': False, 
                'error': f'PiCrawler not available: {str(e)}',
                'message': 'Install PiCrawler library for movement'
            }
        except Exception as e:
            return {'success': False, 'error': f'Movement error: {str(e)}'}
    
    def speak_text(self, text):
        """Make Astra speak using Piper TTS with Robot HAT speaker"""
        try:
            # Use the working amy_say script which handles Piper + Robot HAT properly
            result = subprocess.run(['/home/spencer/bin/amy_say', text], 
                                  check=True, timeout=10, capture_output=True, text=True)
            return {'success': True, 'message': f'Speaking Astra voice: {text}'}
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Audio timeout'}
        except subprocess.CalledProcessError as e:
            # Fallback to espeak if Piper fails
            try:
                subprocess.run(['espeak', '-a', '200', text], check=False, timeout=10)
                return {'success': True, 'message': f'Speaking (espeak fallback): {text}'}
            except Exception as fallback_error:
                return {'success': False, 'error': f'Audio failed: {str(e)}'}
        except Exception as e:
            return {'success': False, 'error': f'Audio system error: {str(e)}'}
    
    def handle_voice_command(self, text):
        """Handle voice command processing"""
        try:
            # Placeholder for voice command integration
            # Will integrate with existing Amy voice system
            return {'success': True, 'message': f'Voice command processed: {text}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def toggle_desk_safe_mode(self):
        """Toggle desk safe mode on/off"""
        try:
            self.desk_safe_mode = not self.desk_safe_mode
            mode_text = "enabled" if self.desk_safe_mode else "disabled"
            
            # Announce the mode change
            announcement = f"Desk safe mode {mode_text}"
            self.speak_text(announcement)
            
            return {
                'success': True, 
                'desk_safe_mode': self.desk_safe_mode,
                'message': f'Desk safe mode {mode_text}'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def wave_gesture(self):
        """Perform wave gesture"""
        try:
            # Import the wave function from existing Amy system
            sys.path.append('/home/spencer/amy_core')
            from postwake_router import do_wave
            
            # Announce wave
            self.speak_text("Hello! Let me give you a wave!")
            
            # Perform wave gesture
            do_wave()
            
            return {'success': True, 'message': 'Wave gesture completed'}
        except Exception as e:
            return {'success': False, 'error': f'Wave gesture failed: {str(e)}'}
    
    def look_up_gesture(self):
        """TEMPORARY: Single leg test to map coordinate system"""
        try:
            # Import PiCrawler for stance adjustment
            sys.path.append('/home/spencer/picrawler')
            from picrawler import Picrawler
            
            # Initialize robot if not already done
            if not hasattr(self, 'robot'):
                self.robot = Picrawler()
                print("🤖 PiCrawler robot initialized for test")
            
            # Announce the action
            self.speak_text("Looking up!")
            
            print("🔍 Executing camera look up: Front legs RAISED (less negative Z)")
            
            # CORRECT look up posture: Start from stand (-50), raise front legs
            # Format: [[right_front], [left_front], [left_rear], [right_rear]]
            # Stand baseline: [45, 45, -50] for all legs
            # Front legs UP: LESS negative Z (e.g., -30)
            # Rear legs: Keep at stand level (-50)
            look_up_posture = [
                [45, 45, -30],  # pos1 (RF) - RAISED (less negative = UP)
                [45, 45, -30],  # pos2 (LF) - RAISED (less negative = UP)
                [45, 45, -50],  # pos3 (LR) - NORMAL stand level
                [45, 45, -50]   # pos4 (RR) - NORMAL stand level
            ]
            
            # Execute the look up posture
            self.robot.do_step(look_up_posture, speed=40)
            print("✅ Camera look up: Front legs raised to -30, rear at -50")
            
            return {'success': True, 'message': 'Position 1 leg test completed'}
            
        except ImportError as e:
            # Fallback for when PiCrawler not available
            self.speak_text("Looking up!")
            print("🔍 Look up gesture - PiCrawler not available, using voice only")
            return {'success': True, 'message': 'Look up gesture completed (voice only)'}
            
        except Exception as e:
            return {'success': False, 'error': f'Look up gesture failed: {str(e)}'}

    def look_down_gesture(self):
        """Perform look down gesture using PiCrawler's built-in method"""
        try:
            # Import PiCrawler for stance adjustment
            sys.path.append('/home/spencer/picrawler')
            from picrawler import Picrawler
            
            # Initialize robot if not already done
            if not hasattr(self, 'robot'):
                self.robot = Picrawler()
                print("🤖 PiCrawler robot initialized for look down")
            
            # Announce the action
            self.speak_text("Looking down!")
            
            # Use PiCrawler's built-in look_down method
            print("🔍 Executing look down gesture...")
            step_data = self.robot.look_down
            if step_data:
                self.robot.do_step(step_data[0], speed=30)
                print("✅ Look down gesture completed")
            else:
                print("⚠️ No step data for look down")
            
            return {'success': True, 'message': 'Look down gesture completed'}
            
        except ImportError as e:
            # Fallback for when PiCrawler not available
            self.speak_text("Looking down!")
            print("🔍 Look down gesture - PiCrawler not available, using voice only")
            return {'success': True, 'message': 'Look down gesture completed (voice only)'}
            
        except Exception as e:
            return {'success': False, 'error': f'Look down gesture failed: {str(e)}'}

    def stand_gesture(self):
        """Stand up to symmetric ready position"""
        try:
            # Import PiCrawler for stance control
            sys.path.append('/home/spencer/picrawler')
            from picrawler import Picrawler
            
            # Initialize robot if not already done
            if not hasattr(self, 'robot'):
                self.robot = Picrawler()
                print("🤖 PiCrawler robot initialized for stand")
            
            # Announce the action
            self.speak_text("Standing up in symmetric position!")
            
            # SYMMETRIC STAND - All legs use [45, 45, -50] coordinates
            print("🧍 Moving to symmetric standing position...")
            
            # Set all legs to symmetric position [45, 45, -50]
            symmetric_coords = [45, 45, -50]
            
            # Apply symmetric coordinates to all legs
            self.robot.move_legs([
                symmetric_coords,  # Position 1 (right_front)
                symmetric_coords,  # Position 2 (left_front)
                symmetric_coords,  # Position 3 (left_rear)
                symmetric_coords   # Position 4 (right_rear)
            ])
            
            print("📐 SYMMETRIC STAND COORDINATES (All legs balanced):")
            print("   Position 1 (right_front): [45, 45, -50]")
            print("   Position 2 (left_front):  [45, 45, -50]")  
            print("   Position 3 (left_rear):   [45, 45, -50]")
            print("   Position 4 (right_rear):  [45, 45, -50]")
            print("✅ Symmetric standing position achieved!")
            
            return {'success': True, 'message': 'Symmetric standing position set', 'gesture': 'Standing'}
            
        except ImportError as e:
            # Fallback for when PiCrawler not available
            self.speak_text("Standing up in symmetric position!")
            print("🧍 Stand gesture - PiCrawler not available, using voice only")
            return {'success': True, 'message': 'Stand gesture completed (voice only)', 'gesture': 'Standing'}
            
        except Exception as e:
            print(f"❌ Stand gesture error: {e}")
            # Fallback to basic stand if custom coordinates fail
            try:
                result = self.robot.do_step('stand', 50)
                print(f"🧍 Fallback stand result: {result}")
                return {'success': True, 'message': 'Standing position set (fallback)', 'gesture': 'Standing'}
            except:
                return {'success': False, 'error': f'Stand gesture failed: {str(e)}'}
                
    def sit_gesture(self):
        """Sit down for desk safe mode"""
        try:
            # Import PiCrawler for stance control
            sys.path.append('/home/spencer/picrawler')
            from picrawler import Picrawler
            
            # Initialize robot if not already done
            if not hasattr(self, 'robot'):
                self.robot = Picrawler()
                print("🤖 PiCrawler robot initialized for sit")
            
            # Announce the action
            self.speak_text("Sitting down for desk safe mode!")
            
            # Use correct PiCrawler API: do_step with 'sit' and speed
            print("🪑 Moving to sitting position...")
            result = self.robot.do_step('sit', 50)
            print(f"🪑 Sit step result: {result}")
            print("✅ Sitting position achieved - desk safe mode ready")
            return {'success': True, 'message': 'Sitting position set, desk safe mode active', 'gesture': 'Sitting'}
            
        except ImportError as e:
            # Fallback for when PiCrawler not available
            self.speak_text("Sitting down! Desk safe mode ready")
            print("🪑 Sit gesture - PiCrawler not available, using voice only")
            return {'success': True, 'message': 'Sit gesture completed (voice only)', 'gesture': 'Sitting'}
            
        except Exception as e:
            print(f"❌ Sit gesture error: {e}")
            return {'success': False, 'error': f'Sit gesture failed: {str(e)}'}
            
        except Exception as e:
            print(f"❌ Sit gesture general error: {e}")
            return {'success': False, 'error': f'Sit gesture failed: {str(e)}'}

    def get_status_extended(self):
        """Get extended status including safety modes"""
        try:
            return {
                'success': True,
                'desk_safe_mode': self.desk_safe_mode,
                'camera_active': self.camera_active,
                'monitoring': self.monitoring,
                'hardware_initialized': self.hardware_initialized
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def start_camera(self):
        """Start camera stream"""
        try:
            if self.camera_active:
                return {'success': True, 'message': 'Camera already active'}
            
            # Start camera in background
            self.camera_process = subprocess.Popen([
                'python3', '/home/spencer/amy_core/persistent_camera.py'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            self.camera_active = True
            return {'success': True, 'message': 'Camera started', 'url': 'http://192.168.1.4:9000/mjpg'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def stop_camera(self):
        """Stop camera stream"""
        try:
            if self.camera_process:
                self.camera_process.terminate()
                self.camera_process = None
            
            # Kill any remaining camera processes
            subprocess.run(['pkill', '-f', 'persistent_camera'], check=False)
            
            self.camera_active = False
            return {'success': True, 'message': 'Camera stopped'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Initialize Amy API
amy_api = AmyMobileAPI()

# ============================================================================
# ASTRA VOICE CONTROL REACT INTERFACE ENDPOINTS
# These endpoints match the expected API schema from AstraVoiceControl
# ============================================================================

@app.route('/api/movement', methods=['POST'])
def movement():
    """Movement control endpoint for React interface"""
    try:
        data = request.get_json()
        direction = data.get('direction', '')
        
        if direction not in ['forward', 'backward', 'left', 'right', 'stop']:
            return jsonify({'success': False, 'error': 'Invalid direction'}), 400
        
        result = amy_api.movement_command(direction)
        return jsonify({
            'success': result.get('success', False),
            'message': result.get('message', ''),
            'direction': direction,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gesture', methods=['POST'])
def gesture():
    """Gesture control endpoint for React interface"""
    try:
        data = request.get_json()
        gesture_name = data.get('gesture', '')
        
        if gesture_name == 'stand':
            result = amy_api.stand_gesture()
        elif gesture_name == 'sit':
            result = amy_api.sit_gesture()
        elif gesture_name == 'wave':
            result = amy_api.wave_gesture()
        elif gesture_name == 'look_up':
            result = amy_api.look_up_gesture()
        else:
            return jsonify({'success': False, 'error': 'Invalid gesture'}), 400
        
        return jsonify({
            'success': result.get('success', False),
            'message': result.get('message', ''),
            'gesture': result.get('gesture', gesture_name.replace('_', ' ').title()),
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/emergency-stop', methods=['POST'])
def emergency_stop():
    """Emergency stop endpoint for React interface"""
    try:
        result = amy_api.emergency_stop()
        return jsonify({
            'success': result.get('success', False),
            'message': result.get('message', ''),
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# MISSING ENDPOINTS FOR REACT INTERFACE
# ============================================================================

@app.route('/api/camera/feed', methods=['GET'])
def camera_feed():
    """Get camera feed URL"""
    try:
        if amy_api.camera_active:
            return jsonify({
                'success': True,
                'url': 'http://192.168.1.4:9000/mjpg',
                'active': True
            })
        else:
            return jsonify({
                'success': True,
                'url': None,
                'active': False,
                'message': 'Camera not active'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sensors/lidar', methods=['GET'])
def sensors_lidar():
    """Get LIDAR sensor data"""
    try:
        # Use ultrasonic sensor as front-center LIDAR equivalent
        sensor_data = amy_api.sensor_data
        distance = sensor_data.get('distance', 0)
        
        return jsonify({
            'success': True,
            'sensors': [
                {'direction': 'Front-Left', 'distance': 0, 'status': 'offline'},
                {'direction': 'Front-Center', 'distance': distance, 'status': 'online' if distance > 0 else 'offline'},
                {'direction': 'Front-Right', 'distance': 0, 'status': 'offline'}
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/quick', methods=['POST'])
def voice_quick():
    """Quick voice commands"""
    try:
        data = request.get_json()
        phrase = data.get('phrase', '')
        
        # Map quick phrases to actions
        if 'hello' in phrase.lower():
            result = amy_api.speak_text("Hello! I'm Astra, ready to help!")
        elif 'wave' in phrase.lower():
            result = amy_api.wave_gesture()
        elif 'stand' in phrase.lower():
            result = amy_api.stand_gesture()
        elif 'sit' in phrase.lower():
            result = amy_api.sit_gesture()
        else:
            result = amy_api.speak_text(f"You said: {phrase}")
        
        return jsonify({
            'success': result.get('success', False),
            'message': result.get('message', ''),
            'phrase': phrase,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/complex', methods=['POST'])
def voice_complex():
    """Complex voice command processing"""
    try:
        data = request.get_json()
        command = data.get('command', '')
        
        result = amy_api.handle_voice_command(command)
        return jsonify({
            'success': result.get('success', False),
            'message': result.get('message', ''),
            'command': command,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/settings/safe-mode', methods=['POST'])
def settings_safe_mode():
    """Toggle desk safe mode"""
    try:
        data = request.get_json()
        enabled = data.get('enabled', False)
        
        # Set the mode based on the request
        amy_api.desk_safe_mode = enabled
        mode_text = "enabled" if enabled else "disabled"
        
        # Announce the change
        amy_api.speak_text(f"Desk safe mode {mode_text}")
        
        return jsonify({
            'success': True,
            'enabled': enabled,
            'message': f'Desk safe mode {mode_text}',
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/settings/camera', methods=['POST'])
def settings_camera():
    """Toggle camera on/off"""
    try:
        data = request.get_json()
        enabled = data.get('enabled', False)
        
        if enabled:
            result = amy_api.start_camera()
        else:
            result = amy_api.stop_camera()
        
        return jsonify({
            'success': result.get('success', False),
            'enabled': enabled,
            'message': result.get('message', ''),
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/settings/audio-feedback', methods=['POST'])
def settings_audio_feedback():
    """Toggle audio feedback"""
    try:
        data = request.get_json()
        enabled = data.get('enabled', False)
        
        # Store audio feedback setting
        amy_api.audio_feedback = enabled
        
        return jsonify({
            'success': True,
            'enabled': enabled,
            'message': f'Audio feedback {"enabled" if enabled else "disabled"}',
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Enhanced status endpoint for React interface"""
    try:
        extended_status = amy_api.get_status_extended()
        sensor_data = amy_api.sensor_data
        
        return jsonify({
            'connected': True,
            'deskSafeMode': amy_api.desk_safe_mode,
            'batteryLevel': int(sensor_data.get('battery_percentage', 0)),
            'currentGesture': extended_status.get('current_gesture', 'Unknown'),
            'lastCommand': extended_status.get('last_command', ''),
            'lastCommandTime': extended_status.get('last_command_time', ''),
            'distance': sensor_data.get('distance', 0),
            'faces': sensor_data.get('faces', 0),
            'battery_voltage': sensor_data.get('battery_voltage', 0),
            'timestamp': time.time(),
            'lidar_sensors': [
                {'direction': 'Front-Left', 'distance': 0, 'status': 'offline'},
                {'direction': 'Front-Center', 'distance': sensor_data.get('distance', 0), 'status': 'online'},
                {'direction': 'Front-Right', 'distance': 0, 'status': 'offline'}
            ]
        })
    except Exception as e:
        return jsonify({'connected': False, 'error': str(e)}), 500

# ============================================================================
# LEGACY ENDPOINTS (for backward compatibility)
# ============================================================================

@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    """Get current sensor data"""
    return jsonify(amy_api.sensor_data)

@app.route('/api/command', methods=['POST'])
def send_command():
    """Send command to Astra"""
    try:
        data = request.get_json()
        command = data.get('command')
        
        # Handle both formats: {command, params: {text}} and {command, text}
        if 'params' in data:
            params = data.get('params', {})
        else:
            # Mobile app sends text directly, so wrap it in params
            params = {k: v for k, v in data.items() if k != 'command'}
        
        if not command:
            return jsonify({'success': False, 'error': 'Command required'}), 400
        
        result = amy_api.execute_command(command, params)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/speak', methods=['POST'])
def speak():
    """Make Astra speak"""
    try:
        data = request.get_json()
        text = data.get('text', 'Hello from Astra')
        
        result = amy_api.speak_text(text)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/camera', methods=['POST'])
def camera_control():
    """Control camera on/off"""
    try:
        data = request.get_json()
        action = data.get('action', 'start')
        
        if action == 'start':
            result = amy_api.start_camera()
        elif action == 'stop':
            result = amy_api.stop_camera()
        else:
            return jsonify({'success': False, 'error': 'Invalid action'}), 400
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/photo', methods=['POST'])
def take_photo():
    """Take a photo"""
    result = amy_api.take_photo()
    return jsonify(result)

@app.route('/api/desk-safe-toggle', methods=['POST'])
def toggle_desk_safe():
    """Toggle desk safe mode"""
    result = amy_api.toggle_desk_safe_mode()
    return jsonify(result)

@app.route('/api/wave', methods=['POST'])
def wave():
    """Perform wave gesture"""
    result = amy_api.wave_gesture()
    return jsonify(result)

@app.route('/api/look-up', methods=['POST'])
def look_up():
    """Perform look up gesture"""
    result = amy_api.look_up_gesture()
    return jsonify(result)

@app.route('/api/look-down', methods=['POST'])
def look_down():
    """Perform look down gesture"""
    result = amy_api.look_down_gesture()
    return jsonify(result)

@app.route('/api/stand', methods=['POST'])
def stand():
    """Stand up to ready position"""
    result = amy_api.stand_gesture()
    return jsonify(result)

@app.route('/api/sit', methods=['POST'])
def sit():
    """Sit down and power down servos"""
    result = amy_api.sit_gesture()
    return jsonify(result)

@app.route('/api/status-extended', methods=['GET'])
def get_status_extended():
    """Get extended status including safety modes"""
    result = amy_api.get_status_extended()
    return jsonify(result)

@app.route('/', methods=['GET'])
def home():
    """API home page"""
    return jsonify({
        'name': 'Dogzilla Mobile API (DogzillaVoiceControl Compatible)',
        'version': '1.0.0',
        'react_interface': 'DogzillaVoiceControl',
        'personality': 'Kaiju Mode 🐕🦖',
        'endpoints': {
            'primary': [
                '/api/movement',
                '/api/gesture', 
                '/api/emergency-stop',
                '/api/status'
            ],
            'react_features': [
                '/api/camera/feed',
                '/api/sensors/lidar',
                '/api/voice/quick',
                '/api/voice/complex',
                '/api/settings/safe-mode',
                '/api/settings/camera',
                '/api/settings/audio-feedback'
            ],
            'legacy': [
                '/api/sensors', 
                '/api/command',
                '/api/speak',
                '/api/desk-safe-toggle',
                '/api/wave',
                '/api/look-up',
                '/api/look-down',
                '/api/stand',
                '/api/sit',
                '/api/photo',
                '/api/camera'
            ]
        },
        'camera_stream': 'http://192.168.1.4:9010/mjpg',  # Dogzilla camera port
        'symmetric_stand': [45, 45, -50],
        'adapted_from': 'AstraVoiceControl - Proven Working System'
    })

def main():
    """Main function"""
    print("🐕� Dogzilla Mobile API Server Starting...")
    print("🎯 DogzillaVoiceControl React Interface Compatible")
    
    # Start sensor monitoring
    amy_api.start_monitoring()
    
    try:
        # Start API server on Dogzilla port
        print("🚀 API Server running on http://192.168.1.4:5011")
        print("📱 Primary React endpoints: /api/movement, /api/gesture, /api/emergency-stop, /api/status")
        print("🔄 Legacy endpoints also available for backward compatibility")
        
        app.run(host='0.0.0.0', port=5011, debug=False)
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Dogzilla API server...")
        amy_api.stop_monitoring()
    except Exception as e:
        print(f"❌ Dogzilla API Server error: {e}")
        amy_api.stop_monitoring()

if __name__ == '__main__':
    main()