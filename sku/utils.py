from .models import Sku
from payout.models import LabourWallet
from inventory.models import InventoryNeeded


def on_approval(sku_code, quantity, labour):
    # Increase SKU stock
    sku = Sku.objects.get(code=sku_code)
    sku.stock += quantity  # mutliply by sku quantity
    sku.save()

    # Add labour_charge to labour wallet
    wallet = LabourWallet.objects.get(labour=labour)
    wallet.amount += sku.labour_charge * quantity  # mutliply by sku quantity
    wallet.save()


def on_decline(sku_code, quantity):
    """Restore inventory stock on decline"""
    sku = Sku.objects.get(code=sku_code)
    required_inventories = InventoryNeeded.objects.filter(sku=sku)

    for item in required_inventories:
        stock_to_restore = item.quantity * quantity  # mutliply by sku quantity
        inventory = item.inventory
        inventory.stock += stock_to_restore
        inventory.save()

