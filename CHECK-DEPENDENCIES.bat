@echo off
title Dependency Checker - Scraper G1000
echo.
echo ========================================
echo   Scraper G1000 - Dependency Check
echo ========================================
echo.

set PYTHON_PATH=C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe

echo Checking Python installation...
"%PYTHON_PATH%" --version
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found at: %PYTHON_PATH%
    echo.
    echo Please install Python 3.11 or update the path in this script.
    pause
    exit /b 1
)

echo.
echo Checking required packages...
echo.

"%PYTHON_PATH%" -c "import flask; print('✓ Flask:', flask.__version__)"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Flask - MISSING
    set MISSING=1
)

"%PYTHON_PATH%" -c "import flask_cors; print('✓ Flask-CORS: OK')"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Flask-CORS - MISSING
    set MISSING=1
)

"%PYTHON_PATH%" -c "import webview; print('✓ PyWebView:', webview.__version__)"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ PyWebView - MISSING
    set MISSING=1
)

"%PYTHON_PATH%" -c "import bs4; print('✓ BeautifulSoup4: OK')"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ BeautifulSoup4 - MISSING
    set MISSING=1
)

"%PYTHON_PATH%" -c "import openpyxl; print('✓ OpenPyXL:', openpyxl.__version__)"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ OpenPyXL - MISSING
    set MISSING=1
)

"%PYTHON_PATH%" -c "import pydantic; print('✓ Pydantic:', pydantic.__version__)"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Pydantic - MISSING
    set MISSING=1
)

"%PYTHON_PATH%" -c "import geopy; print('✓ Geopy: OK')"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Geopy - MISSING
    set MISSING=1
)

"%PYTHON_PATH%" -c "import pgeocode; print('✓ PGeocode: OK')"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ PGeocode - MISSING
    set MISSING=1
)

"%PYTHON_PATH%" -c "import nest_asyncio; print('✓ Nest-Asyncio: OK')"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Nest-Asyncio - MISSING
    set MISSING=1
)

"%PYTHON_PATH%" -c "import dotenv; print('✓ Python-Dotenv: OK')"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Python-Dotenv - MISSING
    set MISSING=1
)

echo.
if defined MISSING (
    echo ========================================
    echo   MISSING DEPENDENCIES DETECTED
    echo ========================================
    echo.
    echo Run INSTALL-DEPENDENCIES.bat to fix this.
    echo.
) else (
    echo ========================================
    echo   ALL DEPENDENCIES INSTALLED ✓
    echo ========================================
    echo.
    echo You're ready to run the app!
    echo.
)

pause
