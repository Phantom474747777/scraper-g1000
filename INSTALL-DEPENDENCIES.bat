@echo off
title Install Dependencies
echo.
echo Installing required Python packages...
echo This may take a few minutes...
echo.

REM Find Python
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON=python
) else if exist "C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON="C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe"
) else if exist "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON="C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe"
) else (
    echo ERROR: Python not found
    pause
    exit /b 1
)

%PYTHON% -m pip install Flask flask-cors pywebview beautifulsoup4 openpyxl pydantic geopy pgeocode nest-asyncio python-dotenv requests

echo.
echo Done! You can now run START-GUI.bat
echo.
pause
