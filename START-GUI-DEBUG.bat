@echo off
title Scraper G1000 (Debug Mode)
color 0A
echo.
echo ========================================
echo   Scraper G1000 - DEBUG MODE
echo ========================================
echo.
echo Starting application with full error logging...
echo.

set PYTHON_PATH=C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe

REM Check if Python exists
if not exist "%PYTHON_PATH%" (
    echo [ERROR] Python not found at:
    echo %PYTHON_PATH%
    echo.
    echo Please install Python 3.11 or update the path in this script.
    echo.
    pause
    exit /b 1
)

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Get timestamp for log file
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set LOGFILE=logs\debug_%mydate%_%mytime%.log

echo Logging to: %LOGFILE%
echo.

REM Run with full error output
"%PYTHON_PATH%" scraper-g1000.py 2>&1 | tee %LOGFILE%

echo.
echo ========================================
echo   APPLICATION CLOSED
echo ========================================
echo.
echo Error log saved to: %LOGFILE%
echo.

pause
