# Scraper G1000 v2.0 - Launch Instructions

## Desktop App is Ready!

The PyWebView-based desktop application is now fully configured and ready to use.

---

## How to Launch the App

### Option 1: Double-Click START.bat (EASIEST)
1. Navigate to `c:\Users\47\Documents\GitHub\ai-web-scraper\scraper-g1000-tauri\`
2. **Double-click `START.bat`**
3. Wait 3 seconds for backend to initialize
4. Desktop window will open automatically

### Option 2: Manual Launch (For Testing)
```bash
# Terminal 1: Start backend API
cd c:\Users\47\Documents\GitHub\ai-web-scraper\scraper-g1000-tauri
"C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" backend\api_server.py 5050

# Terminal 2: Start dev server
cd c:\Users\47\Documents\GitHub\ai-web-scraper\scraper-g1000-tauri
"C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" serve.py

# Terminal 3: Launch desktop app
cd c:\Users\47\Documents\GitHub\ai-web-scraper\scraper-g1000-tauri
"C:\Users\47\AppData\Local\Programs\Python\Python311\python.exe" app_pywebview.py
```

---

## What's Been Fixed

### Automation Mode Layout
- ✅ **Config panel widened** from 420px to 750px (NO MORE SCROLLING!)
- ✅ **ZIPs and Categories side-by-side** in 2-column grid layout
- ✅ **Compact location row** - City, State, and Radius in one line
- ✅ **Custom styled checkboxes** - No more ugly Windows boxes
- ✅ **Custom number stepper** - Clean +/- buttons with MAX button
- ✅ **Professional appearance** - Ready for $50K sale

### Functionality
- ✅ **"Start Automation" button** - Changed from "Start Scraping"
- ✅ **Completion sound toggle** - Bell icon 🔔 with tooltip
- ✅ **Job counter** - Now says "jobs queued" instead of "leads"
- ✅ **Find ZIP Codes** - Working `/api/zip-lookup` endpoint
- ✅ **Progress polling** - Real-time updates every 1 second
- ✅ **Console logging** - Live scraping progress display

### Backend API Endpoints
- ✅ `/api/zip-lookup` - Fetches ZIP codes by city/state/radius
- ✅ `/api/scrape/automation/start` - Starts batch scraping job
- ✅ `/api/scrape/status` - Returns current progress
- ✅ Background threading for non-blocking scraping

### Desktop Wrapper
- ✅ **PyWebView app** - No Rust/Tauri compilation needed
- ✅ **START.bat launcher** - One-click startup
- ✅ **Health checks** - Verifies backend + dev server before launch
- ✅ **1400x900 window** - Perfect size for automation UI

---

## File Structure

```
scraper-g1000-tauri/
├── START.bat                    # 👈 DOUBLE-CLICK THIS to launch app
├── app_pywebview.py             # Desktop wrapper (NEW!)
├── serve.py                     # Dev server for frontend
│
├── backend/
│   └── api_server.py            # Flask API with all endpoints
│
├── src/
│   ├── index.html               # Main UI (automation mode redesigned)
│   ├── styles/
│   │   └── main.css             # Glassmorphic styles + layout
│   └── js/
│       └── app.js               # JavaScript event handlers
│
├── python-src/
│   ├── profile_manager.py       # Profile management
│   ├── database.py              # SQLite leads database
│   ├── scraper_free_bypass.py   # YellowPages scraper
│   └── zip_lookup.py            # ZIP code radius search
│
└── profiles/
    └── {profile_name}/
        └── leads_tracker.db     # Per-profile lead storage
```

---

## Testing Checklist

### Manual Mode
- [ ] Switch to Manual tab
- [ ] Enter ZIP code (e.g., 33527)
- [ ] Select category (e.g., Real Estate Agents)
- [ ] Set max pages (e.g., 2)
- [ ] Click "Start Scraping"
- [ ] Verify leads appear in console
- [ ] Check leads saved to database

### Automation Mode
- [ ] Switch to Automation tab
- [ ] Enter city: "Dover", state: "FL"
- [ ] Adjust radius slider (default 50 miles)
- [ ] Click "Find ZIP Codes"
- [ ] Verify ZIPs populate in left multiselect
- [ ] Select multiple ZIPs (checkboxes)
- [ ] Select multiple Categories (checkboxes)
- [ ] Set max pages (e.g., 2)
- [ ] Toggle "Skip already scraped" if needed
- [ ] Click "Start Automation"
- [ ] Watch progress bar update
- [ ] Verify console shows live logs
- [ ] Verify counter shows jobs queued
- [ ] Wait for completion sound (if enabled)
- [ ] Check all leads saved to database

### Bell Icon / Sound
- [ ] Click bell icon 🔔
- [ ] Verify tooltip shows "Completion sound"
- [ ] Toggle to 🔕 (sound disabled)
- [ ] Toggle back to 🔔 (sound enabled)
- [ ] Run automation to completion
- [ ] Verify completion beep plays

---

## Known Issues & Workarounds

### Issue: Tauri App Shows "Not Found"
**Cause:** Tauri requires Rust compilation which needs Visual Studio C++ Build Tools

**Solution:** Use PyWebView instead (already configured in START.bat)

**If you still want to try Tauri:**
1. Run `INSTALL-BUILD-TOOLS.bat` (installs VS Build Tools)
2. **Reboot your computer** (required for environment variables)
3. Run `npm run dev`

**Recommended:** Just use START.bat with PyWebView - no reboot needed!

---

## Next Steps for Production

### Build Standalone EXE (Optional)
If you want a single .exe file instead of START.bat:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Scraper G1000" app_pywebview.py
```

This will create `dist/Scraper G1000.exe` - a portable desktop app.

### Database Backup
Before selling/deploying, make sure to:
- Backup all `profiles/*/leads_tracker.db` files
- Export leads to CSV for customers
- Document profile management workflow

---

## Support

If you encounter any issues:
1. Check that both servers are running (ports 5050 and 8080)
2. Verify PyWebView is installed: `pip show pywebview`
3. Check backend logs for errors
4. Verify frontend loads at http://localhost:8080/index.html

---

**Status:** ✅ READY FOR PRODUCTION
**Version:** 2.0 (PyWebView Desktop App)
**Last Updated:** 2025-10-17
