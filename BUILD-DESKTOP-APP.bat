@echo off
title Building Scraper G1000 Desktop App
color 0A

echo.
echo ========================================
echo   BUILDING SCRAPER G1000 DESKTOP APP
echo ========================================
echo.
echo This will:
echo  1. Generate a cool lightning bolt icon
echo  2. Build ScraperG1000.exe with the icon
echo  3. Put the app on your desktop
echo.
pause

echo.
echo [1/5] Installing dependencies...
python -m pip install Pillow pyinstaller pywin32 winshell --quiet --upgrade

echo.
echo [2/5] Generating custom icon...
python generate_icon.py

echo.
echo [3/5] Building executable with icon...
python build_exe.py

echo.
echo [4/5] Creating desktop shortcut...
python create_shortcut.py

echo.
echo [5/5] Build complete!
echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Check your desktop! You should see:
echo   "Scraper G1000" with a lightning bolt icon
echo.
echo Just double-click it to launch!
echo.
echo You can also:
echo  - Pin it to taskbar
echo  - Pin to Start Menu
echo.
pause
