"""Find where phone numbers are in the HTML"""
from bs4 import BeautifulSoup
import re

with open('debug_page_1.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find all text that looks like phone numbers
phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')

# Search in all elements
all_text = soup.get_text()
phones_in_text = phone_pattern.findall(all_text)

print(f"Found {len(phones_in_text)} phone-like strings in page text")

# Find the exact HTML elements containing phones
phone_containers = []
for elem in soup.find_all(string=phone_pattern):
    parent = elem.parent
    if parent:
        tag = parent.name
        classes = parent.get('class', [])
        phone_containers.append((tag, classes, elem.strip()[:30]))

print("\nPhone number locations (first 10):")
for i, (tag, classes, text) in enumerate(phone_containers[:10]):
    print(f"  {i+1}. <{tag} class=\"{' '.join(classes) if classes else 'none'}\">{text}...")

# Try common selectors
selectors_to_try = [
    'div.phones',
    'div.phone',
    'a.phone',
    'span.phone',
    'p.phone',
    'div[class*="phone"]',
    'a[href^="tel:"]',
]

print("\nTesting selectors:")
for selector in selectors_to_try:
    elements = soup.select(selector)
    print(f"  {selector:30} -> {len(elements)} elements")

    if len(elements) > 0:
        print(f"    Sample: {elements[0].get_text(strip=True)[:50]}")
