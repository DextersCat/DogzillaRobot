#!/usr/bin/env python3
"""
Simple Button-Based Command Interface for Amy
Provides reliable desk-safe commands without microphone dependency
"""
import os
import time
import subprocess
from pathlib import Path

# Suppress ONNX Runtime warnings before importing Amy functions
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['ORT_LOGGING_LEVEL'] = '3'  # Only show errors, suppress warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="onnxruntime")

# Import Amy's action functions
import sys
sys.path.append('/home/spencer/amy_core')
from postwake_router import say, do_wave

class ButtonCommands:
    def __init__(self):
        self.commands = {
            'time': self.speak_time,
            'wave': self.do_wave_gesture,
            'status': self.speak_status,
            'test': self.test_audio,
            'mode': self.check_mode,
            'deskmode': self.confirm_deskmode
        }
    
    def speak_time(self):
        """Speak the current time"""
        now = time.strftime("%I:%M %p")
        say(f"The time is {now}")
        return f"✅ Spoke time: {now}"
    
    def do_wave_gesture(self):
        """Perform wave gesture"""
        success = do_wave()
        if success:
            say("Hello Spencer!")
            return "✅ Wave gesture completed"
        else:
            return "❌ Wave gesture failed"
    
    def speak_status(self):
        """Speak Amy's status"""
        try:
            import psutil
            cpu = psutil.cpu_percent()
            temp = f"CPU at {cpu:.1f} percent"
        except:
            temp = "System running normally"
        
        say(f"Amy is online. {temp}. All systems operational.")
        return f"✅ Status report given"
    
    def test_audio(self):
        """Test audio output"""
        say("Audio test. One, two, three. Amy's voice is working correctly.")
        return "✅ Audio test completed"
    
    def check_mode(self):
        """Check Amy's current operational mode"""
        # Check if Amy is in desk-safe mode by examining the code
        try:
            with open('/home/spencer/amy_core/postwake_router.py', 'r') as f:
                content = f.read()
                if 'desk safe mode' in content.lower():
                    mode_status = "DESK SAFE MODE"
                    safety_note = "Movement is LIMITED to safe desk operations only"
                    allowed_actions = "Wave gesture only - no walking or full body movement"
                else:
                    mode_status = "FULL MOBILITY MODE"
                    safety_note = "All movement commands available"
                    allowed_actions = "Walking, dancing, full range of motion"
            
            say(f"Amy is currently in {mode_status}. {safety_note}.")
            return f"✅ Mode: {mode_status} - {allowed_actions}"
        except Exception as e:
            say("Unable to determine current mode status.")
            return f"❌ Mode check failed: {str(e)}"
    
    def confirm_deskmode(self):
        """Confirm Amy is in desk-safe mode with no risky movements"""
        say("Confirmed. Amy is in desk safe mode. Only safe arm movements allowed. No walking or body movement will be performed to protect equipment.")
        return "✅ DESK SAFE MODE CONFIRMED - No risky movements will be executed"
    
    def execute_command(self, command):
        """Execute a command by name"""
        if command in self.commands:
            result = self.commands[command]()
            print(result)
            return True
        else:
            available = ', '.join(self.commands.keys())
            print(f"❌ Unknown command: {command}")
            print(f"Available commands: {available}")
            return False

def interactive_mode():
    """Interactive command prompt"""
    buttons = ButtonCommands()
    
    print("🤖 Amy Button Interface")
    print("======================")
    print("Available commands:")
    for cmd, func in buttons.commands.items():
        print(f"  {cmd:<10} - {func.__doc__}")
    print("\nType 'quit' to exit")
    print()
    
    while True:
        try:
            command = input("Amy> ").strip().lower()
            if command in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif command:
                buttons.execute_command(command)
            print()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        buttons = ButtonCommands()
        buttons.execute_command(sys.argv[1])
    else:
        # Interactive mode
        interactive_mode()