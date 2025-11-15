@echo off
title Scraper G1000
echo.
echo ========================================
echo   Scraper G1000
echo   Business Lead Generation
echo ========================================
echo.
echo Starting application...
echo.

REM Auto-detect Python - try PATH first, then common locations
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    python scraper-g1000.py
) else if exist "C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" (
    "C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" scraper-g1000.py
) else if exist "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" (
    "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" scraper-g1000.py
) else (
    echo ERROR: Python not found
    echo Install from: https://www.python.org/downloads/
    echo.
)

pause
