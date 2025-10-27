#!/usr/bin/env python3
"""
Simple Desk Camera Test
Testing basic camera functionality while Amy is stationary
"""

from vilib import Vilib
import time
import os

def simple_camera_test():
    """Simple camera test focused on web stream"""
    print("📷 Starting simple camera test...")
    
    try:
        # Initialize camera with basic settings
        print("🔧 Initializing camera...")
        Vilib.camera_start(vflip=False, hflip=False, size=(640, 480))
        
        # Enable only web display (no local GUI)
        Vilib.display(local=False, web=True)
        
        print("✅ Camera initialized!")
        print("📹 Web stream should be available at: http://192.168.1.4:9000/mjpg")
        
        # Test for 10 seconds
        print("🔍 Camera running for 10 seconds...")
        print("Check the web stream to verify camera is working")
        
        for i in range(10):
            print(f"⏰ {10-i} seconds remaining...")
            time.sleep(1)
        
        print("✅ Camera test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Camera error: {e}")
        return False
    
    finally:
        try:
            Vilib.camera_close()
            print("📷 Camera closed")
        except:
            pass

if __name__ == "__main__":
    print("🤖 Amy Simple Camera Test")
    print("=" * 30)
    
    success = simple_camera_test()
    
    if success:
        print("\n🎉 Camera web stream test passed!")
        print("You can view the camera at: http://192.168.1.4:9000/mjpg")
    else:
        print("\n❌ Camera test failed")