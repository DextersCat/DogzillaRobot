#!/usr/bin/env python3
"""
Desk Mode Ultrasonic Sensor Test
Testing ultrasonic sensor while Amy is on desk - expect short distance readings
"""

from robot_hat import Ultrasonic, Pin
import time

def desk_ultrasonic_test():
    """Test ultrasonic sensor in desk environment"""
    print("📡 Starting desk mode ultrasonic sensor test...")
    print("Expected: Short distance readings from desk surface")
    
    try:
        # Initialize ultrasonic sensor
        # Trig -> D2 (GPIO27), Echo -> D3 (GPIO22)
        print("🔧 Initializing ultrasonic sensor on pins D2 (trig) and D3 (echo)...")
        sonar = Ultrasonic(Pin("D2"), Pin("D3"))
        
        print("✅ Ultrasonic sensor initialized!")
        print("\n📏 Taking distance measurements...")
        print("Note: On desk, expect readings of 5-15cm (desk surface)")
        
        readings = []
        
        for i in range(10):
            distance = sonar.read()
            
            if distance > 0:
                readings.append(distance)
                print(f"📐 Reading {i+1}: {distance:.2f} cm")
            else:
                print(f"❌ Reading {i+1}: Failed (timeout or error)")
            
            time.sleep(0.5)
        
        # Analyze readings
        if readings:
            avg_distance = sum(readings) / len(readings)
            min_distance = min(readings)
            max_distance = max(readings)
            
            print(f"\n📊 Analysis:")
            print(f"   Valid readings: {len(readings)}/10")
            print(f"   Average distance: {avg_distance:.2f} cm")
            print(f"   Min distance: {min_distance:.2f} cm")
            print(f"   Max distance: {max_distance:.2f} cm")
            
            # Desk mode interpretation
            if avg_distance < 20:
                print("✅ Readings consistent with desk surface detection")
            elif avg_distance < 50:
                print("⚠️  Moderate distance - might be detecting desk edge")
            else:
                print("📏 Long distance - sensor looking past desk")
            
            return True
        else:
            print("❌ No valid readings obtained")
            return False
            
    except Exception as e:
        print(f"❌ Sensor error: {e}")
        return False

def continuous_monitoring():
    """Continuous monitoring for manual testing"""
    print("\n🔄 Starting continuous monitoring...")
    print("Wave your hand in front of the sensor to test detection")
    print("Press Ctrl+C to stop")
    
    try:
        sonar = Ultrasonic(Pin("D2"), Pin("D3"))
        
        last_distance = -1
        
        while True:
            distance = sonar.read()
            
            if distance > 0:
                # Only print if distance changed significantly (> 2cm)
                if abs(distance - last_distance) > 2:
                    print(f"📏 Distance: {distance:.2f} cm", end="")
                    
                    # Provide context for desk environment
                    if distance < 10:
                        print(" (very close - desk surface)")
                    elif distance < 20:
                        print(" (close - normal desk range)")
                    elif distance < 50:
                        print(" (moderate - hand/object)")
                    else:
                        print(" (far - past desk edge)")
                    
                    last_distance = distance
            else:
                if last_distance >= 0:  # Only print once per error
                    print("❌ Sensor timeout/error")
                    last_distance = -1
            
            time.sleep(0.2)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")
    except Exception as e:
        print(f"\n❌ Monitoring error: {e}")

def main():
    """Main test function"""
    print("🤖 Amy Desk Mode Ultrasonic Test")
    print("=" * 40)
    
    # Basic functionality test
    success = desk_ultrasonic_test()
    
    if success:
        print("\n🎉 Ultrasonic sensor test passed!")
        
        # Ask if user wants continuous monitoring
        try:
            response = input("\nRun continuous monitoring? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                continuous_monitoring()
        except KeyboardInterrupt:
            pass
    else:
        print("\n❌ Ultrasonic sensor test failed")
        print("Check connections: Trig->D2, Echo->D3, VCC->5V, GND->GND")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")