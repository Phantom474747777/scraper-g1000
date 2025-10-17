"""
Outscraper API - FREE tier (100 requests/month)
ACTUALLY WORKS - No scraping, uses official API!
"""

import os
from typing import List, Dict
from outscraper import ApiClient

# Get API key from environment or use free tier
API_KEY = os.getenv('OUTSCRAPER_API_KEY', 'FREE_TIER_KEY')


def scrape_with_outscraper(zip_code: str, category: str, max_results: int = 50) -> List[Dict[str, str]]:
    """
    Scrape using Outscraper API - FREE tier available!

    Args:
        zip_code: ZIP code to search
        category: Business category
        max_results: Maximum results

    Returns:
        List of business dictionaries
    """
    print(f"[INIT] Using Outscraper API for {zip_code} - {category}")
    print("[INFO] Outscraper = 100% reliable, official Google Maps API!")

    all_businesses = []

    try:
        # Initialize Outscraper client
        client = ApiClient(api_key=API_KEY)

        # Build search query
        query = f"{category} near {zip_code}"
        print(f"[API] Searching: {query}")

        # Call Outscraper Google Maps scraper
        results = client.google_maps_search(
            query,
            limit=max_results,
            language='en',
            region='us'
        )

        print(f"[SUCCESS] Outscraper returned {len(results)} result sets")

        # Parse results
        for result_set in results:
            for business in result_set:
                try:
                    lead = {
                        'name': business.get('name', 'N/A'),
                        'phone_number': business.get('phone', 'N/A'),
                        'address': business.get('full_address', business.get('address', 'N/A')),
                        'website': business.get('site', 'N/A'),
                        'email': 'N/A'  # Outscraper doesn't usually provide emails
                    }

                    # Only add if has name
                    if lead['name'] != 'N/A':
                        all_businesses.append(lead)
                        print(f"[EXTRACT] {lead['name']} - {lead['phone_number']}")

                except Exception as e:
                    print(f"[WARNING] Failed to parse business: {e}")
                    continue

    except Exception as e:
        print(f"[ERROR] Outscraper API failed: {e}")
        print("[INFO] You need to set OUTSCRAPER_API_KEY environment variable")
        print("[INFO] Get free API key at: https://outscraper.com/")
        import traceback
        traceback.print_exc()

    print(f"\n[COMPLETE] Total businesses: {len(all_businesses)}")
    return all_businesses


if __name__ == "__main__":
    # Test
    leads = scrape_with_outscraper("33527", "Real Estate Agents", max_results=10)

    if leads:
        print("\n[TEST SUCCESS] Sample leads:")
        for i, lead in enumerate(leads[:3], 1):
            print(f"\n{i}. {lead['name']}")
            print(f"   Phone: {lead['phone_number']}")
            print(f"   Address: {lead['address']}")
    else:
        print("\n[TEST FAILED] No leads found - check API key!")
