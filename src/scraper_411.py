"""
411.com Scraper - NO Cloudflare, NO blocks, ACTUALLY WORKS!
Simple HTTP requests - NO Selenium needed!
"""

import time
import re
import requests
from typing import List, Dict
from bs4 import BeautifulSoup


def scrape_411(zip_code: str, category: str, max_pages: int = 2) -> List[Dict[str, str]]:
    """
    Scrape 411.com for business leads - SIMPLE and FREE!
    NO Cloudflare, NO JavaScript required!

    Args:
        zip_code: ZIP code to search
        category: Business category
        max_pages: Max pages to scrape

    Returns:
        List of business dictionaries
    """
    print(f"[INIT] Starting 411.com scraper for {zip_code} - {category}")
    print("[INFO] 411.com = NO Cloudflare, SIMPLE HTML!")

    all_businesses = []
    seen_names = set()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    session = requests.Session()

    try:
        for page in range(1, max_pages + 1):
            # 411.com URL format
            search_term = category.replace(' ', '-').lower()
            url = f"https://www.411.com/{zip_code}/{search_term}?page={page}"

            print(f"\n[PAGE {page}] Fetching {url}")

            try:
                response = session.get(url, headers=headers, timeout=15)

                if response.status_code != 200:
                    print(f"[ERROR] HTTP {response.status_code}")
                    # Try alternative URL format
                    url = f"https://411.com/search?category={category}&location={zip_code}&page={page}"
                    print(f"[RETRY] Trying alternative URL: {url}")
                    response = session.get(url, headers=headers, timeout=15)

                if response.status_code != 200:
                    print(f"[ERROR] HTTP {response.status_code} - skipping page")
                    continue

                print(f"[SUCCESS] Got HTML ({len(response.text)} bytes)")

                soup = BeautifulSoup(response.text, 'html.parser')

                # Find business listings - 411.com uses various structures
                business_containers = soup.find_all('div', class_=re.compile(r'business|listing|result'))

                if not business_containers:
                    # Try finding by specific patterns
                    business_containers = soup.find_all('article')

                if not business_containers:
                    # Last resort - find any divs with phone numbers
                    all_divs = soup.find_all('div')
                    business_containers = [d for d in all_divs if d.find(text=re.compile(r'\(\d{3}\)\s?\d{3}-\d{4}'))]

                if not business_containers:
                    print(f"[WARNING] No businesses found on page {page}")
                    # Save HTML for debugging
                    with open(f'debug_411_page_{page}.html', 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"[DEBUG] Saved HTML to debug_411_page_{page}.html")
                    continue

                print(f"[INFO] Found {len(business_containers)} business containers")

                for container in business_containers:
                    try:
                        business = {}

                        # Name - try multiple selectors
                        name_elem = container.find('h2')
                        if not name_elem:
                            name_elem = container.find('h3')
                        if not name_elem:
                            name_elem = container.find('a', class_=re.compile(r'name|title'))
                        if not name_elem:
                            name_elem = container.find('span', class_=re.compile(r'name|title'))

                        if name_elem:
                            business['name'] = name_elem.get_text(strip=True)
                        else:
                            continue  # Skip if no name

                        # Skip duplicates
                        if business['name'] in seen_names:
                            continue
                        seen_names.add(business['name'])

                        # Phone - search for pattern
                        phone_text = container.get_text()
                        phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', phone_text)
                        business['phone_number'] = phone_match.group(0) if phone_match else 'N/A'

                        # Address - look for address elements
                        address_elem = container.find('address')
                        if not address_elem:
                            address_elem = container.find('span', class_=re.compile(r'address|location'))
                        if not address_elem:
                            address_elem = container.find('div', class_=re.compile(r'address|location'))

                        if address_elem:
                            business['address'] = address_elem.get_text(strip=True)
                        else:
                            business['address'] = 'N/A'

                        # Website
                        website_elem = container.find('a', href=re.compile(r'https?://(?!www\.411\.com|411\.com)'))
                        business['website'] = website_elem.get('href', 'N/A') if website_elem else 'N/A'

                        # Email
                        business['email'] = 'N/A'

                        # Only add if we have name and phone or address
                        if business['name'] and (business['phone_number'] != 'N/A' or business['address'] != 'N/A'):
                            all_businesses.append(business)
                            print(f"[EXTRACT] {business['name']} - {business['phone_number']}")

                    except Exception as e:
                        print(f"[WARNING] Failed to extract business: {e}")
                        continue

                print(f"[PAGE {page}] Total extracted so far: {len(all_businesses)}")

                # Delay between pages
                if page < max_pages:
                    time.sleep(2)

            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Request failed: {e}")
                continue

    except Exception as e:
        print(f"[ERROR] Scraping failed: {e}")
        import traceback
        traceback.print_exc()

    print(f"\n[COMPLETE] Total unique businesses: {len(all_businesses)}")
    return all_businesses


if __name__ == "__main__":
    # Quick test
    leads = scrape_411("33527", "Real Estate Agents", max_pages=2)

    if leads:
        print("\n[TEST SUCCESS] Sample leads:")
        for i, lead in enumerate(leads[:5], 1):
            print(f"\n{i}. {lead['name']}")
            print(f"   Phone: {lead['phone_number']}")
            print(f"   Address: {lead['address']}")
    else:
        print("\n[TEST FAILED] No leads found")
