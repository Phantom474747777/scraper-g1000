"""
ZIP Code Lookup - Find all ZIP codes within a radius of any US city
Uses uszipcode library with 42,000+ USA ZIP codes (FREE, offline, no API limits!)
"""
from typing import List, Dict
from uszipcode import SearchEngine, SimpleZipcode


def get_zips_in_radius(city: str, state: str, radius_miles: int = 50) -> List[Dict]:
    """
    Get all ZIP codes within radius of a city - WORKS FOR ANY USA CITY!
    Returns list of dicts with: {zip, city, lat, lng, distance}

    Uses uszipcode library with full USA database (42,000+ ZIPs)
    """
    print(f"\nFinding ZIP codes within {radius_miles} miles of {city}, {state}...")

    # Create search engine (uses local SQLite database)
    search = SearchEngine()

    # Find the city to get coordinates
    print(f"   Looking up {city}, {state}...")
    city_results = search.by_city_and_state(city, state)

    if not city_results:
        print(f"   ERROR: Could not find {city}, {state}")
        return []

    # Use first result's coordinates as center point
    center_zip = city_results[0]
    center_lat = center_zip.lat
    center_lng = center_zip.lng

    print(f"   Found center: {center_zip.major_city}, {state} ({center_lat:.4f}, {center_lng:.4f})")
    print(f"   Searching for all ZIPs within {radius_miles} miles...")

    # Search for all ZIPs within radius
    nearby_zips = search.by_coordinates(
        lat=center_lat,
        lng=center_lng,
        radius=radius_miles,
        returns=1000  # Return up to 1000 ZIPs (plenty for 100 miles)
    )

    # Convert to our format
    results = []
    for zip_obj in nearby_zips:
        if zip_obj.zipcode and zip_obj.major_city and zip_obj.lat and zip_obj.lng:
            # Calculate actual distance (uszipcode doesn't return it directly)
            from math import radians, cos, sin, asin, sqrt

            # Haversine formula
            lat1, lon1 = radians(center_lat), radians(center_lng)
            lat2, lon2 = radians(zip_obj.lat), radians(zip_obj.lng)

            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            distance = 3959 * c  # Earth radius in miles

            results.append({
                'zip': zip_obj.zipcode,
                'city': zip_obj.major_city,
                'lat': zip_obj.lat,
                'lng': zip_obj.lng,
                'distance': round(distance, 1)
            })

    # Sort by distance
    results.sort(key=lambda x: x['distance'])

    print(f"   FOUND {len(results)} ZIP codes within {radius_miles} miles!")

    return results


if __name__ == "__main__":
    # Test with different cities
    print("\n=== Testing ZIP Lookup ===")

    print("\n1. Tampa, FL - 50 miles:")
    zips = get_zips_in_radius("Tampa", "FL", 50)
    print(f"   Total: {len(zips)} ZIPs")
    for z in zips[:10]:
        print(f"   {z['zip']} - {z['city']} ({z['distance']} mi)")

    print("\n2. Largo, FL - 100 miles:")
    zips = get_zips_in_radius("Largo", "FL", 100)
    print(f"   Total: {len(zips)} ZIPs")
    for z in zips[:10]:
        print(f"   {z['zip']} - {z['city']} ({z['distance']} mi)")

    print("\n3. New York, NY - 50 miles:")
    zips = get_zips_in_radius("New York", "NY", 50)
    print(f"   Total: {len(zips)} ZIPs")
    for z in zips[:10]:
        print(f"   {z['zip']} - {z['city']} ({z['distance']} mi)")

    print("\n4. Los Angeles, CA - 75 miles:")
    zips = get_zips_in_radius("Los Angeles", "CA", 75)
    print(f"   Total: {len(zips)} ZIPs")
    for z in zips[:10]:
        print(f"   {z['zip']} - {z['city']} ({z['distance']} mi)")
