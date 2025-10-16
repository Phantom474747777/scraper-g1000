"""
CritterCaptures Lead Generation Tool
Simple scraper - no AI scoring, just raw lead data
"""
import asyncio
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler
from src.scraper import get_browser_config, get_llm_strategy, fetch_and_process_page
from src.database import LeadsDatabase
from models.business import BusinessData

# Load environment variables
load_dotenv(override=True)

# Available search categories
AVAILABLE_CATEGORIES = [
    "Property Management Companies",
    "Real Estate Agents",
    "HOA Management",
    "Vacation Rentals",
    "Apartment Complexes",
    "Mobile Home Parks",
    "Storage Facilities",
    "Hotels Motels",
]

MAX_PAGES_PER_SEARCH = 2

SCRAPER_INSTRUCTIONS = (
    "Extract all business information: 'name', 'address', 'website', 'phone_number', "
    "'email' (if available, otherwise 'N/A') from the following content."
)


def show_menu():
    """Display interactive menu"""
    print("\n" + "=" * 60)
    print("🦝 CritterCaptures Lead Scraper")
    print("=" * 60)
    print("\n📋 MENU:")
    print("  [1] Start New Scrape")
    print("  [2] View Database Stats")
    print("  [3] List Available Categories")
    print("  [4] Exit")
    print("=" * 60)
    
    choice = input("\nSelect option (1-4): ").strip()
    return choice


def get_user_input():
    """Get zip codes and category from user"""
    print("\n" + "=" * 60)
    print("📮 Enter ZIP codes to scrape:")
    print("   (separate multiple with commas, e.g., 33527, 33594, 33612)")
    print("=" * 60)
    
    zip_input = input("\nZip codes: ").strip()
    zip_codes = [z.strip() for z in zip_input.split(',') if z.strip()]
    
    if not zip_codes:
        print("❌ No zip codes entered!")
        return None, None
    
    print("\n" + "=" * 60)
    print("📂 AVAILABLE CATEGORIES:")
    print("=" * 60)
    for i, cat in enumerate(AVAILABLE_CATEGORIES, 1):
        print(f"  [{i}] {cat}")
    print("=" * 60)
    
    cat_choice = input(f"\n🏷️  Select a category number (1-{len(AVAILABLE_CATEGORIES)}): ").strip()
    
    try:
        cat_index = int(cat_choice) - 1
        if 0 <= cat_index < len(AVAILABLE_CATEGORIES):
            category = AVAILABLE_CATEGORIES[cat_index]
            return zip_codes, category
        else:
            print("❌ Invalid category number!")
            return None, None
    except ValueError:
        print("❌ Please enter a number!")
        return None, None


def show_categories():
    """Display all available categories"""
    print("\n" + "=" * 60)
    print("📂 AVAILABLE CATEGORIES:")
    print("=" * 60)
    for i, cat in enumerate(AVAILABLE_CATEGORIES, 1):
        print(f"  [{i}] {cat}")
    print("=" * 60)


def show_stats():
    """Display database statistics"""
    db = LeadsDatabase()
    stats = db.get_stats()
    
    print("\n" + "=" * 60)
    print("📊 DATABASE STATISTICS")
    print("=" * 60)
    print(f"\n📈 Total Unique Leads: {stats['total_leads']}")
    
    if stats['by_location']:
        print("\n📍 Leads by Location:")
        for location, count in stats['by_location']:
            print(f"   • {location}: {count} leads")
    
    if stats['top_zip_codes']:
        print("\n🏙️  Top Zip Codes:")
        for zip_code, count in stats['top_zip_codes']:
            print(f"   • {zip_code}: {count} leads")
    
    print("=" * 60)


async def scrape_zip_category(zip_code: str, category: str, db: LeadsDatabase):
    """Scrape a single zip code + category combination"""
    
    # Check if already scraped
    is_scraped, scraped_date, lead_number = db.is_combo_scraped(zip_code, category)
    
    if is_scraped:
        print(f"\n⚠️  ALREADY SCRAPED!")
        print(f"   📅 Date: {scraped_date}")
        print(f"   📁 Lead Number: {lead_number}")
        print(f"   📦 Combo: ZIP {zip_code} + {category}")
        print(f"   🚫 SKIPPING!")
        return []
    
    print(f"\n🔍 Scraping: {category} in ZIP {zip_code}")
    
    # Build URL
    base_url = f"https://www.yellowpages.com/search?search_terms={category.replace(' ', '+')}&geo_location_terms={zip_code}&page={{page_number}}"
    css_selector = ".result"
    
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
            records, no_results_found = await fetch_and_process_page(
                crawler,
                page_number,
                base_url,
                css_selector,
                llm_strategy,
                session_id,
                seen_names,
            )
            
            if no_results_found or not records:
                break
            
            # Add category and zip to each record
            for record in records:
                record['category'] = category
                record['zip_code'] = zip_code
            
            all_records.extend(records)
            await asyncio.sleep(2)
    
    print(f"   ✓ Found {len(all_records)} leads")
    
    # Mark as scraped
    if all_records:
        lead_number = db.mark_combo_scraped(zip_code, category)
        return all_records, lead_number
    
    return all_records, None


def save_leads(leads, zip_code, category, lead_number):
    """Save leads to organized CSV file"""
    if not leads:
        print("\n⚠️  No leads to save!")
        return None
    
    # Create organized folder structure
    category_folder = category.lower().replace(" ", "_")
    lead_folder = f"lead_{lead_number}_zip_{zip_code}"
    output_dir = os.path.join("data", "leads", category_folder, lead_folder)
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = os.path.join(output_dir, f"{zip_code}_{timestamp}.csv")
    
    # Save to CSV
    fieldnames = ['name', 'address', 'phone_number', 'website', 'email', 'category', 'zip_code']
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)
    
    print(f"\n💾 Saved to: {filename}")
    return filename


def clean_leads(leads, db: LeadsDatabase):
    """Remove duplicates using database"""
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
            source_file="get_critter_leads.py"
        )
    
    total_removed = len(leads) - len(clean_leads)
    if total_removed > 0:
        print(f"\n🧹 Removed {total_removed} duplicates:")
        print(f"   - {session_dupes} duplicates in this session")
        print(f"   - {db_dupes} already in database")
    
    return clean_leads


async def run_scraper():
    """Main scraper function"""
    zip_codes, category = get_user_input()
    
    if not zip_codes or not category:
        return
    
    print("\n" + "=" * 60)
    print(f"🚀 Starting scrape...")
    print(f"   📦 Category: {category}")
    print(f"   📮 Zip Codes: {', '.join(zip_codes)}")
    print("=" * 60)
    
    input("\nPress ENTER to start scraping...")
    
    db = LeadsDatabase()
    initial_count = db.get_total_leads()
    
    all_leads = []
    
    for zip_code in zip_codes:
        result = await scrape_zip_category(zip_code, category, db)
        if result:
            leads, lead_number = result
            if leads and lead_number:
                # Clean and deduplicate
                clean = clean_leads(leads, db)
                if clean:
                    # Save to CSV
                    save_leads(clean, zip_code, category, lead_number)
                    all_leads.extend(clean)
    
    # Final summary
    final_count = db.get_total_leads()
    new_leads = final_count - initial_count
    
    print("\n" + "=" * 60)
    print("✅ SCRAPING COMPLETE!")
    print("=" * 60)
    print(f"   📊 Total leads scraped: {len(all_leads)}")
    print(f"   ✨ NEW unique leads: {new_leads}")
    print(f"   💾 Total in database: {final_count}")
    print("\n   📁 Check data/leads/ folder for your CSV files!")
    print("=" * 60)


async def main():
    """Main entry point with menu"""
    while True:
        choice = show_menu()
        
        if choice == "1":
            await run_scraper()
        elif choice == "2":
            show_stats()
        elif choice == "3":
            show_categories()
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice! Please select 1-4.")
        
        input("\nPress ENTER to continue...")


if __name__ == "__main__":
    # Set UTF-8 encoding for Windows
    if os.name == 'nt':
        import sys
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    asyncio.run(main())
