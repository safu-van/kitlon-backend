from django.db import models

from sku.models import Sku


# Inventory Details
class Inventory(models.Model):
    name = models.CharField(max_length=255)
    stock = models.IntegerField()


# Inventory Needed for SKU
class InventoryNeeded(models.Model):
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
