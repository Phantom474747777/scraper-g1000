console.log('[Debug] Trying to require electron/js2c/browser_init...');

try {
  const browserInit = require('electron/js2c/browser_init');
  console.log('[Success] browser_init type:', typeof browserInit);
  console.log('[Success] browser_init keys:', Object.keys(browserInit).slice(0, 20));
} catch (err) {
  console.log('[Error]', err.message);
}

// Also try requiring the electron APIs directly via global
console.log('\n[Debug] Checking global object for electron APIs...');
console.log('[Debug] global.require:', typeof global.require);
console.log('[Debug] global.process:', typeof global.process);
console.log('[Debug] global._linkedBinding:', typeof global._linkedBinding);
console.log('[Debug] global.electronBinding:', typeof global.electronBinding);

if (global.electronBinding) {
  try {
    const app = global.electronBinding('app');
    console.log('[Success] electronBinding(app):', typeof app);
  } catch (err) {
    console.log('[Error] electronBinding(app):', err.message);
  }
}

// Check process.electron
console.log('\n[Debug] process.electron:', typeof process.electron);
console.log('[Debug] process._linkedBinding:', typeof process._linkedBinding);

if (process._linkedBinding) {
  try {
    const electron_common_features = process._linkedBinding('electron_common_features');
    console.log('[Success] _linkedBinding result:', typeof electron_common_features);
  } catch (err) {
    console.log('[Error] _linkedBinding:', err.message);
  }
}

process.exit(0);
