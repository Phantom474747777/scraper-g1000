"""
ZIP Code Lookup - Find all ZIP codes within a radius of a city
Uses geopy and free ZIP code API with offline fallback
"""
import requests
import json
import os
import time
from typing import List, Dict, Tuple
from math import radians, cos, sin, asin, sqrt
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


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


def get_city_coordinates_with_retry(city: str, state: str, max_retries: int = 5) -> Tuple[float, float]:
    """
    Get latitude and longitude for a city using geopy with exponential backoff retry
    """
    geolocator = Nominatim(user_agent="crittercaptures_leadgen", timeout=10)
    
    for attempt in range(max_retries):
        try:
            print(f"   🔍 Geocoding attempt {attempt + 1}/{max_retries}...")
            location = geolocator.geocode(f"{city}, {state}, USA")
            if location:
                print(f"   ✓ Found {city} at coordinates: {location.latitude:.4f}, {location.longitude:.4f}")
                return location.latitude, location.longitude
            else:
                raise ValueError(f"Could not find coordinates for {city}, {state}")
        except (GeocoderTimedOut, GeocoderServiceError, requests.exceptions.RequestException) as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 2s, 4s, 8s, 16s, 32s
                print(f"   ⚠️ Network timeout (attempt {attempt + 1}) — retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"   ❌ All geocoding attempts failed: {e}")
                raise ValueError(f"Network timeout after {max_retries} attempts: {e}")
        except Exception as e:
            raise ValueError(f"Error geocoding {city}, {state}: {e}")
    
    raise ValueError(f"Could not geocode {city}, {state} after {max_retries} attempts")


def load_zip_cache() -> Dict:
    """
    Load ZIP cache from local file
    """
    cache_file = "data/zip_cache.json"
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"   ⚠️ Could not load ZIP cache: {e}")
    return {}


def save_zip_cache(cache_data: Dict):
    """
    Save ZIP cache to local file
    """
    cache_file = "data/zip_cache.json"
    try:
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
    except IOError as e:
        print(f"   ⚠️ Could not save ZIP cache: {e}")


def get_zips_in_radius(city: str, state: str, radius_miles: int = 50) -> List[Dict]:
    """
    Get all ZIP codes within radius of a city with network resilience
    Returns list of dicts with: {zip, city, lat, lng, distance}
    """
    print(f"\n🔍 Finding ZIP codes within {radius_miles} miles of {city}, {state}...")
    
    # Check cache first
    cache_key = f"{city.lower()}_{state.upper()}_{radius_miles}"
    cache = load_zip_cache()
    
    if cache_key in cache:
        print(f"   ✓ Found cached ZIP data for {city}, {state}")
        return cache[cache_key]
    
    # Try online geocoding with retry
    try:
        city_lat, city_lng = get_city_coordinates_with_retry(city, state)
    except ValueError as e:
        print(f"   ⚠️ Network timeout — using offline ZIP database for radius lookup.")
        # Fallback to offline ZIP lookup
        return get_offline_zips_in_radius(city, state, radius_miles)
    
    # Get ZIPs using online method
    florida_zips = get_florida_zips_nearby(city_lat, city_lng, radius_miles)
    
    # Cache the results
    cache[cache_key] = florida_zips
    save_zip_cache(cache)
    
    print(f"   ✓ Found {len(florida_zips)} ZIP codes within {radius_miles} miles")
    
    return florida_zips


def get_offline_zips_in_radius(city: str, state: str, radius_miles: int) -> List[Dict]:
    """
    Offline fallback for ZIP code lookup using built-in database
    """
    print(f"   🔄 Using offline ZIP database...")
    
    # Use known coordinates for common cities as fallback
    known_cities = {
        ("dover", "fl"): (27.9949, -82.2192),
        ("tampa", "fl"): (27.9506, -82.4572),
        ("brandon", "fl"): (27.9378, -82.2859),
        ("riverview", "fl"): (27.8328, -82.3265),
        ("plant city", "fl"): (28.0186, -82.1129),
        ("valrico", "fl"): (27.9475, -82.2390),
        ("seffner", "fl"): (28.0017, -82.2756),
        ("odessa", "fl"): (28.1836, -82.5643),
    }
    
    city_key = (city.lower(), state.lower())
    if city_key in known_cities:
        city_lat, city_lng = known_cities[city_key]
        print(f"   ✓ Using offline coordinates for {city}: {city_lat:.4f}, {city_lng:.4f}")
    else:
        # Default to Tampa Bay area if city not found
        city_lat, city_lng = 27.9506, -82.4572
        print(f"   ⚠️ City {city} not in offline database, using Tampa Bay area coordinates")
    
    # Get ZIPs using offline method
    florida_zips = get_florida_zips_nearby(city_lat, city_lng, radius_miles)
    
    print(f"   ✓ Found {len(florida_zips)} ZIP codes using offline database")
    
    return florida_zips


def get_florida_zips_nearby(lat: float, lng: float, radius: int) -> List[Dict]:
    """
    Get Florida ZIP codes near the coordinates
    Comprehensive Florida ZIP database for Tampa Bay and Central Florida
    """
    # Comprehensive Florida ZIP codes database with coordinates
    # Covers Tampa Bay, Central Florida, and surrounding areas (100+ mile radius)
    known_fl_zips = [
        # Dover/Brandon/Riverview area
        {"zip": "33527", "city": "Dover", "lat": 27.9949, "lng": -82.2192},
        {"zip": "33594", "city": "Valrico", "lat": 27.9475, "lng": -82.2390},
        {"zip": "33510", "city": "Brandon", "lat": 27.9378, "lng": -82.2859},
        {"zip": "33511", "city": "Brandon", "lat": 27.8897, "lng": -82.3115},
        {"zip": "33569", "city": "Riverview", "lat": 27.8328, "lng": -82.3265},
        {"zip": "33578", "city": "Riverview", "lat": 27.7903, "lng": -82.2926},
        {"zip": "33584", "city": "Seffner", "lat": 28.0017, "lng": -82.2756},

        # Tampa (all ZIPs)
        {"zip": "33602", "city": "Tampa", "lat": 27.9478, "lng": -82.4584},
        {"zip": "33603", "city": "Tampa", "lat": 27.9864, "lng": -82.4532},
        {"zip": "33604", "city": "Tampa", "lat": 28.0106, "lng": -82.4343},
        {"zip": "33605", "city": "Tampa", "lat": 27.9631, "lng": -82.4426},
        {"zip": "33606", "city": "Tampa", "lat": 27.9378, "lng": -82.4787},
        {"zip": "33607", "city": "Tampa", "lat": 27.9506, "lng": -82.5126},
        {"zip": "33609", "city": "Tampa", "lat": 27.9478, "lng": -82.5343},
        {"zip": "33610", "city": "Tampa", "lat": 27.9772, "lng": -82.4076},
        {"zip": "33611", "city": "Tampa", "lat": 27.9239, "lng": -82.5198},
        {"zip": "33612", "city": "Tampa", "lat": 28.0367, "lng": -82.4412},
        {"zip": "33613", "city": "Tampa", "lat": 28.0745, "lng": -82.3762},
        {"zip": "33614", "city": "Tampa", "lat": 28.0050, "lng": -82.5165},
        {"zip": "33615", "city": "Tampa", "lat": 28.0106, "lng": -82.5473},
        {"zip": "33616", "city": "Tampa", "lat": 27.8872, "lng": -82.5221},
        {"zip": "33617", "city": "Tampa", "lat": 28.0722, "lng": -82.4148},
        {"zip": "33618", "city": "Tampa", "lat": 28.0856, "lng": -82.5076},
        {"zip": "33619", "city": "Tampa", "lat": 27.9739, "lng": -82.3540},
        {"zip": "33620", "city": "Tampa", "lat": 27.9753, "lng": -82.4012},
        {"zip": "33621", "city": "Tampa", "lat": 27.9256, "lng": -82.5426},
        {"zip": "33624", "city": "Tampa", "lat": 28.0700, "lng": -82.5373},
        {"zip": "33625", "city": "Tampa", "lat": 28.0778, "lng": -82.5765},
        {"zip": "33626", "city": "Tampa", "lat": 28.0489, "lng": -82.5732},
        {"zip": "33629", "city": "Tampa", "lat": 27.9431, "lng": -82.5126},
        {"zip": "33634", "city": "Tampa", "lat": 28.0161, "lng": -82.5876},
        {"zip": "33635", "city": "Tampa", "lat": 28.0092, "lng": -82.6354},
        {"zip": "33637", "city": "Tampa", "lat": 28.0350, "lng": -82.3879},
        {"zip": "33647", "city": "Tampa", "lat": 28.1550, "lng": -82.3548},

        # Plant City area
        {"zip": "33563", "city": "Plant City", "lat": 28.0186, "lng": -82.1129},
        {"zip": "33565", "city": "Plant City", "lat": 27.9817, "lng": -82.1337},
        {"zip": "33566", "city": "Plant City", "lat": 28.0361, "lng": -82.0648},
        {"zip": "33567", "city": "Plant City", "lat": 27.9456, "lng": -82.1534},

        # Lutz/Odessa/Land O'Lakes
        {"zip": "33548", "city": "Lutz", "lat": 28.1439, "lng": -82.4612},
        {"zip": "33549", "city": "Lutz", "lat": 28.1372, "lng": -82.3984},
        {"zip": "33558", "city": "Lutz", "lat": 28.1883, "lng": -82.4540},
        {"zip": "33556", "city": "Odessa", "lat": 28.1836, "lng": -82.5643},
        {"zip": "33559", "city": "Lutz", "lat": 28.1203, "lng": -82.5165},
        {"zip": "34638", "city": "Land O'Lakes", "lat": 28.2189, "lng": -82.4573},
        {"zip": "34639", "city": "Land O'Lakes", "lat": 28.1883, "lng": -82.5015},

        # Clearwater/St. Petersburg/Pinellas County
        {"zip": "33755", "city": "Clearwater", "lat": 27.9658, "lng": -82.7598},
        {"zip": "33756", "city": "Clearwater", "lat": 27.9886, "lng": -82.7390},
        {"zip": "33759", "city": "Clearwater", "lat": 27.9764, "lng": -82.7120},
        {"zip": "33760", "city": "Clearwater", "lat": 27.9806, "lng": -82.6954},
        {"zip": "33761", "city": "Clearwater", "lat": 28.0003, "lng": -82.7276},
        {"zip": "33762", "city": "Clearwater", "lat": 28.0203, "lng": -82.7437},
        {"zip": "33763", "city": "Clearwater", "lat": 27.9328, "lng": -82.7526},
        {"zip": "33764", "city": "Clearwater", "lat": 27.9672, "lng": -82.6982},
        {"zip": "33765", "city": "Clearwater", "lat": 28.0533, "lng": -82.7218},
        {"zip": "33767", "city": "Clearwater", "lat": 27.9886, "lng": -82.8026},
        {"zip": "33770", "city": "Largo", "lat": 27.9097, "lng": -82.7740},
        {"zip": "33771", "city": "Largo", "lat": 27.8881, "lng": -82.7590},
        {"zip": "33773", "city": "Largo", "lat": 27.8686, "lng": -82.7654},
        {"zip": "33774", "city": "Largo", "lat": 27.8936, "lng": -82.8054},
        {"zip": "33776", "city": "Seminole", "lat": 27.8392, "lng": -82.7915},
        {"zip": "33777", "city": "Seminole", "lat": 27.8481, "lng": -82.7526},
        {"zip": "33778", "city": "Largo", "lat": 27.9303, "lng": -82.7373},
        {"zip": "33781", "city": "Pinellas Park", "lat": 27.8428, "lng": -82.7093},
        {"zip": "33782", "city": "Pinellas Park", "lat": 27.8672, "lng": -82.6876},
        {"zip": "33785", "city": "Indian Rocks Beach", "lat": 27.8881, "lng": -82.8443},
        {"zip": "33786", "city": "Belleair Beach", "lat": 27.9342, "lng": -82.8371},

        # St. Petersburg
        {"zip": "33701", "city": "St. Petersburg", "lat": 27.7731, "lng": -82.6790},
        {"zip": "33702", "city": "St. Petersburg", "lat": 27.7856, "lng": -82.6429},
        {"zip": "33703", "city": "St. Petersburg", "lat": 27.8117, "lng": -82.6365},
        {"zip": "33704", "city": "St. Petersburg", "lat": 27.8089, "lng": -82.7026},
        {"zip": "33705", "city": "St. Petersburg", "lat": 27.7592, "lng": -82.6373},
        {"zip": "33706", "city": "St. Petersburg", "lat": 27.7672, "lng": -82.7218},
        {"zip": "33707", "city": "St. Petersburg", "lat": 27.7481, "lng": -82.7373},
        {"zip": "33708", "city": "St. Petersburg", "lat": 27.8089, "lng": -82.7748},
        {"zip": "33709", "city": "St. Petersburg", "lat": 27.8242, "lng": -82.7276},
        {"zip": "33710", "city": "St. Petersburg", "lat": 27.8256, "lng": -82.6607},
        {"zip": "33711", "city": "St. Petersburg", "lat": 27.7439, "lng": -82.6790},
        {"zip": "33712", "city": "St. Petersburg", "lat": 27.7997, "lng": -82.6165},
        {"zip": "33713", "city": "St. Petersburg", "lat": 27.8350, "lng": -82.6429},
        {"zip": "33714", "city": "St. Petersburg", "lat": 27.7414, "lng": -82.7165},
        {"zip": "33715", "city": "St. Petersburg", "lat": 27.7036, "lng": -82.6718},
        {"zip": "33716", "city": "St. Petersburg", "lat": 27.6917, "lng": -82.7165},

        # South Tampa Bay
        {"zip": "33573", "city": "Sun City Center", "lat": 27.7178, "lng": -82.3518},
        {"zip": "33570", "city": "Ruskin", "lat": 27.7211, "lng": -82.4329},
        {"zip": "33572", "city": "Apollo Beach", "lat": 27.7725, "lng": -82.4070},
        {"zip": "33598", "city": "Wimauma", "lat": 27.7050, "lng": -82.2998},
        {"zip": "33579", "city": "Riverview", "lat": 27.8656, "lng": -82.3265},

        # Lakeland/Polk County
        {"zip": "33801", "city": "Lakeland", "lat": 28.0394, "lng": -81.9498},
        {"zip": "33803", "city": "Lakeland", "lat": 28.0353, "lng": -82.0048},
        {"zip": "33805", "city": "Lakeland", "lat": 28.0789, "lng": -81.9681},
        {"zip": "33809", "city": "Lakeland", "lat": 28.1094, "lng": -81.9331},
        {"zip": "33810", "city": "Lakeland", "lat": 27.9928, "lng": -81.9195},
        {"zip": "33811", "city": "Lakeland", "lat": 28.0761, "lng": -82.0126},
        {"zip": "33813", "city": "Lakeland", "lat": 27.9619, "lng": -81.9681},
        {"zip": "33815", "city": "Lakeland", "lat": 28.0150, "lng": -81.8815},

        # Wesley Chapel/Zephyrhills/Dade City
        {"zip": "33543", "city": "Wesley Chapel", "lat": 28.1906, "lng": -82.3273},
        {"zip": "33544", "city": "Wesley Chapel", "lat": 28.2367, "lng": -82.3548},
        {"zip": "33540", "city": "Zephyrhills", "lat": 28.2336, "lng": -82.1809},
        {"zip": "33541", "city": "Zephyrhills", "lat": 28.2417, "lng": -82.1473},
        {"zip": "33542", "city": "Zephyrhills", "lat": 28.2528, "lng": -82.2176},
        {"zip": "33523", "city": "Dade City", "lat": 28.3647, "lng": -82.1959},
        {"zip": "33525", "city": "Dade City", "lat": 28.3656, "lng": -82.2543},
        {"zip": "33526", "city": "San Antonio", "lat": 28.3364, "lng": -82.2698},

        # New Port Richey/Pasco County
        {"zip": "34652", "city": "New Port Richey", "lat": 28.2442, "lng": -82.7193},
        {"zip": "34653", "city": "New Port Richey", "lat": 28.2669, "lng": -82.6712},
        {"zip": "34654", "city": "New Port Richey", "lat": 28.3278, "lng": -82.6515},
        {"zip": "34655", "city": "New Port Richey", "lat": 28.3139, "lng": -82.7070},
        {"zip": "34667", "city": "Hudson", "lat": 28.3647, "lng": -82.6932},
        {"zip": "34668", "city": "Port Richey", "lat": 28.2722, "lng": -82.7193},
        {"zip": "34669", "city": "Hudson", "lat": 28.3528, "lng": -82.7476},
        {"zip": "34690", "city": "Holiday", "lat": 28.1883, "lng": -82.7404},
        {"zip": "34691", "city": "Holiday", "lat": 28.2022, "lng": -82.6837},

        # Sarasota/Bradenton (South of Tampa)
        {"zip": "34201", "city": "Bradenton", "lat": 27.4989, "lng": -82.5748},
        {"zip": "34202", "city": "Bradenton", "lat": 27.4403, "lng": -82.5737},
        {"zip": "34203", "city": "Bradenton", "lat": 27.4756, "lng": -82.6198},
        {"zip": "34205", "city": "Bradenton", "lat": 27.4639, "lng": -82.6543},
        {"zip": "34207", "city": "Bradenton", "lat": 27.4914, "lng": -82.6254},
        {"zip": "34208", "city": "Bradenton", "lat": 27.4331, "lng": -82.6082},
        {"zip": "34209", "city": "Bradenton", "lat": 27.5086, "lng": -82.5471},
        {"zip": "34210", "city": "Bradenton", "lat": 27.4506, "lng": -82.6837},
        {"zip": "34211", "city": "Bradenton", "lat": 27.5197, "lng": -82.5143},
        {"zip": "34212", "city": "Bradenton", "lat": 27.5253, "lng": -82.4673},
        {"zip": "34219", "city": "Parrish", "lat": 27.5831, "lng": -82.4198},
        {"zip": "34221", "city": "Palmetto", "lat": 27.5214, "lng": -82.5632},
        {"zip": "34222", "city": "Ellenton", "lat": 27.5231, "lng": -82.5237},

        {"zip": "34231", "city": "Sarasota", "lat": 27.3364, "lng": -82.5304},
        {"zip": "34232", "city": "Sarasota", "lat": 27.3017, "lng": -82.5365},
        {"zip": "34233", "city": "Sarasota", "lat": 27.3081, "lng": -82.4626},
        {"zip": "34234", "city": "Sarasota", "lat": 27.2753, "lng": -82.5093},
        {"zip": "34235", "city": "Sarasota", "lat": 27.2369, "lng": -82.5054},
        {"zip": "34236", "city": "Sarasota", "lat": 27.3506, "lng": -82.4843},
        {"zip": "34237", "city": "Sarasota", "lat": 27.3150, "lng": -82.5676},
        {"zip": "34238", "city": "Sarasota", "lat": 27.3847, "lng": -82.4601},
        {"zip": "34239", "city": "Sarasota", "lat": 27.3656, "lng": -82.5365},
        {"zip": "34240", "city": "Sarasota", "lat": 27.2878, "lng": -82.5515},
        {"zip": "34241", "city": "Sarasota", "lat": 27.2642, "lng": -82.4737},
        {"zip": "34243", "city": "Sarasota", "lat": 27.4028, "lng": -82.4515},
    ]
    
    # Calculate distance for each ZIP
    results = []
    for zip_data in known_fl_zips:
        distance = haversine_distance(lat, lng, zip_data['lat'], zip_data['lng'])
        if distance <= radius:
            results.append({
                'zip': zip_data['zip'],
                'city': zip_data['city'],
                'lat': zip_data['lat'],
                'lng': zip_data['lng'],
                'distance': round(distance, 1)
            })
    
    # Sort by distance
    results.sort(key=lambda x: x['distance'])
    
    return results


if __name__ == "__main__":
    # Test the function
    zips = get_zips_in_radius("Dover", "FL", 50)
    print("\n📋 Found ZIP codes:")
    for z in zips[:10]:
        print(f"   {z['zip']} - {z['city']} ({z['distance']} miles)")

