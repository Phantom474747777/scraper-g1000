@echo off
chcp 65001 >nul
REM CritterCaptures Lead Generation - Smart Interactive CLI

echo.
echo ========================================================
echo   CritterCaptures Smart Lead Generation
echo   Interactive CLI with Color-Coded Selection
echo ========================================================
echo.

REM Check if dependencies are installed, if not install them
echo Checking dependencies...
"C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" -c "import InquirerPy, nest_asyncio" 2>nul
if errorlevel 1 (
    echo.
    echo Installing required dependencies...
    echo This will only happen once, please wait...
    echo.
    "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" -m pip install -r requirements.txt --quiet --disable-pip-version-check
    echo.
    echo Dependencies installed successfully!
    echo.
)

echo Starting lead generation system...
echo.

REM Use full path to Python
"C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" leadgen_cli.py %*

echo.
echo ========================================================
echo   Session ended!
echo ========================================================
echo.
pause
