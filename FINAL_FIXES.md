# Scraper G1000 v2.0 - Final Fixes Summary

## ✅ WHAT WORKS NOW:
1. **Progress bar** - Continuously moves forward (smooth animation)
2. **ZIP lookup** - Returns 100+ ZIPs for 100-mile radius using pgeocode (works for ALL USA cities!)
3. **Scraped combo indicators** - Backend API `/api/leads/<id>/scraped-combos` exists
4. **Dropout indicators in Manual Mode** - ZIPs show `⚠️ (2/9 used)` in orange, Categories show `⚠️ (Already scraped)` in red

## ❌ WHAT NEEDS FIXING:

### 1. Combined ZIP+Category Filter on Main Leads Page
**Problem**: When you click "View Leads" after scraping, it filters by ZIP+Category. But when you go to the main Leads page (from dashboard), you can only filter by ZIP OR Category, not BOTH together.

**Solution Needed**:
- Add a "Combined Filter" option to the Leads page
- Show dropdown or checkboxes: [ZIP] + [Category]
- When both are selected, filter leads matching BOTH criteria
- This matches the "View Leads" button behavior from Manual Mode

### 2. Test Scraped Combo Indicators
**Status**: Code exists, needs verification with actual scraped data
- When you scrape ZIP 33770 + "Real Estate Agents"
- Then search again, ZIP 33770 should show `⚠️ (1/9 used)` in orange
- Category "Real Estate Agents" should show `⚠️ (Already scraped)` in red

## 📋 IMPLEMENTATION PLAN:

###Step 1: Add Combined Filter UI to Leads Page
Location: `scraper-g1000-tauri/src/index.html` (leads-dashboard screen)

Add new filter section:
```html
<div class="filter-combined">
  <label>Filter by ZIP + Category:</label>
  <select id="filterCombinedZip">
    <option value="">All ZIPs</option>
    <!-- Populate dynamically -->
  </select>
  <span>+</span>
  <select id="filterCombinedCategory">
    <option value="">All Categories</option>
    <!-- Populate from scraped combos -->
  </select>
  <button onclick="applyCombin edFilter()">Apply</button>
</div>
```

### Step 2: Implement Combined Filter Logic
Location: `scraper-g1000-tauri/src/js/app.js`

Add function:
```javascript
async function applyCombinedFilter() {
  const zip = document.getElementById('filterCombinedZip').value;
  const category = document.getElementById('filterCombinedCategory').value;

  if (zip && category) {
    // Show leads matching BOTH
    showFilteredLeads({type: 'combined', zip, category});
  }
}
```

### Step 3: Populate Combined Filter Dropdowns
Load scraped ZIP+Category combinations from backend and populate dropdowns dynamically.

## 🎯 END GOAL:
User can filter leads by:
1. ZIP only (existing)
2. Category only (existing)
3. ZIP + Category together (NEW!)

This matches the "View Leads" button behavior and makes the app truly v2.0!
