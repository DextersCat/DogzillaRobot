#!/usr/bin/env python3
"""
Quick patch to add missing React interface endpoints
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import subprocess

app = Flask(__name__)
CORS(app)

# Simple mock responses for the missing endpoints
@app.route('/api/camera/feed', methods=['GET'])
def camera_feed():
    return jsonify({
        'success': True,
        'url': None,
        'active': False,
        'message': 'Camera not implemented yet'
    })

@app.route('/api/sensors/lidar', methods=['GET'])
def sensors_lidar():
    return jsonify({
        'success': True,
        'sensors': [
            {'direction': 'Front-Left', 'distance': 0, 'status': 'offline'},
            {'direction': 'Front-Center', 'distance': 25, 'status': 'simulated'},
            {'direction': 'Front-Right', 'distance': 0, 'status': 'offline'}
        ]
    })

@app.route('/api/voice/quick', methods=['POST'])
def voice_quick():
    data = request.get_json()
    phrase = data.get('phrase', '')
    
    # Quick speech for testing
    try:
        subprocess.run(['espeak', '-a', '200', f'You said: {phrase}'], 
                      check=False, timeout=5)
    except:
        pass
    
    return jsonify({
        'success': True,
        'message': f'Quick command processed: {phrase}',
        'phrase': phrase,
        'timestamp': time.time()
    })

@app.route('/api/voice/complex', methods=['POST'])
def voice_complex():
    data = request.get_json()
    command = data.get('command', '')
    
    return jsonify({
        'success': True,
        'message': f'Complex command processed: {command}',
        'command': command,
        'timestamp': time.time()
    })

@app.route('/api/settings/safe-mode', methods=['POST'])
def settings_safe_mode():
    data = request.get_json()
    enabled = data.get('enabled', False)
    
    return jsonify({
        'success': True,
        'enabled': enabled,
        'message': f'Desk safe mode {"enabled" if enabled else "disabled"}',
        'timestamp': time.time()
    })

@app.route('/api/settings/camera', methods=['POST'])
def settings_camera():
    data = request.get_json()
    enabled = data.get('enabled', False)
    
    return jsonify({
        'success': True,
        'enabled': enabled,
        'message': f'Camera {"enabled" if enabled else "disabled"}',
        'timestamp': time.time()
    })

@app.route('/api/settings/audio-feedback', methods=['POST'])
def settings_audio_feedback():
    data = request.get_json()
    enabled = data.get('enabled', False)
    
    return jsonify({
        'success': True,
        'enabled': enabled,
        'message': f'Audio feedback {"enabled" if enabled else "disabled"}',
        'timestamp': time.time()
    })

if __name__ == '__main__':
    print("🔧 Starting API patch server on port 5002...")
    app.run(host='0.0.0.0', port=5002, debug=False)