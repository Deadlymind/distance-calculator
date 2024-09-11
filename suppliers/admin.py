from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.Suppliers)
admin.site.register(models.SupplierPrices)
admin.site.register(models.SpecificationDocumentSuppliers)
admin.site.register(models.CertificationDocumentSuppliers)