@echo off
title Scraper G1000 - Building Standalone EXE...
echo.
echo ========================================
echo   Scraper G1000 - Build Standalone EXE
echo ========================================
echo.
echo This will create a single .exe file that
echo can run on any Windows PC without Python.
echo.
echo Output: dist\Scraper-G1000.exe
echo.
pause

echo.
echo [1/3] Checking PyInstaller...
"C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" -m pip show pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller not found. Installing...
    "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" -m pip install pyinstaller
)

echo.
echo [2/3] Building executable...
echo This may take 2-3 minutes...
echo.

cd /d "%~dp0"

"C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "Scraper-G1000" ^
    --icon=NONE ^
    --add-data "src;src" ^
    --add-data "backend;backend" ^
    --add-data "python-src;python-src" ^
    --hidden-import=webview ^
    --hidden-import=flask ^
    --hidden-import=sqlite3 ^
    app_pywebview.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo   BUILD FAILED!
    echo ========================================
    pause
    exit /b 1
)

echo.
echo [3/3] Cleaning up...
rd /s /q build 2>nul

echo.
echo ========================================
echo   BUILD SUCCESSFUL!
echo ========================================
echo.
echo Executable location:
echo %CD%\dist\Scraper-G1000.exe
echo.
echo You can now distribute this .exe file.
echo Users do NOT need Python installed.
echo.

explorer "%CD%\dist"

pause
