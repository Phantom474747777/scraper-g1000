"""
FREE Cloudflare Bypass Scraper using undetected-chromedriver
NO PAID SERVICES - 100% FREE
"""

import time
import re
from typing import List, Dict
from bs4 import BeautifulSoup
import undetected_chromedriver as uc


def create_stealth_driver():
    """Create an undetected Chrome driver to bypass Cloudflare."""
    options = uc.ChromeOptions()
    # DO NOT USE HEADLESS - Cloudflare detects it!
    # options.add_argument('--headless=new')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--start-maximized')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

    # Use undetected-chromedriver with suppressed automation detection
    driver = uc.Chrome(options=options, version_main=None, use_subprocess=True)

    # Extra stealth: execute CDP commands
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    })
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver


def extract_businesses_from_html(html: str) -> List[Dict[str, str]]:
    """Extract business data from YellowPages HTML - UPDATED 2025 selectors."""
    businesses = []
    soup = BeautifulSoup(html, 'html.parser')

    # YellowPages 2025 structure uses div.info containers
    info_divs = soup.find_all('div', class_='info')

    for info in info_divs:
        business = {}

        # Name - try multiple selectors
        name_elem = info.find('a', class_='business-name')
        if not name_elem:
            name_elem = info.find('h2', class_='n')

        if name_elem:
            business['name'] = name_elem.get_text(strip=True)
        else:
            continue  # Skip if no name

        # Phone - look in parent container or siblings
        phone_elem = info.find('div', class_='phone')  # Changed from 'phones' to 'phone'
        if not phone_elem:
            # Check parent or next siblings
            parent = info.parent
            if parent:
                phone_elem = parent.find('div', class_='phone')

        if phone_elem:
            phone_text = phone_elem.get_text(strip=True)
            phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', phone_text)
            business['phone_number'] = phone_match.group(0) if phone_match else 'N/A'
        else:
            business['phone_number'] = 'N/A'

        # Address - try multiple selectors
        address_elem = info.find('div', class_='street-address')
        if not address_elem:
            address_elem = info.find('p', class_='adr')
        if not address_elem:
            # Try finding in parent
            parent = info.parent
            if parent:
                address_elem = parent.find('div', class_='street-address')

        business['address'] = address_elem.get_text(strip=True) if address_elem else 'N/A'

        # Website
        website_elem = info.find('a', class_='track-visit-website')
        if not website_elem:
            website_elem = info.find('a', href=re.compile(r'http'))

        business['website'] = website_elem.get('href', 'N/A') if website_elem else 'N/A'

        # Email
        business['email'] = 'N/A'

        # Only add if has contact info
        has_contact = (
            business['phone_number'] != 'N/A' or
            business['address'] != 'N/A' or
            business['website'] != 'N/A'
        )

        if has_contact:
            businesses.append(business)

    return businesses


def scrape_yellowpages_free(zip_code: str, category: str, max_pages: int = 2) -> List[Dict[str, str]]:
    """
    Scrape YellowPages using FREE Cloudflare bypass.

    Args:
        zip_code: ZIP code to search
        category: Business category
        max_pages: Max pages to scrape

    Returns:
        List of business dictionaries
    """
    print(f"[INIT] Starting FREE scraper for {zip_code} - {category}")
    print("[INFO] Creating stealth browser...")

    driver = None
    all_businesses = []
    seen_names = set()

    try:
        driver = create_stealth_driver()
        print("[SUCCESS] Stealth browser created")

        for page in range(1, max_pages + 1):
            url = f"https://www.yellowpages.com/search?search_terms={category.replace(' ', '+')}&geo_location_terms={zip_code}&page={page}"

            print(f"\n[PAGE {page}] Fetching {url}")
            driver.get(url)

            # Wait for Cloudflare + page load
            print("[WAIT] Bypassing Cloudflare...")
            time.sleep(15)  # Give Cloudflare time to resolve (increased from 8)

            # Check if we got past Cloudflare
            page_source = driver.page_source

            if "Just a moment" in page_source or "Cloudflare" in page_source or "Sorry, you have been blocked" in page_source:
                print("[WARNING] Still seeing Cloudflare, waiting longer...")
                time.sleep(10)  # Wait even longer (increased from 5)
                page_source = driver.page_source

                # Final check - if still blocked, abort
                if "Sorry, you have been blocked" in page_source:
                    print("[ERROR] Cloudflare blocked us - scraper cannot continue")
                    print("[ERROR] Try again in a few minutes or use a different network")
                    break

            # Check for no results
            if "No Results Found" in page_source or "0 Results" in page_source:
                print(f"[STOP] No results found on page {page}")
                break

            # Extract businesses
            businesses = extract_businesses_from_html(page_source)

            if not businesses:
                print(f"[WARNING] No businesses extracted from page {page}")
                # Save HTML for debugging
                with open(f'debug_page_{page}.html', 'w', encoding='utf-8') as f:
                    f.write(page_source)
                print(f"[DEBUG] Saved HTML to debug_page_{page}.html")
                break

            # Deduplicate
            unique_count = 0
            for biz in businesses:
                name = biz['name'].strip()
                if name not in seen_names:
                    seen_names.add(name)
                    all_businesses.append(biz)
                    unique_count += 1

            print(f"[SUCCESS] Found {len(businesses)} businesses ({unique_count} unique)")

            # Delay between pages
            if page < max_pages:
                print("[WAIT] Pausing before next page...")
                time.sleep(3)

    except Exception as e:
        print(f"[ERROR] Scraping failed: {e}")

    finally:
        if driver:
            print("\n[CLEANUP] Closing browser...")
            driver.quit()

    print(f"\n[COMPLETE] Total unique businesses: {len(all_businesses)}")
    return all_businesses


if __name__ == "__main__":
    # Quick test
    leads = scrape_yellowpages_free("33527", "Real Estate Agents", max_pages=1)

    if leads:
        print("\n[TEST SUCCESS] Sample lead:")
        print(f"  Name: {leads[0]['name']}")
        print(f"  Phone: {leads[0]['phone_number']}")
        print(f"  Address: {leads[0]['address']}")
    else:
        print("\n[TEST FAILED] No leads found")
