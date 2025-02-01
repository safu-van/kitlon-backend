from rest_framework import serializers

from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["id", "name", "stock"]


class StockIncreaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["stock"]