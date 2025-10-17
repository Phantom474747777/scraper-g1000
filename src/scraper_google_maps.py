"""
Google Maps Scraper - FREE Alternative to YellowPages
NO Cloudflare, NO blocks, ACTUALLY WORKS!
"""

import time
import re
from typing import List, Dict
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_google_maps_driver():
    """Create Chrome driver for Google Maps scraping."""
    options = uc.ChromeOptions()
    # Google Maps works better with visible window
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = uc.Chrome(options=options, version_main=None, use_subprocess=True)
    return driver


def extract_google_maps_businesses(driver, max_results=50) -> List[Dict[str, str]]:
    """Extract business data from Google Maps search results."""
    businesses = []
    seen_names = set()

    print(f"[INFO] Scrolling to load up to {max_results} results...")

    # Wait for results to load
    time.sleep(5)

    # Find the scrollable results panel
    try:
        scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
        print("[SUCCESS] Found results feed")
    except Exception as e:
        print(f"[ERROR] Could not find results feed: {e}")
        # Try alternative selector
        try:
            scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div.m6QErb')
            print("[SUCCESS] Found results panel (alternative selector)")
        except:
            print("[ERROR] Could not find scrollable div - aborting")
            return []

    for i in range(20):  # Scroll 20 times to load ~50 results
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        time.sleep(0.5)

        # Check if we've loaded enough
        current_count = len(driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]'))
        if current_count >= max_results:
            break

    print(f"[INFO] Loaded {current_count} results, extracting data...")

    # Extract business cards
    business_cards = driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')

    for card in business_cards[:max_results]:
        try:
            business = {}

            # Name
            try:
                name_elem = card.find_element(By.CSS_SELECTOR, 'div.fontHeadlineSmall')
                business['name'] = name_elem.text.strip()
            except:
                continue  # Skip if no name

            # Skip duplicates
            if business['name'] in seen_names:
                continue
            seen_names.add(business['name'])

            # Click to open details panel
            try:
                card.click()
                time.sleep(1.5)  # Wait for details to load
            except:
                pass

            # Phone
            try:
                phone_button = driver.find_element(By.CSS_SELECTOR, 'button[data-tooltip*="phone" i], button[aria-label*="phone" i]')
                phone_text = phone_button.get_attribute('data-tooltip') or phone_button.get_attribute('aria-label')
                phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', phone_text)
                business['phone_number'] = phone_match.group(0) if phone_match else 'N/A'
            except:
                business['phone_number'] = 'N/A'

            # Address
            try:
                address_button = driver.find_element(By.CSS_SELECTOR, 'button[data-tooltip*="address" i], button[aria-label*="address" i]')
                address_text = address_button.get_attribute('data-tooltip') or address_button.get_attribute('aria-label')
                # Clean up "Copy address" and other artifacts
                address_text = re.sub(r'Copy address:?\s*', '', address_text, flags=re.IGNORECASE)
                business['address'] = address_text.strip() or 'N/A'
            except:
                business['address'] = 'N/A'

            # Website
            try:
                website_link = driver.find_element(By.CSS_SELECTOR, 'a[data-tooltip*="website" i], a[aria-label*="website" i]')
                business['website'] = website_link.get_attribute('href') or 'N/A'
            except:
                business['website'] = 'N/A'

            # Email (usually not available on Google Maps)
            business['email'] = 'N/A'

            # Only add if we have phone or address
            if business['phone_number'] != 'N/A' or business['address'] != 'N/A':
                businesses.append(business)
                print(f"[EXTRACT] {business['name']} - {business['phone_number']}")

        except Exception as e:
            print(f"[WARNING] Failed to extract business: {e}")
            continue

    return businesses


def scrape_google_maps(zip_code: str, category: str, max_results: int = 50) -> List[Dict[str, str]]:
    """
    Scrape Google Maps for business leads - FREE and NO Cloudflare!

    Args:
        zip_code: ZIP code to search
        category: Business category
        max_results: Maximum results to scrape (default 50)

    Returns:
        List of business dictionaries
    """
    print(f"[INIT] Starting Google Maps scraper for {zip_code} - {category}")
    print("[INFO] Google Maps = NO Cloudflare, NO blocks!")

    driver = None
    all_businesses = []

    try:
        driver = create_google_maps_driver()
        print("[SUCCESS] Browser created")

        # Build Google Maps search URL
        search_query = f"{category} near {zip_code}"
        url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"

        print(f"[PAGE 1] Fetching {url}")
        driver.get(url)

        # Wait for map to load
        print("[WAIT] Waiting for Google Maps to load...")
        time.sleep(5)

        # Extract businesses
        all_businesses = extract_google_maps_businesses(driver, max_results)

        print(f"[SUCCESS] Found {len(all_businesses)} unique businesses")

    except Exception as e:
        print(f"[ERROR] Scraping failed: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            print("\n[CLEANUP] Closing browser...")
            driver.quit()

    print(f"\n[COMPLETE] Total unique businesses: {len(all_businesses)}")
    return all_businesses


if __name__ == "__main__":
    # Quick test
    leads = scrape_google_maps("33527", "Real Estate Agents", max_results=20)

    if leads:
        print("\n[TEST SUCCESS] Sample leads:")
        for i, lead in enumerate(leads[:3], 1):
            print(f"\n{i}. {lead['name']}")
            print(f"   Phone: {lead['phone_number']}")
            print(f"   Address: {lead['address']}")
    else:
        print("\n[TEST FAILED] No leads found")
