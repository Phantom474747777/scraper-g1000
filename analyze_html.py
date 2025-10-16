"""Analyze the actual HTML structure"""
from bs4 import BeautifulSoup

with open('debug_page_1.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("=" * 60)
print("HTML STRUCTURE ANALYSIS")
print("=" * 60)

# Check for various possible selectors
selectors = [
    ('div.result', 'YellowPages old structure'),
    ('div[class*="result"]', 'Any div with "result" in class'),
    ('div.search-results', 'Search results container'),
    ('div.organic', 'Organic results'),
    ('div[data-id]', 'Divs with data-id'),
    ('a.business-name', 'Business name links'),
    ('h2.n', 'H2 headers'),
    ('div.info', 'Info divs'),
]

print("\nSELECTOR TEST RESULTS:")
for selector, desc in selectors:
    elements = soup.select(selector)
    status = "FOUND" if len(elements) > 0 else "NOT FOUND"
    print(f"  [{status:10}] {selector:30} - {desc} ({len(elements)} elements)")

# Find all unique div classes
print("\n" + "=" * 60)
print("ALL DIV CLASSES IN HTML:")
print("=" * 60)

div_classes = set()
for div in soup.find_all('div', class_=True):
    classes = div.get('class', [])
    if isinstance(classes, list):
        div_classes.update(classes)

# Print first 50 most common classes
print("\nFound {} unique div classes:".format(len(div_classes)))
for cls in sorted(list(div_classes))[:50]:
    print(f"  - {cls}")

# Check if it's "no results" page
print("\n" + "=" * 60)
print("PAGE TYPE CHECK:")
print("=" * 60)

if "Best 0" in html or "No Results Found" in html:
    print("[INFO] This appears to be a 'NO RESULTS' page")
    print("  - YellowPages has zero listings for this ZIP+category combo")
else:
    print("[INFO] This appears to have results, but selectors are wrong")

# Check for specific result-like structures
print("\n" + "=" * 60)
print("LOOKING FOR BUSINESS DATA:")
print("=" * 60)

# Try to find ANY element that might contain business info
phone_patterns = soup.find_all(text=lambda text: text and '(' in text and ')' in text and '-' in text)
print(f"\nPossible phone numbers found: {len(phone_patterns)}")

if phone_patterns:
    print("Sample phone-like text:")
    for i, phone in enumerate(phone_patterns[:5]):
        print(f"  {i+1}. {phone.strip()[:50]}")
