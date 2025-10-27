#!/usr/bin/env python3
"""
Optimized camera stream for mobile app with better frame handling
"""

import sys
import time
import signal
import os

# Add vilib to path
sys.path.append('/home/spencer/vilib')

try:
    from vilib import Vilib
    
    def signal_handler(sig, frame):
        print('🛑 Stopping camera...')
        Vilib.camera_close()
        sys.exit(0)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print('📹 Starting optimized camera stream...')
    
    # Start camera with optimized settings
    Vilib.camera_start(
        vflip=False, 
        hflip=False,
        resolution=(640, 480),  # Lower resolution for better performance
        framerate=15            # Lower framerate to prevent freezing
    )
    
    # Start web display
    Vilib.display(local=False, web=True)
    print('✅ Camera stream: http://192.168.1.4:9000/mjpg')
    print('🔄 Optimized for mobile viewing (640x480 @ 15fps)')
    
    try:
        while True:
            time.sleep(0.05)  # 20fps loop for smoother handling
    except KeyboardInterrupt:
        signal_handler(None, None)

except ImportError:
    print("❌ vilib not available")
    sys.exit(1)
except Exception as e:
    print(f"❌ Camera error: {e}")
    sys.exit(1)