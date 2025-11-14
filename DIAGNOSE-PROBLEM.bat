@echo off
title Diagnose Problem
color 0E

echo ========================================
echo   DIAGNOSTIC TOOL
echo ========================================
echo.

set PYTHON="C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe"

echo [1/5] Checking Python installation...
if exist %PYTHON% (
    echo FOUND: %PYTHON%
) else (
    echo NOT FOUND: %PYTHON%
    echo.
    echo PROBLEM: Python is not installed at this location
    echo.
    pause
    exit /b 1
)
echo.

echo [2/5] Checking Python version...
%PYTHON% --version
echo.

echo [3/5] Testing imports...
%PYTHON% -c "import sys; print('sys: OK')"
%PYTHON% -c "import flask; print('flask:', flask.__version__)" 2>nul || echo flask: MISSING
%PYTHON% -c "import webview; print('webview:', webview.__version__)" 2>nul || echo webview: MISSING
%PYTHON% -c "import bs4; print('beautifulsoup4: OK')" 2>nul || echo beautifulsoup4: MISSING
%PYTHON% -c "import openpyxl; print('openpyxl: OK')" 2>nul || echo openpyxl: MISSING
echo.

echo [4/5] Running import test script...
%PYTHON% test_imports.py
echo.

echo [5/5] Attempting to start app...
echo Output will be saved to DIAGNOSTIC-OUTPUT.txt
echo.
%PYTHON% scraper-g1000.py > DIAGNOSTIC-OUTPUT.txt 2>&1
echo.

echo Done! Exit code: %ERRORLEVEL%
echo.
echo Opening diagnostic output...
notepad DIAGNOSTIC-OUTPUT.txt
echo.
pause
