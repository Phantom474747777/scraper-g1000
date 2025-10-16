"""
ZIP Code Lookup - Find all ZIP codes within a radius of any US city
Uses pgeocode library - FREE, works EVERYWHERE in USA!
"""
from typing import List, Dict
import pgeocode
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on earth (in miles)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # Radius of earth in miles
    miles = 3959 * c
    return miles


def get_zips_in_radius(city: str, state: str, radius_miles: int = 50) -> List[Dict]:
    """
    Get all ZIP codes within radius of a city - WORKS FOR ANY USA CITY!
    Returns list of dicts with: {zip, city, lat, lng, distance}

    Uses pgeocode library with full USA database (FREE!)
    """
    print(f"\nFinding ZIP codes within {radius_miles} miles of {city}, {state}...")

    # Step 1: Get center city coordinates using geopy
    geolocator = Nominatim(user_agent="scraper_g1000")
    location = geolocator.geocode(f"{city}, {state}, USA")

    if not location:
        print(f"   ERROR: Could not find {city}, {state}")
        return []

    center_lat = location.latitude
    center_lng = location.longitude

    print(f"   Found center: {city}, {state} ({center_lat:.4f}, {center_lng:.4f})")
    print(f"   Searching all USA ZIP codes...")

    # Step 2: Load USA ZIP database
    nomi = pgeocode.Nominatim('US')

    # Step 3: Get all ZIP codes in the same state first (optimization)
    # Then check distance for each
    all_zips = nomi.query_postal_code(None)  # Get all ZIPs

    results = []
    checked = 0

    # Iterate through ALL USA ZIPs and check distance
    for zip_code in all_zips.index:
        if zip_code and str(zip_code).isdigit() and len(str(zip_code)) == 5:
            zip_info = nomi.query_postal_code(zip_code)

            if zip_info is not None and not zip_info.empty:
                try:
                    zip_lat = float(zip_info['latitude'])
                    zip_lng = float(zip_info['longitude'])
                    zip_city = str(zip_info['place_name']) if 'place_name' in zip_info and zip_info['place_name'] else 'Unknown'

                    # Calculate distance
                    distance = haversine_distance(center_lat, center_lng, zip_lat, zip_lng)

                    if distance <= radius_miles:
                        results.append({
                            'zip': str(zip_code).zfill(5),  # Ensure 5 digits
                            'city': zip_city,
                            'lat': zip_lat,
                            'lng': zip_lng,
                            'distance': round(distance, 1)
                        })

                    checked += 1
                    if checked % 1000 == 0:
                        print(f"   Checked {checked} ZIPs, found {len(results)} within radius...")

                except (ValueError, KeyError, TypeError):
                    continue

    # Sort by distance
    results.sort(key=lambda x: x['distance'])

    print(f"   FOUND {len(results)} ZIP codes within {radius_miles} miles!")

    return results


if __name__ == "__main__":
    # Test with Largo, FL
    print("\n=== Testing ZIP Lookup ===")

    print("\n1. Largo, FL - 100 miles:")
    zips = get_zips_in_radius("Largo", "FL", 100)
    print(f"\n   Total: {len(zips)} ZIPs")
    for z in zips[:15]:
        print(f"   {z['zip']} - {z['city']} ({z['distance']} mi)")
