@echo off
echo Running emergency diagnostic... > EMERGENCY-LOG.txt
echo. >> EMERGENCY-LOG.txt
echo Date: %date% %time% >> EMERGENCY-LOG.txt
echo. >> EMERGENCY-LOG.txt

echo ========================================== >> EMERGENCY-LOG.txt
echo STEP 1: Finding Python >> EMERGENCY-LOG.txt
echo ========================================== >> EMERGENCY-LOG.txt

set PYTHON_CMD=
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    echo Found: python command in PATH >> EMERGENCY-LOG.txt
    python --version >> EMERGENCY-LOG.txt 2>&1
) else (
    echo Python not in PATH >> EMERGENCY-LOG.txt
    if exist "C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" (
        set PYTHON_CMD="C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe"
        echo Found: C:\Users\47 Industries\...\python.exe >> EMERGENCY-LOG.txt
    ) else if exist "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" (
        set PYTHON_CMD="C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe"
        echo Found: C:\Users\47\...\python.exe >> EMERGENCY-LOG.txt
    ) else (
        echo ERROR: Python not found anywhere! >> EMERGENCY-LOG.txt
        echo.
        echo Python not found! Check EMERGENCY-LOG.txt
        notepad EMERGENCY-LOG.txt
        pause
        exit /b 1
    )
)

echo. >> EMERGENCY-LOG.txt
echo ========================================== >> EMERGENCY-LOG.txt
echo STEP 2: Checking imports >> EMERGENCY-LOG.txt
echo ========================================== >> EMERGENCY-LOG.txt

%PYTHON_CMD% -c "import sys; print('sys: OK')" >> EMERGENCY-LOG.txt 2>&1
%PYTHON_CMD% -c "import flask; print('flask:', flask.__version__)" >> EMERGENCY-LOG.txt 2>&1
%PYTHON_CMD% -c "import flask_cors; print('flask_cors: OK')" >> EMERGENCY-LOG.txt 2>&1
%PYTHON_CMD% -c "import webview; print('webview:', webview.__version__)" >> EMERGENCY-LOG.txt 2>&1
%PYTHON_CMD% -c "import bs4; print('beautifulsoup4: OK')" >> EMERGENCY-LOG.txt 2>&1
%PYTHON_CMD% -c "import openpyxl; print('openpyxl: OK')" >> EMERGENCY-LOG.txt 2>&1
%PYTHON_CMD% -c "import pydantic; print('pydantic: OK')" >> EMERGENCY-LOG.txt 2>&1
%PYTHON_CMD% -c "import geopy; print('geopy: OK')" >> EMERGENCY-LOG.txt 2>&1
%PYTHON_CMD% -c "import pgeocode; print('pgeocode: OK')" >> EMERGENCY-LOG.txt 2>&1

echo. >> EMERGENCY-LOG.txt
echo ========================================== >> EMERGENCY-LOG.txt
echo STEP 3: Running scraper-g1000.py >> EMERGENCY-LOG.txt
echo ========================================== >> EMERGENCY-LOG.txt

%PYTHON_CMD% scraper-g1000.py >> EMERGENCY-LOG.txt 2>&1

echo. >> EMERGENCY-LOG.txt
echo ========================================== >> EMERGENCY-LOG.txt
echo DIAGNOSTIC COMPLETE >> EMERGENCY-LOG.txt
echo ========================================== >> EMERGENCY-LOG.txt

echo.
echo Diagnostic complete! Opening log file...
notepad EMERGENCY-LOG.txt
