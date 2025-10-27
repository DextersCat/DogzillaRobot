#!/usr/bin/env python3
"""
Dogzilla S2 Hardware Test Script
Tests all major hardware components during setup
"""
import sys
import time
import subprocess

def test_servo_control():
    """Test servo control system"""
    print("🦵 Testing servo control...")
    try:
        sys.path.append('/home/spencer/picrawler')
        from picrawler import Picrawler
        
        dog = Picrawler()
        print("✅ Picrawler library loaded successfully")
        
        # Test basic stand position
        print("   Testing stand position...")
        dog.do_step('stand', 50)
        time.sleep(2)
        
        # Test sit position
        print("   Testing sit position...")
        dog.do_step('sit', 50)
        time.sleep(2)
        
        print("✅ Servo control test PASSED")
        return True
        
    except ImportError as e:
        print(f"❌ Servo control test FAILED: Missing library - {e}")
        return False
    except Exception as e:
        print(f"❌ Servo control test FAILED: {e}")
        return False

def test_camera():
    """Test camera functionality"""
    print("📷 Testing camera...")
    try:
        # Test rpicam-still
        result = subprocess.run(['rpicam-still', '--timeout', '1000', '--output', '/tmp/dogzilla_test.jpg'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Camera test PASSED")
            subprocess.run(['rm', '-f', '/tmp/dogzilla_test.jpg'], check=False)
            return True
        else:
            print(f"❌ Camera test FAILED: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Camera test FAILED: Timeout")
        return False
    except Exception as e:
        print(f"❌ Camera test FAILED: {e}")
        return False

def test_audio():
    """Test audio output"""
    print("🔊 Testing audio output...")
    try:
        # Test espeak
        result = subprocess.run(['espeak', '-a', '200', 'Dogzilla audio test'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ Audio test PASSED")
            return True
        else:
            print(f"❌ Audio test FAILED: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Audio test FAILED: Timeout")
        return False
    except Exception as e:
        print(f"❌ Audio test FAILED: {e}")
        return False

def test_network():
    """Test network connectivity"""
    print("🌐 Testing network connectivity...")
    try:
        # Test local network
        result = subprocess.run(['ping', '-c', '1', '192.168.1.1'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ Network test PASSED")
            return True
        else:
            print("❌ Network test FAILED: No gateway response")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Network test FAILED: Timeout")
        return False
    except Exception as e:
        print(f"❌ Network test FAILED: {e}")
        return False

def test_system_resources():
    """Test system resources"""
    print("💻 Testing system resources...")
    try:
        import psutil
        
        # Check CPU temperature
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = int(f.read()) / 1000
            print(f"   CPU Temperature: {temp:.1f}°C")
            if temp < 70:
                print("✅ Temperature normal")
            else:
                print("⚠️ Temperature high - check cooling")
        except:
            print("⚠️ Could not read temperature")
        
        # Check memory
        memory = psutil.virtual_memory()
        print(f"   RAM Usage: {memory.percent:.1f}% ({memory.used // 1024**3:.1f}GB / {memory.total // 1024**3:.1f}GB)")
        
        # Check disk space
        disk = psutil.disk_usage('/')
        print(f"   Disk Usage: {disk.percent:.1f}% ({disk.used // 1024**3:.1f}GB / {disk.total // 1024**3:.1f}GB)")
        
        print("✅ System resources test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ System resources test FAILED: {e}")
        return False

def main():
    """Run all hardware tests"""
    print("🐕🦖 DOGZILLA S2 HARDWARE TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("System Resources", test_system_resources),
        ("Network", test_network),
        ("Audio", test_audio),
        ("Camera", test_camera),
        ("Servo Control", test_servo_control),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
        
        if result:
            print(f"✅ {test_name} test completed successfully")
        else:
            print(f"❌ {test_name} test failed")
    
    # Summary
    print("\n" + "=" * 50)
    print("🐕🦖 DOGZILLA HARDWARE TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 ALL TESTS PASSED - Dogzilla hardware is ready!")
        return True
    else:
        print("⚠️ Some tests failed - check hardware connections")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)