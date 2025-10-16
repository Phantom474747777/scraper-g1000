# 🦗 CritterCaptures Lead Scraper

**The easiest lead scraping system ever created.**

## 🚀 Quick Start

**Just double-click `START.bat` in File Explorer**

That's literally it. 🚀

---

## 🎯 What This Does

Scrapes local business leads for **CritterCaptures wildlife removal** services.

**Target customers** (NOT competitors):
- Property Management Companies
- Real Estate Agents
- HOA Management
- Apartment Complexes
- Vacation Rentals
- Storage Facilities
- Mobile Home Parks

---

## 📋 How It Works

### Step 1: Double-click `START.bat`

### Step 2: Choose from menu:
```
🦗 CritterCaptures Lead Scraper
============================================================

📋 MENU:
  [1] Start New Scrape
  [2] View Database Stats
  [3] List Available Categories
  [4] Exit
============================================================
```

### Step 3: Enter zip codes:
```
📮 Enter ZIP codes to scrape:
   (separate multiple with commas, e.g., 33527, 33594, 33612)

   Zip codes: 33527, 33594
```

### Step 4: Pick category:
```
📂 AVAILABLE CATEGORIES:
============================================================
  [1] Property Management Companies
  [2] Real Estate Agents
  [3] HOA Management
  [4] Apartment Complexes
  [5] Vacation Rentals
  [6] Storage Facilities
  [7] Mobile Home Parks
============================================================

🏷️  Select a category number (1-7):
   Category: 1
```

### Step 5: Press ENTER to start!

The scraper runs automatically and saves everything to organized folders.

---

## 📁 Where Are My Leads?

```
data/leads/
├── property_management_companies/
│   ├── lead_1_zip_33527/
│   │   └── 33527_2025-10-15_143022.csv
│   └── lead_2_zip_33594/
│       └── 33594_2025-10-15_143045.csv
│
├── real_estate_agents/
│   ├── lead_3_zip_33527/  ← SAME zip, different category!
│   └── lead_4_zip_33594/
│
└── hoa_management/
    └── lead_5_zip_33527/  ← SAME zip again!
```

**Each category gets its own folder.**
**Lead numbers increment automatically (1, 2, 3...).**

---

## 🔒 Safety Features

### ✅ Prevents Duplicate Leads
Once a zip+category combo is scraped, it's **BLOCKED FOREVER**:

```
⚠️  ALREADY SCRAPED!
   📅 Date: 2025-10-15 14:30:22
   📁 Folder: property_management_companies/lead_1_zip_33527
   🚫 SKIPPING!
```

### ✅ Allows Same Zip for Different Categories
You CAN scrape the same zip multiple times - just pick a different category!

Example:
- ZIP 33527 + Property Management = ✅ Lead 1
- ZIP 33527 + Real Estate Agents = ✅ Lead 2
- ZIP 33527 + Property Management = ❌ BLOCKED (already done!)

### ✅ Permanent Memory
Database remembers everything forever:
- Restart computer? Still remembers.
- Months later? Still remembers.
- Never sell duplicate leads!

---

## 🧹 Cleaning the Data

The data will be **messy** (no AI used during scraping).

**To clean:**
1. Open any CSV file
2. Copy all data
3. Paste into **ChatGPT Plus**
4. Say: "Clean this business data CSV. Extract name, phone, address. Return clean CSV."
5. Done!

---

## 💡 Pro Tips

### Tip #1: Start with Big Cities
Small towns have fewer results. Try:
- Tampa area: `33612`, `33629`, `33618`
- Brandon area: `33511`, `33510`
- Plant City: `33563`, `33566`

### Tip #2: Run All 7 Categories
Each category = different set of leads from same zips!
- Day 1: Property Management
- Day 2: Real Estate Agents
- Day 3: HOA Management
- etc.

### Tip #3: Use the Stats Feature
Check menu option [2] to see:
- Total leads in database
- Leads per zip code
- Your progress

### Tip #4: Scrape Regularly
Run weekly or monthly for fresh leads. The database prevents duplicates automatically!

---

## 📊 Menu Options Explained

### [1] Start New Scrape
Interactive wizard - asks for zips and category, then scrapes automatically.

### [2] View Database Stats
Shows total leads, breakdown by zip code.

### [3] List Available Categories
Quick reference of all 7 categories.

### [4] Exit
Closes the program.

---

## ⚙️ Technical Details

**What it does:**
- Scrapes YellowPages.com (no AI credits needed)
- Extracts: name, phone, address, website, email
- Saves to organized CSV files
- Tracks everything in SQLite database

**Database location:**
`data/leads_tracker.db`

**DO NOT DELETE THIS FILE** - it's your duplicate protection!

---

## 🔧 Troubleshooting

**"No businesses found"**
- Try bigger cities (Tampa instead of small towns)
- Try different category
- Some zips don't have all business types

**"All duplicates skipped"**
- You've already scraped this zip+category combo
- Pick a different category OR different zips

**Data looks messy**
- That's normal! No AI = raw data
- Upload to ChatGPT Plus to clean it

---

## 📈 Example Workflow

### Week 1: Property Management
```
Zips: 33527, 33594, 33612
Category: Property Management Companies
Result: 50 leads
```

### Week 2: Real Estate (SAME ZIPS!)
```
Zips: 33527, 33594, 33612
Category: Real Estate Agents
Result: 45 new leads (different businesses!)
```

### Week 3: HOA (SAME ZIPS AGAIN!)
```
Zips: 33527, 33594, 33612
Category: HOA Management
Result: 30 new leads
```

**Total: 125 leads from same 3 zips, 3 different categories!**

---

## ✅ Best Practices

**DO:**
- Run all 7 categories for maximum leads
- Use multiple zips at once
- Check stats regularly
- Keep the database file safe

**DON'T:**
- Delete `data/leads_tracker.db` (your safety net!)
- Delete the `data/` folder
- Worry about duplicates (system handles it)
- Expect perfect data (clean with ChatGPT)

---

## 🎉 That's It!

**You now have a production-ready lead scraping system that:**
- ✅ Asks you what to scrape (interactive menu)
- ✅ Organizes everything automatically
- ✅ Never duplicates leads
- ✅ Requires ZERO AI credits
- ✅ Works forever

**Just double-click `START.bat` and follow the prompts!** 🚀

---

## 📞 Need Help?

Check the menu option [3] to see all available categories.

Check option [2] to see your database stats.

Everything else is automatic!
