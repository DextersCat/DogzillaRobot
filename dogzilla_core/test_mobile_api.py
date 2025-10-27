#!/usr/bin/env python3
"""
Quick Mobile App Test
Test all mobile app functionality from command line
"""

import requests
import json
import time

API_BASE = "http://192.168.1.4:5001"

def test_api():
    """Test all API endpoints"""
    print("🧪 Testing Amy Mobile API...")
    
    # Test status
    try:
        response = requests.get(f"{API_BASE}/api/status")
        print(f"📊 Status: {response.json()}")
    except Exception as e:
        print(f"❌ Status test failed: {e}")
    
    # Test sensors
    try:
        response = requests.get(f"{API_BASE}/api/sensors")
        data = response.json()
        print(f"📏 Distance: {data['distance']:.1f}cm")
        print(f"👤 Faces: {data['faces']}")
        print(f"🔋 Battery: {data['battery_voltage']:.2f}V ({data['battery_percentage']:.1f}%)")
    except Exception as e:
        print(f"❌ Sensor test failed: {e}")
    
    # Test speak command
    try:
        response = requests.post(f"{API_BASE}/api/command", 
                               json={"command": "speak", "params": {"text": "Mobile app test successful"}})
        result = response.json()
        print(f"🔊 Speak test: {result}")
    except Exception as e:
        print(f"❌ Speak test failed: {e}")
    
    # Test photo command
    try:
        response = requests.post(f"{API_BASE}/api/photo")
        result = response.json()
        print(f"📸 Photo test: {result}")
    except Exception as e:
        print(f"❌ Photo test failed: {e}")
    
    print("✅ API tests completed!")

if __name__ == "__main__":
    test_api()