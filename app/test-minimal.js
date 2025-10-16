/**
 * Minimal Electron test
 */

console.log('[Test] Loading Electron...');

try {
  const electron = require('electron');
  console.log('[Test] Electron type:', typeof electron);
  console.log('[Test] Electron keys:', Object.keys(electron).slice(0, 10));

  const { app, BrowserWindow } = electron;
  console.log('[Test] app type:', typeof app);
  console.log('[Test] BrowserWindow type:', typeof BrowserWindow);

  if (app && app.whenReady) {
    console.log('[Test] SUCCESS - app.whenReady exists!');

    app.whenReady().then(() => {
      console.log('[Test] App is ready!');
      app.quit();
    });
  } else {
    console.error('[Test] FAIL - app or app.whenReady is undefined');
    console.error('[Test] app:', app);
  }
} catch (error) {
  console.error('[Test] Error:', error.message);
  console.error('[Test] Stack:', error.stack);
}
