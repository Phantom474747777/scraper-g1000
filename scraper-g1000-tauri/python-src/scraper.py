import json
import re
import asyncio
from pydantic import BaseModel
from typing import List, Set, Tuple, Optional
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)
from bs4 import BeautifulSoup
from src.utils import is_duplicated
import os


def get_browser_config() -> BrowserConfig:
    """
    Returns the browser configuration for the crawler.

    Returns:
        BrowserConfig: The configuration settings for the browser.
    """
    # https://docs.crawl4ai.com/core/browser-crawler-config/
    return BrowserConfig(
        browser_type="chromium",  # Type of browser to simulate
        headless=True,  # Whether to run in headless mode (no GUI)
        verbose=False,  # Reduce verbosity to avoid clutter
    )


def get_llm_strategy(llm_instructions: str, output_format: BaseModel, llm_model: str = None, api_token: str = None) -> Optional[LLMExtractionStrategy]:
    """
    Returns the configuration for the language model extraction strategy.

    Args:
        llm_instructions: Instructions for the LLM
        output_format: Pydantic model for data extraction
        llm_model: LLM model to use (defaults to Gemini)
        api_token: API token (defaults to GEMINI_API_KEY from env)

    Returns:
        LLMExtractionStrategy or None: The settings for how to extract data using LLM, or None if no API key.
    """
    # Default to environment variables if not provided
    if llm_model is None:
        llm_model = os.getenv("LLM_MODEL", "gemini/gemini-2.0-flash-exp")
    if api_token is None:
        api_token = os.getenv("GEMINI_API_KEY")

    # If no API token, return None (will use fallback extraction)
    if not api_token:
        print("⚠️  No LLM API key found - using fallback extraction")
        return None

    # https://docs.crawl4ai.com/api/strategies/#llmextractionstrategy
    try:
        return LLMExtractionStrategy(
            provider=llm_model,  # Name of the LLM provider
            api_token=api_token,  # API token for authentication
            schema=output_format.model_json_schema(),  # JSON schema of the data model
            extraction_type="schema",  # Type of extraction to perform
            instruction=llm_instructions,  # Instructions for the LLM
            input_format="markdown",  # Format of the input content
            verbose=False,  # Reduce verbosity
        )
    except Exception as e:
        print(f"⚠️  Error creating LLM strategy: {e}")
        return None


def extract_business_from_html(html_content: str) -> List[dict]:
    """
    Fallback extraction using BeautifulSoup when LLM is unavailable or rate-limited.
    Extracts business information directly from YellowPages HTML.

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
        if name_elem:
            business['name'] = name_elem.get_text(strip=True)
        else:
            # Try alternative selectors
            name_elem = result.find('h2')
            if name_elem:
                business['name'] = name_elem.get_text(strip=True)
        
        # Extract phone number
        phone_elem = result.find('div', class_='phones')
        if phone_elem:
            phone_text = phone_elem.get_text(strip=True)
            # Extract just the phone number using regex
            phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', phone_text)
            if phone_match:
                business['phone_number'] = phone_match.group(0)
        
        # Extract address
        address_elem = result.find('div', class_='street-address')
        if address_elem:
            business['address'] = address_elem.get_text(strip=True)
        else:
            # Try alternative selector
            address_elem = result.find('p', class_='adr')
            if address_elem:
                business['address'] = address_elem.get_text(strip=True)
        
        # Extract website
        website_elem = result.find('a', class_='track-visit-website')
        if website_elem:
            business['website'] = website_elem.get('href', 'N/A')
        else:
            business['website'] = 'N/A'
        
        # Email is rarely on listing pages
        business['email'] = 'N/A'
        
        # Only add if we have at least a name
        if business.get('name'):
            businesses.append(business)
    
    return businesses


def validate_business_data(business: dict) -> bool:
    """
    Validate that a business entry has essential data.

    Args:
        business: Business dictionary

    Returns:
        bool: True if valid, False otherwise
    """
    # Must have name and at least one contact method
    has_name = bool(business.get('name', '').strip())
    has_contact = bool(
        business.get('phone_number', '').strip() or 
        business.get('address', '').strip() or
        business.get('website', '').strip()
    )
    
    return has_name and has_contact


async def check_no_results_with_retry(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
    max_retries: int = 3
) -> bool:
    """
    Checks if the "No Results Found" message is present on the page with retry logic.

    Args:
        crawler (AsyncWebCrawler): The web crawler instance.
        url (str): The URL to check.
        session_id (str): The session identifier.
        max_retries (int): Maximum number of retry attempts.

    Returns:
        bool: True if "No Results Found" message is found, False otherwise.
    """
    for attempt in range(max_retries):
        try:
            # Fetch the page without any CSS selector or extraction strategy
            result = await crawler.arun(
                url=url,
                config=CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    session_id=session_id,
                ),
            )

            if result.success:
                if "No Results Found" in result.cleaned_html:
                    return True
                return False
            else:
                error_msg = str(result.error_message).lower()
                if any(network_error in error_msg for network_error in ['net::err_network_changed', 'timeout', 'connection', 'network']):
                    if attempt < max_retries - 1:
                        print(f"   ⚠️ Network issue, retrying page check (attempt {attempt + 1}/{max_retries})...")
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    else:
                        print(f"   ❌ Network error after {max_retries} attempts: {result.error_message}")
                        return False
                else:
                    print(f"   ⚠️ Error checking for results: {result.error_message}")
                    return False
        except Exception as e:
            error_msg = str(e).lower()
            if any(network_error in error_msg for network_error in ['timeout', 'connection', 'network']):
                if attempt < max_retries - 1:
                    print(f"   ⚠️ Network issue, retrying page check (attempt {attempt + 1}/{max_retries})...")
                    await asyncio.sleep(2 ** attempt)
                    continue
                else:
                    print(f"   ❌ Network error after {max_retries} attempts: {e}")
                    return False
            else:
                print(f"   ⚠️ Exception checking results: {e}")
                return False

    return False


async def fetch_and_process_page(
    crawler: AsyncWebCrawler,
    page_number: int,
    base_url: str,
    css_selector: str,
    llm_strategy: Optional[LLMExtractionStrategy],
    session_id: str,
    seen_names: Set[str],
) -> Tuple[List[dict], bool]:
    """
    Fetches and processes a single page from yellowpages with network resilience.
    Uses LLM if available, falls back to BeautifulSoup extraction.

    Args:
        crawler (AsyncWebCrawler): The web crawler instance.
        page_number (int): The page number to fetch.
        base_url (str): The base URL of the website.
        css_selector (str): The CSS selector to target the content.
        llm_strategy (LLMExtractionStrategy or None): The LLM extraction strategy.
        session_id (str): The session identifier.
        seen_names (Set[str]): Set of business names that have already been seen.

    Returns:
        Tuple[List[dict], bool]:
            - List[dict]: A list of processed businesses from the page.
            - bool: A flag indicating if the "No Results Found" message was encountered.
    """
    url = base_url.format(page_number=page_number)
    print(f"   📄 Loading page {page_number}...")

    # Check if "No Results Found" message is present with retry
    try:
        no_results = await check_no_results_with_retry(crawler, url, session_id)
        if no_results:
            return [], True  # No more results, signal to stop crawling
    except Exception as e:
        print(f"   ⚠️  Error checking results: {e}")

    all_businesses = []
    use_fallback = False

    # Try LLM extraction first (if available) with retry logic
    if llm_strategy:
        for llm_attempt in range(3):  # Max 3 attempts for LLM
            try:
                result = await crawler.arun(
                    url=url,
                    config=CrawlerRunConfig(
                        cache_mode=CacheMode.BYPASS,
                        extraction_strategy=llm_strategy,
                        css_selector=css_selector,
                        session_id=session_id,
                    ),
                )

                if result.success and result.extracted_content:
                    # Parse extracted content
                    extracted_data = json.loads(result.extracted_content)
                    
                    if extracted_data and isinstance(extracted_data, list):
                        for business in extracted_data:
                            # Use .get() to safely access fields
                            if business.get("error") is False:
                                business.pop("error", None)
                            
                            # Validate business data
                            if not validate_business_data(business):
                                print(f"   [WARN] Missing essential data - Skipped entry")
                                continue
                            
                            # Check for duplicates
                            name = business.get('name', '')
                            if is_duplicated(name, seen_names):
                                print(f"   [SKIP] Duplicate: '{name}'")
                                continue
                            
                            seen_names.add(name)
                            all_businesses.append(business)
                        break  # Success, exit retry loop
                    else:
                        # LLM returned empty or invalid data, use fallback
                        use_fallback = True
                        break
                else:
                    # Check for specific error types
                    error_msg = str(result.error_message).lower()
                    if 'rate limit' in error_msg or '429' in error_msg or 'quota' in error_msg:
                        print(f"   ⚠️ API quota or timeout — continuing with direct scrape.")
                        use_fallback = True
                        break
                    elif any(network_error in error_msg for network_error in ['net::err_network_changed', 'timeout', 'connection', 'network']):
                        if llm_attempt < 2:  # Retry network errors
                            print(f"   ⚠️ Network issue, retrying LLM extraction (attempt {llm_attempt + 1}/3)...")
                            await asyncio.sleep(2 ** llm_attempt)
                            continue
                        else:
                            print(f"   ⚠️ Network error after 3 attempts - using fallback extraction")
                            use_fallback = True
                            break
                    else:
                        print(f"   ⚠️  LLM extraction failed: {result.error_message}")
                        use_fallback = True
                        break

            except Exception as e:
                error_msg = str(e).lower()
                if 'rate limit' in error_msg or '429' in error_msg or 'quota' in error_msg:
                    print(f"   ⚠️ API quota or timeout — continuing with direct scrape.")
                    use_fallback = True
                    break
                elif any(network_error in error_msg for network_error in ['timeout', 'connection', 'network']):
                    if llm_attempt < 2:
                        print(f"   ⚠️ Network issue, retrying LLM extraction (attempt {llm_attempt + 1}/3)...")
                        await asyncio.sleep(2 ** llm_attempt)
                        continue
                    else:
                        print(f"   ⚠️ Network error after 3 attempts - using fallback extraction")
                        use_fallback = True
                        break
                else:
                    print(f"   ⚠️  LLM exception: {e}")
                    use_fallback = True
                    break
    else:
        # No LLM strategy provided, use fallback from start
        use_fallback = True

    # Fallback: Extract using BeautifulSoup with retry logic
    if use_fallback or not all_businesses:
        for fallback_attempt in range(3):  # Max 3 attempts for fallback
            try:
                print(f"   🔄 Using fallback extraction (BeautifulSoup)...")
                
                # Fetch raw HTML
                result = await crawler.arun(
                    url=url,
                    config=CrawlerRunConfig(
                        cache_mode=CacheMode.BYPASS,
                        session_id=session_id,
                    ),
                )
                
                if result.success and result.html:
                    fallback_businesses = extract_business_from_html(result.html)
                    
                    for business in fallback_businesses:
                        # Validate and check duplicates
                        if not validate_business_data(business):
                            continue
                        
                        name = business.get('name', '')
                        if is_duplicated(name, seen_names):
                            continue
                        
                        seen_names.add(name)
                        all_businesses.append(business)
                    break  # Success, exit retry loop
                else:
                    error_msg = str(result.error_message).lower()
                    if any(network_error in error_msg for network_error in ['net::err_network_changed', 'timeout', 'connection', 'network']):
                        if fallback_attempt < 2:
                            print(f"   ⚠️ Network issue, retrying page {page_number} (attempt {fallback_attempt + 1}/3)...")
                            await asyncio.sleep(2 ** fallback_attempt)
                            continue
                        else:
                            print(f"   ❌ Network error after 3 attempts: {result.error_message}")
                            return [], False
                    else:
                        print(f"   ❌ Failed to fetch HTML: {result.error_message}")
                        return [], False

            except Exception as e:
                error_msg = str(e).lower()
                if any(network_error in error_msg for network_error in ['timeout', 'connection', 'network']):
                    if fallback_attempt < 2:
                        print(f"   ⚠️ Network issue, retrying page {page_number} (attempt {fallback_attempt + 1}/3)...")
                        await asyncio.sleep(2 ** fallback_attempt)
                        continue
                    else:
                        print(f"   ❌ Network error after 3 attempts: {e}")
                        return [], False
                else:
                    print(f"   ❌ Fallback extraction error: {e}")
                    return [], False

    if not all_businesses:
        print(f"   ⚠️  No businesses found on page {page_number}")
        return [], False

    print(f"   ✓ Extracted {len(all_businesses)} businesses from page {page_number}")
    return all_businesses, False  # Continue crawling
