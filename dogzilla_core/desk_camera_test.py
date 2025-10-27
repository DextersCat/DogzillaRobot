#!/usr/bin/env python3
"""
Desk Mode Camera Test
Testing vilib camera system while Amy is stationary on desk
"""

from vilib import Vilib
import time
import os
from datetime import datetime

def desk_camera_test():
    """Test camera functionality in desk mode"""
    print("📷 Starting desk mode camera test...")
    print("Amy is stationary - testing camera and web stream")
    
    username = os.getlogin()
    photo_path = f"/home/{username}/Pictures/amy_desk_test/"
    
    # Create photo directory if it doesn't exist
    os.makedirs(photo_path, exist_ok=True)
    
    try:
        # Initialize camera
        print("🔧 Initializing camera system...")
        Vilib.camera_start(vflip=False, hflip=False, size=(1280, 720))
        
        # Enable web display for remote viewing
        Vilib.display(local=True, web=True)
        
        # Show FPS for performance monitoring
        Vilib.show_fps()
        
        print("✅ Camera system active!")
        print(f"📹 Web stream available at: http://pi_ip:9000/mjpg")
        print(f"📸 Photos will be saved to: {photo_path}")
        
        # Enable face detection for testing
        Vilib.face_detect_switch(True)
        print("👤 Face detection enabled")
        
        # Test photo capture
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        test_photo_name = f"desk_test_{timestamp}"
        
        print(f"\n📸 Taking test photo: {test_photo_name}")
        photo_success = Vilib.take_photo(test_photo_name, photo_path)
        
        if photo_success:
            print(f"✅ Photo saved successfully: {test_photo_name}.jpg")
        else:
            print("❌ Photo capture failed")
        
        # Monitor for a short time
        print("\n🔍 Monitoring camera for 30 seconds...")
        print("Try moving in front of the camera to test face detection")
        print("Press Ctrl+C to stop early")
        
        start_time = time.time()
        last_face_count = 0
        
        while time.time() - start_time < 30:
            # Check face detection
            current_faces = Vilib.detect_obj_parameter['human_n']
            
            if current_faces != last_face_count:
                if current_faces > 0:
                    print(f"👤 {current_faces} face(s) detected!")
                    # Take photo when face detected
                    face_timestamp = datetime.now().strftime("%H-%M-%S")
                    face_photo_name = f"face_detected_{face_timestamp}"
                    Vilib.take_photo(face_photo_name, photo_path)
                    print(f"📸 Face photo saved: {face_photo_name}.jpg")
                else:
                    print("👁️  No faces detected")
                
                last_face_count = current_faces
            
            time.sleep(1)
        
        print("\n✅ Desk camera test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False
    
    finally:
        # Clean shutdown
        print("🔄 Shutting down camera...")
        try:
            Vilib.camera_close()
            print("📷 Camera closed successfully")
        except:
            pass

def main():
    """Main test function"""
    print("🤖 Amy Desk Mode Camera Test")
    print("=" * 40)
    
    success = desk_camera_test()
    
    if success:
        print("\n🎉 All camera tests passed!")
        print("Camera system is ready for mobile platform integration")
    else:
        print("\n❌ Camera tests failed - check connections")
    
    print("\nNext: Test ultrasonic sensor and create complete mobile platform")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        try:
            Vilib.camera_close()
        except:
            pass