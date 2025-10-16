# CritterCaptures Lead Generation - Project Memory

## 📋 Project Overview

**Project Name:** CritterCaptures Smart Lead Generation System  
**Purpose:** Interactive CLI tool that scrapes local business leads for wildlife/pest control services  
**Technology Stack:** Crawl4AI + InquirerPy (interactive CLI) + SQLite + Geopy  
**Target Area:** 50-mile radius from any US city (default: Dover, FL)  
**Data Source:** YellowPages.com

## 🎯 What Makes This System Smart

### Interactive CLI Features:
1. **City-based ZIP lookup**: Enter any city/state, get all ZIPs within 50 miles
2. **Color-coded ZIP selection**:
   - 🟢 Green = Fully available (no categories scraped)
   - 🟡 Yellow = Partially used (some categories remaining)
   - 🔴 Red = Fully used (all categories already scraped)
3. **Color-coded category selection**:
   - 🟢 Green = Not yet scraped for this ZIP
   - 🔴 Red = Already scraped (warns if user tries to re-scrape)
4. **Smart tracking**: `data/used_zips.json` prevents duplicate work
5. **No AI scoring needed**: Raw data → you clean with ChatGPT Plus

## 🏗️ Project Structure

```
ai-web-scraper/
├── START.bat              # 👈 DOUBLE-CLICK THIS to launch CLI
├── leadgen_cli.py         # 🌟 NEW: Main interactive CLI entry point
├── get_critter_leads.py   # Old entry point (kept for reference)
├── requirements.txt       # Python dependencies
├── README.md             # User documentation
├── CLAUDE.md             # This file - project memory
├── .gitignore            # Git ignore rules
├── .env                  # Environment variables (optional - no AI keys needed!)
│
├── models/
│   ├── __init__.py
│   └── business.py       # Pydantic model for business data structure
│
├── src/
│   ├── __init__.py
│   ├── scraper.py        # Core scraping functions (browser config, LLM strategy)
│   ├── database.py       # SQLite database for permanent lead storage
│   ├── utils.py          # Utility functions (CSV, deduplication)
│   ├── zip_lookup.py     # 🆕 ZIP code radius search using geopy
│   └── tracking.py       # 🆕 Track used ZIP+category combinations
│
└── data/
    ├── leads_tracker.db   # SQLite database (NEVER DELETE)
    ├── used_zips.json     # 🆕 Tracks which ZIP+category combos are used
    └── {zip}_{category}_leads_{timestamp}.csv  # Output files
```

## 🔑 Environment Variables (Optional)

Previously required, now optional:
```
GEMINI_API_KEY=not_needed_anymore
GROQ_API_KEY=not_needed_anymore
```

**Why optional?** The scraper extracts data using Crawl4AI's built-in LLM, but we removed AI-based lead scoring. You clean leads yourself in ChatGPT Plus.

## 📦 Dependencies

```
Crawl4AI==0.4.247        # AI-powered web scraping framework
python-dotenv==1.0.1     # Environment variable management
pydantic==2.10.6         # Data validation and modeling
InquirerPy==0.3.4        # 🆕 Interactive CLI with color support
geopy==2.4.1             # 🆕 Geocoding and distance calculations
requests>=2.31.0         # 🆕 HTTP requests for ZIP APIs
```

Install with: `pip install -r requirements.txt`

## 🚀 How to Use

### Quick Start:
1. **Double-click `START.bat`** in File Explorer
2. Enter your target city (e.g., "Dover")
3. Enter state code (e.g., "FL")
4. Select a ZIP code from the color-coded list
5. Select a category from the color-coded list
6. Confirm and watch it scrape!

### What Happens:
```
1. Find ZIPs → System finds all ZIPs within 50 miles of your city
2. Show ZIPs → Color-coded dropdown (green=available, red=used)
3. Select ZIP → Pick which ZIP to scrape
4. Show Categories → Color-coded by availability for that ZIP
5. Select Category → Pick which business type to scrape
6. Scrape → Automatically scrapes YellowPages
7. Clean → Removes duplicates using database
8. Save → Writes to data/{zip}_{category}_leads_{timestamp}.csv
9. Track → Marks ZIP+category as "used" in used_zips.json
10. Continue? → Option to scrape another combo
```

## 🎨 Customer-Oriented Categories

These are **potential customers** who might need wildlife removal (NOT competitors):

1. Real Estate Agents
2. Property Managers
3. Home Inspectors
4. Construction Companies
5. Roofing Contractors
6. HVAC Services
7. Plumbing Companies
8. Landscaping Companies
9. Cleaning Services

## 📊 Output Format

**Filename Pattern:** `data/{zip}_{category}_leads_{timestamp}.csv`

**Example:** `data/33527_real_estate_agents_leads_2025-10-15_143022.csv`

**CSV Columns:**
- `name` - Business name
- `address` - Full address
- `phone_number` - Contact phone
- `website` - Business website URL
- `email` - Email address (if available, else "N/A")
- `category` - Which category was scraped
- `zip_code` - ZIP code scraped

## 🗄️ Tracking Systems

### 1. Database (`data/leads_tracker.db`)
**Purpose:** Permanent storage of all unique leads ever scraped

**Prevents:** Saving the same business twice (across all sessions)

### 2. JSON Tracker (`data/used_zips.json`)
**Purpose:** Track which ZIP+category combinations have been scraped

**Structure:**
```json
{
  "33527": {
    "categories": ["Real Estate Agents", "Property Managers"],
    "history": [
      {
        "category": "Real Estate Agents",
        "scraped_at": "2025-10-15T14:30:22",
        "leads_found": 45,
        "output_file": "data/33527_real_estate_agents_leads_2025-10-15_143022.csv"
      }
    ]
  }
}
```

**Prevents:** Re-scraping the same ZIP+category combo

## 🎨 Color Coding System

### ZIP Code Colors:
- 🟢 **Green**: All 9 categories available
- 🟡 **Yellow**: Some categories used, some available (e.g., "3 categories available")
- 🔴 **Red**: All categories already scraped

### Category Colors (for selected ZIP):
- 🟢 **Green**: Not yet scraped for this ZIP
- 🔴 **Red**: Already scraped for this ZIP (warns before allowing re-scrape)

## 🔧 Configuration

**Search radius:** 50 miles (configurable in `zip_lookup.py`)

**Pages per search:** 2 (configurable in `leadgen_cli.py`)

**Known Tampa Bay ZIPs:** Pre-loaded in `zip_lookup.py` for Florida searches

## 🧹 Data Flow Pipeline

```
1. USER INPUT
   └─> City: "Dover", State: "FL"

2. ZIP LOOKUP (geopy + haversine)
   └─> Finds ~30 ZIPs within 50 miles

3. ZIP SELECTION (InquirerPy)
   ├─> Load tracking from used_zips.json
   ├─> Color-code each ZIP (green/yellow/red)
   └─> User selects one ZIP

4. CATEGORY SELECTION (InquirerPy)
   ├─> Load categories for selected ZIP
   ├─> Color-code each category (green/red)
   └─> User selects one category

5. SCRAPING (Crawl4AI)
   └─> Scrapes YellowPages for selected ZIP+category

6. CLEANING (database.py)
   ├─> Remove duplicates within session
   └─> Remove duplicates from database

7. SAVING (CSV)
   └─> Write to data/{zip}_{category}_leads_{timestamp}.csv

8. TRACKING (tracking.py)
   ├─> Mark ZIP+category as "used"
   ├─> Save to used_zips.json
   └─> Update database

9. CONTINUE?
   └─> Prompt user to scrape another combo or exit
```

## 🎨 Code Quality Standards

1. **PEP8 Compliance** - Follow Python style guidelines
2. **Modular Design** - Separate concerns (scraping, database, tracking, UI)
3. **Type Hints** - Use Pydantic for data validation
4. **Error Handling** - Graceful failures with try/except
5. **User Feedback** - Clear messages with emojis
6. **Interactive UX** - Color-coded, arrow-key navigation

## 🔒 Important Rules

### DO:
✅ Keep `data/leads_tracker.db` - permanent lead storage  
✅ Keep `data/used_zips.json` - prevents duplicate work  
✅ Use the interactive CLI (`leadgen_cli.py`) for all scraping  
✅ Follow color codes (green=go, red=stop)  
✅ Clean leads yourself in ChatGPT Plus (faster than AI scoring)

### DON'T:
❌ Delete the database file (`leads_tracker.db`)  
❌ Delete `used_zips.json` (you'll lose tracking)  
❌ Re-scrape red-marked ZIP+category combos (wastes time)  
❌ Expect AI scoring (we removed it - you'll clean manually)  
❌ Commit CSV files to git (.gitignore handles this)

## 📝 Logging & Output

The CLI uses emoji-based logging:
- 🔍 = Searching/looking up
- ✓ = Success
- ⚠️ = Warning
- ❌ = Error/failure
- 💾 = Saving data
- 🧹 = Cleaning data
- 📊 = Statistics
- 🟢🟡🔴 = Status indicators

## 🔄 Session History

**2025-10-15 (Morning):**
- ✅ Completed cleanup phase
- ✅ Fixed Python path in START.bat
- ✅ Removed AI scoring (GROQ/Gemini)

**2025-10-15 (Evening - MAJOR UPGRADE):**
- ✅ Created interactive CLI with color-coded dropdowns
- ✅ Added ZIP code radius search (50 miles)
- ✅ Implemented smart tracking system (used_zips.json)
- ✅ Fixed data saving bug (verified CSV creation)
- ✅ Updated categories to customer-oriented businesses
- ✅ Integrated InquirerPy for beautiful terminal UI
- ✅ Added geopy for geocoding
- ✅ System now prevents duplicate work automatically

## 💡 Future Enhancements

Potential improvements:
- [ ] Export to Excel format
- [ ] Email validation/verification
- [ ] Bulk city import (scrape multiple cities at once)
- [ ] Visual progress bar for long scrapes
- [ ] Web dashboard (optional)
- [ ] Integration with CRM systems

## 🆘 Troubleshooting

**Issue:** "No ZIP codes found"
- Solution: Check city spelling, try nearby larger city

**Issue:** "All categories already scraped"  
- Solution: Select a different ZIP (green or yellow)

**Issue:** Import errors
- Solution: Run `pip install -r requirements.txt`

**Issue:** No CSV files created
- Solution: Check `data/` folder exists, verify file permissions

**Issue:** Colors not showing
- Solution: Windows Terminal or PowerShell 7+ recommended

## 📞 How It Works Internally

### ZIP Lookup:
1. User enters "Dover, FL"
2. Geopy geocodes → lat/lng coordinates
3. Haversine formula calculates distance to known FL ZIPs
4. Returns all ZIPs within 50 miles, sorted by distance

### Color Coding:
1. Load `used_zips.json`
2. For each ZIP, check how many categories used
3. Green if 0, Yellow if 1-8, Red if all 9

### Scraping:
1. Build YellowPages URL with ZIP+category
2. Crawl4AI extracts business data (name, phone, address, etc.)
3. Store in memory, dedupe against database
4. Write to CSV with timestamp
5. Mark as "used" in tracking

---

**Last Updated:** 2025-10-15  
**Status:** ✅ Production Ready (Smart CLI Upgrade)  
**Version:** 2.0 (Interactive CLI with Smart Tracking)
