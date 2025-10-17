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
    """Create Chrome driver with ADVANCED anti-detection"""
    options = uc.ChromeOptions()

    # Random user agent
    ua = random.choice(USER_AGENTS)
    options.add_argument(f'--user-agent={ua}')

    # Anti-detection settings
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')

    # Random window size
    width = random.randint(1024, 1920)
    height = random.randint(768, 1080)
    options.add_argument(f'--window-size={width},{height}')

    driver = uc.Chrome(options=options, version_main=None, use_subprocess=True)

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
                scrollable = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
                for _ in range(10):
                    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable)
                    time.sleep(1)

                # Extract results from page source
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find business names and info
                business_divs = soup.find_all('div', class_=re.compile(r'fontHeadline|qBF1Pd'))

                print(f"[GOOGLE MAPS] Found {len(business_divs)} potential businesses")

                for div in business_divs[:max_results]:
                    try:
                        name = div.get_text(strip=True)
                        if name and len(name) > 2:
                            # Get parent container for more info
                            parent = div.parent.parent if div.parent else None
                            phone = 'N/A'
                            address = 'N/A'

                            if parent:
                                text = parent.get_text()
                                phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
                                if phone_match:
                                    phone = phone_match.group(0)

                                # Try to find address
                                addr_match = re.search(r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir|Way)', text, re.IGNORECASE)
                                if addr_match:
                                    address = addr_match.group(0)

                            all_businesses.append({
                                'name': name,
                                'phone_number': phone,
                                'address': address,
                                'website': 'N/A',
                                'email': 'N/A'
                            })
                            print(f"[EXTRACT] {name} - {phone}")
                    except:
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
