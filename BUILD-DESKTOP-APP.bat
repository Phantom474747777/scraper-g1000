@echo off
title Building Scraper G1000 Desktop App
color 0A

echo.
echo ========================================
echo   BUILDING SCRAPER G1000 DESKTOP APP
echo ========================================
echo.
echo This will create ScraperG1000.exe
echo A standalone desktop application!
echo.
pause

echo.
echo [1/3] Installing PyInstaller...
python -m pip install pyinstaller --quiet

echo [2/3] Building executable...
python build_exe.py

echo.
echo [3/3] Build complete!
echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Your app is ready: dist\ScraperG1000.exe
echo.
echo Right-click ScraperG1000.exe and:
echo  - Send to Desktop (create shortcut)
echo  - Pin to taskbar
echo.
pause
