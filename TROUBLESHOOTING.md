# Scraper G1000 - Troubleshooting Guide

## App Won't Start - Quick Fix

### Step 1: Install Dependencies
Double-click: **INSTALL-DEPENDENCIES.bat**

This will automatically install all required packages.

### Step 2: Test Installation
Double-click: **TEST-IMPORTS.bat**

This will verify all packages are installed correctly.

### Step 3: Launch App
Double-click: **START-GUI.bat**

---

## Common Issues

### Issue: "Python not found"
**Solution:**
- Install Python 3.11 from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Update the Python path in START-GUI.bat if installed in a different location

### Issue: App crashes immediately (window flashes and closes)
**Causes:**
1. Missing dependencies
2. Port 5050 is already in use
3. Corrupted database file

**Solutions:**
1. Run **INSTALL-DEPENDENCIES.bat**
2. Close any other apps using port 5050
3. Run **START-GUI-DEBUG.bat** to see detailed errors

### Issue: "Module not found" errors
**Solution:**
```
Run: INSTALL-DEPENDENCIES.bat
```

### Issue: Port 5050 already in use
**Solution:**
- Close the app if it's already running
- Check Task Manager for python.exe processes
- Kill any python.exe processes related to Scraper G1000

### Issue: GUI doesn't load / blank window
**Causes:**
- UI files missing
- Flask backend not starting

**Solution:**
- Verify `scraper-g1000-tauri/src/` folder exists
- Check that `index.html`, `js/app.js`, and `styles/main.css` are present
- Run START-GUI-DEBUG.bat to see backend errors

---

## Debug Mode

For detailed error logs, run: **START-GUI-DEBUG.bat**

Error logs will be saved to `logs/debug_DATE_TIME.log`

---

## Manual Installation

If the automatic installer doesn't work:

```cmd
python -m pip install --upgrade pip
python -m pip install Flask flask-cors pywebview beautifulsoup4 openpyxl pydantic geopy pgeocode nest-asyncio python-dotenv requests
```

---

## Check What's Installed

Run: **CHECK-DEPENDENCIES.bat**

This shows which packages are installed and which are missing.

---

## Getting Help

1. Run **START-GUI-DEBUG.bat**
2. Copy the error message
3. Include your Python version (`python --version`)
4. Include your Windows version

---

## Files Overview

| File | Purpose |
|------|---------|
| **START-GUI.bat** | Launch the app (use this normally) |
| **START-GUI-DEBUG.bat** | Launch with detailed error logging |
| **INSTALL-DEPENDENCIES.bat** | Install all required packages |
| **CHECK-DEPENDENCIES.bat** | Verify which packages are installed |
| **TEST-IMPORTS.bat** | Test if all imports work |
| **scraper-g1000.py** | Main application (Python file) |
| **requirements.txt** | List of required packages |

---

## Advanced: Reinstall Everything

```cmd
python -m pip uninstall -y Flask flask-cors pywebview beautifulsoup4 openpyxl pydantic geopy pgeocode nest-asyncio python-dotenv
```

Then run: **INSTALL-DEPENDENCIES.bat**
