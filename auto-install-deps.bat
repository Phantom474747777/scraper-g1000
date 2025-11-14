@echo off
echo Checking dependencies... > dependency-check.log

REM Find Python
set PYTHON_FOUND=0
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    set PYTHON_FOUND=1
    echo Found Python in PATH >> dependency-check.log
) else (
    if exist "C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" (
        set PYTHON_CMD="C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe"
        set PYTHON_FOUND=1
        echo Found Python at 47 Industries path >> dependency-check.log
    ) else if exist "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" (
        set PYTHON_CMD="C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe"
        set PYTHON_FOUND=1
        echo Found Python at 47 path >> dependency-check.log
    )
)

if %PYTHON_FOUND% EQU 0 (
    echo ERROR: Python not found! >> dependency-check.log
    echo Python not installed. Install from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found: %PYTHON_CMD% >> dependency-check.log
echo. >> dependency-check.log

REM Check each required package
echo Checking Flask... >> dependency-check.log
%PYTHON_CMD% -c "import flask" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo MISSING: Flask >> dependency-check.log
    set MISSING=1
) else (
    echo OK: Flask >> dependency-check.log
)

echo Checking flask-cors... >> dependency-check.log
%PYTHON_CMD% -c "import flask_cors" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo MISSING: flask-cors >> dependency-check.log
    set MISSING=1
) else (
    echo OK: flask-cors >> dependency-check.log
)

echo Checking webview... >> dependency-check.log
%PYTHON_CMD% -c "import webview" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo MISSING: webview >> dependency-check.log
    set MISSING=1
) else (
    echo OK: webview >> dependency-check.log
)

echo Checking beautifulsoup4... >> dependency-check.log
%PYTHON_CMD% -c "import bs4" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo MISSING: beautifulsoup4 >> dependency-check.log
    set MISSING=1
) else (
    echo OK: beautifulsoup4 >> dependency-check.log
)

echo Checking openpyxl... >> dependency-check.log
%PYTHON_CMD% -c "import openpyxl" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo MISSING: openpyxl >> dependency-check.log
    set MISSING=1
) else (
    echo OK: openpyxl >> dependency-check.log
)

echo Checking pydantic... >> dependency-check.log
%PYTHON_CMD% -c "import pydantic" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo MISSING: pydantic >> dependency-check.log
    set MISSING=1
) else (
    echo OK: pydantic >> dependency-check.log
)

echo Checking geopy... >> dependency-check.log
%PYTHON_CMD% -c "import geopy" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo MISSING: geopy >> dependency-check.log
    set MISSING=1
) else (
    echo OK: geopy >> dependency-check.log
)

echo Checking pgeocode... >> dependency-check.log
%PYTHON_CMD% -c "import pgeocode" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo MISSING: pgeocode >> dependency-check.log
    set MISSING=1
) else (
    echo OK: pgeocode >> dependency-check.log
)

echo. >> dependency-check.log

if defined MISSING (
    echo MISSING DEPENDENCIES DETECTED >> dependency-check.log
    echo. >> dependency-check.log
    echo Some packages are missing. Installing now...
    echo.

    echo Installing packages... >> dependency-check.log
    %PYTHON_CMD% -m pip install --quiet Flask flask-cors pywebview beautifulsoup4 openpyxl pydantic geopy pgeocode nest-asyncio python-dotenv requests >> dependency-check.log 2>&1

    if %ERRORLEVEL% EQU 0 (
        echo Installation complete! >> dependency-check.log
        echo Dependencies installed successfully!
        echo.
    ) else (
        echo Installation FAILED >> dependency-check.log
        echo ERROR: Could not install dependencies.
        echo Check dependency-check.log for details.
        pause
        exit /b 1
    )
) else (
    echo All dependencies OK! >> dependency-check.log
    echo All dependencies are already installed.
)

echo. >> dependency-check.log
echo Dependency check complete. >> dependency-check.log
