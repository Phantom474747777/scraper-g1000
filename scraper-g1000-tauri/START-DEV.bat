@echo off
title Scraper G1000 - Starting...
echo.
echo ========================================
echo   Scraper G1000 - Development Mode
echo ========================================
echo.
echo Starting Python backend...
start /B "Backend" "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" backend\api_server.py 5050

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting dev server...
start /B "DevServer" "C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" serve.py

echo Waiting for dev server...
timeout /t 2 /nobreak >nul

echo.
echo Launching Tauri app...
cd %~dp0
call npm run dev

echo.
echo Scraper G1000 closed.
pause
