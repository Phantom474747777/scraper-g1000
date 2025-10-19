@echo off
cd /d "%~dp0"

REM Kill any existing Python processes
echo Cleaning up old processes...
"C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" kill_all_python.py
timeout /t 2 /nobreak >nul

REM Start backend API
echo Starting backend API...
start /B "" "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" backend\api_server.py 5050
timeout /t 3 /nobreak >nul

REM Launch desktop app (includes frontend server)
echo Launching desktop app...
"C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" app_pywebview.py

echo.
echo App closed.
pause
