# Scraper G1000 v2.0 - COMPLETE FIX LIST ($100 BET)

## ISSUES REPORTED:

1. **❌ Page counter shows "Page 0/2" instead of "1/2", "2/2"**
2. **❌ Scraping returns 0 leads** - Backend scraper failing
3. **❌ Scraped combo indicators inaccurate** - Only showing 1 used when multiple should show
4. **❌ Combined ZIP+Category button doesn't work** - Just added UI, needs JavaScript logic

## FIXES NEEDED:

### 1. Fix Page Counter (app.js)
**Location:** `pollManualScrapingProgress()` function
**Change:** `currentPage` starts at 0, should start at 1
**Fix:** Add +1 to display: `Page ${currentPage + 1}/${maxPages}`

### 2. Fix Scraper Returning 0 Leads
**Check:** Backend scraper (`scraper_free_bypass.py` or similar)
**Issue:** YellowPages scraping logic may be broken
**Fix:** Debug scraper, check selectors, verify Crawl4AI extraction

### 3. Fix Scraped Combo Accuracy
**Location:** `/api/leads/<id>/scraped-combos` endpoint
**Check:** Database query in `api_server.py`
**Issue:** Query might not be returning all combinations
**Fix:** Verify SQL query groups by ZIP+Category correctly

### 4. Implement Combined Filter JavaScript
**Location:** `app.js` - add event listeners and logic
**Needed:**
```javascript
// Toggle to combined view
function toggleToCombinedView() {
  // Hide ZIP and Category sections
  document.getElementById('zipSection').style.display = 'none';
  document.getElementById('categorySection').style.display = 'none';
  document.getElementById('combinedSection').style.display = 'block';

  // Update button states
  document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('btnViewCombined').classList.add('active');

  // Populate dropdowns with scraped combos
  loadCombinedFilterOptions();
}

// Load combined filter dropdowns
async function loadCombinedFilterOptions() {
  const combos = await apiCall(`/api/leads/${currentProfileId}/scraped-combos`);

  // Populate ZIP dropdown
  const zipSelect = document.getElementById('filterCombinedZip');
  const uniqueZips = [...new Set(combos.combos.map(c => c.zip))];
  uniqueZips.forEach(zip => {
    const opt = document.createElement('option');
    opt.value = zip;
    opt.textContent = zip;
    zipSelect.appendChild(opt);
  });

  // Populate Category dropdown
  const catSelect = document.getElementById('filterCombinedCategory');
  const uniqueCats = [...new Set(combos.combos.map(c => c.category))];
  uniqueCats.forEach(cat => {
    const opt = document.createElement('option');
    opt.value = cat;
    opt.textContent = cat;
    catSelect.appendChild(opt);
  });
}

// Apply combined filter
async function applyCombinedFilter() {
  const zip = document.getElementById('filterCombinedZip').value;
  const cat = document.getElementById('filterCombinedCategory').value;

  if (!zip || !cat) {
    alert('Please select both ZIP and Category');
    return;
  }

  // Navigate to leads list with combined filter
  showFilteredLeads({type: 'combined', zip, category: cat});
}
```

## PRIORITY ORDER:
1. Fix page counter (2 min)
2. Debug scraper returning 0 leads (10 min)
3. Implement combined filter JS (15 min)
4. Fix scraped combo accuracy (5 min)

## TOTAL TIME: ~30 minutes to win the $100 bet!
