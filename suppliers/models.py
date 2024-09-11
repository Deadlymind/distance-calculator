from django.utils import timezone
from django.db import models

from accounts.models import User
from countries.models import Regions
from products.models import Product

class Suppliers(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True, blank=True)

    identifier = models.CharField(max_length=50, null=True, blank=True)
    format = models.CharField(max_length=5000, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    company_name = models.CharField(max_length=1000, null=True, blank=True)
    contact_name = models.CharField(max_length=1000, null=True, blank=True)
    landline = models.CharField(max_length=1000, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=1000, null=True, blank=True)

    departure_address_lat = models.FloatField(null=True, blank=True)
    departure_address_lng = models.FloatField(null=True, blank=True)

    destination_address_lat = models.FloatField(null=True, blank=True)
    destination_address_lng = models.FloatField(null=True, blank=True)

    margin = models.FloatField(null=True, blank=True)
    weight_of_full_truck = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)

    price_exwb = models.FloatField(null=True, blank=True)
    price_exws = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.id}, {self.company_name}"

    def get_supplier_prices(self):
        return SupplierPrices.objects.filter(
            suppliers=self,
        ).order_by("-added_on", "-id")


class SupplierPrices(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    suppliers = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name="supplier_prices")
    price_exwb = models.FloatField(null=True, blank=True)
    price_exws = models.FloatField(null=True, blank=True)
    added_on = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.suppliers.company_name}, {self.added_on.date}"


class CertificationDocumentSuppliers(models.Model):
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='certifications')
    file = models.FileField(null=True, blank=True, upload_to='certifications/')


class SpecificationDocumentSuppliers(models.Model):
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='specifications')
    file = models.FileField(null=True, blank=True, upload_to='specifications/')
