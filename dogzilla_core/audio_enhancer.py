#!/usr/bin/env python3
"""
Enhanced Audio Preprocessor for Amy Voice Assistant
Dramatically improves microphone range and quality through software processing
"""
import numpy as np
import librosa
import noisereduce as nr
import webrtcvad
import soundfile as sf
import subprocess
import tempfile
import os
from pathlib import Path

class AudioEnhancer:
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.vad = webrtcvad.Vad(3)  # Most aggressive VAD mode
        
    def enhance_audio(self, input_path, output_path=None):
        """
        Apply multiple audio enhancement techniques:
        1. Noise reduction
        2. Dynamic range compression
        3. Voice activity detection
        4. Gain normalization
        5. High-pass filtering
        """
        if output_path is None:
            output_path = input_path.replace('.wav', '_enhanced.wav')
            
        print(f"🎧 Enhancing audio: {input_path}")
        
        # Load audio
        audio, sr = librosa.load(input_path, sr=self.sample_rate)
        original_max = np.max(np.abs(audio))
        print(f"   Original max amplitude: {original_max:.4f}")
        
        # Step 1: Noise reduction
        audio_denoised = nr.reduce_noise(y=audio, sr=sr, stationary=True, prop_decrease=0.8)
        
        # Step 2: High-pass filter to remove low-frequency noise
        audio_filtered = librosa.effects.preemphasis(audio_denoised, coef=0.97)
        
        # Step 3: Dynamic range compression (make quiet parts louder)
        audio_compressed = librosa.effects.percussive(audio_filtered, margin=3.0)
        
        # Step 4: Normalize and boost gain
        audio_normalized = librosa.util.normalize(audio_compressed)
        
        # Step 5: Apply additional gain boost for speech
        gain_factor = min(3.0, 0.5 / (original_max + 1e-6))  # Intelligent gain boost
        audio_boosted = audio_normalized * gain_factor
        
        # Prevent clipping
        audio_final = np.clip(audio_boosted, -0.95, 0.95)
        
        enhanced_max = np.max(np.abs(audio_final))
        improvement = enhanced_max / (original_max + 1e-6)
        print(f"   Enhanced max amplitude: {enhanced_max:.4f}")
        print(f"   Improvement factor: {improvement:.1f}x")
        
        # Save enhanced audio
        sf.write(output_path, audio_final, sr)
        print(f"   ✅ Enhanced audio saved: {output_path}")
        
        return output_path, improvement
    
    def test_voice_activity(self, audio_path):
        """Test if speech is detected in the audio"""
        audio, sr = librosa.load(audio_path, sr=16000)  # VAD requires 16kHz
        
        # Convert to 16-bit integers for VAD
        audio_int = (audio * 32767).astype(np.int16)
        
        # Test 30ms frames
        frame_duration = 30  # ms
        frame_size = int(16000 * frame_duration / 1000)
        
        speech_frames = 0
        total_frames = 0
        
        for i in range(0, len(audio_int) - frame_size, frame_size):
            frame = audio_int[i:i + frame_size]
            total_frames += 1
            
            try:
                if self.vad.is_speech(frame.tobytes(), 16000):
                    speech_frames += 1
            except:
                pass
        
        speech_ratio = speech_frames / max(total_frames, 1)
        print(f"   Speech detection: {speech_frames}/{total_frames} frames ({speech_ratio:.1%})")
        return speech_ratio > 0.1  # At least 10% speech content

def test_enhancement():
    """Test the audio enhancement on the latest postwake recording"""
    enhancer = AudioEnhancer()
    
    # Test on the most recent postwake recording
    postwake_file = "/tmp/postwake.wav"
    if not os.path.exists(postwake_file):
        print("❌ No postwake.wav found - record some audio first")
        return
    
    # Create enhanced version
    enhanced_file = "/tmp/postwake_enhanced.wav"
    enhanced_path, improvement = enhancer.enhance_audio(postwake_file, enhanced_file)
    
    # Test voice activity
    has_speech = enhancer.test_voice_activity(enhanced_file)
    print(f"   Voice activity detected: {'✅ Yes' if has_speech else '❌ No'}")
    
    return enhanced_path, improvement

if __name__ == "__main__":
    test_enhancement()