@echo off
cls
echo.
echo STEP 1: Can you see this message? (YES/NO)
echo.
echo If YES, batch files work.
echo If NO, something is very wrong with Windows.
echo.
pause
cls

echo.
echo STEP 2: Testing if Python exists...
echo.

if exist "C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" (
    echo FOUND: Python is installed
) else (
    echo NOT FOUND: Python is missing
    echo.
    echo Install Python from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
pause
cls

echo.
echo STEP 3: Testing Python version...
echo.
"C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" --version
echo.
pause
cls

echo.
echo STEP 4: Testing if Python can run a simple command...
echo.
"C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" -c "print('Python works!')"
echo.
pause
cls

echo.
echo STEP 5: Creating error log...
echo.
"C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" scraper-g1000.py > ERROR-LOG.txt 2>&1
echo.
echo Done! Opening ERROR-LOG.txt...
echo.
notepad ERROR-LOG.txt
echo.
pause
