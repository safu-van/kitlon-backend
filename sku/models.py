from django.db import models
from accounts.models import CustomUserAccount


# SKU Details
class Sku(models.Model):
    code = models.CharField(max_length=255, unique=True)
    labour_charge = models.DecimalField(max_digits=20, decimal_places=2)
    stock = models.IntegerField(default=0)


# SKU Submission Data
class SkuSubmission(models.Model):
    created_at = models.DateField(auto_now_add=True)
    labour = models.ForeignKey(CustomUserAccount, on_delete=models.CASCADE)
    sku_code = models.CharField(max_length=255)
    quantity = models.IntegerField()
    status = models.CharField(max_length=255, default="Pending")
