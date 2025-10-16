/**
 * Scraper G1000 - Frontend
 */

const API_BASE = 'http://localhost:5050';
let currentProfileId = null;
let currentProfileData = null;
let currentFilter = null;

console.log('[App] Scraper G1000 loaded');

// === API Helper ===
async function apiCall(endpoint, method = 'GET', body = null) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store'  // Disable browser caching
  };
  if (body) options.body = JSON.stringify(body);
  const response = await fetch(`${API_BASE}${endpoint}`, options);
  return await response.json();
}

// === Toast Notifications ===
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  const icons = {
    success: '✓',
    error: '✗',
    info: 'ℹ'
  };

  toast.innerHTML = `
    <div class="toast-icon">${icons[type] || icons.info}</div>
    <div class="toast-message">${message}</div>
  `;

  container.appendChild(toast);

  // Auto-remove after 4 seconds
  setTimeout(() => {
    toast.classList.add('toast-exit');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// === Screen Navigation ===
function showScreen(screenId) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(screenId).classList.add('active');
}

// === Load Profiles on Startup ===
document.addEventListener('DOMContentLoaded', async () => {
  console.log('[App] DOM loaded, fetching profiles...');
  const profileList = document.getElementById('profileList');

  try {
    const data = await apiCall('/api/profiles');
    console.log('[App] Profiles response:', data);

    if (!data.success || !data.profiles || data.profiles.length === 0) {
      profileList.innerHTML = '<div class="profile-empty">No profiles yet. Create one to get started!</div>';
      return;
    }

    window.allProfiles = data.profiles;

    profileList.innerHTML = data.profiles.map(p => `
      <div class="profile-card" onclick="selectProfile('${p.id}')">
        <div class="profile-info">
          <h3>${p.name}</h3>
          <p>${p.businessType || 'General'}</p>
          <span class="profile-stats">${p.totalLeads || 0} Valid Leads${p.flaggedLeads > 0 ? ' • ' + p.flaggedLeads + ' Flagged' : ''}</span>
        </div>
      </div>
    `).join('');

    console.log('[App] Loaded', data.profiles.length, 'profiles');
  } catch (error) {
    console.error('[App] Failed to load profiles:', error);
    profileList.innerHTML = '<div class="profile-error">Failed to load profiles: ' + error.message + '</div>';
  }

  setupEventListeners();
});

// === Profile Selection ===
function selectProfile(profileId) {
  console.log('[App] Selected profile:', profileId);
  currentProfileId = profileId;
  currentProfileData = window.allProfiles.find(p => p.id === profileId);

  document.getElementById('currentProfile').textContent = currentProfileData.name;
  document.getElementById('statTotalLeads').textContent = currentProfileData.totalLeads || 0;

  showScreen('dashboard');
}

// === Setup Event Listeners ===
function setupEventListeners() {
  document.getElementById('btnBack')?.addEventListener('click', () => showScreen('profile-selector'));
  document.getElementById('cardManualScrape')?.addEventListener('click', () => {
    showScreen('manual-scrape');
    loadCategories();
  });

  // View Leads now loads dashboard
  document.getElementById('btnViewLeads')?.addEventListener('click', loadLeadsDashboard);

  // Back buttons
  document.getElementById('btnBackFromManual')?.addEventListener('click', () => showScreen('dashboard'));
  document.getElementById('btnBackFromLeadsDashboard')?.addEventListener('click', () => showScreen('dashboard'));
  document.getElementById('btnBackFromList')?.addEventListener('click', () => {
    // Reload dashboard to refresh stats after status changes
    loadLeadsDashboard();
  });

  // Toggle buttons for ZIP / Category view
  document.getElementById('btnViewZips')?.addEventListener('click', toggleToZipView);
  document.getElementById('btnViewCategories')?.addEventListener('click', toggleToCategoryView);

  // Scraping
  document.getElementById('btnStartScrape')?.addEventListener('click', startManualScrape);
  document.getElementById('inputRadius')?.addEventListener('input', (e) => {
    document.getElementById('radiusValue').textContent = e.target.value;
  });

  // Export button
  document.getElementById('btnExportLeads')?.addEventListener('click', exportFilteredLeads);

  // Select All checkbox
  document.getElementById('selectAll')?.addEventListener('change', (e) => {
    const checkboxes = document.querySelectorAll('#leadsTableBody input[type="checkbox"]');
    checkboxes.forEach(cb => cb.checked = e.target.checked);
  });

  // Search functionality
  document.getElementById('searchLeads')?.addEventListener('input', (e) => {
    filterLeadsTable(e.target.value);
  });

  document.addEventListener('keydown', handleKeyboardShortcuts);
}

// === Keyboard Shortcuts ===
function handleKeyboardShortcuts(e) {
  const activeScreen = document.querySelector('.screen.active')?.id;
  if (activeScreen === 'scraping-progress') {
    if (e.key === 'p' || e.key === 'P') document.getElementById('btnPauseScrape')?.click();
    else if (e.key === 'r' || e.key === 'R') document.getElementById('btnPauseScrape')?.click();
    else if (e.key === 'q' || e.key === 'Q') document.getElementById('btnCancelScrape')?.click();
  }
}

// === Load Categories ===
function loadCategories() {
  const select = document.getElementById('selectCategory');
  const categories = ['Real Estate Agents', 'Property Managers', 'Home Inspectors', 'Construction Companies', 'Roofing Contractors', 'HVAC Services', 'Plumbing Companies', 'Landscaping Companies', 'Cleaning Services'];
  select.innerHTML = '<option value="">Choose a category...</option>' + categories.map(cat => `<option value="${cat}">${cat}</option>`).join('');
}

// === Toggle View Functions ===
function toggleToZipView() {
  document.getElementById('btnViewZips').classList.add('active');
  document.getElementById('btnViewCategories').classList.remove('active');
  document.getElementById('zipSection').style.display = 'block';
  document.getElementById('categorySection').style.display = 'none';
}

function toggleToCategoryView() {
  document.getElementById('btnViewCategories').classList.add('active');
  document.getElementById('btnViewZips').classList.remove('active');
  document.getElementById('categorySection').style.display = 'block';
  document.getElementById('zipSection').style.display = 'none';
}

// === Load Leads Dashboard ===
async function loadLeadsDashboard() {
  console.log('[Dashboard] Loading dashboard for profile:', currentProfileId);
  showScreen('leads-dashboard');

  try {
    // ALWAYS fetch fresh data from server
    const statsData = await apiCall(`/api/dashboard/${currentProfileId}`);
    console.log('[Dashboard] Stats:', statsData);

    if (!statsData.success) {
      alert('Failed to load dashboard: ' + statsData.error);
      return;
    }

    const stats = statsData.stats;

    // Populate KPI cards with FRESH data
    document.getElementById('cardAllLeadsCount').textContent = stats.total || 0;
    document.getElementById('cardUncontactedCount').textContent = stats.by_status?.New || 0;
    document.getElementById('cardContactedCount').textContent = stats.by_status?.Contacted || 0;
    document.getElementById('cardArchivedCount').textContent = stats.by_status?.Archived || 0;

    // Load FRESH leads data
    const leadsData = await apiCall(`/api/leads/${currentProfileId}`);
    const allLeads = leadsData.success ? leadsData.leads : [];

    // Generate ZIP cards with breakdown
    const zipCards = document.getElementById('zipCards');
    if (stats.by_zip && stats.by_zip.length > 0) {
      zipCards.innerHTML = stats.by_zip.map(([zip, count]) => {
        // Calculate breakdown for this ZIP from FRESH data
        const zipLeads = allLeads.filter(lead => lead.zipCode === zip);
        const newCount = zipLeads.filter(lead => (lead.status || 'New') === 'New').length;
        const contactedCount = zipLeads.filter(lead => lead.status === 'Contacted').length;
        const archivedCount = zipLeads.filter(lead => lead.status === 'Archived').length;

        return `
          <div class="zip-card" onclick="showFilteredLeads({type: 'zip', value: '${zip}'})">
            <div class="zip-card-header">
              <div class="zip-code">ZIP ${zip}</div>
            </div>
            <div class="zip-count">${count}</div>
            <div class="zip-breakdown">
              <div class="breakdown-item new">
                <span class="breakdown-dot"></span>
                <span>${newCount} New</span>
              </div>
              <div class="breakdown-item contacted">
                <span class="breakdown-dot"></span>
                <span>${contactedCount} Contacted</span>
              </div>
              <div class="breakdown-item archived">
                <span class="breakdown-dot"></span>
                <span>${archivedCount} Archived</span>
              </div>
            </div>
          </div>
        `;
      }).join('');
    } else {
      zipCards.innerHTML = '<div class="loading-placeholder">No ZIP data available</div>';
    }

    // Generate Category cards
    const categoryCards = document.getElementById('categoryCards');
    if (stats.by_category && stats.by_category.length > 0) {
      categoryCards.innerHTML = stats.by_category.map(([category, count]) => `
        <div class="category-card" onclick="showFilteredLeads({type: 'category', value: '${category}'})">
          <div class="category-card-header">${category}</div>
          <div class="category-count">${count}</div>
          <div class="category-label">Leads</div>
        </div>
      `).join('');
    } else {
      categoryCards.innerHTML = '<div class="loading-placeholder">No category data available</div>';
    }

    // Setup KPI card click handlers
    document.getElementById('cardAllLeads')?.addEventListener('click', () => showFilteredLeads({type: 'all'}));
    document.getElementById('cardUncontacted')?.addEventListener('click', () => showFilteredLeads({type: 'status', value: 'New'}));
    document.getElementById('cardContacted')?.addEventListener('click', () => showFilteredLeads({type: 'status', value: 'Contacted'}));
    document.getElementById('cardArchived')?.addEventListener('click', () => showFilteredLeads({type: 'status', value: 'Archived'}));

  } catch (error) {
    console.error('[Dashboard] Error:', error);
    alert('Failed to load dashboard: ' + error.message);
  }
}

// === Show Filtered Leads ===
async function showFilteredLeads(filter) {
  console.log('[Filter] Showing filtered leads:', filter);
  currentFilter = filter;

  // Update breadcrumb
  const breadcrumb = document.getElementById('breadcrumb');
  switch (filter.type) {
    case 'all':
      breadcrumb.textContent = 'All Leads';
      break;
    case 'status':
      breadcrumb.textContent = `Status: ${filter.value}`;
      break;
    case 'zip':
      breadcrumb.textContent = `ZIP: ${filter.value}`;
      break;
    case 'category':
      breadcrumb.textContent = `Category: ${filter.value}`;
      break;
  }

  showScreen('leads-list');

  // Load leads with loading indicator
  const tbody = document.getElementById('leadsTableBody');
  tbody.innerHTML = '<tr><td colspan="7" class="loading">Loading leads...</td></tr>';

  try {
    // ALWAYS fetch FRESH data from server
    const data = await apiCall(`/api/leads/${currentProfileId}`);
    console.log('[Filter] Fresh leads data:', data);

    if (!data.success || !data.leads || data.leads.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" class="empty">No leads found</td></tr>';
      document.getElementById('leadsCount').textContent = '0';
      return;
    }

    // Apply filter to FRESH data
    let filteredLeads = data.leads;
    if (filter.type === 'status') {
      filteredLeads = data.leads.filter(lead => lead.status === filter.value);
    } else if (filter.type === 'zip') {
      filteredLeads = data.leads.filter(lead => lead.zipCode === filter.value);
    } else if (filter.type === 'category') {
      filteredLeads = data.leads.filter(lead => lead.category === filter.value);
    }

    renderLeadsTable(filteredLeads, data.leads);

  } catch (error) {
    console.error('[Filter] Error:', error);
    tbody.innerHTML = '<tr><td colspan="7" class="error">Failed to load leads</td></tr>';
  }
}

// === Render Leads Table ===
function renderLeadsTable(leads, allLeads) {
  const tbody = document.getElementById('leadsTableBody');

  if (leads.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" class="empty">No leads match this filter</td></tr>';
    document.getElementById('leadsCount').textContent = '0';
    return;
  }

  tbody.innerHTML = leads.map(lead => `
    <tr>
      <td><input type="checkbox" data-id="${lead.id}"></td>
      <td>${lead.name}</td>
      <td>${lead.phone}</td>
      <td>${lead.category || 'N/A'}</td>
      <td>${lead.zipCode || 'N/A'}</td>
      <td><span class="status-badge status-${(lead.status || 'New').toLowerCase()}">${lead.status || 'New'}</span></td>
      <td>
        <button class="btn-action btn-contact" onclick="updateLeadStatus(${lead.id}, 'Contacted')" ${lead.status === 'Contacted' ? 'disabled' : ''}>Contact</button>
        <button class="btn-action btn-archive" onclick="updateLeadStatus(${lead.id}, 'Archived')" ${lead.status === 'Archived' ? 'disabled' : ''}>Archive</button>
      </td>
    </tr>
  `).join('');

  document.getElementById('leadsCount').textContent = leads.length;

  // Store all leads for search functionality
  window.currentAllLeads = allLeads;
  window.currentFilteredLeads = leads;
}

// === Filter Leads Table (Search) ===
function filterLeadsTable(searchQuery) {
  if (!window.currentAllLeads) return;

  if (!searchQuery || searchQuery.trim() === '') {
    // Show all filtered leads (based on current filter)
    if (currentFilter.type === 'all') {
      renderLeadsTable(window.currentAllLeads, window.currentAllLeads);
    } else if (currentFilter.type === 'status') {
      const filtered = window.currentAllLeads.filter(lead => lead.status === currentFilter.value);
      renderLeadsTable(filtered, window.currentAllLeads);
    } else if (currentFilter.type === 'zip') {
      const filtered = window.currentAllLeads.filter(lead => lead.zipCode === currentFilter.value);
      renderLeadsTable(filtered, window.currentAllLeads);
    } else if (currentFilter.type === 'category') {
      const filtered = window.currentAllLeads.filter(lead => lead.category === currentFilter.value);
      renderLeadsTable(filtered, window.currentAllLeads);
    }
    return;
  }

  const query = searchQuery.toLowerCase();
  let filtered = window.currentAllLeads;

  // Apply current filter first
  if (currentFilter.type === 'status') {
    filtered = filtered.filter(lead => lead.status === currentFilter.value);
  } else if (currentFilter.type === 'zip') {
    filtered = filtered.filter(lead => lead.zipCode === currentFilter.value);
  } else if (currentFilter.type === 'category') {
    filtered = filtered.filter(lead => lead.category === currentFilter.value);
  }

  // Apply search query
  filtered = filtered.filter(lead =>
    lead.name.toLowerCase().includes(query) ||
    lead.phone.toLowerCase().includes(query) ||
    (lead.address && lead.address.toLowerCase().includes(query)) ||
    (lead.category && lead.category.toLowerCase().includes(query)) ||
    (lead.zipCode && lead.zipCode.toLowerCase().includes(query))
  );

  renderLeadsTable(filtered, window.currentAllLeads);
}

// === Update Lead Status ===
async function updateLeadStatus(leadId, newStatus) {
  console.log('[Status] Updating lead', leadId, 'to', newStatus);

  try {
    const result = await apiCall(`/api/leads/${currentProfileId}/${leadId}/status`, 'PUT', { status: newStatus });

    if (result.success) {
      console.log('[Status] Update successful, reloading view with fresh data...');
      // Reload the entire filtered view with FRESH data from server
      await showFilteredLeads(currentFilter);
    } else {
      alert('Failed to update status: ' + result.error);
    }
  } catch (error) {
    console.error('[Status] Error:', error);
    alert('Failed to update status: ' + error.message);
  }
}

// === Export Filtered Leads ===
async function exportFilteredLeads() {
  console.log('[Export] Exporting filtered leads...');

  try {
    // Get currently displayed leads from table
    const leadsToExport = window.currentFilteredLeads || [];

    if (leadsToExport.length === 0) {
      alert('No leads to export');
      return;
    }

    const headers = ['Name', 'Phone', 'Address', 'Website', 'Email', 'Category', 'ZIP Code', 'Status'];
    const csv = [
      headers.join(','),
      ...leadsToExport.map(lead => [
        lead.name,
        lead.phone,
        lead.address || 'N/A',
        lead.website || 'N/A',
        lead.email || 'N/A',
        lead.category || 'N/A',
        lead.zipCode || 'N/A',
        lead.status || 'New'
      ].map(field => `"${field}"`).join(','))
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;

    // Generate filename based on filter
    let filterName = 'all_leads';
    if (currentFilter.type === 'status') filterName = `status_${currentFilter.value}`;
    else if (currentFilter.type === 'zip') filterName = `zip_${currentFilter.value}`;
    else if (currentFilter.type === 'category') filterName = currentFilter.value.replace(/\s+/g, '_').toLowerCase();

    a.download = `${currentProfileData.name}_${filterName}_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);

    console.log('[Export] Downloaded', leadsToExport.length, 'leads');
  } catch (error) {
    console.error('[Export] Error:', error);
    alert('Failed to export: ' + error.message);
  }
}

// === Manual Scrape ===
async function startManualScrape() {
  const city = document.getElementById('inputCity').value;
  const state = document.getElementById('inputState').value;
  const category = document.getElementById('selectCategory').value;

  if (!city || !state || !category) {
    alert('Please fill in all fields');
    return;
  }

  console.log('[Scrape] Starting:', { city, state, category });
  showScreen('scraping-progress');
  document.getElementById('scrapeStatus').textContent = `${city}, ${state} · ${category}`;

  try {
    const result = await apiCall('/api/scrape/start', 'POST', {
      profileId: currentProfileId,
      zipCode: '33527',
      category: category,
      maxPages: 2
    });

    if (result.success) pollScrapeStatus();
    else {
      alert('Failed to start: ' + result.error);
      showScreen('manual-scrape');
    }
  } catch (error) {
    console.error('[Scrape] Error:', error);
    alert('Error: ' + error.message);
    showScreen('manual-scrape');
  }
}

// === Poll Scrape Status ===
async function pollScrapeStatus() {
  const interval = setInterval(async () => {
    try {
      const result = await apiCall('/api/scrape/status');
      if (result.success && result.status) {
        const status = result.status;
        document.getElementById('progressBar').style.width = status.progress + '%';
        document.getElementById('progressText').textContent = `${status.total_leads || 0} leads found`;

        if (!status.active) {
          clearInterval(interval);
          setTimeout(() => {
            showScreen('dashboard');
            alert(`Complete! Found ${status.total_leads || 0} leads`);
            location.reload();
          }, 1000);
        }
      }
    } catch (error) {
      console.error('[Poll] Error:', error);
      clearInterval(interval);
    }
  }, 1000);
}

// === Create Profile ===
document.getElementById('btnCreateProfile')?.addEventListener('click', () => {
  const name = prompt('Enter profile name:');
  if (name) {
    apiCall('/api/profiles', 'POST', { name })
      .then(() => location.reload())
      .catch(err => alert('Error: ' + err.message));
  }
});

console.log('[App] Ready');
