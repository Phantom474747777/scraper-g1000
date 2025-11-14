@echo off
title Scraper G1000
cls

REM Auto-check and install dependencies first
call auto-install-deps.bat
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Scraper G1000
echo   Business Lead Generation
echo ========================================
echo.
echo Starting application...
echo.

REM Find Python
set PYTHON_FOUND=0
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    python scraper-g1000.py
    set PYTHON_FOUND=1
) else (
    if exist "C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" (
        "C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" scraper-g1000.py
        set PYTHON_FOUND=1
    ) else if exist "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" (
        "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" scraper-g1000.py
        set PYTHON_FOUND=1
    )
)

if %PYTHON_FOUND% EQU 0 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/downloads/
    echo.
)

pause
