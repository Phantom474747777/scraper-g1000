# 🚀 Scraper G1000 - Universal Lead Generation System

**The most powerful universal lead scraping system with a beautiful modern desktop GUI.**

---

## 🎯 Quick Start - Build Desktop App

### **Option 1: Desktop Executable (RECOMMENDED)**

**Just double-click:** `BUILD-DESKTOP-APP.bat`

This creates `ScraperG1000.exe` - a real desktop app you can:
- Double-click to launch
- Pin to taskbar
- Create desktop shortcut
- Run like any other Windows app

**See:** `HOW-TO-BUILD-EXE.md` for details

---

### **Option 2: Run with Python**

```bash
pip install -r requirements.txt
python scraper-g1000.py
```

---

## ✨ What This Does

**Scraper G1000** is a universal business lead generation system that scrapes local business leads for **ANY** business type.

**Key Features:**
- 🎨 **Beautiful Modern GUI** - Dark theme with glassmorphic effects
- 🔄 **Multi-Source Scraping** - YellowPages + demo mode fallback
- 📊 **Dashboard Analytics** - View lead statistics and breakdowns
- 📤 **Export Functionality** - Export leads to CSV/Excel
- 🏷️ **Lead Management** - Mark leads as contacted, archived, or new
- 📱 **Bulk Operations** - Select multiple leads for batch actions
- 🔍 **Smart Filtering** - Filter by ZIP, category, status
- ✅ **Duplicate Prevention** - Automatic deduplication

---

## 📋 How It Works

1. **Launch the App** - Double-click ScraperG1000.exe
2. **Create/Select Profile** - Organize leads by business
3. **Choose Manual Mode** - Configure your scraping
4. **Enter Location** - City, state, radius
5. **Find ZIP Codes** - Discover nearby areas
6. **Select Category** - Any business type
7. **Start Scraping** - Watch the live console
8. **Manage Leads** - View, filter, export, contact tracking

---

## 🎨 Modern UI Features

- **Dark Theme** with gradient backgrounds
- **Glass Effects** and smooth animations
- **Toast Notifications** instead of ugly popups
- **Modal Dialogs** for professional UX
- **KPI Dashboard** with clickable analytics
- **Toggle Actions** - Archive/unarchive with one click

---

## 🗂️ Lead Management

### Status System
- **New** - Freshly scraped leads
- **Contacted** - Leads you've reached out to
- **Archived** - Leads you want to set aside

### Actions Available
- **Individual Actions** - Toggle status for single leads
- **Bulk Actions** - Select multiple leads for batch operations
- **Search & Filter** - Find leads by name, phone, location, category
- **Export Options** - CSV or Excel with custom styling

---

## 🔧 Technical Details

**What it scrapes:**
- YellowPages.com (primary source)
- Demo mode (fallback for testing)

**What it extracts:**
- Business name
- Phone number
- Address
- Website
- Email (when available)
- Category
- ZIP code
- City

**Database:**
- SQLite with automatic migrations
- Prevents duplicate leads
- Tracks lead status and history
- Supports multiple business profiles

**File Structure:**
```
Scraper G1000/
├── ScraperG1000.exe          # Desktop app (after building)
├── scraper-g1000.py           # Python launcher
├── backend/api_server.py      # REST API
├── src/                       # Core modules
│   ├── scraper_universal.py   # Scraper engine
│   ├── database.py            # Database ORM
│   └── ...
├── scraper-g1000-tauri/src/   # Frontend UI
└── data/                      # Database & history
```

---

## 💡 Pro Tips

### Tip #1: Use the Dashboard
The dashboard shows exactly where your leads come from and helps you plan your scraping strategy.

### Tip #2: Leverage Bulk Actions
Select multiple leads and use bulk operations to efficiently manage large lead lists.

### Tip #3: Export Regularly
Export your leads to CSV/Excel for external CRM systems or backup purposes.

### Tip #4: Use Toggle Actions
Don't worry about mistakes - you can always unarchive or mark leads as "not contacted."

---

## 🔒 Safety Features

✅ **Prevents Duplicate Leads** - Once scraped, automatically blocked from re-scraping
✅ **Status Tracking** - Never lose track of which leads you've contacted
✅ **Data Persistence** - All data saved automatically
✅ **Smart Validation** - Filters out junk leads with no phone/invalid data

---

## 🚀 Live Scraping vs Demo Mode

**Demo Mode (Current):**
- Generates realistic test data
- Perfect for testing the app
- No rate limiting issues
- Instant results

**To Enable Live Scraping:**
1. Use residential proxies (BrightData, Oxylabs)
2. Use paid scraping APIs (ScraperAPI, ScrapingBee)
3. Use browser automation (Playwright, Puppeteer)
4. See `FIXES_SUMMARY.md` for details

---

## 📞 Need Help?

The app is designed to be intuitive:
- Check the dashboard for lead statistics
- Use the search function to find specific leads
- Export your data regularly for backup
- Use bulk actions for efficient lead management

---

## 🎉 You're Ready!

**Just run:** `BUILD-DESKTOP-APP.bat`

Then double-click `ScraperG1000.exe` and start generating leads! 🚀

---

**Version:** 2.0
**Last Updated:** 2025-11-06
**Platform:** Windows
**License:** Private Use
