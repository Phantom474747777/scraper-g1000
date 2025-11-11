"""
ALL-IN-ONE Desktop Icon Creator
Generates icon and creates desktop shortcut in ONE step
"""
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw
import math

print("=" * 60)
print("SCRAPER G1000 - DESKTOP ICON CREATOR")
print("=" * 60)
print()

# Get paths
app_dir = os.path.dirname(os.path.abspath(__file__))
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
python_exe = sys.executable

print("[1/4] Creating lightning bulb icon...")

# ===== CREATE ICON =====
size = 256
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

center_x, center_y = size // 2, size // 2
max_radius = 118

# Electric blue gradient background
for i in range(100):
    progress = i / 100
    radius = int(max_radius * (1 - progress * 0.3))
    r = int(20 + progress * 80)
    g = int(40 + progress * 160)
    b = int(100 + progress * 155)
    alpha = int(200 + progress * 55)
    draw.ellipse([center_x - radius, center_y - radius,
                 center_x + radius, center_y + radius],
                fill=(r, g, b, alpha))

# Outer glow
for i in range(8):
    alpha = int(100 - i * 12)
    draw.ellipse([center_x - max_radius - i*2, center_y - max_radius - i*2,
                 center_x + max_radius + i*2, center_y + max_radius + i*2],
                outline=(0, 200, 255, alpha), width=2)

# Main border
draw.ellipse([center_x - max_radius, center_y - max_radius,
             center_x + max_radius, center_y + max_radius],
            outline=(0, 230, 255, 255), width=4)

# Light bulb
bulb_top, bulb_bottom = 70, 160
bulb_left, bulb_right = center_x - 45, center_x + 45

for i in range(30):
    alpha = int(180 - i * 3)
    draw.ellipse([bulb_left + i, bulb_top + i,
                 bulb_right - i, bulb_bottom - i//2],
                outline=(200, 230, 255, alpha), width=1)

draw.ellipse([bulb_left, bulb_top, bulb_right, bulb_bottom],
            outline=(220, 240, 255, 255), width=3)

# Screw threads
base_top = bulb_bottom - 5
for i in range(4):
    y = base_top + i * 6
    draw.rectangle([bulb_left, y, bulb_right, y + 3], fill=(180, 180, 200, 255))
    draw.rectangle([bulb_left, y + 3, bulb_right, y + 5], fill=(140, 140, 160, 255))

# Bottom cap
cap_y = base_top + 25
draw.ellipse([bulb_left - 3, cap_y - 3, bulb_right + 3, cap_y + 8],
            fill=(160, 160, 180, 255))

# Lightning bolt
bolt_scale = 0.8
lightning = [
    (center_x - 8*bolt_scale, 85),
    (center_x + 8*bolt_scale, 110),
    (center_x, 110),
    (center_x + 12*bolt_scale, 135),
    (center_x + 3*bolt_scale, 135),
    (center_x + 10*bolt_scale, 155),
    (center_x - 5*bolt_scale, 125),
    (center_x + 3*bolt_scale, 125),
    (center_x - 8*bolt_scale, 85),
]

# Glow
for glow in range(15, 0, -1):
    alpha = int(150 - glow * 8)
    glow_bolt = [(x + (glow/3 if x > center_x else -glow/3), y) for x, y in lightning]
    draw.polygon(glow_bolt, fill=(255, 255, 100, alpha))

draw.polygon(lightning, fill=(255, 240, 0, 255))

# Highlight
highlight = [
    (center_x - 6*bolt_scale, 90),
    (center_x + 5*bolt_scale, 110),
    (center_x - 1*bolt_scale, 110),
    (center_x - 6*bolt_scale, 90),
]
draw.polygon(highlight, fill=(255, 255, 220, 200))

# Glow rays
num_rays = 8
for i in range(num_rays):
    angle = (i / num_rays) * 2 * math.pi
    for length in range(20, 5, -2):
        x_end = center_x + math.cos(angle) * length
        y_end = 120 + math.sin(angle) * length
        alpha = int(100 - length * 3)
        draw.line([center_x, 120, x_end, y_end],
                 fill=(255, 255, 150, alpha), width=2)

# Save icon
icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
images = [img.resize(s, Image.Resampling.LANCZOS) for s in icon_sizes]

icon_path = os.path.join(app_dir, 'scraper_icon.ico')
images[0].save(icon_path, format='ICO', sizes=icon_sizes)

print(f"✓ Icon created: {icon_path}")

# ===== CREATE LAUNCHER BAT =====
print("[2/4] Creating launcher script...")

launcher_bat = os.path.join(app_dir, "launch_app.bat")
launcher_content = f"""@echo off
cd /d "{app_dir}"
start "" /B pythonw "{python_exe.replace('python.exe', 'pythonw.exe')}" scraper-g1000.py
exit
"""

with open(launcher_bat, 'w') as f:
    f.write(launcher_content)

print(f"✓ Launcher created: {launcher_bat}")

# ===== DELETE OLD SHORTCUT =====
print("[3/4] Removing old desktop shortcuts...")

old_shortcuts = [
    os.path.join(desktop, "Scraper G1000.lnk"),
    os.path.join(desktop, "Scraper G1000.bat"),
]

for old in old_shortcuts:
    if os.path.exists(old):
        os.remove(old)
        print(f"  ✓ Removed {os.path.basename(old)}")

# ===== CREATE NEW SHORTCUT WITH ICON =====
print("[4/4] Creating desktop shortcut with icon...")

try:
    from win32com.client import Dispatch

    shortcut_path = os.path.join(desktop, "Scraper G1000.lnk")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = launcher_bat
    shortcut.WorkingDirectory = app_dir
    shortcut.Description = "Scraper G1000 - Business Lead Generation"
    shortcut.IconLocation = icon_path + ",0"
    shortcut.save()

    print(f"✓ Shortcut created: {shortcut_path}")
    print(f"✓ Icon applied: {icon_path}")

except Exception as e:
    print(f"✗ Error creating shortcut: {e}")
    print("\nTrying alternative method...")

    # Fallback: VBScript method
    vbs_script = os.path.join(app_dir, 'create_shortcut_temp.vbs')
    vbs_content = f'''Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{os.path.join(desktop, 'Scraper G1000.lnk')}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{launcher_bat}"
oLink.WorkingDirectory = "{app_dir}"
oLink.Description = "Scraper G1000 - Business Lead Generation"
oLink.IconLocation = "{icon_path},0"
oLink.Save
'''

    with open(vbs_script, 'w') as f:
        f.write(vbs_content)

    os.system(f'cscript //nologo "{vbs_script}"')
    os.remove(vbs_script)

    print("✓ Shortcut created using VBScript")

print()
print("=" * 60)
print("SUCCESS!")
print("=" * 60)
print()
print("🎯 CHECK YOUR DESKTOP NOW!")
print()
print("You should see:")
print("  💡⚡ Scraper G1000 (with lightning bulb icon)")
print()
print("Double-click it to launch your app!")
print()
print("=" * 60)

input("\nPress Enter to close...")
