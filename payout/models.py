from django.db import models
from accounts.models import CustomUserAccount


# Labour Wallet
class LabourWallet(models.Model):
    labour = models.OneToOneField(CustomUserAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)


# Transaction History
class WalletTransaction(models.Model):
    created_at = models.DateField(auto_now_add=True)
    labour = models.ForeignKey(CustomUserAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

