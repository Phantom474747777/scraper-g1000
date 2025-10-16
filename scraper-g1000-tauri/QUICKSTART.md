# Scraper G1000 - Quick Start Guide

## 🚀 First Time Setup

### 1. Prerequisites Check

Make sure you have:
- ✅ Python 3.11 installed
- ✅ Rust installed (you should have this already)
- ✅ Visual Studio Build Tools with C++ (installing now)

### 2. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Node packages
npm install
```

### 3. First Run (Development)

```bash
# Double-click this file:
START-DEV.bat

# Or manually:
npm run dev
```

The app will:
1. Start Python backend on port 5050
2. Start dev server on port 8080
3. Launch Tauri window

## 📦 Building Production .exe

```bash
# Double-click this file:
BUILD.bat

# Or manually:
npm run build
```

Output: `src-tauri/target/release/bundle/nsis/Scraper G1000_1.0.0_x64-setup.exe`

## 🎮 Using the App

### Profile Management
1. Launch app → Profile selector appears
2. Click "Create New Profile" or select existing
3. Default profile: **CritterCaptures** (wildlife removal)

### Scraping Leads
1. Select profile → Dashboard opens
2. Click "Manual Scrape"
3. Enter city/state (e.g., "Tampa, FL")
4. Select ZIP code (green = available, red = already used)
5. Select category (Real Estate, Property Managers, etc.)
6. Click "Start Scraping"

### Keyboard Shortcuts (During Scraping)
- **P** - Pause
- **R** - Resume
- **Q** - Quit
- **ESC** - Go back

### Viewing Leads
- Dashboard → "View Leads" button
- Browse all scraped leads
- Filter by category, ZIP, date
- Export to CSV (coming soon)

## 🔧 Troubleshooting

### "Cannot find Python"
Edit `src-tauri/src/lib.rs` line 13:
```rust
let python_path = "YOUR_PYTHON_PATH_HERE";
```

### "Port 5050 already in use"
Kill existing process:
```bash
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Backend"
```

### Tauri won't compile
```bash
# Clean and rebuild
cargo clean
npm run dev
```

### No leads found
- Check internet connection
- Try different category
- YellowPages structure may have changed (check scraper_free_bypass.py)

## 📂 Important Files

- `data/leads_tracker.db` - Main database (DON'T DELETE)
- `data/used_zips.json` - Tracks scraped ZIPs
- `profiles/` - Profile-specific databases
- `backend/api_server.py` - REST API server
- `src/index.html` - Main UI

## 🎨 Customization

### Change App Name
Edit `src-tauri/tauri.conf.json`:
```json
"productName": "Your App Name"
```

### Change Categories
Edit `python-src/profile_manager.py` → `CATEGORIES` list

### Change UI Colors
Edit `src/styles/main.css` → `:root` variables

## 📞 Support

If stuck, check:
1. Backend logs (terminal running api_server.py)
2. Browser console (F12 in dev mode)
3. Rust console output
4. Check README.md for detailed docs

---

**Need help? Check the full README.md for detailed documentation.**
