@echo off
title Scraper G1000 - Debug Output
color 0B

echo ========================================
echo   Scraper G1000
echo   This window will STAY OPEN
echo ========================================
echo.

set PYTHON="C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe"

echo Running: %PYTHON% scraper-g1000.py
echo.
echo ----------------------------------------
echo.

%PYTHON% scraper-g1000.py

echo.
echo ----------------------------------------
echo.
echo Python exited with code: %ERRORLEVEL%
echo.

REM The window will NEVER close automatically
REM You must close it manually with the X button
cmd /k
