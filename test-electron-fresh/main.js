const { app, BrowserWindow } = require('electron');

console.log('[Test] Electron app loaded successfully!');
console.log('[Test] app type:', typeof app);

app.whenReady().then(() => {
  console.log('[Test] App is ready!');

  const win = new BrowserWindow({
    width: 800,
    height: 600
  });

  win.loadURL('data:text/html,<h1>Test Electron App Works!</h1>');

  setTimeout(() => {
    console.log('[Test] Quitting...');
    app.quit();
  }, 2000);
});
