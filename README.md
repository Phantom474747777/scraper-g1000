# Scraper G1000 - Quick Start

## First Time Setup

1. **Install Dependencies**
   - Double-click `INSTALL-DEPENDENCIES.bat`
   - Wait for it to finish (2-3 minutes)

2. **Launch the App**
   - Double-click `START-GUI.bat`
   - The app window will open

## If It Doesn't Work

Check `startup.log` - it will show the exact error.

Common issues:
- **Missing packages**: Run `INSTALL-DEPENDENCIES.bat`
- **Python not found**: Install Python 3.11 from https://www.python.org/downloads/
- **Port 5050 in use**: Close any other instance of the app

## Files

- **START-GUI.bat** - Launch the app
- **INSTALL-DEPENDENCIES.bat** - Install required packages
- **scraper-g1000.py** - Main application
- **startup.log** - Created automatically, shows errors

## What This App Does

Universal business lead scraper with:
- Web scraping from multiple sources
- Lead management dashboard
- Multi-profile support
- Export to CSV/Excel
- Email extraction
- ZIP code radius search
