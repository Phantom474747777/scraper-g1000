"""
Create desktop shortcut for ScraperG1000.exe
Automatically puts the app icon on your desktop
"""

import os
import winshell
from pathlib import Path

def create_desktop_shortcut():
    """Create a shortcut on the Windows desktop"""

    # Get the desktop path
    desktop = winshell.desktop()

    # Get the executable path
    script_dir = Path(__file__).parent
    exe_path = script_dir / "dist" / "ScraperG1000.exe"

    if not exe_path.exists():
        print(f"[ERROR] Executable not found: {exe_path}")
        print("Please build the app first!")
        return False

    # Create shortcut path
    shortcut_path = os.path.join(desktop, "Scraper G1000.lnk")

    # Create the shortcut
    with winshell.shortcut(shortcut_path) as shortcut:
        shortcut.path = str(exe_path)
        shortcut.description = "Scraper G1000 - Business Lead Generation"
        shortcut.working_directory = str(script_dir)

        # Set icon (if available)
        icon_path = script_dir / "app_icon.ico"
        if icon_path.exists():
            shortcut.icon_location = (str(icon_path), 0)

    print(f"✓ Desktop shortcut created!")
    print(f"  Location: {shortcut_path}")
    print()
    print("Check your desktop - the Scraper G1000 icon should be there!")

    return True

if __name__ == "__main__":
    print()
    print("=" * 60)
    print("Creating Desktop Shortcut")
    print("=" * 60)
    print()

    success = create_desktop_shortcut()

    if success:
        print()
        print("=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print()
        print("Look at your desktop - double-click the icon to launch!")
    else:
        print()
        print("Failed to create shortcut.")
        print("You can manually create one by right-clicking")
        print("dist\\ScraperG1000.exe > Send to > Desktop")

    input("\nPress Enter to close...")
