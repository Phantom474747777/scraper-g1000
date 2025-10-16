/**
 * Workaround for Electron require() bug
 * Manually access Electron APIs via process._linkedBinding
 */

console.log('[Workaround] Loading Electron APIs manually...');

// Try to get Electron APIs via process bindings
let app, BrowserWindow;

try {
  // Attempt 1: Try normal require (will fail but good to try)
  const electronRequire = require('electron');
  if (typeof electronRequire === 'object' && electronRequire.app) {
    app = electronRequire.app;
    BrowserWindow = electronRequire.BrowserWindow;
    console.log('[Workaround] Success via normal require');
  }
} catch (err) {
  console.log('[Workaround] Normal require failed:', err.message);
}

// Attempt 2: Access via process._linkedBinding or Module._load with different cache
if (!app) {
  try {
    // Delete the cached electron module that returns path string
    const Module = require('module');
    const electronPath = require.resolve('electron');
    delete require.cache[electronPath];

    // Try to load electron's internal module directly
    const internalElectron = Module._load('electron', module.parent || module, true);
    if (typeof internalElectron === 'object' && internalElectron.app) {
      app = internalElectron.app;
      BrowserWindow = internalElectron.BrowserWindow;
      console.log('[Workaround] Success via Module._load with cache clear');
    }
  } catch (err) {
    console.log('[Workaround] Module._load failed:', err.message);
  }
}

// Attempt 3: Use remote module pattern (Electron < 14)
if (!app) {
  try {
    const remote = require('@electron/remote');
    app = remote.app;
    BrowserWindow = remote.BrowserWindow;
    console.log('[Workaround] Success via @electron/remote');
  } catch (err) {
    console.log('[Workaround] Remote failed:', err.message);
  }
}

console.log('[Workaround] Final app type:', typeof app);

if (!app || !app.whenReady) {
  console.error('[FATAL] Could not load Electron APIs!');
  console.error('[FATAL] This Electron installation may be corrupted.');
  console.error('[FATAL] Try: rm -rf node_modules && npm install');
  process.exit(1);
}

// Now use the app
console.log('[Test] Electron app loaded successfully!');

app.whenReady().then(() => {
  console.log('[Test] App is ready!');

  const win = new BrowserWindow({
    width: 800,
    height: 600
  });

  win.loadURL('data:text/html,<h1>Workaround Test - Success!</h1>');

  setTimeout(() => {
    console.log('[Test] Quitting...');
    app.quit();
  }, 2000);
});
