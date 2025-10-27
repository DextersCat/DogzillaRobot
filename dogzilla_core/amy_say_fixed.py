#!/usr/bin/env python3
"""
Fixed Amy Say script for mobile app TTS
Uses Piper TTS with Robot HAT speaker
"""
import subprocess
import tempfile
import os
import sys

def amy_say(text):
    """Make Amy speak using Piper TTS and Robot HAT speaker"""
    try:
        # Turn on amp
        subprocess.run(['/home/spencer/bin/amp_on.sh'], check=False)
        
        # Create temp WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
            temp_path = temp_wav.name
        
        # Generate speech with Piper
        piper_cmd = [
            '/home/spencer/bin/piper',
            '--model', '/home/spencer/voices/en_US-amy-medium.onnx',
            '--output', temp_path
        ]
        
        result = subprocess.run(piper_cmd, input=text, text=True, check=True)
        
        # Play with correct audio device
        aplay_cmd = [
            'aplay',
            '-D', 'plughw:2,0',
            temp_path
        ]
        
        subprocess.run(aplay_cmd, check=True)
        
        return True
        
    except Exception as e:
        print(f"Error in amy_say: {e}")
        return False
    finally:
        # Clean up temp file
        try:
            os.unlink(temp_path)
        except:
            pass

if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Hello, I am Amy."
    amy_say(text)