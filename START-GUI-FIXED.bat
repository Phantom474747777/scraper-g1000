@echo off
title Scraper G1000
echo.
echo ========================================
echo   Scraper G1000
echo   Business Lead Generation
echo ========================================
echo.

REM Try to find Python in common locations
set PYTHON_EXE=

REM Check if python is in PATH
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXE=python
    goto :found
)

REM Check for py launcher
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXE=py
    goto :found
)

REM Check for python3
where python3 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXE=python3
    goto :found
)

REM Check common installation paths
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PYTHON_EXE="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    goto :found
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PYTHON_EXE="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto :found
)

if exist "C:\Python311\python.exe" (
    set PYTHON_EXE="C:\Python311\python.exe"
    goto :found
)

if exist "C:\Python312\python.exe" (
    set PYTHON_EXE="C:\Python312\python.exe"
    goto :found
)

:notfound
echo [ERROR] Python not found!
echo.
echo Please install Python from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:found
echo Found Python: %PYTHON_EXE%
echo.

REM Check if dependencies are installed
echo Checking dependencies...
%PYTHON_EXE% -c "import flask" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Installing required dependencies...
    echo This may take a few minutes...
    echo.
    %PYTHON_EXE% -m pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo [ERROR] Failed to install dependencies!
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Starting application...
echo.

%PYTHON_EXE% scraper-g1000.py

pause
