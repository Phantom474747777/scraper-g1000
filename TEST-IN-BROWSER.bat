@echo off
echo Starting backend only for browser testing...
echo.
echo Once backend starts, open your browser to:
echo http://localhost:5050/test.html
echo.
echo Press Ctrl+C to stop
echo.

"C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" backend/api_server.py 5050

pause
