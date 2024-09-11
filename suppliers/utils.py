from geopy.distance import geodesic
from countries.models import Regions

def calculate_road_distance(source, destination):
    distance = geodesic(source, destination).km
    
    return distance

def calculate_road_distance_price(source, destination, region):
    distance = calculate_road_distance(
        source, destination
    )
    if distance < region.coefficient_distance:
        distance_price = distance * region.price * region.coefficient_price
    else:
        distance_price = distance * region.price
    return distance_price

# FROM SALES
def calculate_price_exws_from_exwb(buying_price, margin):
    return float(buying_price) + float(margin)

def calculate_price_exwb_from_dapb(price, distance_price, truck_weight):
    return float(price) - (float(distance_price) / float(truck_weight))

# 
def calculate_price_exws_from_daps(price, distance_price, truck_weight):
    return float(price) - (float(distance_price) / float(truck_weight))

def calculate_price_exwb_from_exws(selling_price, margin):
    return float(selling_price) - float(margin)


def calculate_price_from_source(data):
    if data['price_type'] == 'EXW':
        exwb = data['price']
        exws = calculate_price_exws_from_exwb(
            exwb, data['margin']
        )
        return {
            "exws": exws,
            "exwb": exwb
        }

    if data['price_type'] == 'DAP':
        distance_per_km = calculate_road_distance_price(
            [data['departure_address_lat'], data['departure_address_lng']],
            [data['destination_address_lat'], data['destination_address_lng']],
            Regions.objects.get(id=data['region'])
        )

        exwb = calculate_price_exwb_from_dapb(
            data['price'], distance_per_km, data['weight_of_full_truck']
        )
        exws = calculate_price_exws_from_exwb(
            exwb, data['margin']
        )

        return {
            "exws": exws,
            "exwb": exwb
        }


def calculate_price_from_sales(data):
    region = Regions.objects.get(id=data['region'])
    if data['price_type'] == 'EXW':
        exws = data['price']
        exwb = calculate_price_exwb_from_exws(
            exws, data['margin']
        )
        return {
            "exws": exws,
            "exwb": exwb
        }

    if data['price_type'] == 'DAP':
        distance_price = calculate_road_distance_price(
            [data['departure_address_lat'], data['departure_address_lng']],
            [data['destination_address_lat'], data['destination_address_lng']],
            region
        )

        exws = calculate_price_exws_from_daps(
            data['price'], distance_price, float(data['weight_of_full_truck'])
        )
        exwb = calculate_price_exwb_from_exws(
            exws, data['margin']
        )

        return {
            "exws": exws,
            "exwb": exwb
        }
