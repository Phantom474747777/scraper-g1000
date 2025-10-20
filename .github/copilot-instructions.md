## Project snapshot for AI coding agents

This repo is a desktop-focused lead-scraping application (Python + Flask backend + Tauri-like frontend). Key components:
- Backend API: `backend/api_server.py` — Flask app serving a static UI (usually `scraper-g1000-tauri/src`) and REST endpoints for profiles, scraping control, leads, and exports.
- Scraper core: `src/scraper_universal.py` — Selenium/undetected-chromedriver-based universal scraper (Google Maps first) with advanced anti-detection controls.
- Persistence: `src/database.py` (LeadsDatabase) and per-profile DBs under `profiles/<profile_id>/leads_tracker.db`.
- Profile management: `src/profile_manager.py` — holds profile metadata in `profiles/profiles.json` and migrates legacy `data/` files.

High-value files to inspect when changing behavior
- `backend/api_server.py` — how endpoints expect profile IDs, zip/category payloads, and how scraping runs in a background thread (run_scrape_job).
- `src/scraper_universal.py` — how drivers are created (create_advanced_driver), headless mode and user agents, selectors used for extraction.
- `src/database.py` — DB schema, duplicate detection (business_hash), scraped_combos tracking and validation via `src/validators.py`.
- `src/profile_manager.py` — profile directory layout and where to find per-profile databases and tracking files.
- `requirements.txt` — third-party deps (undetected-chromedriver, pgeocode, openpyxl, Flask, pywebview).

Workflows & commands (what humans run)
- GUI: double-click `START-GUI.bat` (Windows) — launches the packaged app.
- Backend dev server: run `python backend/api_server.py` or `python backend/api_server.py 5050` to pick a port. The server serves static files from `scraper-g1000-tauri/src` when present.
- Quick script runs / tests: many modules include `if __name__ == "__main__"` test runners (ProfileManager, scraper). Use those for small local tests.

Project-specific conventions
- Per-profile storage: every profile has its own folder under `profiles/<profile_id>/` containing `leads_tracker.db`, `used_zips.json` and a `data/` subfolder for CSVs. Avoid writing to global `data/` except for migration.
- Duplicate detection: LeadsDatabase._generate_hash(name,phone,address) is authoritative — use it rather than custom dedupe logic.
- Scrape-skipping: `scraped_combos` prevents re-scraping a zip+category combo. When adding or modifying scrape logic, ensure `mark_combo_scraped` / `is_combo_scraped` are updated accordingly.
- Logging: backend captures scraper prints and stores them in `scraping_state['logs']` via a stdout interceptor (LogCapture). Prefer print() messages with recognizable tags like `[PAGE n]`, `[INFO]`, `[ERROR]` to update progress.

Integration notes & gotchas
- UI directory selection: `backend/api_server.py` prefers `scraper-g1000-tauri/src` and falls back to `app/`. When changing static assets or routes, update UI_DIR logic.
- Headless scraping: `scraper_universal` uses undetected-chromedriver with `--headless=new`. CI or dev machines may require installed Chrome that matches undetected-chromedriver expectations.
- Encoding/emoji issues: server code intentionally suppresses emoji prints in ZIP lookup and log capture to avoid Windows console encoding errors.
- SQLite migrations: code will ALTER TABLE to add columns (category, status) at runtime. Be careful when changing schema — prefer migrations in LeadsDatabase._init_database.

Small examples to copy/paste
- Start backend locally (port 5050):
  python backend/api_server.py 5050

- Start a quick scraper test directly:
  python src/scraper_universal.py

- Open default profile DB location from Python:
  from src.profile_manager import ProfileManager
  pm = ProfileManager(); p = pm.get_profile('crittercaptures'); print(p.get_database_path())

Editing style & priorities for AI edits
- Small, focused changes only: avoid touching scraping selectors or anti-detection heuristics without a working local test (use the scraper test runner).
- When modifying persistence or profile layout, update `Profile.get_database_path()` and `ProfileManager._migrate_existing_data` together.
- Keep CLI and GUI behavior stable: many Windows users start the app via `.bat` wrappers — changing entry points requires updating those files under repo root (START-GUI.bat / START.bat / START-GUI-FIXED.bat).

When you need clarification
- If a behavior depends on Chrome/driver versions, ask which environment (local dev vs build machine). Provide a minimal repro: exact command, profile id, zip, category, and full server logs.

If you update this file, preserve the short examples and the references to the 5 files listed above.
