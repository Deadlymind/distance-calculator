from geopy.geocoders import Nominatim
from regions import data_v2 as data
from countries.models import Countries, Regions
from django.core.management.base import BaseCommand
from django.db import transaction
from offers.utils import generate_offers_for_new_departments


class Command(BaseCommand):

    def get_center_of_department_coordinates(self, address):
        geolocator = Nominatim(user_agent="Map1")
        location = geolocator.geocode(address)
        return location.latitude, location.longitude

    def generate_departments(self, country, departments, key='name:en'):
        country.regions.all().delete()  # DELETING ALL PREVIOUS REGIONS.
        for department in departments:
            lat, lng = self.get_center_of_department_coordinates(department[key])
            r = Regions.objects.create(
                country=country,
                name=department[key],
                center_lat=lat,
                center_lng=lng,
            )
            # generate_offers_for_new_departments(r)
            print(r)


    def handle(self, *args, **options):
        with transaction.atomic():
            self.generate_departments(
                Countries.objects.get_or_create(name='france')[0], data.france, 'name'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='albania')[0], data.albania
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='armenia')[0], data.armenia
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='austria')[0], data.austria
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='azerbaijan')[0], data.azerbaijan
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='bosnia')[0], data.bosnia
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='belgium')[0], data.belgium
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='bulgaria')[0], data.bulgaria
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='belarus')[0], data.belarus
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='switzerland')[0], data.switzerland
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='cyprus')[0], data.cyprus
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='czechia')[0], data.czechia
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='germany')[0], data.germany
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='denmark')[0], data.denmark
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='estonia')[0], data.estonia
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='spain')[0], data.spain
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='finland')[0], data.finland
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='united_kingdom')[0], data.united_kingdom, 'name'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='georgia')[0], data.georgia
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='greece')[0], data.greece
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='croatia')[0], data.croatia
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='hungary')[0], data.hungary
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='ireland')[0], data.ireland
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='iraq')[0], data.iraq
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='iceland')[0], data.iceland
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='italy')[0], data.italy
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='liechtenstein')[0], data.liechtenstein
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='morocco')[0], data.morocco
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='moldova')[0], data.moldova
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='montenegro')[0], data.montenegro
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='netherlands')[0], data.netherlands
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='norway')[0], data.norway
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='poland')[0], data.poland
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='portugal')[0], data.portugal
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='romania')[0], data.romania
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='serbia')[0], data.serbia
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='russia')[0], data.russia
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='sweden')[0], data.sweden
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='slovakia')[0], data.slovakia
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='syria')[0], data.syria
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='turkey')[0], data.turkey
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='ukraine')[0], data.ukraine
            )
            print("COMPLETED")        
