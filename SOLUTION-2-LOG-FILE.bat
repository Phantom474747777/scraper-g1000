@echo off
echo Running app and saving output to ERROR.txt...
"C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe" scraper-g1000.py > ERROR.txt 2>&1
echo.
echo Done! Opening ERROR.txt...
notepad ERROR.txt
pause
