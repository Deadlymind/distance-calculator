from django.db import models



class Offers(models.Model):
    supplier = models.ForeignKey("suppliers.Suppliers", on_delete=models.CASCADE)
    region = models.ForeignKey("countries.Regions", on_delete=models.CASCADE)

    road_distance_price = models.FloatField()
    price_exwb = models.FloatField()
    price_exws = models.FloatField()
    weight = models.FloatField()
    offer_m_price = models.FloatField(default=0)
    offer_f_price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.supplier.product.name}: {self.supplier.company_name} -> {self.region.name}"
