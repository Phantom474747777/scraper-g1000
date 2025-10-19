@echo off
title Installing Visual Studio Build Tools...
echo.
echo ========================================
echo   Installing VS Build Tools for Tauri
echo ========================================
echo.
echo This will download and install:
echo - Visual Studio Build Tools 2022
echo - C++ Build Tools Workload
echo.
echo Download size: ~1.5 GB
echo Install time: 5-10 minutes
echo.
pause

echo.
echo [1/2] Downloading Visual Studio Build Tools...
echo.

:: Download VS Build Tools bootstrapper
curl -L -o "%TEMP%\vs_buildtools.exe" "https://aka.ms/vs/17/release/vs_buildtools.exe"

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to download build tools
    pause
    exit /b 1
)

echo.
echo [2/2] Installing C++ Build Tools...
echo This will take several minutes...
echo.

:: Install with C++ workload
"%TEMP%\vs_buildtools.exe" --quiet --wait --norestart --nocache ^
    --installPath "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools" ^
    --add Microsoft.VisualStudio.Workload.VCTools ^
    --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 ^
    --add Microsoft.VisualStudio.Component.Windows11SDK.22000 ^
    --includeRecommended

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo WARNING: Installation may have failed or was cancelled
    echo Please try again or install manually from:
    echo https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
    echo.
    pause
    exit /b 1
)

:: Cleanup
del "%TEMP%\vs_buildtools.exe"

echo.
echo ========================================
echo   INSTALLATION COMPLETE!
echo ========================================
echo.
echo Visual Studio Build Tools installed successfully.
echo You can now run: npm run dev
echo.
pause
