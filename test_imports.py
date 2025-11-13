#!/usr/bin/env python3
"""
Test all imports to diagnose startup issues
"""
import sys

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✓ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"✗ {package_name or module_name} - MISSING")
        print(f"  Error: {e}")
        return False
    except Exception as e:
        print(f"✗ {package_name or module_name} - ERROR")
        print(f"  Error: {e}")
        return False

def main():
    print("=" * 60)
    print("   Scraper G1000 - Import Test")
    print("=" * 60)
    print()
    print("Testing standard library imports...")
    print()

    all_ok = True

    # Standard library
    all_ok &= test_import('sys')
    all_ok &= test_import('os')
    all_ok &= test_import('threading')
    all_ok &= test_import('time')
    all_ok &= test_import('sqlite3')
    all_ok &= test_import('pathlib')
    all_ok &= test_import('json')
    all_ok &= test_import('urllib.request', 'urllib')
    all_ok &= test_import('datetime')
    all_ok &= test_import('re')
    all_ok &= test_import('hashlib')
    all_ok &= test_import('typing')

    print()
    print("Testing third-party packages...")
    print()

    # Required packages
    all_ok &= test_import('flask', 'Flask')
    all_ok &= test_import('flask_cors', 'Flask-CORS')
    all_ok &= test_import('webview', 'PyWebView')
    all_ok &= test_import('bs4', 'BeautifulSoup4')
    all_ok &= test_import('openpyxl', 'OpenPyXL')
    all_ok &= test_import('pydantic', 'Pydantic')
    all_ok &= test_import('geopy', 'Geopy')
    all_ok &= test_import('pgeocode', 'PGeocode')
    all_ok &= test_import('nest_asyncio', 'Nest-Asyncio')
    all_ok &= test_import('dotenv', 'Python-Dotenv')
    all_ok &= test_import('requests', 'Requests')

    print()
    print("Testing application modules...")
    print()

    # Local modules
    all_ok &= test_import('src.profile_manager')
    all_ok &= test_import('src.database')
    all_ok &= test_import('src.zip_lookup')
    all_ok &= test_import('src.validators')
    all_ok &= test_import('backend.api_server')

    print()
    print("=" * 60)
    if all_ok:
        print("   ALL IMPORTS SUCCESSFUL ✓")
        print("=" * 60)
        print()
        print("The application should work!")
        return 0
    else:
        print("   SOME IMPORTS FAILED ✗")
        print("=" * 60)
        print()
        print("Run INSTALL-DEPENDENCIES.bat to fix missing packages.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
