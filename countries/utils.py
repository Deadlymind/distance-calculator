import math
from mapbox import Geocoder

from django.conf import settings

def haversine_distance(lat1, lng1, lat2, lng2):
    # Radius of the Earth in km
    R = 6371.0
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    # Difference in coordinates
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Distance in kilometers
    distance = R * c
    return distance

def closest_location(lat, lng, locations):
    closest_loc = None
    min_distance = float('inf')
    
    for location in locations:
        loc_lat, loc_lng = location.center_lat, location.center_lng
        distance = haversine_distance(lat, lng, loc_lat, loc_lng)
        # print(location, distance)
        
        if distance < min_distance:
            min_distance = distance
            closest_loc = location
    
    return closest_loc

def get_address_coordinates_from_mapbox(address_text):
    geocoder = Geocoder(access_token=settings.MAPBOX_ACCESS_TOKEN)
    resp = geocoder.forward(address_text)

    if resp.status_code == 200:
        data = resp.json()
        if data['features']:
            coordinates = data['features'][0]['geometry']['coordinates']
            return {
                "lat": coordinates[1],
                "lng": coordinates[0],
            }

    return None
        
