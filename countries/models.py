from django.db import models
from offers.models import Offers
# Create your models here.

class Countries(models.Model):
    name = models.CharField(max_length=1000)

    def get_regions(self):
        return Regions.objects.filter(country=self)

    def __str__(self):
        return self.name

class Regions(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, related_name='regions')
    name = models.CharField(max_length=1000)
    price = models.FloatField(default=1)  # PER KM
    coefficient_price = models.FloatField(default=1.1)  # PER KM
    coefficient_distance = models.FloatField(default=100)  # PER KM

    center_lat = models.FloatField(default=0)
    center_lng = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def get_best_m_offers(self, product_id):
        return Offers.objects.filter(
            region=self,
            supplier__product_id=product_id,
        ).order_by('offer_m_price')[:3]
    
    def get_best_f_offer(self, product_id):
        return Offers.objects.filter(
            region=self,
            supplier__region=self,
            supplier__product_id=product_id
        ).order_by('offer_f_price').first()

    def get_red_offers(self, product_id, offer_price):
        final_offer_data = []
        offers = Offers.objects.filter(
            region=self,
            supplier__product_id=product_id,
        )
        for offer in offers:
            diff = offer_price - offer.offer_m_price
            if diff >= 0 and diff < 1:
                final_offer_data.append(offer)
        return final_offer_data

    def get_green_offers(self, product_id, offer_price):
        final_offer_data = []
        offers = Offers.objects.filter(
            region=self,
            supplier__product_id=product_id,
        )
        for offer in offers:
            if offer_price - offer.offer_m_price > 40:
                final_offer_data.append(offer)
        return final_offer_data

    def get_yellow_offers(self, product_id, offer_price):
        final_offer_data = []
        offers = Offers.objects.filter(
            region=self,
            supplier__product_id=product_id,
        ).order_by('offer_m_price')
        for offer in offers:
            diff = offer_price - offer.offer_m_price
            if diff <= 40 and diff > 20:
                final_offer_data.append(offer)
        return final_offer_data