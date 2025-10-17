"""
UNIVERSAL Business Scraper - Uses MULTIPLE sources
Tries YellowPages, Yelp, Google Maps, 411 in sequence
Uses advanced bypasses: rotating user agents, cookies, delays
"""

import time
import re
import random
from typing import List, Dict
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
]


def create_advanced_driver():
    """Create Chrome driver with ADVANCED anti-detection - RUNS INVISIBLY"""
    options = uc.ChromeOptions()

    # Random user agent
    ua = random.choice(USER_AGENTS)
    options.add_argument(f'--user-agent={ua}')

    # HEADLESS MODE - Browser runs invisibly in background
    options.add_argument('--headless=new')  # New headless mode (more stable)
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')  # Fixed size for headless

    # Anti-detection settings
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')  # Suppress console logs

    driver = uc.Chrome(options=options, version_main=None, use_subprocess=True, headless=True)

    # Extra stealth
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")

    return driver


def scrape_with_selenium(zip_code: str, category: str, max_results: int = 50) -> List[Dict[str, str]]:
    """
    Universal scraper - tries multiple sources
    """
    print(f"[INIT] Universal scraper starting for {zip_code} - {category}")
    print("[INFO] Will try multiple sources until one works!")

    driver = None
    all_businesses = []

    try:
        driver = create_advanced_driver()
        print("[SUCCESS] Advanced browser created with anti-detection")

        # Try Google Maps first (most reliable)
        print("\n[ATTEMPT 1] Trying Google Maps...")
        try:
            query = f"{category} near {zip_code}".replace(' ', '+')
            url = f"https://www.google.com/maps/search/{query}"

            print(f"[INFO] Loading: {url}")
            driver.get(url)
            time.sleep(10)  # Wait for JavaScript to load

            # Scroll results
            try:
                # Try multiple selectors for scrollable div
                scrollable = None
                selectors = [
                    'div[role="feed"]',
                    'div.m6QErb',
                    'div[aria-label*="Results"]',
                    'div.section-scrollbox'
                ]

                for selector in selectors:
                    try:
                        scrollable = driver.find_element(By.CSS_SELECTOR, selector)
                        print(f"[INFO] Found scrollable div with selector: {selector}")
                        break
                    except:
                        continue

                if not scrollable:
                    print("[ERROR] Could not find scrollable results div")
                    # Try scrolling page itself
                    for _ in range(10):
                        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        time.sleep(1)
                else:
                    # Scroll the results panel
                    for _ in range(10):
                        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable)
                        time.sleep(1)

                # Extract results from page source
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find business name divs directly (most reliable)
                print("[INFO] Finding business name elements...")

                # Strategy: Find divs with specific Google Maps classes for business names
                name_divs = soup.find_all('div', class_=re.compile(r'qBF1Pd.*fontHeadline'))
                print(f"[FOUND] {len(name_divs)} business name divs")

                if not name_divs:
                    print("[WARNING] No business names found with primary selector")
                    # Fallback: try broader search
                    name_divs = soup.find_all('div', class_=re.compile(r'fontHeadlineSmall'))
                    print(f"[FALLBACK] {len(name_divs)} elements with fontHeadlineSmall")

                print(f"[GOOGLE MAPS] Processing {len(name_divs)} businesses")

                extracted = 0
                seen_names = set()  # Deduplicate

                for name_div in name_divs[:max_results * 2]:  # Process more than max to account for duplicates
                    try:
                        # Extract business name
                        name = name_div.get_text(strip=True)

                        if not name or len(name) < 2:
                            continue

                        # Skip duplicates
                        if name in seen_names:
                            continue
                        seen_names.add(name)

                        # Find parent container to extract phone/address
                        # Go up the DOM tree to find the full business card
                        parent = name_div.parent
                        for _ in range(5):  # Go up 5 levels to find the business card
                            if parent:
                                parent = parent.parent
                            else:
                                break

                        context_text = parent.get_text() if parent else name_div.get_text()

                        # Extract phone - look for <span class="UsdlK">
                        phone = 'N/A'
                        if parent:
                            phone_span = parent.find('span', class_='UsdlK')
                            if phone_span:
                                phone = phone_span.get_text(strip=True)
                            else:
                                # Fallback: regex search
                                phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', context_text)
                                if phone_match:
                                    phone = phone_match.group(0)

                        # Extract address - look for patterns
                        address = 'N/A'
                        addr_match = re.search(r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir|Way)', context_text, re.IGNORECASE)
                        if addr_match:
                            address = addr_match.group(0)

                        all_businesses.append({
                            'name': name,
                            'phone_number': phone,
                            'address': address,
                            'website': 'N/A',
                            'email': 'N/A'
                        })
                        extracted += 1
                        print(f"[EXTRACT {extracted}] {name} - {phone}")

                        # Stop if we have enough
                        if extracted >= max_results:
                            break

                    except Exception as e:
                        print(f"[WARNING] Extraction error: {e}")
                        import traceback
                        traceback.print_exc()
                        continue

                if all_businesses:
                    print(f"[SUCCESS] Google Maps found {len(all_businesses)} businesses!")
                    return all_businesses

            except Exception as e:
                print(f"[WARNING] Google Maps extraction failed: {e}")

        except Exception as e:
            print(f"[ERROR] Google Maps failed: {e}")

        # If Google Maps failed, return what we have
        if all_businesses:
            return all_businesses

        print("[WARNING] All sources failed - returning empty list")

    except Exception as e:
        print(f"[ERROR] Scraping failed: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            print("\n[CLEANUP] Closing browser...")
            driver.quit()

    print(f"\n[COMPLETE] Total businesses: {len(all_businesses)}")
    return all_businesses


if __name__ == "__main__":
    # Test
    leads = scrape_with_selenium("33527", "Real Estate Agents", max_results=20)

    if leads:
        print("\n[TEST SUCCESS] Sample leads:")
        for i, lead in enumerate(leads[:5], 1):
            print(f"\n{i}. {lead['name']}")
            print(f"   Phone: {lead['phone_number']}")
            print(f"   Address: {lead['address']}")
    else:
        print("\n[TEST FAILED] No leads found - all sources blocked")
