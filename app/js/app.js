/**
 * Scraper G1000 - Frontend Application Logic
 * Handles UI interactions and communication with backend
 */

// State management
let currentProfile = null;
let currentScreen = 'profile-selector';

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
  console.log('[App] Initializing Scraper G1000...');

  // Load profiles
  await loadProfiles();

  // Setup event listeners
  setupEventListeners();

  console.log('[App] Initialization complete');
});

// === PROFILE MANAGEMENT ===

async function loadProfiles() {
  const profileList = document.getElementById('profileList');

  try {
    const profiles = await window.api.getProfiles();

    if (profiles.length === 0) {
      profileList.innerHTML = '<div class="profile-loading">No profiles found. Create your first profile!</div>';
      return;
    }

    profileList.innerHTML = profiles.map(profile => `
      <div class="profile-card" data-profile-id="${profile.id}" onclick="selectProfile('${profile.id}')">
        <div class="profile-icon">${profile.icon}</div>
        <div class="profile-info">
          <div class="profile-name">${profile.name}</div>
          <div class="profile-stats">${profile.totalLeads} leads · Last used ${formatDate(profile.lastUsed)}</div>
        </div>
        <div class="profile-arrow">→</div>
      </div>
    `).join('');
  } catch (error) {
    console.error('[App] Failed to load profiles:', error);
    profileList.innerHTML = '<div class="profile-loading">Error loading profiles</div>';
  }
}

function selectProfile(profileId) {
  console.log('[App] Selected profile:', profileId);
  currentProfile = profileId;

  // Update UI
  document.getElementById('currentProfile').textContent = profileId;

  // Navigate to dashboard
  navigateTo('dashboard');

  // Load profile data
  loadDashboardData();
}

// === SCREEN NAVIGATION ===

function navigateTo(screenId) {
  // Hide all screens
  document.querySelectorAll('.screen').forEach(screen => {
    screen.classList.remove('active');
  });

  // Show target screen
  const targetScreen = document.getElementById(screenId);
  if (targetScreen) {
    targetScreen.classList.add('active');
    currentScreen = screenId;
    console.log('[App] Navigated to:', screenId);
  }
}

// === DASHBOARD ===

async function loadDashboardData() {
  try {
    // Load leads count
    const leads = await window.api.getLeads(currentProfile);
    document.getElementById('statTotalLeads').textContent = leads.length.toLocaleString();

    // TODO: Load recent activity
    // TODO: Load other stats
  } catch (error) {
    console.error('[App] Failed to load dashboard data:', error);
  }
}

// === MANUAL SCRAPING ===

function validateManualScrapeForm() {
  const city = document.getElementById('inputCity').value.trim();
  const state = document.getElementById('inputState').value.trim();
  const categorySelect = document.getElementById('selectCategory').value;
  const customCategory = document.getElementById('inputCustomCategory').value.trim();
  const selectedZip = document.querySelector('.zip-item.selected');
  const btnStartScrape = document.getElementById('btnStartScrape');

  // Check if all required fields are filled
  const hasCity = city.length > 0;
  const hasState = state.length > 0;
  const hasZip = selectedZip !== null;

  // Category is valid if:
  // - A predefined category is selected, OR
  // - "custom" is selected AND custom input has text
  const hasCategory = (categorySelect && categorySelect !== '' && categorySelect !== 'custom') ||
                      (categorySelect === 'custom' && customCategory.length > 0);

  const isFormValid = hasCity && hasState && hasZip && hasCategory;

  if (btnStartScrape) {
    btnStartScrape.disabled = !isFormValid;
  }

  return isFormValid;
}

async function startManualScrape() {
  const city = document.getElementById('inputCity').value.trim();
  const state = document.getElementById('inputState').value.trim();
  const categorySelect = document.getElementById('selectCategory').value;
  const customCategory = document.getElementById('inputCustomCategory').value.trim();
  const selectedZip = document.querySelector('.zip-item.selected')?.dataset.zip;

  // Determine which category to use
  let category = categorySelect;
  if (categorySelect === 'custom') {
    category = customCategory;
  }

  if (!city || !state || !selectedZip || !category) {
    alert('Please fill in all fields');
    return;
  }

  const config = {
    profileId: currentProfile,
    city,
    state,
    zipCode: selectedZip,
    category,
    maxPages: 2
  };

  console.log('[App] Starting scrape:', config);

  try {
    await window.api.startScraping(config);
    navigateTo('scraping-progress');
  } catch (error) {
    console.error('[App] Scraping failed:', error);
    alert('Failed to start scraping: ' + error.message);
  }
}

// === EVENT LISTENERS ===

function setupEventListeners() {
  // Profile selector
  const btnCreateProfile = document.getElementById('btnCreateProfile');
  if (btnCreateProfile) {
    btnCreateProfile.addEventListener('click', () => {
      alert('Create Profile feature coming soon!');
    });
  }

  // Dashboard
  const cardManualScrape = document.getElementById('cardManualScrape');
  if (cardManualScrape) {
    cardManualScrape.addEventListener('click', () => {
      navigateTo('manual-scrape');
    });
  }

  const cardAutoScrape = document.getElementById('cardAutoScrape');
  if (cardAutoScrape) {
    cardAutoScrape.addEventListener('click', () => {
      navigateTo('auto-scrape');
    });
  }

  const btnViewLeads = document.getElementById('btnViewLeads');
  if (btnViewLeads) {
    btnViewLeads.addEventListener('click', () => {
      navigateTo('leads-viewer');
      loadLeadsTable();
    });
  }

  // Navigation
  const btnBack = document.getElementById('btnBack');
  if (btnBack) {
    btnBack.addEventListener('click', () => {
      navigateTo('profile-selector');
      currentProfile = null;
    });
  }

  const btnBackFromManual = document.getElementById('btnBackFromManual');
  if (btnBackFromManual) {
    btnBackFromManual.addEventListener('click', () => {
      navigateTo('dashboard');
    });
  }

  const btnBackFromLeads = document.getElementById('btnBackFromLeads');
  if (btnBackFromLeads) {
    btnBackFromLeads.addEventListener('click', () => {
      navigateTo('dashboard');
    });
  }

  // Manual scrape
  const btnFindZips = document.getElementById('btnFindZips');
  if (btnFindZips) {
    btnFindZips.addEventListener('click', findZipsNearLocation);
  }

  const btnStartScrape = document.getElementById('btnStartScrape');
  if (btnStartScrape) {
    btnStartScrape.addEventListener('click', startManualScrape');
  }

  // Radius slider
  const inputRadius = document.getElementById('inputRadius');
  const radiusValue = document.getElementById('radiusValue');
  if (inputRadius && radiusValue) {
    inputRadius.addEventListener('input', (e) => {
      radiusValue.textContent = e.target.value;
    });
  }

  // Category dropdown - show custom input when "custom" selected
  const selectCategory = document.getElementById('selectCategory');
  const customCategoryContainer = document.getElementById('customCategoryContainer');
  const inputCustomCategory = document.getElementById('inputCustomCategory');

  if (selectCategory && customCategoryContainer) {
    selectCategory.addEventListener('change', (e) => {
      if (e.target.value === 'custom') {
        customCategoryContainer.style.display = 'block';
        inputCustomCategory.focus();
      } else {
        customCategoryContainer.style.display = 'none';
      }
      validateManualScrapeForm();
    });
  }

  // Validate form on input changes
  const inputCity = document.getElementById('inputCity');
  const inputState = document.getElementById('inputState');

  if (inputCity) inputCity.addEventListener('input', validateManualScrapeForm);
  if (inputState) inputState.addEventListener('input', validateManualScrapeForm);
  if (inputCustomCategory) inputCustomCategory.addEventListener('input', validateManualScrapeForm);

  // Progress
  const btnPauseScrape = document.getElementById('btnPauseScrape');
  if (btnPauseScrape) {
    btnPauseScrape.addEventListener('click', () => {
      window.api.pauseScraping();
    });
  }

  const btnCancelScrape = document.getElementById('btnCancelScrape');
  if (btnCancelScrape) {
    btnCancelScrape.addEventListener('click', () => {
      if (confirm('Are you sure you want to cancel scraping?')) {
        window.api.stopScraping();
        navigateTo('dashboard');
      }
    });
  }

  // Listen for scraping events
  window.api.onScrapingProgress((data) => {
    updateScrapingProgress(data);
  });

  window.api.onScrapingComplete((data) => {
    alert(`Scraping complete! Found ${data.totalLeads} leads`);
    navigateTo('dashboard');
    loadDashboardData();
  });

  window.api.onScrapingError((error) => {
    alert('Scraping error: ' + error.message);
    navigateTo('dashboard');
  });
}

// === HELPER FUNCTIONS ===

async function findZipsNearLocation() {
  const city = document.getElementById('inputCity').value;
  const state = document.getElementById('inputState').value;
  const radius = document.getElementById('inputRadius').value;

  if (!city || !state) {
    alert('Please enter city and state');
    return;
  }

  const zipList = document.getElementById('zipList');
  zipList.innerHTML = '<div class="loading">Finding ZIP codes...</div>';

  // TODO: Call backend to get ZIPs
  setTimeout(() => {
    zipList.innerHTML = `
      <div class="zip-item" data-zip="33527" onclick="selectZip('33527')">
        <span class="zip-code">33527</span>
        <span class="zip-city">Dover</span>
      </div>
      <div class="zip-item" data-zip="33510" onclick="selectZip('33510')">
        <span class="zip-code">33510</span>
        <span class="zip-city">Gibsonton</span>
      </div>
    `;
  }, 1000);
}

function selectZip(zipCode) {
  document.querySelectorAll('.zip-item').forEach(item => {
    item.classList.remove('selected');
  });

  const selectedItem = document.querySelector(`[data-zip="${zipCode}"]`);
  if (selectedItem) {
    selectedItem.classList.add('selected');
  }

  // Validate form after ZIP selection
  validateManualScrapeForm();
}

async function loadLeadsTable() {
  const tbody = document.getElementById('leadsTableBody');

  try {
    const leads = await window.api.getLeads(currentProfile);

    if (leads.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="loading">No leads found</td></tr>';
      return;
    }

    tbody.innerHTML = leads.map(lead => `
      <tr>
        <td><input type="checkbox" value="${lead.id}"></td>
        <td>${lead.name}</td>
        <td>${lead.category}</td>
        <td>${lead.phone}</td>
        <td>${lead.address}</td>
        <td>${lead.zipCode}</td>
      </tr>
    `).join('');

    document.getElementById('leadsCount').textContent = leads.length.toLocaleString();
  } catch (error) {
    console.error('[App] Failed to load leads:', error);
    tbody.innerHTML = '<tr><td colspan="6" class="loading">Error loading leads</td></tr>';
  }
}

function updateScrapingProgress(data) {
  const progressBar = document.getElementById('progressBar');
  const progressText = document.getElementById('progressText');
  const progressTime = document.getElementById('progressTime');

  if (progressBar) {
    progressBar.style.width = data.progress + '%';
  }

  if (progressText) {
    progressText.textContent = `Page ${data.currentPage} of ${data.totalPages} · ${data.leadsFound} leads`;
  }

  if (progressTime && data.estimatedTimeRemaining) {
    progressTime.textContent = `${data.estimatedTimeRemaining} seconds remaining`;
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));

  if (diffHours < 1) return 'just now';
  if (diffHours < 24) return `${diffHours} hours ago`;
  if (diffHours < 48) return 'yesterday';

  return date.toLocaleDateString();
}

console.log('[App] Module loaded');
