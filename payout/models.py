from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Labour Wallet
class LabourWallet(models.Model):
    labour = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)


# Transaction History
class WalletTransaction(models.Model):
    created_at = models.DateField(auto_now_add=True)
    labour = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

