// Simple test to see if Electron works at all
const electron = require('electron');
console.log('Electron loaded:', !!electron);
console.log('Electron.app exists:', !!electron.app);

if (electron.app) {
  electron.app.whenReady().then(() => {
    console.log('Electron is ready!');
    const win = new electron.BrowserWindow({ width: 800, height: 600 });
    win.loadURL('data:text/html,<h1>Test</h1>');
  });
}
