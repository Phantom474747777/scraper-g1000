@echo off
title Scraper G1000
color 0B

REM IMPORTANT: This window will NOT close until you press a key
REM This ensures you can see any errors

REM Create logs directory
if not exist "logs" mkdir logs

REM Generate log filename with timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/: " %%a in ('time /t') do (set mytime=%%a%%b)
set LOG_FILE=logs\startup_%mydate%_%mytime%.log

echo ========================================
echo   Scraper G1000
echo   Business Lead Generation
echo ========================================
echo.
echo Log file: %LOG_FILE%
echo.

REM Redirect output to both console and log file
call :MAIN 2>&1 | "%SystemRoot%\System32\more.com" > "%LOG_FILE%"
type "%LOG_FILE%"

echo.
echo ========================================
echo.
echo Full log saved to: %LOG_FILE%
echo.
echo THIS WINDOW WILL NOT CLOSE AUTOMATICALLY
echo Press any key to exit...
pause >nul
exit /b

:MAIN
set PYTHON_PATH=C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe

echo Checking Python installation...
echo Python path: %PYTHON_PATH%
echo.

if not exist "%PYTHON_PATH%" (
    echo [ERROR] Python not found at:
    echo %PYTHON_PATH%
    echo.
    echo Please install Python 3.11 from:
    echo https://www.python.org/downloads/
    echo.
    exit /b 1
)

echo Python found!
echo.

echo Checking Python version...
"%PYTHON_PATH%" --version
echo.

echo Starting application...
echo.
echo ========================================
echo   OUTPUT FROM scraper-g1000.py
echo ========================================
echo.

REM Run the application
"%PYTHON_PATH%" scraper-g1000.py

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%
echo.
echo.
echo ========================================

if %EXIT_CODE% NEQ 0 (
    echo   APPLICATION CRASHED
    echo ========================================
    echo.
    echo Exit Code: %EXIT_CODE%
    echo.
    echo Common fixes:
    echo   1. Run: INSTALL-DEPENDENCIES.bat
    echo   2. Check if port 5050 is already in use
    echo   3. Review the error messages above
    echo.
) else (
    echo   APPLICATION CLOSED NORMALLY
    echo ========================================
    echo.
)

exit /b %EXIT_CODE%
