import os
from mapbox import Geocoder

REAL_COORDINATES = "42.018145977927034, 23.097379838826164"

# Set your Mapbox access token
access_token = "pk.eyJ1Ijoic2FtaTIwMjQiLCJhIjoiY20xNHdrZHVoMDJuMjJrc2pzYzRxc3gwZSJ9.dedAS2SGVF6478Dt1nkiew"
os.environ['MAPBOX_ACCESS_TOKEN'] = access_token

# Initialize the geocoder
geocoder = Geocoder(access_token=access_token)

# Search for an address
response = geocoder.forward("""
Todor Aleksandrov Str 43
2700, Blagoevgrad
Bulgaria
""")

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    features = data['features']

    # Display results
    for feature in features:
        place_name = feature['place_name']
        coordinates = feature['geometry']['coordinates']
        print(f"Place Name: {place_name}, Coordinates: {coordinates}")
else:
    print(f"Error: {response.status_code}, {response.text}")