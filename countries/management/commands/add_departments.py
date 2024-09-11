from regions import data
from countries.models import Countries, Regions
from django.core.management.base import BaseCommand
from django.db import transaction
from offers.utils import generate_offers_for_new_departments


class Command(BaseCommand):
    help = 'Get Information On Dribble Products'

    def get_dribble_url(self, dribble_product_id):
        return f"https://dribbble.com/shots/{dribble_product_id}"

    def generate_departments(self, country, departments, key='department'):
        country.regions.all().delete()  # DELETING ALL PREVIOUS REGIONS.
        for department in departments:
            r = Regions.objects.create(
                country=country,
                name=department[key],
                center_lat=department['coordinates']['latitude'],
                center_lng=department['coordinates']['longitude'],
            )
            generate_offers_for_new_departments(r)
            print(r)


    def handle(self, *args, **options):
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='france')[0], data.france
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='germany')[0], data.germany
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='albania')[0], data.albania
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='bulgaria')[0], data.bulgaria
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='netherlands')[0], data.netherlands
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='italy')[0], data.italy
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='spain')[0], data.spain
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='lithuainia')[0], data.lithuainia
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='croatia')[0], data.croatia
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='austria')[0], data.austria
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='czech')[0], data.czech
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='poland')[0], data.poland
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='portugal')[0], data.portugal
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='ukraine')[0], data.ukraine
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='turkey')[0], data.turkey
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='latvia')[0], data.latvia
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='serbia')[0], data.serbia
        # )
        # self.generate_departments(
        #     Countries.objects.get_or_create(name='russia')[0], data.russia
        # )
        with transaction.atomic():
            self.generate_departments(
                Countries.objects.get_or_create(name='United Kingdom')[0], data.uk_counties, 'county'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Switzerland')[0], data.switzerland_cantons, 'canton'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Sweden')[0], data.sweden_counties, 'county'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Slovenia')[0], data.slovenia_regions, 'region'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Slovakia')[0], data.slovakia_regions, 'region'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='San Marino')[0], data.san_marino_castelli, 'castello'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Romania')[0], data.romania_counties, 'county'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Norway')[0], data.norway_counties, 'county'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='North Macedonia')[0], data.north_macedonia_regions, 'region'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Monaco')[0], data.monaco_quarters, 'quarter'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Moldova')[0], data.moldova_districts, 'district'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Luxembourg')[0], data.luxembourg_cantons, 'canton'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Liechtenstein')[0], data.liechtenstein_municipalities, 'municipality'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Kosovo')[0], data.kosovo_districts, 'district'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Kazakhstan')[0], data.kazakhstan_regions, 'region'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Ireland')[0], data.ireland_counties, 'county'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Iceland')[0], data.iceland_regions, 'region'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Hungary')[0], data.hungary_counties, 'county'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Greece')[0], data.greece_regions, 'region'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Finland')[0], data.finland_regions, 'region'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Estonia')[0], data.estonia_counties, 'county'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Denmark')[0], data.denmark_regions, 'region'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Cyprus')[0], data.cyprus_districts, 'district'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Bosnia')[0], data.bosnia_rs_regions, 'region'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Belgium')[0], data.belgium_provinces, 'province'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Herzegovina')[0], data.herzegovina_cities, 'city'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Belarus')[0], data.belarus_regions, 'region'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Armenia')[0], data.armenia_provinces, 'province'
            )
            self.generate_departments(
                Countries.objects.get_or_create(name='Andorra')[0], data.andorra_parishes, 'parish'
            )
            print("COMPLETED")        
