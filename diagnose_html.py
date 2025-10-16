"""Diagnose YellowPages HTML structure"""
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from bs4 import BeautifulSoup

async def diagnose():
    url = "https://www.yellowpages.com/search?search_terms=Real+Estate+Agents&geo_location_terms=33527&page=1"

    config = BrowserConfig(
        browser_type="chromium",
        headless=True,
        verbose=False
    )

    async with AsyncWebCrawler(config=config) as crawler:
        result = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
        )

        if result.success and result.html:
            soup = BeautifulSoup(result.html, 'html.parser')

            # Save HTML to file for inspection
            with open('yellowpages_sample.html', 'w', encoding='utf-8') as f:
                f.write(result.html)

            print("[SUCCESS] HTML saved to yellowpages_sample.html")
            print(f"[INFO] HTML length: {len(result.html)} characters")

            # Try different selectors
            print("\n[TESTING SELECTORS]")

            selectors = [
                ('div.result', 'result class'),
                ('div.search-results', 'search-results class'),
                ('div.organic', 'organic class'),
                ('div[class*="result"]', 'result wildcard'),
                ('a.business-name', 'business-name links'),
            ]

            for selector, desc in selectors:
                elements = soup.select(selector)
                print(f"  {selector:<30} -> {len(elements)} elements ({desc})")

            # Show first business name if found
            name_elem = soup.find('a', class_='business-name')
            if name_elem:
                print(f"\n[FOUND] First business: {name_elem.get_text(strip=True)}")
            else:
                print("\n[NOT FOUND] No business-name elements")

                # Try to find ANY links that might be businesses
                all_links = soup.find_all('a', href=True)
                print(f"\n[INFO] Total links found: {len(all_links)}")
                if len(all_links) > 0:
                    print(f"[INFO] First 5 link texts:")
                    for i, link in enumerate(all_links[:5]):
                        text = link.get_text(strip=True)[:50]
                        print(f"  {i+1}. {text}")
        else:
            print(f"[ERROR] Failed to fetch: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(diagnose())
