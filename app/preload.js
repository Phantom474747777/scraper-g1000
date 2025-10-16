/**
 * Preload script - Secure API bridge
 * Updated for REST API backend
 */

const { contextBridge, ipcRenderer } = require('electron');

// Helper to make API requests
async function apiRequest(endpoint, method = 'GET', body = null) {
  return await ipcRenderer.invoke('api-request', endpoint, method, body);
}

// Expose protected methods
contextBridge.exposeInMainWorld('api', {
  // Profile management
  getProfiles: async () => {
    return await apiRequest('/api/profiles', 'GET');
  },

  createProfile: async (profileData) => {
    return await apiRequest('/api/profiles', 'POST', profileData);
  },

  deleteProfile: async (profileId) => {
    return await apiRequest(`/api/profiles/${profileId}`, 'DELETE');
  },

  // Scraping operations
  startScraping: async (config) => {
    return await apiRequest('/api/scrape/start', 'POST', config);
  },

  stopScraping: async () => {
    return await apiRequest('/api/scrape/stop', 'POST');
  },

  pauseScraping: async () => {
    return await apiRequest('/api/scrape/pause', 'POST');
  },

  resumeScraping: async () => {
    return await apiRequest('/api/scrape/resume', 'POST');
  },

  getScrapeStatus: async () => {
    return await apiRequest('/api/scrape/status', 'GET');
  },

  // Lead management
  getLeads: async (profileId, filters = {}) => {
    const query = new URLSearchParams(filters).toString();
    return await apiRequest(`/api/leads/${profileId}?${query}`, 'GET');
  },

  exportLeads: async (profileId, format) => {
    return await apiRequest(`/api/leads/${profileId}/export?format=${format}`, 'GET');
  },

  deleteLeads: async (profileId, leadIds) => {
    return await apiRequest(`/api/leads/${profileId}`, 'DELETE', { leadIds });
  },

  // Settings
  getSettings: async () => {
    return await apiRequest('/api/settings', 'GET');
  },

  saveSettings: async (settings) => {
    return await apiRequest('/api/settings', 'POST', settings);
  },

  // Event listeners for backend events
  onBackendReady: (callback) => {
    ipcRenderer.on('backend-ready', (event, data) => callback(data));
  },

  onScrapingProgress: (callback) => {
    ipcRenderer.on('scraping-progress', (event, data) => callback(data));
  },

  onScrapingComplete: (callback) => {
    ipcRenderer.on('scraping-complete', (event, data) => callback(data));
  },

  onScrapingError: (callback) => {
    ipcRenderer.on('scraping-error', (event, error) => callback(error));
  }
});

console.log('[Preload] API bridge initialized');
