@echo off
title Scraper G1000 - Safe Launcher
cls

echo ========================================
echo   Scraper G1000 - Safe Mode
echo ========================================
echo.

REM Find Python
set PYTHON_CMD=
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
) else (
    if exist "C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" (
        set PYTHON_CMD="C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe"
    ) else if exist "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" (
        set PYTHON_CMD="C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe"
    )
)

if not defined PYTHON_CMD (
    echo ERROR: Python not found!
    echo.
    echo Install Python 3.11 from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Using Python: %PYTHON_CMD%
echo.
echo Checking and installing dependencies...
echo.

REM Run the safe launcher
%PYTHON_CMD% launch.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application exited with errors.
    echo.
)

pause
