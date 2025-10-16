/**
 * Scraper G1000 - Frontend (Browser/PyWebView Compatible)
 */

const API_BASE = 'http://localhost:5050';

console.log('[App] Scraper G1000 loaded');

// === API Helper ===
async function apiCall(endpoint, method = 'GET', body = null) {
  const options = { method, headers: { 'Content-Type': 'application/json' } };
  if (body) options.body = JSON.stringify(body);

  const response = await fetch(`${API_BASE}${endpoint}`, options);
  return await response.json();
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

    profileList.innerHTML = data.profiles.map(p => `
      <div class="profile-card" onclick="selectProfile('${p.id}')">
        <div class="profile-icon">${p.icon || '📊'}</div>
        <div class="profile-info">
          <h3>${p.name}</h3>
          <p>${p.businessType || 'General'}</p>
          <span class="profile-stats">
            ${p.totalLeads || 0} Valid Leads
            ${p.flaggedLeads > 0 ? ` • ${p.flaggedLeads} Flagged` : ''}
          </span>
        </div>
      </div>
    `).join('');

    console.log('[App] Loaded', data.profiles.length, 'profiles');

  } catch (error) {
    console.error('[App] Failed to load profiles:', error);
    profileList.innerHTML = '<div class="profile-error">Failed to load profiles: ' + error.message + '</div>';
  }
});

// === Profile Selection ===
function selectProfile(profileId) {
  console.log('[App] Selected profile:', profileId);
  alert('Selected: ' + profileId + '\\n\\nDashboard coming soon!');
}

// === Create Profile ===
const btnCreate = document.getElementById('btnCreateProfile');
if (btnCreate) {
  btnCreate.addEventListener('click', () => {
    const name = prompt('Enter profile name:');
    if (name) {
      apiCall('/api/profiles', 'POST', { name })
        .then(() => location.reload())
        .catch(err => alert('Error: ' + err.message));
    }
  });
}

console.log('[App] Ready');
