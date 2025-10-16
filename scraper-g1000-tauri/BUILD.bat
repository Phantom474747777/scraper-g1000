@echo off
title Scraper G1000 - Building...
echo.
echo ========================================
echo   Scraper G1000 - Production Build
echo ========================================
echo.

echo [1/3] Cleaning previous builds...
if exist "src-tauri\target\release\bundle" (
    echo Removing old bundle...
    rd /s /q "src-tauri\target\release\bundle"
)

echo.
echo [2/3] Building Tauri app...
echo This may take 5-10 minutes...
call npm run build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo   BUILD FAILED!
    echo ========================================
    pause
    exit /b 1
)

echo.
echo [3/3] Build complete!
echo.
echo ========================================
echo   BUILD SUCCESSFUL!
echo ========================================
echo.
echo Installer location:
echo src-tauri\target\release\bundle\nsis\
echo.

explorer "src-tauri\target\release\bundle\nsis"

pause
