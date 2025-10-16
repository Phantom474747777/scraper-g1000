console.log('[Debug] Module cache keys:');
console.log(Object.keys(require.cache).filter(k => k.includes('electron')).slice(0, 10));

console.log('\n[Debug] Trying different require approaches...');

// Try 1: Direct require
try {
  const e1 = require('electron');
  console.log('[Try 1] Direct require - type:', typeof e1);
} catch (err) {
  console.log('[Try 1] Error:', err.message);
}

// Try 2: Module.require
try {
  const Module = require('module');
  const e2 = Module._load('electron', module, false);
  console.log('[Try 2] Module._load - type:', typeof e2);
  if (typeof e2 === 'object') {
    console.log('[Try 2] Keys:', Object.keys(e2).slice(0, 10));
  }
} catch (err) {
  console.log('[Try 2] Error:', err.message);
}

// Try 3: Check if 'electron' is in built-in modules
try {
  const Module = require('module');
  console.log('[Try 3] Built-in modules:', Module.builtinModules.filter(m => m.includes('electron')));
} catch (err) {
  console.log('[Try 3] Error:', err.message);
}

// Try 4: Check process.mainModule
try {
  console.log('[Try 4] process.mainModule:', process.mainModule);
} catch (err) {
  console.log('[Try 4] Error:', err.message);
}

// Exit after debug
process.exit(0);
