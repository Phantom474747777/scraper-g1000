# Scraper G1000 - Business Lead Generation Tool

A powerful desktop application for scraping business leads from YellowPages with profile management, smart tracking, and a beautiful dark-mode interface.

## 🚀 Features

- **Multi-Profile System** - Manage unlimited business profiles (CritterCaptures, etc.)
- **Smart Scraping** - Automatically scrapes YellowPages with Cloudflare bypass
- **ZIP Radius Search** - Find all ZIPs within 50 miles of any US city
- **Progress Tracking** - Real-time scraping progress with pause/resume/stop
- **Keyboard Hotkeys** - P (Pause), R (Resume), Q (Quit) during scraping
- **Lead Management** - SQLite database with deduplication
- **Dark Mode UI** - Apple/Tesla-inspired interface
- **Cross-Platform** - Built with Tauri (Rust + WebView)

## 📦 Tech Stack

### Frontend
- **HTML/CSS/JS** - Vanilla JavaScript (no frameworks)
- **Tauri 2.0** - Desktop framework (Rust + WebView)

### Backend
- **Python 3.11** - Flask REST API
- **Crawl4AI** - Web scraping with AI
- **SQLite** - Lead storage
- **undetected-chromedriver** - Cloudflare bypass

## 🛠️ Development Setup

### Prerequisites
- **Python 3.11** - Installed at `C:\Users\47\AppData\Local\Programs\Python\Python311\`
- **Rust 1.90+** - Installed via rustup
- **Node.js** - For npm (Tauri CLI)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/scraper-g1000.git
   cd scraper-g1000-tauri
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node dependencies**
   ```bash
   npm install
   ```

### Running in Development

**Option 1: Use the batch file (Recommended)**
```bash
START-DEV.bat
```

**Option 2: Manual start**
```bash
# Terminal 1: Start Python backend
python backend/api_server.py 5050

# Terminal 2: Start dev server
python serve.py

# Terminal 3: Start Tauri
npm run dev
```

## 📦 Building for Production

### Build Windows .exe

```bash
npm run build
```

The installer will be created at:
```
src-tauri/target/release/bundle/nsis/Scraper G1000_1.0.0_x64-setup.exe
```

### What Gets Bundled

- Tauri app (Rust binary + WebView)
- Frontend assets (HTML/CSS/JS)
- Python backend (api_server.py)
- Python scraper modules (src/)
- App icons

**Note:** Python runtime is NOT bundled. Users must have Python 3.11 installed.

## 🎮 Usage

### First Launch

1. Double-click `Scraper G1000.exe`
2. Python backend starts automatically on port 5050
3. App window opens to profile selector

### Creating a Profile

1. Click "Create New Profile"
2. Enter profile name (e.g., "Real Estate Leads")
3. Select categories to scrape
4. Set default city/state

### Scraping Leads

1. Select a profile from the home screen
2. Click "Manual Scrape" or "Automation Mode"
3. Enter city/state (e.g., "Dover, FL")
4. Select ZIP codes (color-coded availability)
5. Select categories (Real Estate, Property Managers, etc.)
6. Click "Start Scraping"

### Keyboard Shortcuts

During scraping:
- **P** - Pause scraping
- **R** - Resume scraping
- **Q** - Quit/Stop scraping
- **ESC** - Go back to previous screen

### Viewing Leads

1. From dashboard, click "View Leads"
2. Browse all scraped leads in table
3. Export to CSV (TODO)
4. Filter by category, ZIP, date

## 📂 Project Structure

```
scraper-g1000-tauri/
├── src/                      # Frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── js/app.js
│   └── styles/main.css
│
├── src-tauri/                # Tauri (Rust)
│   ├── src/
│   │   ├── main.rs
│   │   └── lib.rs           # Spawns Python backend
│   ├── icons/               # App icons
│   ├── Cargo.toml
│   └── tauri.conf.json
│
├── backend/                  # Python REST API
│   └── api_server.py        # Flask server (port 5050)
│
├── python-src/               # Python scraper modules
│   ├── scraper_free_bypass.py
│   ├── database.py
│   ├── profile_manager.py
│   ├── tracking.py
│   └── zip_lookup.py
│
├── models/                   # Pydantic models
│   └── business.py
│
├── data/                     # Generated data
│   ├── leads_tracker.db     # SQLite database
│   ├── used_zips.json       # Tracking
│   └── *.csv                # Exported leads
│
├── profiles/                 # Profile-specific data
│   └── {profile_id}/
│       ├── leads_tracker.db
│       └── settings.json
│
├── serve.py                  # Dev server (port 8080)
├── START-DEV.bat            # Dev launcher
├── package.json
└── README.md
```

## 🔧 Configuration

### Change Backend Port

Edit `src/js/app.js`:
```javascript
const API_BASE = 'http://localhost:5050';  // Change port here
```

And update `src-tauri/src/lib.rs`:
```rust
.arg("5050")  // Change port here
```

### Change Python Path

Edit `src-tauri/src/lib.rs`:
```rust
let python_path = "C:\\Users\\47\\AppData\\Local\\Programs\\Python\\Python311\\python.exe";
```

### Add Custom Categories

Edit `python-src/profile_manager.py`:
```python
'categories': [
    'Real Estate Agents',
    'Property Managers',
    'Home Inspectors',
    # Add more here
]
```

## 🐛 Troubleshooting

### "Python backend failed to start"

**Solution:** Ensure Python 3.11 is installed and path in `lib.rs` is correct.

### "Failed to connect to backend"

**Solution:** Check if port 5050 is available. Change port if needed.

### "No leads found"

**Solution:** Check internet connection. YellowPages may have changed structure.

### Tauri build fails

**Solution:**
```bash
cargo clean
npm run build
```

## 🎨 Customization

### Change App Icon

Replace files in `src-tauri/icons/`:
- `icon.ico` - Windows icon
- `icon.png` - Source image (1024x1024 recommended)

### Modify UI Theme

Edit `src/styles/main.css` CSS variables:
```css
:root {
  --color-bg: #0D0D0D;
  --color-accent: #0A84FF;
  /* ... */
}
```

## 📝 API Endpoints

The Python backend exposes these endpoints:

- `GET /health` - Health check
- `GET /api/profiles` - List all profiles
- `POST /api/profiles` - Create new profile
- `POST /api/scrape/start` - Start scraping
- `POST /api/scrape/pause` - Pause scraping
- `POST /api/scrape/resume` - Resume scraping
- `POST /api/scrape/stop` - Stop scraping
- `GET /api/scrape/status` - Get scraping status
- `GET /api/leads/:profileId` - Get leads for profile

## 🤝 Contributing

This is a personal project, but feedback and suggestions are welcome!

## 📄 License

MIT License - Free to use and modify

## 🔗 Related Projects

- [Tauri](https://tauri.app/) - Desktop framework
- [Crawl4AI](https://github.com/unclecode/crawl4ai) - Web scraping
- [Flask](https://flask.palletsprojects.com/) - Python web framework

---

**Made with ⚡ by Scraper G1000**
