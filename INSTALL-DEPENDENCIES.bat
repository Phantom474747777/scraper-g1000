@echo off
title Install Dependencies - Scraper G1000
echo.
echo ========================================
echo   Scraper G1000 - Dependency Installer
echo ========================================
echo.

set PYTHON_PATH=C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe

echo Checking Python installation...
"%PYTHON_PATH%" --version
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found at: %PYTHON_PATH%
    echo.
    echo Please install Python 3.11 from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Installing required packages...
echo This may take a few minutes...
echo.

"%PYTHON_PATH%" -m pip install --upgrade pip

"%PYTHON_PATH%" -m pip install Flask>=3.0.0 flask-cors>=4.0.0 pywebview>=5.0.0 beautifulsoup4>=4.12.0 openpyxl>=3.1.5 pydantic>=2.0.0 geopy>=2.4.0 pgeocode>=0.4.0 nest-asyncio>=1.5.0 python-dotenv>=1.0.0 requests>=2.31.0

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   INSTALLATION COMPLETE ✓
    echo ========================================
    echo.
    echo All dependencies installed successfully!
    echo You can now run START-GUI.bat
    echo.
) else (
    echo.
    echo ========================================
    echo   INSTALLATION FAILED ✗
    echo ========================================
    echo.
    echo There was an error installing dependencies.
    echo Please check the error messages above.
    echo.
)

pause
