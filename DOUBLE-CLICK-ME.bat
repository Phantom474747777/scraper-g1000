@echo off
title Scraper G1000 - One-Click Launcher
color 0B
cls

echo.
echo ============================================================
echo   SCRAPER G1000 - AUTOMATIC LAUNCHER
echo ============================================================
echo.
echo This will:
echo   1. Find Python automatically
echo   2. Check all dependencies
echo   3. Install missing packages
echo   4. Launch the app
echo.
echo Starting in 2 seconds...
timeout /t 2 >nul

REM Try python command first
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found Python in PATH
    set PYTHON=python
    goto :FOUND
)

REM Try common paths
if exist "C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" (
    echo Found Python at: 47 Industries path
    set PYTHON="C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe"
    goto :FOUND
)

if exist "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" (
    echo Found Python at: 47 path
    set PYTHON="C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe"
    goto :FOUND
)

echo.
echo ERROR: Python not found!
echo.
echo Please install Python 3.11 from:
echo https://www.python.org/downloads/
echo.
pause
exit /b 1

:FOUND
echo.
echo Checking dependencies...
echo.

REM Quick dependency check
%PYTHON% -c "import flask, webview, bs4, openpyxl, pydantic, geopy, pgeocode" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Some packages are missing. Installing now...
    echo This may take 2-3 minutes...
    echo.
    %PYTHON% -m pip install --quiet Flask flask-cors pywebview beautifulsoup4 openpyxl pydantic geopy pgeocode nest-asyncio python-dotenv requests
    echo.
    echo Installation complete!
    echo.
)

echo All dependencies OK!
echo.
echo Launching Scraper G1000...
echo.
echo ============================================================
echo.

%PYTHON% scraper-g1000.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================================
    echo   APP CRASHED - Check startup.log for errors
    echo ============================================================
    echo.
    if exist startup.log (
        echo Opening error log...
        notepad startup.log
    )
)

pause
