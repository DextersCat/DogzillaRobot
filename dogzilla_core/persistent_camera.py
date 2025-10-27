#!/usr/bin/env python3
"""
Persistent Camera Stream for Mobile App
Keeps camera stream running continuously
"""

from vilib import Vilib
import time

def start_persistent_camera():
    """Start camera stream that runs continuously"""
    print("📷 Starting persistent camera stream for mobile app...")
    
    try:
        # Initialize camera
        Vilib.camera_start(vflip=False, hflip=False, size=(640, 480))
        
        # Enable web display only
        Vilib.display(local=False, web=True)
        
        print("✅ Camera stream active!")
        print("📹 Web stream: http://192.168.1.4:9000/mjpg")
        print("🔄 Running continuously... Press Ctrl+C to stop")
        
        # Run indefinitely
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Camera stream stopped by user")
    except Exception as e:
        print(f"❌ Camera error: {e}")
    finally:
        try:
            Vilib.camera_close()
            print("📷 Camera closed")
        except:
            pass

if __name__ == "__main__":
    start_persistent_camera()