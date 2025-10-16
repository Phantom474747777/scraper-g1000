"""
CritterCaptures Lead Generation - Interactive CLI
Smart color-coded interface for scraping leads with autopilot mode
"""
import asyncio
import csv
import os
import sys
import argparse
import threading
import time
import select
from datetime import datetime
from dotenv import load_dotenv
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

# Try to import keyboard for better hotkey support
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

# Fix for nested event loop issues (works in any environment)
import nest_asyncio
nest_asyncio.apply()

from crawl4ai import AsyncWebCrawler
from src.scraper import get_browser_config, get_llm_strategy, fetch_and_process_page
from src.database import LeadsDatabase
from src.zip_lookup import get_zips_in_radius
from src.tracking import ZipTracker
from models.business import BusinessData

# Load environment variables
load_dotenv(override=True)

# Customer-oriented categories (potential clients who need wildlife removal)
CATEGORIES = [
    "Real Estate Agents",
    "Property Managers",
    "Home Inspectors",
    "Construction Companies",
    "Roofing Contractors",
    "HVAC Services",
    "Plumbing Companies",
    "Landscaping Companies",
    "Cleaning Services"
]

MAX_PAGES_PER_SEARCH = 2

SCRAPER_INSTRUCTIONS = (
    "Extract all business information: 'name', 'address', 'website', 'phone_number', "
    "'email' (if available, otherwise 'N/A') from the following content."
)

# Global autopilot state
AUTOPILOT_STATE = {
    'running': False,
    'paused': False,
    'should_quit': False,
    'current_zip': None,
    'current_category': None,
    'total_leads': 0,
    'zip_index': 0,
    'category_index': 0,
    'total_zips': 0,
    'total_categories': 0
}

# Keyboard input thread
keyboard_thread = None


def print_header():
    """Print colorful ASCII header"""
    print("\n" + "=" * 60)
    print("🦝 CritterCaptures Lead Generation System")
    print("=" * 60)


def keyboard_listener():
    """Listen for keyboard input in automation mode with improved responsiveness"""
    global AUTOPILOT_STATE
    
    if KEYBOARD_AVAILABLE:
        # Use keyboard library for better cross-platform support
        try:
            def on_key_press(key):
                try:
                    key_name = key.name.upper()
                    if key_name == 'P':
                        AUTOPILOT_STATE['paused'] = True
                        print_hotkey_feedback("⏸ PAUSED — Press R to resume", "yellow")
                    elif key_name == 'R':
                        AUTOPILOT_STATE['paused'] = False
                        print_hotkey_feedback("▶️ RESUMING…", "green")
                    elif key_name == 'Q':
                        AUTOPILOT_STATE['should_quit'] = True
                        print_hotkey_feedback("❌ STOPPED by user. Progress saved.", "red")
                except AttributeError:
                    pass  # Handle special keys
            
            keyboard.on_press(on_key_press)
            
            while AUTOPILOT_STATE['running']:
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Keyboard library error: {e}")
            # Fallback to basic method
            basic_keyboard_listener()
    else:
        # Fallback to basic keyboard detection
        basic_keyboard_listener()


def basic_keyboard_listener():
    """Basic keyboard listener fallback"""
    global AUTOPILOT_STATE
    try:
        import msvcrt  # Windows-specific for immediate key detection
        
        while AUTOPILOT_STATE['running']:
            if msvcrt.kbhit():  # Check if key is pressed
                key = msvcrt.getch().decode('utf-8').upper()
                
                if key == 'P':
                    AUTOPILOT_STATE['paused'] = True
                    print_hotkey_feedback("⏸ PAUSED — Press R to resume", "yellow")
                elif key == 'R':
                    AUTOPILOT_STATE['paused'] = False
                    print_hotkey_feedback("▶️ RESUMING…", "green")
                elif key == 'Q':
                    AUTOPILOT_STATE['should_quit'] = True
                    print_hotkey_feedback("❌ STOPPED by user. Progress saved.", "red")
            
            time.sleep(0.05)  # Faster polling for better responsiveness
    except ImportError:
        # Fallback for non-Windows systems
        try:
            while AUTOPILOT_STATE['running']:
                if sys.stdin in select.select([sys.stdin], [], [], 0.05)[0]:
                    key = sys.stdin.read(1).upper()
                    if key == 'P':
                        AUTOPILOT_STATE['paused'] = True
                        print_hotkey_feedback("⏸ PAUSED — Press R to resume", "yellow")
                    elif key == 'R':
                        AUTOPILOT_STATE['paused'] = False
                        print_hotkey_feedback("▶️ RESUMING…", "green")
                    elif key == 'Q':
                        AUTOPILOT_STATE['should_quit'] = True
                        print_hotkey_feedback("❌ STOPPED by user. Progress saved.", "red")
                time.sleep(0.05)
        except:
            pass  # Handle any keyboard input errors gracefully
    except:
        pass  # Handle any keyboard input errors gracefully


def start_keyboard_listener():
    """Start the keyboard listener thread"""
    global keyboard_thread, AUTOPILOT_STATE
    AUTOPILOT_STATE['running'] = True
    keyboard_thread = threading.Thread(target=keyboard_listener, daemon=True)
    keyboard_thread.start()


def stop_keyboard_listener():
    """Stop the keyboard listener thread"""
    global AUTOPILOT_STATE
    AUTOPILOT_STATE['running'] = False


def update_status_display():
    """Update the live status display"""
    if not AUTOPILOT_STATE['running']:
        return
    
    zip_progress = f"ZIP {AUTOPILOT_STATE['current_zip']} ({AUTOPILOT_STATE['zip_index']}/{AUTOPILOT_STATE['total_zips']})"
    cat_progress = f"Category: {AUTOPILOT_STATE['current_category']} ({AUTOPILOT_STATE['category_index']}/{AUTOPILOT_STATE['total_categories']})"
    leads_count = f"Total Leads: {AUTOPILOT_STATE['total_leads']}"
    paused_status = f"Paused: {AUTOPILOT_STATE['paused']}"
    
    status_line = f"Progress: {zip_progress} | {cat_progress} | {leads_count} | {paused_status}"
    print(f"\r{status_line}", end="", flush=True)


def beep():
    """Play a system beep"""
    try:
        import winsound
        winsound.Beep(1000, 200)  # 1000Hz for 200ms
    except:
        print("\a", end="")  # Fallback to ASCII bell


def print_hotkey_bar():
    """Print persistent hotkey bar in top-right corner using ANSI positioning"""
    import shutil

    # Get terminal width
    term_width = shutil.get_terminal_size().columns

    # Hotkey bar content
    bar_text = " 🧠 [P] Pause [R] Resume [Q] Quit "
    bar_width = len(bar_text)

    # Calculate position for top-right
    right_margin = 2
    col_position = term_width - bar_width - right_margin

    # Save cursor position
    print("\033[s", end="")  # Save cursor position

    # Move to top-right (row 1, calculated column)
    print(f"\033[1;{col_position}H", end="")  # Move to row 1, column X

    # Print the hotkey bar with background color
    print(f"\033[44m\033[97m{bar_text}\033[0m", end="")  # Blue background, white text

    # Restore cursor position
    print("\033[u", end="")  # Restore cursor position
    print("", flush=True)


def print_hotkey_feedback(message, color="white"):
    """Print colored feedback message"""
    color_codes = {
        "red": "\033[91m",
        "green": "\033[92m", 
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "white": "\033[97m"
    }
    reset = "\033[0m"
    
    color_code = color_codes.get(color, color_codes["white"])
    print(f"\n{color_code}{message}{reset}")


def print_automation_status():
    """Print clean automation status display"""
    global AUTOPILOT_STATE
    
    # Determine status
    if AUTOPILOT_STATE['should_quit']:
        status = "STOPPED"
        status_icon = "❌"
    elif AUTOPILOT_STATE['paused']:
        status = "PAUSED"
        status_icon = "⏸"
    else:
        status = "RUNNING"
        status_icon = "▶"
    
    print("\n" + "=" * 60)
    print("Mode: AUTOMATION")
    
    if AUTOPILOT_STATE['current_zip'] and AUTOPILOT_STATE['current_category']:
        print(f"ZIP: {AUTOPILOT_STATE['current_zip']} | Category: {AUTOPILOT_STATE['current_category']}")
    
    if AUTOPILOT_STATE['total_zips'] > 0:
        zip_progress = f"ZIP {AUTOPILOT_STATE['zip_index']}/{AUTOPILOT_STATE['total_zips']}"
        cat_progress = f"Category {AUTOPILOT_STATE['category_index']}/{AUTOPILOT_STATE['total_categories']}"
        print(f"Progress: {zip_progress} | {cat_progress}")
    
    print(f"Total Leads: {AUTOPILOT_STATE['total_leads']}")
    print("=" * 60)


def select_mode():
    """Display mode selector and return selected mode"""
    print("=" * 60)
    print("🦝 CritterCaptures Lead Generation System")
    print("=" * 60)
    print("Select Mode:")
    
    choices = [
        Choice(value="manual", name="Manual Mode"),
        Choice(value="automation", name="Automation Mode")
    ]
    
    selected = inquirer.select(
        message="Choose your mode:",
        choices=choices,
        default="manual"
    ).execute()
    
    print("=" * 60)
    return selected


async def wait_for_resume():
    """Wait for user to resume if paused"""
    while AUTOPILOT_STATE['paused'] and not AUTOPILOT_STATE['should_quit']:
        await asyncio.sleep(0.5)
        update_status_display()


async def autopilot_scrape_zip_category(zip_code: str, category: str, tracker: ZipTracker, db: LeadsDatabase):
    """Scrape a single ZIP + category combination in autopilot mode"""
    global AUTOPILOT_STATE
    
    # Update status
    AUTOPILOT_STATE['current_zip'] = zip_code
    AUTOPILOT_STATE['current_category'] = category
    update_status_display()
    
    # Check if we should quit
    if AUTOPILOT_STATE['should_quit']:
        return []
    
    # Wait if paused
    await wait_for_resume()
    
    if AUTOPILOT_STATE['should_quit']:
        return []
    
    print(f"\n🚀 Auto-scraping {zip_code} - {category}")
    
    # Build URL
    base_url = f"https://www.yellowpages.com/search?search_terms={category.replace(' ', '+')}&geo_location_terms={zip_code}&page={{page_number}}"
    css_selector = ".result"
    
    try:
        browser_config = get_browser_config()
        llm_strategy = get_llm_strategy(
            llm_instructions=SCRAPER_INSTRUCTIONS,
            output_format=BusinessData
        )
        session_id = f"critter_{zip_code}_{category}".replace(" ", "_")
        
        all_records = []
        seen_names = set()
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            for page_number in range(1, MAX_PAGES_PER_SEARCH + 1):
                # Check for quit/pause
                if AUTOPILOT_STATE['should_quit']:
                    break
                await wait_for_resume()
                if AUTOPILOT_STATE['should_quit']:
                    break
                
                print(f"   📄 Page {page_number}...")
                
                try:
                    records, no_results_found = await fetch_and_process_page(
                        crawler,
                        page_number,
                        base_url,
                        css_selector,
                        llm_strategy,
                        session_id,
                        seen_names,
                    )
                    
                    if no_results_found:
                        break
                    
                    if not records:
                        break
                    
                    # Add metadata to each record
                    for record in records:
                        record['category'] = category
                        record['zip_code'] = zip_code
                    
                    all_records.extend(records)
                    print(f"   ✓ {len(records)} leads")
                    
                    await asyncio.sleep(2)  # Be respectful
                    
                except Exception as e:
                    error_msg = str(e).lower()
                    if any(network_error in error_msg for network_error in ['timeout', 'connection', 'network']):
                        print(f"   ⚠️ Network issue on page {page_number}, skipping...")
                        continue
                    else:
                        print(f"   ❌ Error on page {page_number}: {e}")
                        continue
        
        # Clean and dedupe with error handling
        if all_records:
            try:
                clean_leads = clean_and_dedupe(all_records, db)
                
                # Save leads
                if clean_leads:
                    # Generate lead number
                    existing_leads = []
                    if os.path.exists("data/leads"):
                        for category_folder in os.listdir("data/leads"):
                            cat_path = os.path.join("data/leads", category_folder)
                            if os.path.isdir(cat_path):
                                for lead_folder in os.listdir(cat_path):
                                    if lead_folder.startswith("lead_") and "_zip_" in lead_folder:
                                        try:
                                            num = int(lead_folder.split("_")[1])
                                            existing_leads.append(num)
                                        except:
                                            pass
                    
                    lead_number = max(existing_leads) + 1 if existing_leads else 1
                    
                    # Save to CSV
                    output_file = save_leads(clean_leads, zip_code, category, lead_number, tracker)
                    
                    if output_file:
                        # Mark as used in tracker
                        tracker.mark_used(
                            zip_code=zip_code,
                            category=category,
                            leads_count=len(clean_leads),
                            output_file=output_file
                        )
                        
                        # Update total leads count
                        AUTOPILOT_STATE['total_leads'] += len(clean_leads)
                        
                        print(f"   ✅ Saved {len(clean_leads)} leads")
                    else:
                        print(f"   ❌ Failed to save leads")
                else:
                    print(f"   ⚠️ No valid leads after cleaning")
            except Exception as e:
                print(f"   ⚠️ Error processing leads: {e}")
        else:
            print(f"   ⚠️ No leads found")
        
        return all_records
        
    except Exception as e:
        error_msg = str(e).lower()
        if any(network_error in error_msg for network_error in ['timeout', 'connection', 'network']):
            print(f"   ❌ Network error: {e}")
        else:
            print(f"   ❌ Scraping error: {e}")
        return []


def display_automation_status(zip_code, city, category, zip_index, total_zips, cat_index, total_categories, total_leads):
    """Display automation status"""
    print("\n" + "=" * 60)
    print("Mode: AUTOMATION")
    print(f"Current ZIP: {zip_code} ({city})")
    print(f"Category: {category}")
    print(f"Progress: {zip_index}/{total_zips} ZIPs | {cat_index}/{total_categories} Categories")
    print(f"Total Leads: {total_leads}")
    print("=" * 60)


async def run_automation_mode():
    """Run the automation mode"""
    global AUTOPILOT_STATE
    
    print_header()
    print("🤖 AUTOMATION MODE - Hands-Free Scraping")
    print("=" * 60)
    print("HOTKEYS:")
    print("  P = Pause automation")
    print("  R = Resume automation") 
    print("  Q = Quit and save progress")
    print("=" * 60)
    
    # Show initial hotkey bar
    print_hotkey_bar()
    
    # Initialize systems
    try:
        db = LeadsDatabase()
        tracker = ZipTracker()
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return
    
    # Use Dover, FL as default
    city, state = "Dover", "FL"
    print(f"\n📍 Target: {city}, {state}")
    
    # Get ZIP codes
    try:
        zips_data = get_zips_in_radius(city, state, radius_miles=50)
    except Exception as e:
        print(f"❌ ZIP lookup failed: {e}")
        return
    
    if not zips_data:
        print("❌ No ZIP codes found!")
        return
    
    # Filter to only available ZIPs (not fully used)
    available_zips = []
    for zip_info in zips_data:
        zip_code = zip_info['zip']
        if not tracker.is_zip_fully_used(zip_code, CATEGORIES):
            available_zips.append(zip_info)
    
    if not available_zips:
        print("✅ All ZIP codes are fully scraped!")
        return
    
    print(f"📋 Found {len(available_zips)} ZIP codes with available categories")
    print(f"📊 Total categories to scrape: {len(CATEGORIES)}")
    print(f"🎯 Estimated total combinations: ~{len(available_zips) * len(CATEGORIES)}")

    # Ask for confirmation before starting
    print("\n" + "=" * 60)
    confirm = inquirer.confirm(
        message="Ready to start automation? (Press hotkeys during scraping: P=Pause, R=Resume, Q=Quit)",
        default=True
    ).execute()

    if not confirm:
        print("\n❌ Automation cancelled.")
        return

    print("\n🚀 Starting automation mode...")
    print("=" * 60)

    # Start keyboard listener
    start_keyboard_listener()
    
    # Initialize automation state
    AUTOPILOT_STATE.update({
        'total_zips': len(available_zips),
        'total_categories': len(CATEGORIES),
        'zip_index': 0,
        'category_index': 0,
        'total_leads': 0,
        'current_zip': None,
        'current_category': None
    })
    
    # Show initial status
    print_automation_status()
    
    try:
        # Loop through each ZIP
        for zip_index, zip_info in enumerate(available_zips):
            if AUTOPILOT_STATE['should_quit']:
                break
            
            zip_code = zip_info['zip']
            city_name = zip_info['city']
            AUTOPILOT_STATE['zip_index'] = zip_index + 1
            
            # Get available categories for this ZIP
            try:
                available_categories = tracker.get_available_categories(zip_code, CATEGORIES)
            except Exception as e:
                print(f"\n⚠️ Error getting categories for {zip_code}: {e}")
                continue
            
            if not available_categories:
                print(f"\n⏭️ Skipping {zip_code} - all categories used")
                continue
            
            print(f"\n📍 Processing ZIP {zip_code} ({city_name}) - {len(available_categories)} categories available")

            # Loop through each available category
            for cat_index, category in enumerate(available_categories):
                if AUTOPILOT_STATE['should_quit']:
                    break
                
                AUTOPILOT_STATE['category_index'] = cat_index + 1
                AUTOPILOT_STATE['current_zip'] = zip_code
                AUTOPILOT_STATE['current_category'] = category
                
                # Display status
                print_automation_status()

                # Wait if paused
                await wait_for_resume()
                if AUTOPILOT_STATE['should_quit']:
                    break
                
                # Scrape this ZIP + category combination with error handling
                try:
                    leads = await autopilot_scrape_zip_category(zip_code, category, tracker, db)
                except Exception as e:
                    print(f"\n⚠️ Error scraping {zip_code} - {category}: {e}")
                    print("   Continuing to next category...")
                    continue
                
                # Update status after scraping
                print_automation_status()

                # Small delay between categories
                await asyncio.sleep(1)
        
        # Completion
        if not AUTOPILOT_STATE['should_quit']:
            print(f"\n\n✅ Automation complete — all ZIPs and categories scraped. Total leads collected: {AUTOPILOT_STATE['total_leads']}")
            beep()
            print("🎉 Done!")
        else:
            print(f"\n\n❌ Stopped by user. Total leads collected: {AUTOPILOT_STATE['total_leads']}")
    
    finally:
        # Clean up
        stop_keyboard_listener()
        print(f"\n💾 Progress saved to tracker.")


def get_city_input():
    """Get city and state from user"""
    print("\n📍 Enter your target location:")
    city = inquirer.text(
        message="City name:",
        default="Dover"
    ).execute()
    
    state = inquirer.text(
        message="State (2-letter code):",
        default="FL"
    ).execute()
    
    return city.strip(), state.strip().upper()


def select_zip_code(zips_data, tracker: ZipTracker):
    """
    Display color-coded ZIP code dropdown
    🟢 Green = available (has unused categories)
    🔴 Red = fully used (all categories scraped)
    """
    if not zips_data:
        print("\n❌ No ZIP codes found in the specified radius!")
        return None
    
    choices = []
    choices.append(Separator("=" * 50))
    choices.append(Separator("🟢 = Available  |  🔴 = Fully Scraped"))
    choices.append(Separator("=" * 50))
    
    for zip_info in zips_data:
        zip_code = zip_info['zip']
        city = zip_info['city']
        distance = zip_info['distance']
        
        # Check if this ZIP is fully used
        is_full = tracker.is_zip_fully_used(zip_code, CATEGORIES)
        used_count = len(tracker.get_used_categories(zip_code))
        
        if is_full:
            # Red for fully used
            label = f"🔴 {zip_code} - {city} ({distance} mi) [All {used_count} categories used]"
        elif used_count > 0:
            # Yellow/Orange for partially used
            remaining = len(CATEGORIES) - used_count
            label = f"🟡 {zip_code} - {city} ({distance} mi) [{remaining} categories available]"
        else:
            # Green for fully available
            label = f"🟢 {zip_code} - {city} ({distance} mi) [All {len(CATEGORIES)} available]"
        
        choices.append(Choice(value=zip_code, name=label))
    
    selected = inquirer.select(
        message="Select a ZIP code:",
        choices=choices,
        default=zips_data[0]['zip']
    ).execute()
    
    return selected


def select_category(zip_code: str, tracker: ZipTracker):
    """
    Display color-coded category dropdown
    🟢 Green = not scraped yet for this ZIP
    🔴 Red = already scraped for this ZIP
    """
    used_categories = set(tracker.get_used_categories(zip_code))
    
    choices = []
    choices.append(Separator("=" * 50))
    choices.append(Separator(f"Categories for ZIP {zip_code}"))
    choices.append(Separator("🟢 = Available  |  🔴 = Already Scraped"))
    choices.append(Separator("=" * 50))
    
    for category in CATEGORIES:
        if category in used_categories:
            label = f"🔴 {category} [Already scraped]"
            # Still allow selection but mark it
            choices.append(Choice(value=category, name=label, enabled=False))
        else:
            label = f"🟢 {category}"
            choices.append(Choice(value=category, name=label))
    
    # Check if any categories are available
    available = [c for c in CATEGORIES if c not in used_categories]
    
    if not available:
        print(f"\n❌ All categories already scraped for ZIP {zip_code}!")
        print("   Please select a different ZIP code.")
        return None
    
    selected = inquirer.select(
        message="Select a category to scrape:",
        choices=choices,
        default=available[0] if available else CATEGORIES[0]
    ).execute()
    
    # Double-check if user selected an already-used category
    if selected in used_categories:
        print(f"\n⚠️  WARNING: {selected} was already scraped for ZIP {zip_code}")
        confirm = inquirer.confirm(
            message="Do you want to scrape it again anyway?",
            default=False
        ).execute()
        
        if not confirm:
            return None
    
    return selected


async def scrape_zip_category(zip_code: str, category: str):
    """Scrape a single ZIP + category combination with network resilience"""
    print(f"\n{'='*60}")
    print(f"🚀 Starting scrape...")
    print(f"   📮 ZIP: {zip_code}")
    print(f"   📦 Category: {category}")
    print(f"{'='*60}\n")
    
    # Build URL
    base_url = f"https://www.yellowpages.com/search?search_terms={category.replace(' ', '+')}&geo_location_terms={zip_code}&page={{page_number}}"
    css_selector = ".result"
    
    try:
        browser_config = get_browser_config()
        llm_strategy = get_llm_strategy(
            llm_instructions=SCRAPER_INSTRUCTIONS,
            output_format=BusinessData
        )
        session_id = f"critter_{zip_code}_{category}".replace(" ", "_")

        all_records = []
        seen_names = set()

        async with AsyncWebCrawler(config=browser_config) as crawler:
            for page_number in range(1, MAX_PAGES_PER_SEARCH + 1):
                print(f"   📄 Scraping page {page_number}...")

                try:
                    records, no_results_found = await fetch_and_process_page(
                        crawler,
                        page_number,
                        base_url,
                        css_selector,
                        llm_strategy,
                        session_id,
                        seen_names,
                    )

                    if no_results_found:
                        print(f"   ⚠️  No results found on page {page_number}")
                        break

                    if not records:
                        print(f"   ⚠️  No records extracted from page {page_number}")
                        break

                    # Add metadata to each record
                    for record in records:
                        record['category'] = category
                        record['zip_code'] = zip_code

                    all_records.extend(records)
                    print(f"   ✓ Found {len(records)} leads on page {page_number}")

                    await asyncio.sleep(2)  # Be respectful

                except Exception as e:
                    error_msg = str(e).lower()
                    if any(network_error in error_msg for network_error in ['timeout', 'connection', 'network']):
                        print(f"   ⚠️ Network issue on page {page_number}, skipping...")
                        continue
                    else:
                        print(f"   ❌ Error on page {page_number}: {e}")
                        continue

        print(f"\n   📊 Total leads found: {len(all_records)}")
        return all_records

    except Exception as e:
        error_msg = str(e).lower()
        if any(network_error in error_msg for network_error in ['timeout', 'connection', 'network']):
            print(f"\n❌ Persistent network issue — please check your internet or try again later.")
            print(f"   Error: {e}")
        else:
            print(f"\n❌ Scraping failed: {e}")
        return []


def clean_and_dedupe(leads, db: LeadsDatabase):
    """Remove duplicates using database"""
    if not leads:
        return []
    
    print(f"\n🧹 Cleaning and deduplicating {len(leads)} leads...")
    
    clean_leads = []
    session_dupes = 0
    db_dupes = 0
    seen_session = set()
    
    for lead in leads:
        if not lead.get('name') or not lead.get('phone_number'):
            continue
        
        name = lead['name'].strip()
        phone = lead['phone_number'].strip()
        address = lead.get('address', '').strip()
        
        # Check session duplicates
        key = (name.lower(), phone)
        if key in seen_session:
            session_dupes += 1
            continue
        
        # Check database duplicates
        if db.is_duplicate(name, phone, address):
            db_dupes += 1
            continue
        
        # New unique lead
        seen_session.add(key)
        clean_leads.append(lead)
        
        # Add to database
        db.add_lead(
            name=name,
            address=address,
            phone=phone,
            email=lead.get('email', 'N/A'),
            website=lead.get('website', 'N/A'),
            zip_code=lead.get('zip_code', ''),
            category=lead.get('category', ''),
            location="Tampa Bay Area",
            source_file="leadgen_cli.py"
        )
    
    total_removed = len(leads) - len(clean_leads)
    if total_removed > 0:
        print(f"   ✓ Removed {total_removed} duplicates:")
        print(f"      - {session_dupes} within this session")
        print(f"      - {db_dupes} from previous scrapes")
    
    print(f"   ✓ {len(clean_leads)} unique leads ready to save")
    return clean_leads


def save_leads(leads, zip_code, category, lead_number=None, tracker=None):
    """Save leads to CSV file with validation and confirmation"""
    if not leads:
        print("\n⚠️  No leads to save!")
        return None
    
    # Validate leads have essential data
    valid_leads = []
    for lead in leads:
        if lead.get('name') and (lead.get('phone_number') or lead.get('address')):
            valid_leads.append(lead)
        else:
            print(f"   [WARN] Skipping invalid lead: {lead.get('name', 'Unknown')}")
    
    if not valid_leads:
        print("\n⚠️  No valid leads to save after validation!")
        return None
    
    # Create organized folder structure: data/leads/{category}/lead_{number}_zip_{zipcode}/
    safe_category = category.lower().replace(" ", "_")
    
    # If no lead number provided, get next available number
    if lead_number is None:
        # Use provided tracker or create a new one if needed
        if tracker is None:
            try:
                tracker = ZipTracker()
            except Exception as e:
                print(f"❌ ZipTracker initialization failed — please check imports or class definition: {e}")
                return None
        
        # Check if this combo exists in tracker
        if tracker.is_used(zip_code, category):
            # Already scraped, this shouldn't happen but handle it
            lead_number = len([f for f in os.listdir("data/leads") if f.startswith("lead_")]) + 1 if os.path.exists("data/leads") else 1
        else:
            # Get next lead number
            existing_leads = []
            if os.path.exists("data/leads"):
                for item in os.listdir("data/leads"):
                    if item.startswith("lead_") and "_zip_" in item:
                        try:
                            num = int(item.split("_")[1])
                            existing_leads.append(num)
                        except:
                            pass
            lead_number = max(existing_leads) + 1 if existing_leads else 1
    
    lead_folder = f"lead_{lead_number}_zip_{zip_code}"
    output_dir = os.path.join("data", "leads", safe_category, lead_folder)
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"\n💾 Preparing to save {len(valid_leads)} valid leads...")
        print(f"   📁 Folder: {output_dir}")
    except Exception as e:
        print(f"\n❌ ERROR creating directory: {e}")
        return None
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = os.path.join(output_dir, f"{zip_code}_{timestamp}.csv")
    
    # Write CSV
    fieldnames = ['name', 'address', 'phone_number', 'website', 'email', 'category', 'zip_code']
    
    try:
        # Fill in missing fields with defaults
        for lead in valid_leads:
            lead.setdefault('name', 'N/A')
            lead.setdefault('address', 'N/A')
            lead.setdefault('phone_number', 'N/A')
            lead.setdefault('website', 'N/A')
            lead.setdefault('email', 'N/A')
            lead.setdefault('category', category)
            lead.setdefault('zip_code', zip_code)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(valid_leads)
        
        # Verify file was created and get stats
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"\n💾 ✅ SUCCESS! File saved:")
            print(f"   📁 Path: {os.path.abspath(filename)}")
            print(f"   📊 Leads: {len(valid_leads)}")
            print(f"   💿 Size: {file_size:,} bytes")
            
            # Count rows to confirm
            with open(filename, 'r', encoding='utf-8') as f:
                row_count = sum(1 for _ in f) - 1  # Subtract header
            print(f"   ✅ Verified: {row_count} rows written to CSV")
        else:
            print(f"\n❌ ERROR: File was not created at {filename}")
            return None
        
        return filename
    
    except PermissionError:
        print(f"\n❌ PERMISSION ERROR: Cannot write to {filename}")
        print(f"   Try running as administrator or check folder permissions")
        return None
    except Exception as e:
        print(f"\n❌ ERROR saving file: {type(e).__name__}: {e}")
        return None


async def run_interactive_flow():
    """Main interactive workflow with network resilience"""
    print_header()
    print("📋 MANUAL MODE - Interactive Selection")
    print("=" * 60)
    
    # Initialize systems with safety checks
    try:
        db = LeadsDatabase()
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("\n❌ Persistent network issue — please check your internet or try again later.")
        return

    try:
        tracker = ZipTracker()
    except Exception as e:
        print(f"❌ ZipTracker initialization failed — please check imports or class definition: {e}")
        print("\n❌ Persistent network issue — please check your internet or try again later.")
        return

    # Get city input
    try:
        city, state = get_city_input()
    except Exception as e:
        print(f"❌ Input error: {e}")
        return

    # Find ZIP codes within radius with network resilience
    try:
        zips_data = get_zips_in_radius(city, state, radius_miles=50)
    except Exception as e:
        print(f"❌ ZIP lookup failed: {e}")
        print("\n❌ Persistent network issue — please check your internet or try again later.")
        return
    
    if not zips_data:
        print("\n❌ No ZIP codes found! Exiting.")
        return
    
    # Select ZIP code
    selected_zip = select_zip_code(zips_data, tracker)
    
    if not selected_zip:
        print("\n❌ No ZIP code selected. Exiting.")
        return
    
    # Select category
    selected_category = select_category(selected_zip, tracker)
    
    if not selected_category:
        print("\n❌ No valid category selected. Exiting.")
        return
    
    # Confirm before scraping
    print(f"\n{'='*60}")
    print("📋 SCRAPING SUMMARY")
    print(f"{'='*60}")
    print(f"   📮 ZIP Code: {selected_zip}")
    print(f"   📦 Category: {selected_category}")
    print(f"   📄 Max Pages: {MAX_PAGES_PER_SEARCH}")
    print(f"{'='*60}\n")
    
    confirm = inquirer.confirm(
        message="Ready to start scraping?",
        default=True
    ).execute()
    
    if not confirm:
        print("\n❌ Scraping cancelled.")
        return
    
    # Run scraper with error handling
    try:
        leads = await scrape_zip_category(selected_zip, selected_category)
    except Exception as e:
        print(f"\n❌ Scraping failed: {e}")
        print("\n❌ Persistent network issue — please check your internet or try again later.")
        return

    if not leads:
        print("\n⚠️ No leads found. This could be due to network issues or no results for this ZIP/category.")
        print("   Try a different ZIP code or category.")
        return

    # Clean and dedupe
    try:
        clean_leads = clean_and_dedupe(leads, db)
    except Exception as e:
        print(f"\n❌ Data processing failed: {e}")
        return

    # Generate lead number for folder structure
    try:
        existing_leads = []
        if os.path.exists("data/leads"):
            # Look in all category folders
            for category_folder in os.listdir("data/leads"):
                cat_path = os.path.join("data/leads", category_folder)
                if os.path.isdir(cat_path):
                    for lead_folder in os.listdir(cat_path):
                        if lead_folder.startswith("lead_") and "_zip_" in lead_folder:
                            try:
                                num = int(lead_folder.split("_")[1])
                                existing_leads.append(num)
                            except:
                                pass

        lead_number = max(existing_leads) + 1 if existing_leads else 1
    except Exception as e:
        print(f"\n❌ Error generating lead number: {e}")
        lead_number = 1  # Fallback
    
    # Save to CSV with proper folder structure
    try:
        output_file = save_leads(clean_leads, selected_zip, selected_category, lead_number, tracker)
    except Exception as e:
        print(f"\n❌ File saving failed: {e}")
        return
    
    if output_file:
        # Mark as used in tracker
        try:
            tracker.mark_used(
                zip_code=selected_zip,
                category=selected_category,
                leads_count=len(clean_leads),
                output_file=output_file
            )
        except Exception as e:
            print(f"\n⚠️ Warning: Could not update tracker: {e}")

        print(f"\n{'='*60}")
        print("✅ SCRAPING COMPLETE!")
        print(f"{'='*60}")
        print(f"   📊 Total leads scraped: {len(leads)}")
        print(f"   ✨ Unique leads saved: {len(clean_leads)}")
        print(f"   📁 File: {output_file}")
        try:
            print(f"   💾 Database total: {db.get_total_leads()} leads")
        except:
            print(f"   💾 Database total: Unable to retrieve")
        print(f"{'='*60}\n")
    else:
        print("\n⚠️ No file was saved. Check the error messages above.")

    # Ask if user wants to continue
    try:
        continue_scraping = inquirer.confirm(
            message="Do you want to scrape another ZIP/category?",
            default=True
        ).execute()

        if continue_scraping:
            await run_interactive_flow()
        else:
            print("\n👋 Thanks for using CritterCaptures Lead Generation!")
            try:
                tracker.print_stats()
            except:
                print("   (Stats unavailable)")
    except Exception as e:
        print(f"\n⚠️ Input error: {e}")
        print("\n👋 Thanks for using CritterCaptures Lead Generation!")


async def main():
    """Main entry point with mode selection"""
    # Set UTF-8 encoding for Windows
    if os.name == 'nt':
        import sys
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Select mode
    mode = select_mode()
    
    # Run the appropriate mode
    if mode == "manual":
        await run_interactive_flow()
    elif mode == "automation":
        await run_automation_mode()


if __name__ == "__main__":
    asyncio.run(main())

