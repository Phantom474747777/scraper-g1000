@echo off
title Scraper G1000 - Desktop App Builder
color 0A

echo.
echo ========================================
echo   SCRAPER G1000 - DESKTOP APP BUILDER
echo ========================================
echo.
echo This will create a desktop app with a cool icon!
echo.
echo What this does:
echo  1. Generate lightning bolt icon
echo  2. Build ScraperG1000.exe
echo  3. Put it on your desktop
echo.
echo Just sit back and relax...
echo.
pause

echo.
echo [Step 1/4] Installing tools...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet Pillow pyinstaller pywin32

echo.
echo [Step 2/4] Creating icon...
python -c "from PIL import Image, ImageDraw; img = Image.new('RGBA', (256, 256), (0,0,0,0)); draw = ImageDraw.Draw(img); [draw.ellipse([20+i, 20+i, 236-i, 236-i], fill=(30+i, 40+i*2, 60+i*3, 255-i*2)) for i in range(50)]; draw.ellipse([20, 20, 236, 236], outline=(0, 200, 255, 255), width=8); bolt = [(110, 60), (135, 118), (125, 118), (140, 138), (128, 138), (145, 196), (118, 148), (130, 148), (110, 60)]; [draw.polygon([(x+o, y) for x,y in bolt], fill=(255, 220, 0, 100-o*8)) for o in range(10, 0, -1)]; draw.polygon(bolt, fill=(255, 220, 0, 255)); img.save('app_icon.ico', format='ICO', sizes=[(256,256), (128,128), (64,64), (48,48), (32,32), (16,16)]); print('Icon created!')"

echo.
echo [Step 3/4] Building executable...
echo This takes 2-5 minutes, please wait...

pyinstaller --onefile --windowed --name=ScraperG1000 --icon=app_icon.ico --hidden-import=flask --hidden-import=flask_cors --hidden-import=webview --hidden-import=sqlite3 --hidden-import=openpyxl --hidden-import=requests --hidden-import=bs4 --hidden-import=pgeocode --add-data="backend;backend" --add-data="src;src" --add-data="scraper-g1000-tauri\src;scraper-g1000-tauri/src" --distpath=dist --workpath=build --clean --noconfirm scraper-g1000.py

if not exist "dist\ScraperG1000.exe" (
    echo.
    echo ERROR: Build failed!
    echo Check the output above for errors.
    pause
    exit /b 1
)

echo.
echo [Step 4/4] Creating desktop shortcut...

set SCRIPT="%TEMP%\create_shortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\Scraper G1000.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%CD%\dist\ScraperG1000.exe" >> %SCRIPT%
echo oLink.WorkingDirectory = "%CD%" >> %SCRIPT%
echo oLink.Description = "Scraper G1000 - Business Lead Generation" >> %SCRIPT%
echo oLink.IconLocation = "%CD%\app_icon.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Check your DESKTOP now!
echo You should see: "Scraper G1000" with a lightning bolt icon
echo.
echo Just double-click it to launch!
echo.
echo You can also:
echo  - Pin it to taskbar
echo  - Pin to Start Menu
echo.
echo Your app is ready to use!
echo.
pause
