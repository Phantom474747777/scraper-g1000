"""
ZIP Code Lookup - Find all ZIP codes within a radius of any US city
Uses pgeocode library - FAST and works for ALL USA cities!
"""
from typing import List, Dict
import pgeocode
from geopy.geocoders import Nominatim


def get_zips_in_radius(city: str, state: str, radius_miles: int = 50) -> List[Dict]:
    """
    Get all ZIP codes within radius of a city - WORKS FOR ANY USA CITY!
    Returns list of dicts with: {zip, city, lat, lng, distance}

    Uses pgeocode library with full USA database (FREE + FAST!)
    """
    print(f"\n[ZIP Lookup] Finding ZIP codes within {radius_miles} miles of {city}, {state}...")

    try:
        # Step 1: Get center city coordinates
        geolocator = Nominatim(user_agent="scraper_g1000", timeout=10)
        print(f"[ZIP Lookup] Geocoding {city}, {state}...")
        location = geolocator.geocode(f"{city}, {state}, USA")

        if not location:
            print(f"[ZIP Lookup] ERROR: Could not find {city}, {state}")
            return []

        center_lat = location.latitude
        center_lng = location.longitude
        print(f"[ZIP Lookup] Found coordinates: {center_lat:.4f}, {center_lng:.4f}")

        # Step 2: Use pgeocode to search by radius
        print(f"[ZIP Lookup] Searching ZIP codes within {radius_miles} miles...")
        nomi = pgeocode.GeoDistance('US')

        # Convert miles to kilometers (pgeocode uses km)
        radius_km = radius_miles * 1.60934

        # Search for ZIPs within radius using pgeocode's optimized search
        # We'll get a sample center ZIP first, then search around it
        search_engine = pgeocode.Nominatim('US')

        # Find nearest ZIP to our coordinates
        import pandas as pd
        import numpy as np

        # Get the database
        db = search_engine._data

        # Filter out invalid entries
        valid_zips = db[(db['latitude'].notna()) & (db['longitude'].notna())].copy()

        # Calculate distances for all ZIPs (vectorized - FAST!)
        from math import radians, sin, cos, sqrt, asin

        # Convert to radians
        lat1 = radians(center_lat)
        lon1 = radians(center_lng)
        lat2 = np.radians(valid_zips['latitude'].values)
        lon2 = np.radians(valid_zips['longitude'].values)

        # Haversine formula (vectorized)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        distances_miles = 3959 * c  # Earth radius in miles

        # Filter by radius
        mask = distances_miles <= radius_miles
        results_df = valid_zips[mask].copy()
        results_df['distance'] = distances_miles[mask]

        # Sort by distance
        results_df = results_df.sort_values('distance')

        # Convert to our format
        results = []
        for idx, row in results_df.iterrows():
            results.append({
                'zip': str(idx).zfill(5),
                'city': str(row['place_name']) if pd.notna(row['place_name']) else 'Unknown',
                'lat': float(row['latitude']),
                'lng': float(row['longitude']),
                'distance': round(float(row['distance']), 1)
            })

        print(f"[ZIP Lookup] FOUND {len(results)} ZIP codes!")
        return results

    except Exception as e:
        print(f"[ZIP Lookup] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return []


if __name__ == "__main__":
    # Test
    print("\n=== Testing ZIP Lookup ===")
    zips = get_zips_in_radius("Largo", "FL", 100)
    print(f"\nTotal: {len(zips)} ZIPs")
    for z in zips[:20]:
        print(f"   {z['zip']} - {z['city']} ({z['distance']} mi)")
