$pythonPath = "C:\Users\47 Industries\AppData\Local\Programs\Python\Python311\python.exe"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Scraper G1000 - PowerShell Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Checking Python..." -ForegroundColor Yellow
if (Test-Path $pythonPath) {
    Write-Host "FOUND: $pythonPath" -ForegroundColor Green
} else {
    Write-Host "NOT FOUND: $pythonPath" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Python Version:" -ForegroundColor Yellow
& $pythonPath --version

Write-Host ""
Write-Host "Starting application..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

& $pythonPath scraper-g1000.py

$exitCode = $LASTEXITCODE

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Exit Code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { "Green" } else { "Red" })
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
