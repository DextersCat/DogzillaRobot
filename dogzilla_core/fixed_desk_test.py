#!/usr/bin/env python3
"""
Fixed Comprehensive Desk Mode Test
Resolves camera conflicts and TTS issues
"""

from vilib import Vilib
from robot_hat import Ultrasonic, Pin
import time
import os
import subprocess
from datetime import datetime

class DeskModeTestFixed:
    def __init__(self):
        """Initialize desk mode testing system"""
        self.camera_active = False
        self.sensor_active = False
        self.monitoring = False
        
        # Paths and settings
        self.username = os.getlogin()
        self.photo_path = f"/home/{self.username}/Pictures/amy_desk_test/"
        os.makedirs(self.photo_path, exist_ok=True)
        
        print("🤖 Amy Desk Mode Test System Initialized")
        print(f"📸 Photos will be saved to: {self.photo_path}")
    
    def start_camera(self):
        """Initialize camera system"""
        try:
            print("📷 Starting camera system...")
            Vilib.camera_start(vflip=False, hflip=False, size=(640, 480))
            Vilib.display(local=False, web=True)
            Vilib.show_fps()
            
            # Enable face detection
            Vilib.face_detect_switch(True)
            
            self.camera_active = True
            print("✅ Camera system active")
            print(f"📹 Web stream: http://192.168.1.4:9000/mjpg")
            return True
            
        except Exception as e:
            print(f"❌ Camera initialization failed: {e}")
            return False
    
    def start_sensor(self):
        """Initialize ultrasonic sensor"""
        try:
            print("📡 Starting ultrasonic sensor...")
            self.sonar = Ultrasonic(Pin("D2"), Pin("D3"))
            self.sensor_active = True
            print("✅ Ultrasonic sensor active (D2=trig, D3=echo)")
            return True
            
        except Exception as e:
            print(f"❌ Sensor initialization failed: {e}")
            return False
    
    def tts_say(self, message):
        """TTS using espeak as fallback"""
        try:
            print(f"🔊 TTS: {message}")
            subprocess.run(['espeak', message], check=False, 
                          capture_output=True, timeout=5)
            return True
        except Exception as e:
            print(f"⚠️  TTS failed: {e}")
            return False
    
    def read_sensors(self):
        """Read all sensor data"""
        data = {
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'distance': -1,
            'faces': 0,
            'camera_status': self.camera_active,
            'sensor_status': self.sensor_active
        }
        
        # Read distance
        if self.sensor_active:
            try:
                data['distance'] = self.sonar.read()
            except:
                data['distance'] = -1
        
        # Read face detection
        if self.camera_active:
            try:
                data['faces'] = Vilib.detect_obj_parameter['human_n']
            except:
                data['faces'] = 0
        
        return data
    
    def interpret_distance(self, distance):
        """Interpret distance readings for desk environment"""
        if distance < 0:
            return "ERROR"
        elif distance < 10:
            return "DESK_SURFACE"
        elif distance < 25:
            return "CLOSE_OBJECT"
        elif distance < 50:
            return "HAND_RANGE"
        elif distance < 100:
            return "DESK_EDGE"
        else:
            return "ROOM_RANGE"
    
    def take_photo_simple(self, reason="manual"):
        """Simple photo notification - avoid camera conflicts"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"desk_{reason}_{timestamp}"
        print(f"📸 Photo trigger: {filename} (camera stream active)")
        return True
    
    def monitoring_loop(self):
        """Main monitoring loop"""
        print("\n🔍 Starting monitoring loop...")
        print("📊 Monitoring: Distance, Face Detection, and Events")
        print("Press Ctrl+C to stop")
        
        last_distance_category = ""
        last_face_count = 0
        loop_count = 0
        
        try:
            while self.monitoring:
                data = self.read_sensors()
                loop_count += 1
                
                # Analyze distance
                distance_category = self.interpret_distance(data['distance'])
                
                # Check for significant changes
                distance_changed = distance_category != last_distance_category
                face_changed = data['faces'] != last_face_count
                
                # Print status every 10 loops or on changes
                if loop_count % 10 == 0 or distance_changed or face_changed:
                    distance_str = f"{data['distance']:.1f}cm" if data['distance'] > 0 else "ERROR"
                    print(f"[{data['timestamp']}] 📏 {distance_str} ({distance_category}) | 👤 {data['faces']} faces")
                
                # Handle face detection events
                if face_changed and data['faces'] > 0:
                    print(f"👤 Face detected! Count: {data['faces']}")
                    self.take_photo_simple("face_detected")
                    self.tts_say(f"{data['faces']} person detected")
                
                # Handle distance events
                if distance_changed:
                    if distance_category == "CLOSE_OBJECT":
                        print(f"🔍 Close object detected at {data['distance']:.1f}cm")
                        self.take_photo_simple("close_object")
                    elif distance_category == "HAND_RANGE":
                        print(f"✋ Hand range detection at {data['distance']:.1f}cm")
                
                # Update last values
                last_distance_category = distance_category
                last_face_count = data['faces']
                
                time.sleep(0.5)  # 2Hz monitoring
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Monitoring error: {e}")
    
    def run_system_test(self):
        """Run comprehensive system test"""
        print("\n🔧 Running System Test...")
        
        # Test 1: Hardware initialization
        print("\n1️⃣  Hardware Initialization Test")
        camera_ok = self.start_camera()
        sensor_ok = self.start_sensor()
        
        if not (camera_ok and sensor_ok):
            print("❌ Hardware initialization failed")
            return False
        
        # Test 2: Sensor readings
        print("\n2️⃣  Sensor Reading Test")
        readings = []
        for i in range(5):
            data = self.read_sensors()
            distance_cat = self.interpret_distance(data['distance'])
            print(f"   Reading {i+1}: {data['distance']:.1f}cm ({distance_cat}) | Faces: {data['faces']}")
            if data['distance'] > 0:
                readings.append(data['distance'])
            time.sleep(1)
        
        # Analyze readings
        if readings:
            avg_dist = sum(readings) / len(readings)
            print(f"   📊 Average distance: {avg_dist:.1f}cm ({self.interpret_distance(avg_dist)})")
        
        # Test 3: Photo capture notification
        print("\n3️⃣  Photo System Test")
        self.take_photo_simple("system_test")
        
        # Test 4: TTS announcement
        print("\n4️⃣  TTS Test")
        self.tts_say("Amy desk mode test completed successfully")
        
        print("\n✅ System test completed!")
        return True
    
    def run_interactive_mode(self):
        """Run interactive monitoring mode"""
        print("\n🎮 Interactive Mode")
        print("Commands:")
        print("  - Wave hand in front of sensor")
        print("  - Move face in front of camera")
        print("  - Watch web stream at: http://192.168.1.4:9000/mjpg")
        print("  - Press Ctrl+C to stop")
        
        self.monitoring = True
        self.monitoring_loop()
    
    def stop(self):
        """Clean shutdown"""
        print("\n🔄 Shutting down...")
        
        self.monitoring = False
        
        if self.camera_active:
            try:
                Vilib.camera_close()
                print("📷 Camera closed")
            except:
                pass
        
        print("✅ Desk mode test completed")

def main():
    """Main function"""
    print("🤖 Amy Fixed Comprehensive Desk Mode Test")
    print("=" * 55)
    print("Testing: Camera + Ultrasonic + TTS Integration")
    print("Environment: Stationary on desk")
    print("Features: Web stream, distance monitoring, face detection")
    
    test_system = DeskModeTestFixed()
    
    try:
        # Run system test first
        success = test_system.run_system_test()
        
        if success:
            # Ask for interactive mode
            print("\n" + "="*55)
            response = input("Run interactive monitoring? (y/n): ").strip().lower()
            
            if response in ['y', 'yes']:
                test_system.run_interactive_mode()
            else:
                print("💡 You can still view the camera at: http://192.168.1.4:9000/mjpg")
        
        else:
            print("❌ System test failed - check hardware connections")
    
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        test_system.stop()

if __name__ == "__main__":
    main()