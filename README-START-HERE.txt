========================================
  SCRAPER G1000 - START HERE
========================================

Your app keeps crashing instantly. Let's fix this step by step.

========================================
STEP 1: TEST IF BATCH FILES WORK
========================================

Double-click: TEST-IF-YOU-CAN-SEE-THIS.bat

Can you see a window that says "THIS IS A TEST"?

  YES → Batch files work! Go to STEP 2
  NO  → Windows is blocking batch files. Right-click → "Run as Administrator"


========================================
STEP 2: RUN SIMPLE DIAGNOSTIC
========================================

Double-click: SIMPLE-TEST.bat

This will:
- Check if Python is installed
- Test if Python works
- Run the app and save output to ERROR-LOG.txt
- Open the error log automatically

Follow the on-screen prompts.

If ERROR-LOG.txt shows "ModuleNotFoundError" or "No module named":
→ Go to STEP 3


========================================
STEP 3: INSTALL DEPENDENCIES
========================================

Double-click: INSTALL-DEPENDENCIES.bat

This installs Flask, pywebview, and all required packages.

After it finishes, go back to STEP 2.


========================================
STILL NOT WORKING?
========================================

Try these alternatives in order:

1. RUN-POWERSHELL.bat
   (Uses PowerShell instead of CMD)

2. LAUNCH-WITH-VBS.vbs
   (Uses VBScript)

3. Send me the ERROR-LOG.txt file
   (Created by SIMPLE-TEST.bat)


========================================
WHAT EACH FILE DOES
========================================

TEST-IF-YOU-CAN-SEE-THIS.bat
  → Tests if batch files work at all

SIMPLE-TEST.bat
  → Step-by-step diagnostic that creates ERROR-LOG.txt

INSTALL-DEPENDENCIES.bat
  → Installs all required Python packages

RUN-POWERSHELL.bat
  → Launches app using PowerShell

ERROR-LOG.txt
  → Created by SIMPLE-TEST.bat, contains error details

START-GUI.bat
  → Normal launcher (use this once everything works)


========================================
COMMON ERRORS & FIXES
========================================

Error: "Python was not found"
Fix: Install Python 3.11 from https://www.python.org/downloads/

Error: "No module named 'flask'"
Fix: Run INSTALL-DEPENDENCIES.bat

Error: "No module named 'webview'"
Fix: Run INSTALL-DEPENDENCIES.bat

Error: "Port 5050 is already in use"
Fix: Close any other instances of the app

Error: "Permission denied"
Fix: Right-click → Run as Administrator


========================================
QUICKSTART (If you know what you're doing)
========================================

1. Run: INSTALL-DEPENDENCIES.bat
2. Run: START-GUI.bat
3. Done!

