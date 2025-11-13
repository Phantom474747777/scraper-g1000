@echo off
title Test Imports - Scraper G1000
echo.
echo ========================================
echo   Scraper G1000 - Import Test
echo ========================================
echo.

set PYTHON_PATH=C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe

if not exist "%PYTHON_PATH%" (
    echo [ERROR] Python not found!
    echo.
    pause
    exit /b 1
)

"%PYTHON_PATH%" test_imports.py

echo.
pause
