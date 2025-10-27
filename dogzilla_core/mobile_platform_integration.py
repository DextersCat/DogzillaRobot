#!/usr/bin/env python3
"""
Mobile Platform Integration Example
Combines camera, LIDAR, and mobile control for PiCrawler
"""

from vilib import Vilib
from robot_hat import Ultrasonic, Pin, TTS
from picrawler import Picrawler
import time
import threading
from os import getlogin

class MobilePlatform:
    def __init__(self):
        # Initialize hardware components
        self.crawler = Picrawler()
        self.sonar = Ultrasonic(Pin("D2"), Pin("D3"))  # LIDAR/Distance sensor
        self.tts = TTS()
        
        # Mobile platform settings
        self.alert_distance = 20  # cm - obstacle detection threshold
        self.speed = 50
        
        # Camera settings
        self.username = getlogin()
        self.photo_path = f"/home/{self.username}/Pictures/mobile_platform/"
        
        # Initialize camera
        self.camera_active = False
        
    def start_camera(self):
        """Initialize camera system"""
        try:
            Vilib.camera_start(vflip=False, hflip=False, size=(1280, 720))
            Vilib.display(local=True, web=True)
            Vilib.show_fps()
            
            # Enable face detection for security
            Vilib.face_detect_switch(True)
            
            self.camera_active = True
            print("✅ Camera system active")
            print(f"📹 Web view: http://pi_ip:9000/mjpg")
            return True
        except Exception as e:
            print(f"❌ Camera initialization failed: {e}")
            return False
    
    def read_sensors(self):
        """Read all sensor data"""
        distance = self.sonar.read()
        faces_detected = Vilib.detect_obj_parameter['human_n'] if self.camera_active else 0
        
        return {
            'distance': distance,
            'faces_detected': faces_detected,
            'camera_active': self.camera_active
        }
    
    def take_photo(self, reason="auto"):
        """Capture photo with timestamp"""
        if not self.camera_active:
            return False
            
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        filename = f"mobile_platform_{reason}_{timestamp}"
        
        try:
            status = Vilib.take_photo(filename, self.photo_path)
            if status:
                print(f"📸 Photo saved: {filename}.jpg")
                return True
        except Exception as e:
            print(f"❌ Photo capture failed: {e}")
        return False
    
    def obstacle_avoidance(self):
        """Basic obstacle avoidance behavior"""
        sensor_data = self.read_sensors()
        distance = sensor_data['distance']
        
        if distance < 0:
            # Sensor reading failed
            self.crawler.do_action('stop', 1, 0)
            return "sensor_error"
        
        elif distance <= self.alert_distance:
            # Obstacle detected
            print(f"⚠️  Obstacle detected at {distance}cm")
            self.crawler.do_action('stop', 1, 0)
            time.sleep(0.2)
            
            # Take photo of obstacle
            self.take_photo("obstacle")
            
            # Announce obstacle
            self.tts.say(f"Obstacle detected at {distance} centimeters")
            
            # Turn left to avoid
            self.crawler.do_action('turn left angle', 3, self.speed)
            time.sleep(0.5)
            
            return "obstacle_avoided"
        
        else:
            # Path clear, move forward
            self.crawler.do_action('forward', 1, self.speed)
            time.sleep(0.2)
            return "moving_forward"
    
    def security_patrol(self):
        """Security patrol with face detection"""
        sensor_data = self.read_sensors()
        
        if sensor_data['faces_detected'] > 0:
            print(f"👤 {sensor_data['faces_detected']} person(s) detected")
            
            # Stop and take photo
            self.crawler.do_action('stop', 1, 0)
            self.take_photo("person_detected")
            
            # Security announcement
            self.tts.say("Person detected. Taking security photo.")
            time.sleep(2)
        
        # Continue with obstacle avoidance
        return self.obstacle_avoidance()
    
    def autonomous_mode(self):
        """Main autonomous operation loop"""
        print("🤖 Starting autonomous mobile platform mode")
        print("Features: Camera, LIDAR, Face Detection, Obstacle Avoidance")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                status = self.security_patrol()
                
                # Log status every 10 iterations
                if hasattr(self, '_iteration_count'):
                    self._iteration_count += 1
                else:
                    self._iteration_count = 1
                
                if self._iteration_count % 10 == 0:
                    sensor_data = self.read_sensors()
                    print(f"Status: {status} | Distance: {sensor_data['distance']}cm | "
                          f"Faces: {sensor_data['faces_detected']} | Camera: {sensor_data['camera_active']}")
                
                time.sleep(0.1)  # Main loop delay
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping autonomous mode")
            self.stop()
    
    def stop(self):
        """Safe shutdown of all systems"""
        print("🔄 Shutting down mobile platform...")
        
        # Stop movement
        self.crawler.do_action('stop', 1, 0)
        
        # Close camera
        if self.camera_active:
            Vilib.camera_close()
            print("📷 Camera closed")
        
        print("✅ Mobile platform stopped safely")

def main():
    """Example usage and testing"""
    platform = MobilePlatform()
    
    # Initialize camera
    if not platform.start_camera():
        print("❌ Cannot proceed without camera")
        return
    
    # Brief system test
    print("\n🔧 System Test:")
    sensor_data = platform.read_sensors()
    print(f"Distance sensor: {sensor_data['distance']}cm")
    print(f"Camera: {'✅ Active' if sensor_data['camera_active'] else '❌ Inactive'}")
    print(f"Face detection: {sensor_data['faces_detected']} faces")
    
    # Take test photo
    platform.take_photo("system_test")
    
    time.sleep(2)
    
    # Start autonomous mode
    platform.autonomous_mode()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Ensure clean shutdown
        try:
            Vilib.camera_close()
        except:
            pass