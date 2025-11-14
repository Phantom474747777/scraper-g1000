#!/usr/bin/env python3
"""
Standalone diagnostic - Run this with: python diagnostic.py
"""
import sys
import os
import subprocess
from datetime import datetime

LOG_FILE = "FULL-DIAGNOSTIC.txt"

def write_log(message):
    """Write to both console and log file"""
    print(message)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

def main():
    # Clear log file
    open(LOG_FILE, 'w').close()

    write_log("=" * 70)
    write_log("SCRAPER G1000 - FULL DIAGNOSTIC")
    write_log("=" * 70)
    write_log(f"Timestamp: {datetime.now()}")
    write_log(f"Python Version: {sys.version}")
    write_log(f"Python Executable: {sys.executable}")
    write_log(f"Current Directory: {os.getcwd()}")
    write_log("")

    write_log("=" * 70)
    write_log("STEP 1: Testing Standard Library Imports")
    write_log("=" * 70)

    modules_to_test = [
        'sys', 'os', 'threading', 'time', 'sqlite3',
        'pathlib', 'json', 'urllib', 'datetime'
    ]

    for module in modules_to_test:
        try:
            __import__(module)
            write_log(f"✓ {module}")
        except ImportError as e:
            write_log(f"✗ {module} - {e}")

    write_log("")
    write_log("=" * 70)
    write_log("STEP 2: Testing Required Packages")
    write_log("=" * 70)

    packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'webview': 'PyWebView',
        'bs4': 'BeautifulSoup4',
        'openpyxl': 'OpenPyXL',
        'pydantic': 'Pydantic',
        'geopy': 'Geopy',
        'pgeocode': 'PGeocode',
        'nest_asyncio': 'Nest-Asyncio',
        'dotenv': 'Python-Dotenv',
        'requests': 'Requests'
    }

    missing = []
    for module, name in packages.items():
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'OK')
            write_log(f"✓ {name}: {version}")
        except ImportError as e:
            write_log(f"✗ {name}: MISSING - {e}")
            missing.append(name)

    if missing:
        write_log("")
        write_log("!" * 70)
        write_log("MISSING PACKAGES DETECTED:")
        for pkg in missing:
            write_log(f"  - {pkg}")
        write_log("")
        write_log("FIX: Run INSTALL-DEPENDENCIES.bat")
        write_log("!" * 70)

    write_log("")
    write_log("=" * 70)
    write_log("STEP 3: Testing App Imports")
    write_log("=" * 70)

    try:
        write_log("Importing backend.api_server...")
        from backend.api_server import app as flask_app
        write_log("✓ Backend imported successfully")
    except Exception as e:
        write_log(f"✗ Backend import failed: {e}")
        import traceback
        write_log(traceback.format_exc())

    write_log("")
    write_log("=" * 70)
    write_log("STEP 4: Attempting to Start App")
    write_log("=" * 70)

    try:
        write_log("Importing scraper-g1000.py...")
        with open('scraper-g1000.py', 'r', encoding='utf-8') as f:
            code = f.read()

        write_log("Executing main application...")
        exec(code)

    except Exception as e:
        write_log(f"✗ App startup failed: {e}")
        import traceback
        write_log(traceback.format_exc())

    write_log("")
    write_log("=" * 70)
    write_log("DIAGNOSTIC COMPLETE")
    write_log("=" * 70)
    write_log(f"Log saved to: {LOG_FILE}")
    write_log("")

    input("Press Enter to exit...")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n\nFATAL ERROR: {e}\n")
            import traceback
            f.write(traceback.format_exc())
        print(f"Fatal error. Check {LOG_FILE}")
        input("Press Enter to exit...")
