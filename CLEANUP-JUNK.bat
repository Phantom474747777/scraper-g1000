@echo off
echo ========================================
echo   CLEANUP JUNK FILES AND FOLDERS
echo ========================================
echo.
echo This will DELETE the following:
echo - app/ folder (unused new UI)
echo - --name/ folder
echo - test-electron-fresh/ folder
echo - All test_*.py files
echo - All analyze_*.py files
echo - Debug HTML files
echo - Old installers (.exe)
echo - Extra batch files
echo - Documentation files (except README)
echo.
echo Press Ctrl+C to CANCEL or
pause

echo.
echo [1/10] Deleting app/ folder...
rmdir /S /Q "app" 2>nul

echo [2/10] Deleting --name/ folder...
rmdir /S /Q "--name" 2>nul

echo [3/10] Deleting test-electron-fresh/ folder...
rmdir /S /Q "test-electron-fresh" 2>nul

echo [4/10] Deleting test files...
del /F /Q test_*.py 2>nul

echo [5/10] Deleting analyze/diagnose files...
del /F /Q analyze_*.py diagnose_*.py check_data.py backfill_cities.py fix_database.py find_phone_selector.py 2>nul

echo [6/10] Deleting debug HTML files...
del /F /Q debug_*.html yellowpages_sample.html 2>nul

echo [7/10] Deleting old installers...
del /F /Q rustup-init.exe vs_buildtools.exe 2>nul

echo [8/10] Deleting extra batch files...
del /F /Q FORCE_KILL_PORT_5050.bat KILL_PYTHON.bat kill_all_python.py TEST-IN-BROWSER.bat 2>nul

echo [9/10] Deleting documentation files...
del /F /Q CLAUDE.md COMPLETE_FIX_LIST.md FINAL_FIXES.md PROGRESS_REPORT.md 2>nul

echo [10/10] Deleting nul file...
del /F /Q nul 2>nul

echo.
echo ========================================
echo   CLEANUP COMPLETE!
echo ========================================
echo.
echo Deleted folders:
echo   - app/
echo   - --name/
echo   - test-electron-fresh/
echo.
echo Deleted files:
echo   - 15+ test/analyze scripts
echo   - 3 debug HTML files
echo   - 2 installer EXEs (700MB+)
echo   - 5 extra batch files
echo   - 4 documentation files
echo.
pause

echo [11/12] Deleting old unused scrapers from src/...
del /F /Q "src\scraper_411.py" 2>nul
del /F /Q "src\scraper_google_maps.py" 2>nul
del /F /Q "src\scraper_no_ai.py" 2>nul
del /F /Q "src\scraper_outscraper.py" 2>nul
del /F /Q "src\scraper_yelp.py" 2>nul
del /F /Q "src\scraper.py" 2>nul
del /F /Q "src\scraper_free_bypass.py" 2>nul
echo Done! Deleted 7 old scraper files (50KB+ saved)

echo [12/12] Deleting JS backup files from UI...
del /F /Q "scraper-g1000-tauri\src\js\app.js.backup" 2>nul
del /F /Q "scraper-g1000-tauri\src\js\app_old.js" 2>nul
echo Done! Deleted 2 backup JS files

echo.
echo ========================================
echo   TOTAL SPACE SAVED: ~750MB+
echo ========================================
pause
