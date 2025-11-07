# 🚀 How to Build Desktop App

## Super Simple - Just 2 Steps!

### Step 1: Run the Build Script
Double-click: **`BUILD-DESKTOP-APP.bat`**

That's it! The script will:
1. Install PyInstaller
2. Build ScraperG1000.exe
3. Put it in the `dist/` folder

### Step 2: Use Your App
Go to `dist/` folder and you'll see: **`ScraperG1000.exe`**

Right-click it and:
- **"Send to > Desktop (create shortcut)"** - Put icon on desktop
- **"Pin to taskbar"** - Keep it in your taskbar

---

## That's All!

Now you have a **REAL desktop app** you just double-click!

No more:
- ❌ Hunting for BAT files
- ❌ Opening command prompts
- ❌ Navigating through folders
- ❌ Dealing with Python scripts

Just:
- ✅ Double-click the icon
- ✅ App opens
- ✅ Done!

---

## What If I Get Errors?

If the build fails, you might need to install dependencies first:
```
pip install -r requirements.txt
```

Then run `BUILD-DESKTOP-APP.bat` again.

---

## Build Takes Too Long?

The first build takes 2-5 minutes. It's creating a standalone executable with everything bundled inside.

Subsequent builds are faster (30 seconds).

---

## Want a Custom Icon?

1. Get a `.ico` file (Windows icon format)
2. Rename it to `app_icon.ico`
3. Put it in the same folder as `build_exe.py`
4. Run the build again

The executable will have your custom icon!

---

**Questions?** Just run the app and start scraping leads! 🎯
