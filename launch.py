#!/usr/bin/env python3
"""
Pre-flight check - Verify all dependencies before launching main app
"""
import sys
import os

def check_imports():
    """Check all required imports"""
    errors = []

    # Standard library (should always work)
    try:
        import threading, time, sqlite3, pathlib, json, datetime, re, hashlib, typing
    except ImportError as e:
        errors.append(f"Standard library error: {e}")

    # Required packages
    required = {
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

    for module, name in required.items():
        try:
            __import__(module)
        except ImportError:
            errors.append(f"Missing package: {name}")

    return errors

def main():
    print("=" * 60)
    print("  SCRAPER G1000 - PRE-FLIGHT CHECK")
    print("=" * 60)
    print()

    print("Checking dependencies...")
    errors = check_imports()

    if errors:
        print()
        print("ERROR: Missing dependencies detected:")
        print()
        for error in errors:
            print(f"  ✗ {error}")
        print()
        print("Installing missing packages...")
        print()

        import subprocess
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '--quiet',
            'Flask', 'flask-cors', 'pywebview', 'beautifulsoup4',
            'openpyxl', 'pydantic', 'geopy', 'pgeocode',
            'nest-asyncio', 'python-dotenv', 'requests'
        ])

        if result.returncode == 0:
            print("✓ Installation complete!")
            print()
            # Re-check
            errors = check_imports()
            if errors:
                print("ERROR: Some packages still missing:")
                for error in errors:
                    print(f"  ✗ {error}")
                return False
        else:
            print("✗ Installation failed")
            return False

    print("✓ All dependencies OK!")
    print()

    # Try to import the main app
    try:
        print("Loading main application...")
        sys.path.insert(0, os.path.dirname(__file__))

        # Import scraper-g1000.py
        with open('scraper-g1000.py', 'r', encoding='utf-8') as f:
            code = f.read()

        exec(code, {'__name__': '__main__', '__file__': 'scraper-g1000.py'})
        return True

    except Exception as e:
        print()
        print("=" * 60)
        print("  ERROR STARTING APPLICATION")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    try:
        success = main()
        if not success:
            input("\nPress Enter to exit...")
            sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
