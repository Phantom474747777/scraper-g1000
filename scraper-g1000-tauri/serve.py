#!/usr/bin/env python3
"""
Simple HTTP server to serve Tauri frontend during development
"""
import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = "src"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

os.chdir(os.path.dirname(__file__))

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"[Dev Server] Serving {DIRECTORY} on http://localhost:{PORT}")
    print(f"[Dev Server] Press Ctrl+C to stop")
    httpd.serve_forever()
