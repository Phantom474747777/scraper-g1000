/**
 * Automation Mode Logic
 */

let automationQueue = [];
let selectedZipsForAuto = [];

// Navigation
const btnBackFromAuto = document.getElementById('btnBackFromAuto');
if (btnBackFromAuto) {
  btnBackFromAuto.addEventListener('click', () => {
    navigateTo('dashboard');
  });
}

// Radius slider for automation
const autoInputRadius = document.getElementById('autoInputRadius');
const autoRadiusValue = document.getElementById('autoRadiusValue');
if (autoInputRadius && autoRadiusValue) {
  autoInputRadius.addEventListener('input', (e) => {
    autoRadiusValue.textContent = e.target.value;
  });
}

// Find ZIPs for automation
const btnAutoFindZips = document.getElementById('btnAutoFindZips');
if (btnAutoFindZips) {
  btnAutoFindZips.addEventListener('click', findZipsForAutomation);
}

async function findZipsForAutomation() {
  const city = document.getElementById('autoInputCity').value;
  const state = document.getElementById('autoInputState').value;

  if (!city || !state) {
    alert('Please enter city and state');
    return;
  }

  // TODO: Call backend to get ZIPs
  selectedZipsForAuto = ['33527', '33510', '33534'];
  alert(`Found ${selectedZipsForAuto.length} ZIP codes within radius`);
  validateAutomationForm();
}

// Category checkboxes
const categoryCheckboxes = document.querySelectorAll('.category-checkbox');
if (categoryCheckboxes.length > 0) {
  categoryCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', validateAutomationForm);
  });
}

// Select/Deselect all categories
const btnSelectAllCategories = document.getElementById('btnSelectAllCategories');
const btnDeselectAllCategories = document.getElementById('btnDeselectAllCategories');

if (btnSelectAllCategories) {
  btnSelectAllCategories.addEventListener('click', () => {
    categoryCheckboxes.forEach(cb => cb.checked = true);
    validateAutomationForm();
  });
}

if (btnDeselectAllCategories) {
  btnDeselectAllCategories.addEventListener('click', () => {
    categoryCheckboxes.forEach(cb => cb.checked = false);
    validateAutomationForm();
  });
}

// Build Queue button
const btnBuildQueue = document.getElementById('btnBuildQueue');
if (btnBuildQueue) {
  btnBuildQueue.addEventListener('click', buildAutomationQueue);
}

function validateAutomationForm() {
  const city = document.getElementById('autoInputCity').value.trim();
  const state = document.getElementById('autoInputState').value.trim();
  const hasZips = selectedZipsForAuto.length > 0;
  const selectedCategories = Array.from(categoryCheckboxes).filter(cb => cb.checked);

  const isValid = city && state && hasZips && selectedCategories.length > 0;

  if (btnBuildQueue) {
    btnBuildQueue.disabled = !isValid;
  }
}

function buildAutomationQueue() {
  const selectedCategories = Array.from(categoryCheckboxes)
    .filter(cb => cb.checked)
    .map(cb => cb.value);

  const maxLeads = parseInt(document.getElementById('autoMaxLeads').value) || 50;
  const delay = parseInt(document.getElementById('autoDelay').value) || 5;

  // Build queue: each ZIP × each category
  automationQueue = [];
  selectedZipsForAuto.forEach(zip => {
    selectedCategories.forEach(category => {
      automationQueue.push({
        zip,
        category,
        maxLeads,
        status: 'pending'
      });
    });
  });

  displayQueue();
  updateQueueStats();

  // Enable start button
  const btnStartAutomation = document.getElementById('btnStartAutomation');
  const btnClearQueue = document.getElementById('btnClearQueue');
  if (btnStartAutomation) btnStartAutomation.disabled = false;
  if (btnClearQueue) btnClearQueue.disabled = false;
}

function displayQueue() {
  const queueList = document.getElementById('queueList');
  const queueCount = document.getElementById('queueCount');

  if (automationQueue.length === 0) {
    queueList.innerHTML = `
      <div class="queue-empty">
        <div class="empty-icon">📭</div>
        <p>No jobs in queue</p>
        <p class="empty-hint">Configure settings and click "Build Queue" to start</p>
      </div>
    `;
    queueCount.textContent = '0 jobs';
    return;
  }

  queueList.innerHTML = automationQueue.map((job, index) => `
    <div class="queue-item">
      <div class="queue-item-info">
        <div class="queue-item-title">${job.zip} · ${job.category}</div>
        <div class="queue-item-subtitle">Max ${job.maxLeads} leads</div>
      </div>
      <button class="queue-item-remove" onclick="removeFromQueue(${index})">×</button>
    </div>
  `).join('');

  queueCount.textContent = `${automationQueue.length} jobs`;
}

function removeFromQueue(index) {
  automationQueue.splice(index, 1);
  displayQueue();
  updateQueueStats();

  if (automationQueue.length === 0) {
    const btnStartAutomation = document.getElementById('btnStartAutomation');
    const btnClearQueue = document.getElementById('btnClearQueue');
    if (btnStartAutomation) btnStartAutomation.disabled = true;
    if (btnClearQueue) btnClearQueue.disabled = true;
  }
}

function updateQueueStats() {
  const queueStats = document.getElementById('queueStats');

  if (automationQueue.length === 0) {
    queueStats.style.display = 'none';
    return;
  }

  queueStats.style.display = 'block';

  const uniqueZips = new Set(automationQueue.map(j => j.zip));
  const uniqueCategories = new Set(automationQueue.map(j => j.category));
  const totalJobs = automationQueue.length;
  const estimatedTime = Math.ceil(totalJobs * 0.5); // 30 seconds per job

  document.getElementById('statTotalZips').textContent = uniqueZips.size;
  document.getElementById('statTotalCategories').textContent = uniqueCategories.size;
  document.getElementById('statTotalJobs').textContent = totalJobs;
  document.getElementById('statEstimatedTime').textContent = `~${estimatedTime} min`;
}

// Clear Queue
const btnClearQueue = document.getElementById('btnClearQueue');
if (btnClearQueue) {
  btnClearQueue.addEventListener('click', () => {
    if (confirm('Clear all jobs from queue?')) {
      automationQueue = [];
      displayQueue();
      updateQueueStats();
      btnClearQueue.disabled = true;
      document.getElementById('btnStartAutomation').disabled = true;
    }
  });
}

// Start Automation
const btnStartAutomation = document.getElementById('btnStartAutomation');
if (btnStartAutomation) {
  btnStartAutomation.addEventListener('click', startAutomation);
}

async function startAutomation() {
  if (automationQueue.length === 0) {
    alert('Queue is empty');
    return;
  }

  navigateTo('auto-progress');

  // Initialize progress UI
  document.getElementById('autoJobsComplete').textContent = '0';
  document.getElementById('autoJobsRemaining').textContent = automationQueue.length;
  document.getElementById('autoTotalLeads').textContent = '0';

  let jobsComplete = 0;
  let totalLeads = 0;

  // Process queue
  for (const job of automationQueue) {
    document.getElementById('autoCurrentJob').textContent = `${job.zip} · ${job.category}`;
    document.getElementById('autoCurrentStats').textContent = 'Starting scrape...';

    // Show upcoming jobs
    const remainingJobs = automationQueue.slice(jobsComplete + 1, jobsComplete + 6);
    const upcomingList = document.getElementById('upcomingJobsList');
    upcomingList.innerHTML = remainingJobs.map(j => `
      <div class="upcoming-job-item">${j.zip} · ${j.category}</div>
    `).join('');

    try {
      // Start scraping
      const config = {
        profileId: currentProfile,
        zipCode: job.zip,
        category: job.category,
        maxPages: Math.ceil(job.maxLeads / 25)
      };

      await window.api.startScraping(config);

      // Wait for completion (simplified - should listen to events)
      await new Promise(resolve => setTimeout(resolve, 30000)); // 30 sec per job

      jobsComplete++;
      totalLeads += 20; // Placeholder

      document.getElementById('autoJobsComplete').textContent = jobsComplete;
      document.getElementById('autoJobsRemaining').textContent = automationQueue.length - jobsComplete;
      document.getElementById('autoTotalLeads').textContent = totalLeads;

      // Delay between jobs
      const delay = parseInt(document.getElementById('autoDelay').value) || 5;
      if (delay > 0 && jobsComplete < automationQueue.length) {
        document.getElementById('autoCurrentStats').textContent = `Waiting ${delay} seconds...`;
        await new Promise(resolve => setTimeout(resolve, delay * 1000));
      }

    } catch (error) {
      console.error('[Automation] Job failed:', error);
      alert(`Failed to scrape ${job.zip} · ${job.category}`);
    }
  }

  // Automation complete
  alert(`Automation complete! Found ${totalLeads} leads across ${jobsComplete} jobs`);
  navigateTo('dashboard');
  loadDashboardData();
}

// Pause/Cancel automation
const btnPauseAutomation = document.getElementById('btnPauseAutomation');
const btnCancelAutomation = document.getElementById('btnCancelAutomation');

if (btnPauseAutomation) {
  btnPauseAutomation.addEventListener('click', () => {
    alert('Pause functionality coming soon!');
  });
}

if (btnCancelAutomation) {
  btnCancelAutomation.addEventListener('click', () => {
    if (confirm('Stop automation and return to dashboard?')) {
      navigateTo('dashboard');
    }
  });
}

console.log('[Automation] Module loaded');
