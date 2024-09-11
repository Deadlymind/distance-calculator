from suppliers.models import Suppliers
from countries.models import Regions
from suppliers.utils import calculate_road_distance_price
from .models import Offers


def calculate_offer_m_price(price, road_distance_price, weight):
    return price + (road_distance_price/float(weight))

def calculate_offer_f_price(price, road_distance_price, weight):
    return price + (road_distance_price/float(weight))

def create_offer_data(supplier, region):
    road_distance_price = calculate_road_distance_price(
        [supplier.departure_address_lat, supplier.departure_address_lng],
        [region.center_lat, region.center_lng], region
    )

    price_exwb = float(supplier.price_exwb)
    price_exws = float(supplier.price_exws)
    weight = float(supplier.weight_of_full_truck)

    offer_m_price =  calculate_offer_m_price(price_exws, road_distance_price, weight)
    offer_f_price =  calculate_offer_f_price(price_exws, road_distance_price, weight)

    return {
        "supplier": supplier,
        "region": region,
        "road_distance_price": road_distance_price,
        "price_exwb": price_exwb,
        "price_exws": price_exws,
        "weight": weight,
        "offer_m_price": offer_m_price,
        "offer_f_price": offer_f_price
    }

def generate_offers():
    print("Generating Offers")
    Offers.objects.all().delete()
    suppliers = Suppliers.objects.all()
    for supplier in suppliers:
        regions = Regions.objects.all()
        for region in regions:
            print(f"Offer Created for {supplier.company_name} - {region.name}")
            Offers.objects.create(
                **create_offer_data(supplier, region)
            )

def generate_offers_for_new_supplier(supplier):
    print("Generating Offers For New Supplier")
    regions = Regions.objects.all()
    for region in regions:
        print(f"Offer Created for {supplier.company_name} - {region.name}")
        Offers.objects.create(
            **create_offer_data(supplier, region)
        )

def generate_offers_for_supplier_new_price(supplier):
    print("Generating Offers For New Price Of Supplier")
    Offers.objects.filter(supplier=supplier).delete()
    regions = Regions.objects.all()
    for region in regions:
        print(f"Offer Created for {supplier.company_name} - {region.name}")
        Offers.objects.create(
            **create_offer_data(supplier, region)
        )

def delete_offers_of_suppliers_on_supplier_delete(supplier):
    print("Deleting Offers of Deleted Supplier")
    Offers.objects.filter(supplier=supplier).delete()

def generate_offers_for_new_departments(department):
    print("Generating Offers FOr New Department")
    suppliers = Suppliers.objects.all()
    for supplier in suppliers:
        print(f"Offer Created for {supplier.company_name} - {department.name}")
        Offers.objects.create(
            **create_offer_data(supplier, department)
        )

def generate_offers_for_department_on_location_update(department):
    print("Generating Offers FOr New Department")
    Offers.objects.filter(region=department).delete()
    suppliers = Suppliers.objects.all()
    for supplier in suppliers:
        print(f"Offer Created for {supplier.company_name} - {department.name}")
        Offers.objects.create(
            **create_offer_data(supplier, department)
        )

def opportunity_detection_algorithm_by_color(fp_offer, m_offer):
    if fp_offer and m_offer:
        opportunity_difference = fp_offer.offer_f_price - m_offer.offer_m_price
        if opportunity_difference > 40:
            return "Green"
        elif opportunity_difference > 20:
            return "Yellow"
        elif opportunity_difference == 0:
            return "Red"
        elif opportunity_difference < 0:
            return "Purple"
    else:
        return "white"

