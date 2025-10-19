#!/usr/bin/env python3
"""
PyWebView Desktop Wrapper for Scraper G1000
Serves frontend files directly - no separate dev server needed
"""
import webview
import sys
import os
import threading
import time
from flask import Flask, send_from_directory

# Setup Flask to serve frontend files
frontend_app = Flask(__name__, static_folder='src', static_url_path='')

@frontend_app.route('/')
def index():
    return send_from_directory('src', 'index.html')

@frontend_app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('src', path)

def start_frontend_server():
    """Start Flask server for frontend files on port 8080"""
    frontend_app.run(host='127.0.0.1', port=8080, debug=False, threaded=True)

def check_backend():
    """Wait for backend API server to be ready"""
    import requests
    print("[PyWebView] Waiting for backend API server on port 5050...")
    for i in range(30):
        try:
            r = requests.get('http://localhost:5050/health', timeout=1)
            if r.status_code == 200:
                print("[PyWebView] Backend is ready!")
                return True
        except:
            time.sleep(0.5)
    return False

if __name__ == '__main__':
    # Check if backend is running
    if not check_backend():
        print("[ERROR] Backend API server not running on port 5050")
        print("[ERROR] Please start backend/api_server.py first")
        input("Press Enter to exit...")
        sys.exit(1)

    # Start frontend file server in background thread
    print("[PyWebView] Starting frontend file server on port 8080...")
    frontend_thread = threading.Thread(target=start_frontend_server, daemon=True)
    frontend_thread.start()

    # Wait for frontend server to start
    time.sleep(2)

    # Create desktop window
    print("[PyWebView] Creating desktop window...")
    window = webview.create_window(
        'Scraper G1000 - Business Lead Generation',
        'http://localhost:8080/index.html',
        width=1400,
        height=900,
        resizable=True,
        background_color='#1a1a1a'
    )

    print("[PyWebView] Launching application...")
    webview.start()

    print("[PyWebView] Application closed")
