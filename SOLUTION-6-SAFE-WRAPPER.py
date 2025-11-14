#!/usr/bin/env python3
"""
Safe wrapper that catches ALL errors and displays them
"""
import sys
import os
import traceback
from datetime import datetime

def main():
    print("=" * 70)
    print(" SCRAPER G1000 - SAFE MODE LAUNCHER")
    print("=" * 70)
    print()
    print(f"Started at: {datetime.now()}")
    print(f"Python: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print()
    print("-" * 70)
    print()

    try:
        # Import and run the actual app
        print("Loading scraper-g1000.py...")
        print()

        # Execute the main script
        with open('scraper-g1000.py', 'r', encoding='utf-8') as f:
            code = f.read()

        exec(code, {'__name__': '__main__', '__file__': 'scraper-g1000.py'})

    except SystemExit as e:
        print()
        print("-" * 70)
        print(f"Application exited with code: {e.code}")

    except Exception as e:
        print()
        print("=" * 70)
        print(" FATAL ERROR CAUGHT")
        print("=" * 70)
        print()
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        print()
        print("Full Traceback:")
        print("-" * 70)
        traceback.print_exc()
        print("-" * 70)
        print()
        print("SAVE THIS ERROR MESSAGE AND SEND IT FOR DEBUGGING")
        print()

        # Write to error log
        error_file = f"ERROR_LOG_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(error_file, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("SCRAPER G1000 ERROR LOG\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Python Version: {sys.version}\n\n")
            f.write(f"Error Type: {type(e).__name__}\n")
            f.write(f"Error Message: {e}\n\n")
            f.write("Full Traceback:\n")
            f.write("-" * 70 + "\n")
            traceback.print_exc(file=f)
            f.write("-" * 70 + "\n")

        print(f"Error saved to: {error_file}")
        print()

    finally:
        print()
        print("=" * 70)
        print(" Press ENTER to close this window...")
        print("=" * 70)
        input()

if __name__ == '__main__':
    main()
