from .models import Sku
from payout.models import LabourWallet


def on_approval(sku_code, quantity, labour):
    # Increase SKU stock
    sku = Sku.objects.get(code=sku_code)
    sku.stock += quantity  # mutliply by sku quantity
    sku.save()

    # Add labour_charge to labour wallet
    wallet = LabourWallet.objects.get(labour=labour)
    wallet.amount += sku.labour_charge * quantity  # mutliply by sku quantity
    wallet.save()