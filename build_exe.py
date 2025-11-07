"""
Build script for creating Scraper G1000 executable
Creates a standalone .exe with icon
"""

import PyInstaller.__main__
import sys
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build arguments for PyInstaller
args = [
    'scraper-g1000.py',                    # Main script
    '--name=ScraperG1000',                 # Name of executable
    '--onefile',                           # Single executable file
    '--windowed',                          # No console window
    '--clean',                             # Clean cache
    '--noconfirm',                         # Don't ask for confirmation

    # Add data files
    f'--add-data={os.path.join(script_dir, "backend")}{os.pathsep}backend',
    f'--add-data={os.path.join(script_dir, "src")}{os.pathsep}src',
    f'--add-data={os.path.join(script_dir, "scraper-g1000-tauri", "src")}{os.pathsep}scraper-g1000-tauri/src',

    # Hidden imports that might not be detected
    '--hidden-import=flask',
    '--hidden-import=flask_cors',
    '--hidden-import=webview',
    '--hidden-import=sqlite3',
    '--hidden-import=openpyxl',
    '--hidden-import=requests',
    '--hidden-import=bs4',
    '--hidden-import=pgeocode',

    # Exclude unnecessary packages to reduce size
    '--exclude-module=matplotlib',
    '--exclude-module=numpy',
    '--exclude-module=pandas',
    '--exclude-module=PIL',

    # Output directory
    '--distpath=./dist',
    '--workpath=./build',
    '--specpath=.',
]

# Add icon if it exists
icon_path = os.path.join(script_dir, 'app_icon.ico')
if os.path.exists(icon_path):
    args.append(f'--icon={icon_path}')

print("=" * 60)
print("Building Scraper G1000 Executable")
print("=" * 60)
print()
print("This will create a standalone .exe file that you can")
print("double-click to run the app - no Python required!")
print()
print("Building...")
print()

# Run PyInstaller
PyInstaller.__main__.run(args)

print()
print("=" * 60)
print("BUILD COMPLETE!")
print("=" * 60)
print()
print("Your executable is in: ./dist/ScraperG1000.exe")
print()
print("You can now:")
print("1. Double-click ScraperG1000.exe to run")
print("2. Create a desktop shortcut to it")
print("3. Pin it to taskbar")
print()
