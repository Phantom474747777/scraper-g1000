#!/usr/bin/env python3
"""
Scraper G1000 - Desktop Application
Launches Flask backend + PyWebView window
"""
import sys
import os
import threading
import time

print("[Startup] Python interpreter started")
print(f"[Startup] Python version: {sys.version}")
print(f"[Startup] Current directory: {os.getcwd()}")
print()

# Test imports one by one to identify failures
print("[Startup] Testing imports...")

try:
    import webview
    print("[Startup] ✓ webview imported")
except ImportError as e:
    print(f"[ERROR] Failed to import webview: {e}")
    print()
    print("Fix: Run INSTALL-DEPENDENCIES.bat")
    print()
    input("Press Enter to exit...")
    sys.exit(1)

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from backend.api_server import app as flask_app
    print("[Startup] ✓ Flask backend imported")
except ImportError as e:
    print(f"[ERROR] Failed to import Flask backend: {e}")
    print()
    print("Fix: Run INSTALL-DEPENDENCIES.bat")
    print()
    input("Press Enter to exit...")
    sys.exit(1)

print("[Startup] All imports successful")
print()

BACKEND_PORT = 5050
BACKEND_URL = f"http://localhost:{BACKEND_PORT}"

def start_flask_server():
    """Start Flask backend in a thread"""
    print("[Scraper G1000] Starting Flask backend...")
    flask_app.run(host='127.0.0.1', port=BACKEND_PORT, debug=False, threaded=True, use_reloader=False)

def wait_for_backend(max_retries=10):
    """Wait for Flask backend to be ready"""
    import urllib.request

    for i in range(max_retries):
        try:
            urllib.request.urlopen(f"{BACKEND_URL}/health", timeout=1)
            print("[Scraper G1000] Backend ready!")
            return True
        except:
            time.sleep(1)

    print("[Scraper G1000] Backend failed to start!")
    return False

class API:
    """JavaScript API exposed to the frontend"""

    def save_file(self, file_data, filename, file_format):
        """Open save dialog and write file"""
        try:
            import base64

            # Determine file type
            if file_format == 'xlsx':
                file_types = ('Excel Files (*.xlsx)', 'All Files (*.*)')
                default_ext = '.xlsx'
            else:
                file_types = ('CSV Files (*.csv)', 'All Files (*.*)')
                default_ext = '.csv'

            # Ensure filename has extension
            if not filename.endswith(default_ext):
                filename = f"{filename}{default_ext}"

            # Open save dialog
            result = webview.windows[0].create_file_dialog(
                webview.SAVE_DIALOG,
                save_filename=filename,
                file_types=file_types
            )

            if result:
                save_path = result if isinstance(result, str) else result[0]

                # Decode base64 data
                file_bytes = base64.b64decode(file_data)

                # Write file
                with open(save_path, 'wb') as f:
                    f.write(file_bytes)

                print(f"[Export] Saved file to: {save_path}")
                return {'success': True, 'path': save_path}
            else:
                print("[Export] User cancelled save dialog")
                return {'success': False, 'error': 'User cancelled'}

        except Exception as e:
            print(f"[Export] Error saving file: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}

def main():
    """Main application entry point"""
    print("=" * 60)
    print("   Scraper G1000 - Business Lead Generation")
    print("=" * 60)
    print()

    # Start Flask backend in background thread
    backend_thread = threading.Thread(target=start_flask_server, daemon=True)
    backend_thread.start()

    # Wait for backend to be ready
    if not wait_for_backend():
        print("[ERROR] Could not start backend server!")
        sys.exit(1)

    # Create PyWebView window
    print("[Scraper G1000] Launching desktop application...")

    # Copy UI files to temp location for PyWebView to serve
    import shutil
    from pathlib import Path

    # Use scraper-g1000-tauri/src as the UI source
    ui_source = Path(__file__).parent / "scraper-g1000-tauri" / "src"

    if not ui_source.exists():
        # Fallback to app folder if tauri folder doesn't exist
        ui_source = Path(__file__).parent / "app"

    # Create API instance
    api = API()

    # Create the window pointing to Flask server
    window = webview.create_window(
        title="Scraper G1000",
        url=f"{BACKEND_URL}/",  # Load UI from Flask backend
        width=1400,
        height=900,
        resizable=True,
        fullscreen=False,
        min_size=(1200, 800),
        background_color='#0D0D0D',
        js_api=api  # Expose API to JavaScript
    )

    # Start the GUI loop
    webview.start(debug=False)

    print("\n[Scraper G1000] Application closed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Scraper G1000] Interrupted by user")
        input("\nPress Enter to exit...")
        sys.exit(0)
    except Exception as e:
        print("\n" + "=" * 60)
        print("   FATAL ERROR")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        print("Full traceback:")
        print()
        import traceback
        traceback.print_exc()
        print()
        print("=" * 60)
        print()
        print("Common fixes:")
        print("  1. Run: INSTALL-DEPENDENCIES.bat")
        print("  2. Check logs folder for details")
        print("  3. Make sure port 5050 is not in use")
        print()
        input("Press Enter to exit...")
        sys.exit(1)
