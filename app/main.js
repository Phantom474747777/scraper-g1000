/**
 * Scraper G1000 - Main Electron Process
 */

// Access Electron APIs using module.require to bypass npm package resolution
const { app, BrowserWindow, ipcMain } = process.type === 'browser'
  ? (global.require || require)('electron')
  : require('electron');

const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

let mainWindow;
let pythonProcess;
let backendPort = 5050;

// Create main application window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    backgroundColor: '#0D0D0D',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  mainWindow.loadFile('index.html');

  // Open DevTools in development
  if (process.env.NODE_ENV === 'development' || process.argv.includes('--dev')) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Start Python backend server
function startPythonBackend() {
  return new Promise((resolve, reject) => {
    const pythonPath = process.env.PYTHON_PATH || 'python';
    const scriptPath = path.join(__dirname, '..', 'backend', 'api_server.py');

    console.log('[Backend] Starting Python API server...');
    console.log('[Backend] Python:', pythonPath);
    console.log('[Backend] Script:', scriptPath);

    pythonProcess = spawn(pythonPath, [scriptPath, backendPort.toString()]);

    pythonProcess.stdout.on('data', (data) => {
      const message = data.toString().trim();
      console.log(`[Backend] ${message}`);

      if (message.includes('Running on')) {
        resolve(backendPort);
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`[Backend Error] ${data}`);
    });

    pythonProcess.on('close', (code) => {
      console.log(`[Backend] Process exited with code ${code}`);
    });

    pythonProcess.on('error', (err) => {
      console.error(`[Backend] Failed to start: ${err}`);
      reject(err);
    });

    // Timeout fallback
    setTimeout(() => resolve(backendPort), 3000);
  });
}

// Check if backend is ready
async function waitForBackend(port, maxRetries = 10) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await new Promise((resolve, reject) => {
        const req = http.get(`http://localhost:${port}/health`, (res) => {
          if (res.statusCode === 200) resolve();
          else reject();
        });
        req.on('error', reject);
        req.setTimeout(1000, () => req.destroy());
      });
      console.log('[Backend] Health check passed');
      return true;
    } catch (err) {
      console.log(`[Backend] Waiting... (attempt ${i + 1}/${maxRetries})`);
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  return false;
}

// App lifecycle
app.whenReady().then(async () => {
  console.log('[App] Scraper G1000 starting...');

  createWindow();

  try {
    await startPythonBackend();
    const ready = await waitForBackend(backendPort);

    if (ready) {
      console.log('[App] Backend ready on port', backendPort);
      mainWindow.webContents.send('backend-ready', { port: backendPort });
    } else {
      console.warn('[App] Backend not responding, continuing anyway');
    }
  } catch (err) {
    console.error('[App] Failed to start backend:', err);
  }

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('quit', () => {
  if (pythonProcess) {
    console.log('[App] Terminating Python backend...');
    pythonProcess.kill();
  }
});

// IPC Handlers - Forward requests to Python backend
ipcMain.handle('api-request', async (event, endpoint, method = 'GET', body = null) => {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: backendPort,
      path: endpoint,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (err) {
          resolve({ error: 'Invalid JSON response' });
        }
      });
    });

    req.on('error', (err) => {
      reject(err);
    });

    if (body && method !== 'GET') {
      req.write(JSON.stringify(body));
    }

    req.end();
  });
});

console.log('[Main] Module loaded successfully');
