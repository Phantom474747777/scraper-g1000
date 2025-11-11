"""
Auto-creates Scraper G1000 desktop launcher with custom icon
Run this once and the app appears on your desktop
"""
import os
from pathlib import Path
import sys
from win32com.client import Dispatch

# Get current directory (where the app is)
app_dir = os.path.dirname(os.path.abspath(__file__))

# Get desktop path
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Get Python executable path (the one currently running this script)
python_exe = sys.executable

# Create the launcher BAT file in the project folder (not on desktop)
launcher_content = f"""@echo off
cd /d "{app_dir}"
start "" "{python_exe}" scraper-g1000.py
exit
"""

# Write launcher.bat to project folder
launcher_bat = os.path.join(app_dir, "launch_app.bat")
with open(launcher_bat, 'w') as f:
    f.write(launcher_content)

print("✓ Created launcher script")

# Create shortcut on desktop pointing to the .bat file
shortcut_path = os.path.join(desktop, "Scraper G1000.lnk")

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.TargetPath = launcher_bat
shortcut.WorkingDirectory = app_dir
shortcut.Description = "Scraper G1000 - Business Lead Generation"

# Set icon if it exists
icon_path = os.path.join(app_dir, "scraper_icon.ico")
if os.path.exists(icon_path):
    shortcut.IconLocation = icon_path
    print("✓ Icon applied to shortcut")
else:
    print("⚠ Icon file not found - run create_icon.py first")

shortcut.save()
print("✓ Desktop shortcut created with icon")

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
