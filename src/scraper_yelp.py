"""
Yelp Scraper - SIMPLE, FREE, NO Cloudflare!
Uses requests + BeautifulSoup - NO Selenium needed!
"""

import time
import re
import requests
from typing import List, Dict
from bs4 import BeautifulSoup


def scrape_yelp(zip_code: str, category: str, max_results: int = 50) -> List[Dict[str, str]]:
    """
    Scrape Yelp for business leads - SIMPLE and FREE!

    Args:
        zip_code: ZIP code to search
        category: Business category
        max_results: Maximum results to scrape

    Returns:
        List of business dictionaries
    """
    print(f"[INIT] Starting Yelp scraper for {zip_code} - {category}")
    print("[INFO] Yelp = NO Cloudflare, SIMPLE HTTP requests!")

    all_businesses = []
    seen_names = set()

    # Calculate pages needed (10 results per page)
    max_pages = (max_results // 10) + 1

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.yelp.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        for page in range(max_pages):
            start = page * 10
            # Yelp URL format: /search?find_desc=category&find_loc=zipcode&start=0
            search_term = category.replace(' ', '+')
            url = f"https://www.yelp.com/search?find_desc={search_term}&find_loc={zip_code}&start={start}"

            print(f"\n[PAGE {page+1}] Fetching {url}")

            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code != 200:
                print(f"[ERROR] HTTP {response.status_code} - skipping page {page+1}")
                continue

            print(f"[SUCCESS] Got HTML ({len(response.text)} bytes)")

            soup = BeautifulSoup(response.text, 'html.parser')

            # Yelp uses div with data-testid or class patterns
            # Try multiple selectors
            business_containers = soup.find_all('div', attrs={'data-testid': re.compile(r'serp-ia-card')})

            if not business_containers:
                # Alternative: look for links with business names
                business_containers = soup.find_all('a', class_=re.compile(r'business-name'))

            if not business_containers:
                print(f"[WARNING] No businesses found on page {page+1}")
                continue

            print(f"[INFO] Found {len(business_containers)} business containers")

            for container in business_containers:
                try:
                    business = {}

                    # Name - try multiple patterns
                    name_elem = container.find('a', class_=re.compile(r'business-name'))
                    if not name_elem:
                        name_elem = container.find('h3')
                    if not name_elem:
                        name_elem = container.find('h2')

                    if name_elem:
                        business['name'] = name_elem.get_text(strip=True)
                    else:
                        continue  # Skip if no name

                    # Skip duplicates
                    if business['name'] in seen_names:
                        continue
                    seen_names.add(business['name'])

                    # Phone - Yelp sometimes shows phones in text
                    phone_elem = container.find(text=re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'))
                    if phone_elem:
                        phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', phone_elem)
                        business['phone_number'] = phone_match.group(0) if phone_match else 'N/A'
                    else:
                        business['phone_number'] = 'N/A'

                    # Address - look for address elements
                    address_elem = container.find('address')
                    if not address_elem:
                        address_elem = container.find('p', class_=re.compile(r'address'))

                    if address_elem:
                        business['address'] = address_elem.get_text(strip=True)
                    else:
                        business['address'] = 'N/A'

                    # Website - usually not directly available on search results
                    website_elem = container.find('a', href=re.compile(r'https?://(?!www\.yelp\.com)'))
                    business['website'] = website_elem.get('href', 'N/A') if website_elem else 'N/A'

                    # Email
                    business['email'] = 'N/A'

                    # Only add if we have name and at least address
                    if business['name'] and business['address'] != 'N/A':
                        all_businesses.append(business)
                        print(f"[EXTRACT] {business['name']}")

                except Exception as e:
                    print(f"[WARNING] Failed to extract business: {e}")
                    continue

            print(f"[PAGE {page+1}] Extracted {len(all_businesses) - len([b for b in all_businesses if b not in all_businesses[-len(business_containers):]])} businesses")

            # Stop if we have enough
            if len(all_businesses) >= max_results:
                break

            # Delay between pages
            if page < max_pages - 1:
                print("[WAIT] Pausing before next page...")
                time.sleep(2)

    except Exception as e:
        print(f"[ERROR] Scraping failed: {e}")
        import traceback
        traceback.print_exc()

    print(f"\n[COMPLETE] Total unique businesses: {len(all_businesses)}")
    return all_businesses


if __name__ == "__main__":
    # Quick test
    leads = scrape_yelp("33527", "Real Estate Agents", max_results=20)

    if leads:
        print("\n[TEST SUCCESS] Sample leads:")
        for i, lead in enumerate(leads[:3], 1):
            print(f"\n{i}. {lead['name']}")
            print(f"   Phone: {lead['phone_number']}")
            print(f"   Address: {lead['address']}")
    else:
        print("\n[TEST FAILED] No leads found")
