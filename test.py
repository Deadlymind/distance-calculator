from geopy.geocoders import Nominatim

def get_region_center(region_name):
    geolocator = Nominatim(user_agent="region_center_finder")
    location = geolocator.geocode(region_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Example usage
region_name = input("Enter the name of the region: ")
center_coordinates = get_region_center(region_name)
if center_coordinates:
    print(f"Center coordinates of {region_name}: Latitude: {center_coordinates[0]}, Longitude: {center_coordinates[1]}")
else:
    print("Region not found or coordinates not available.")