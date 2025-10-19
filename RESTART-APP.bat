@echo off
echo Killing all Python processes...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting Scraper G1000...
START-GUI.bat
