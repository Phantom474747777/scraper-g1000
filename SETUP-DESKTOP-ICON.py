"""
Auto-creates Scraper G1000 desktop launcher
Run this once and the app appears on your desktop
"""
import os
from pathlib import Path
import sys

# Get current directory (where the app is)
app_dir = os.path.dirname(os.path.abspath(__file__))

# Get desktop path
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Get Python executable path (the one currently running this script)
python_exe = sys.executable

# Create the launcher script with FULL Python path
launcher_content = f"""@echo off
cd /d "{app_dir}"
start "" "{python_exe}" scraper-g1000.py
exit
"""

# Write to desktop
launcher_path = os.path.join(desktop, "Scraper G1000.bat")

with open(launcher_path, 'w') as f:
    f.write(launcher_content)

print("=" * 60)
print("SUCCESS!")
print("=" * 60)
print()
print(f"Desktop launcher created: {launcher_path}")
print()
print("Go to your desktop and double-click:")
print("  'Scraper G1000.bat'")
print()
print("Your app will open!")
print()
print("=" * 60)
input("Press Enter to close...")
