@echo off
echo Starting diagnostic... > CRASH-LOG.txt
echo Date: %date% %time% >> CRASH-LOG.txt
echo. >> CRASH-LOG.txt

echo [1] Checking Python... >> CRASH-LOG.txt
if exist "C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" (
    echo Python found >> CRASH-LOG.txt
) else (
    echo Python NOT found >> CRASH-LOG.txt
)

echo. >> CRASH-LOG.txt
echo [2] Running Python version check... >> CRASH-LOG.txt
"C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" --version >> CRASH-LOG.txt 2>&1

echo. >> CRASH-LOG.txt
echo [3] Running scraper-g1000.py... >> CRASH-LOG.txt
echo ======================================== >> CRASH-LOG.txt
"C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" scraper-g1000.py >> CRASH-LOG.txt 2>&1

echo. >> CRASH-LOG.txt
echo ======================================== >> CRASH-LOG.txt
echo Finished. Exit code: %ERRORLEVEL% >> CRASH-LOG.txt

REM Open the log file
start notepad CRASH-LOG.txt
