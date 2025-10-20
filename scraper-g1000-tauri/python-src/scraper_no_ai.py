"""
Pure BeautifulSoup scraper - NO AI/LLM required
Lightweight, fast, no API keys needed
"""

import asyncio
import re
from typing import List, Set, Tuple
from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
from bs4 import BeautifulSoup


def get_browser_config() -> BrowserConfig:
    """Returns browser configuration for the crawler."""
    return BrowserConfig(
        browser_type="chromium",
        headless=True,
        verbose=False,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        extra_args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-sandbox"
        ]
    )


def extract_business_from_html(html_content: str) -> List[dict]:
    """
    Extract business information from YellowPages HTML using BeautifulSoup.

    Args:
        html_content: Raw HTML content

    Returns:
        List of business dictionaries
    """
    businesses = []
    soup = BeautifulSoup(html_content, 'html.parser')

    # YellowPages uses .result class for each listing
    results = soup.find_all('div', class_='result')

    for result in results:
        business = {}

        # Extract business name
        name_elem = result.find('a', class_='business-name')
        if not name_elem:
            name_elem = result.find('h2', class_='n')
            if not name_elem:
                name_elem = result.find('span', {'itemprop': 'name'})

        if name_elem:
            business['name'] = name_elem.get_text(strip=True)
        else:
            continue  # Skip if no name found

        # Extract phone number
        phone_elem = result.find('div', class_='phones')
        if not phone_elem:
            phone_elem = result.find('div', class_='phone')

        if phone_elem:
            phone_text = phone_elem.get_text(strip=True)
            phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', phone_text)
            if phone_match:
                business['phone_number'] = phone_match.group(0)
            else:
                business['phone_number'] = 'N/A'
        else:
            business['phone_number'] = 'N/A'

        # Extract address
        address_elem = result.find('div', class_='street-address')
        if not address_elem:
            address_elem = result.find('span', {'itemprop': 'streetAddress'})
        if not address_elem:
            address_elem = result.find('p', class_='adr')

        if address_elem:
            business['address'] = address_elem.get_text(strip=True)
        else:
            business['address'] = 'N/A'

        # Extract website
        website_elem = result.find('a', class_='track-visit-website')
        if not website_elem:
            website_elem = result.find('a', {'track': 'website'})

        if website_elem:
            business['website'] = website_elem.get('href', 'N/A')
        else:
            business['website'] = 'N/A'

        # Extract email using regex from page text
        email = 'N/A'
        result_text = result.get_text()
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', result_text)
        if email_match:
            email = email_match.group(0)
        business['email'] = email

        # Only add if we have name and at least one contact method
        has_contact = (
            business.get('phone_number', 'N/A') != 'N/A' or
            business.get('address', 'N/A') != 'N/A' or
            business.get('website', 'N/A') != 'N/A'
        )

        if business.get('name') and has_contact:
            businesses.append(business)

    return businesses


async def check_no_results(crawler: AsyncWebCrawler, url: str, session_id: str) -> bool:
    """
    Check if the "No Results Found" message is present on the page.

    Args:
        crawler: The web crawler instance
        url: URL to check
        session_id: Session identifier

    Returns:
        True if no results found, False otherwise
    """
    try:
        result = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                session_id=session_id,
                page_timeout=60000,
                delay_before_return_html=5.0,
            ),
        )

        if result.success and result.cleaned_html:
            return "No Results Found" in result.cleaned_html
        return False

    except Exception as e:
        print(f"   [WARNING] Error checking results: {e}")
        return False


async def fetch_page_with_retry(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
    max_retries: int = 3
) -> Tuple[str, bool]:
    """
    Fetch page HTML with retry logic for network errors.

    Args:
        crawler: Web crawler instance
        url: URL to fetch
        session_id: Session identifier
        max_retries: Maximum retry attempts

    Returns:
        Tuple of (html_content, success)
    """
    for attempt in range(max_retries):
        try:
            result = await crawler.arun(
                url=url,
                config=CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    session_id=session_id,
                    page_timeout=60000,  # 60 seconds for Cloudflare
                    delay_before_return_html=5.0,  # Wait 5s for JavaScript to load
                ),
            )

            if result.success and result.html:
                return result.html, True

            # Check for network errors
            error_msg = str(result.error_message).lower() if result.error_message else ""
            if any(err in error_msg for err in ['timeout', 'connection', 'network']):
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"   [WARNING] Network issue, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    continue

            print(f"   [ERROR] Failed to fetch: {result.error_message}")
            return "", False

        except Exception as e:
            error_msg = str(e).lower()
            if any(err in error_msg for err in ['timeout', 'connection', 'network']):
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"   [WARNING] Network issue, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    continue

            print(f"   [ERROR] Exception: {e}")
            return "", False

    print(f"   [ERROR] Failed after {max_retries} attempts")
    return "", False


async def scrape_yellowpages_page(
    crawler: AsyncWebCrawler,
    page_number: int,
    base_url: str,
    session_id: str,
    seen_names: Set[str],
) -> Tuple[List[dict], bool]:
    """
    Scrape a single YellowPages page.

    Args:
        crawler: Web crawler instance
        page_number: Page number to scrape
        base_url: Base URL template (with {page_number} placeholder)
        session_id: Session identifier
        seen_names: Set of already seen business names (for deduplication)

    Returns:
        Tuple of (businesses_list, no_results_found)
    """
    url = base_url.format(page_number=page_number)
    print(f"   [Page {page_number}] Scraping...")

    # Check if no results
    if await check_no_results(crawler, url, session_id):
        print(f"   [Page {page_number}] No results found")
        return [], True

    # Fetch page HTML with retries
    html, success = await fetch_page_with_retry(crawler, url, session_id)
    if not success or not html:
        return [], False

    # Extract businesses
    businesses = extract_business_from_html(html)

    # Deduplicate
    unique_businesses = []
    for business in businesses:
        name = business.get('name', '').strip()
        if name and name not in seen_names:
            seen_names.add(name)
            unique_businesses.append(business)

    if unique_businesses:
        print(f"   [SUCCESS] Found {len(unique_businesses)} unique businesses")
    else:
        print(f"   [WARNING] No businesses extracted from page {page_number}")

    return unique_businesses, False


async def scrape_yellowpages(
    zip_code: str,
    category: str,
    max_pages: int = 2
) -> List[dict]:
    """
    Scrape YellowPages for a specific ZIP code and category.

    Args:
        zip_code: ZIP code to search
        category: Business category to search
        max_pages: Maximum pages to scrape

    Returns:
        List of business dictionaries
    """
    base_url = f"https://www.yellowpages.com/search?search_terms={category.replace(' ', '+')}&geo_location_terms={zip_code}&page={{page_number}}"
    session_id = f"scraper_{zip_code}_{category}".replace(" ", "_")

    browser_config = get_browser_config()
    all_businesses = []
    seen_names = set()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for page_number in range(1, max_pages + 1):
            businesses, no_results = await scrape_yellowpages_page(
                crawler,
                page_number,
                base_url,
                session_id,
                seen_names
            )

            if no_results:
                print(f"   [STOP] No more results")
                break

            if not businesses:
                print(f"   [SKIP] Moving to next page")
                continue

            all_businesses.extend(businesses)

            # Respectful delay between pages
            if page_number < max_pages:
                await asyncio.sleep(2)

    return all_businesses
