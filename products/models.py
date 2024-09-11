from django.db import models

class Units(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.id} | {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=1000)
    default_unit = models.ForeignKey(Units, on_delete=models.DO_NOTHING)
    default_margin = models.FloatField(default=0)

    def __str__(self):
        return f"{self.id} | {self.name} | {self.default_unit.name}"