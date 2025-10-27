#!/usr/bin/env python3
"""
Simple HTTP server for Astra Web Control Panel
Serves the HTML interface on port 8080
"""

import http.server
import socketserver
import os
from pathlib import Path

# Change to the directory containing the HTML file
web_dir = Path('/home/spencer/amy_core')
os.chdir(web_dir)

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

class CORSHandler(Handler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CORSHandler) as httpd:
        print(f"🌐 Astra Web Control Panel")
        print(f"📱 Serving at: http://192.168.1.4:{PORT}/astra_web_control.html")
        print(f"💻 Local access: http://localhost:{PORT}/astra_web_control.html")
        print(f"🔗 Bookmark this URL for easy access!")
        print(f"🛑 Press Ctrl+C to stop")
        httpd.serve_forever()