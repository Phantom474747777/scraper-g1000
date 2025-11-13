@echo off
title Scraper G1000
color 0B
echo.
echo ========================================
echo   Scraper G1000
echo   Business Lead Generation
echo ========================================
echo.

set PYTHON_PATH=C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe

REM Check if Python exists
if not exist "%PYTHON_PATH%" (
    echo [ERROR] Python not found!
    echo.
    echo Expected location: %PYTHON_PATH%
    echo.
    echo Please install Python 3.11 from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Starting application...
echo.

REM Run the application
"%PYTHON_PATH%" scraper-g1000.py

REM Check if it crashed
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo   ERROR DETECTED
    echo ========================================
    echo.
    echo The application crashed with error code: %ERRORLEVEL%
    echo.
    echo Possible causes:
    echo 1. Missing dependencies - Run INSTALL-DEPENDENCIES.bat
    echo 2. Port 5050 already in use
    echo 3. Configuration error
    echo.
    echo Run START-GUI-DEBUG.bat for detailed error logs.
    echo.
)

pause
