from rest_framework import serializers

from .models import Sku, SkuSubmission
from inventory.models import InventoryNeeded


class InventoryNeededSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryNeeded
        fields = ["inventory", "quantity"]


class SkuSerailizer(serializers.ModelSerializer):
    inventory_needed = InventoryNeededSerializer(many=True)

    class Meta:
        model = Sku
        fields = ["id", "code", "labour_charge", "stock", "inventory_needed"]

    def validate_code(self, value):
        """Ensure SKU code is unique except for the current instance during updates."""
        queryset = Sku.objects.filter(code=value)

        # Exclude the current instance during update
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError("Sku Code already exists")

        return value

    def create(self, validated_data):
        code = validated_data["code"]
        stock = validated_data["stock"]
        labour_charge = validated_data["labour_charge"]
        inventory_needed = validated_data["inventory_needed"]

        sku = Sku.objects.create(code=code, stock=stock, labour_charge=labour_charge)

        # Create InventoryNeeded records
        for inventory in inventory_needed:
            InventoryNeeded.objects.create(
                sku=sku,
                inventory=inventory["inventory"],
                quantity=inventory["quantity"],
            )

        return sku

    def update(self, instance, validated_data):
        instance.stock = validated_data.get("stock", instance.stock)
        instance.labour_charge = validated_data.get(
            "labour_charge", instance.labour_charge
        )
        instance.save()

        inventory_needed = validated_data.get("inventory_needed", None)
        if inventory_needed is not None:
            # Remove old inventory records
            InventoryNeeded.objects.filter(sku=instance).delete()

            # Add new inventory records
            for inventory in inventory_needed:
                InventoryNeeded.objects.create(
                    sku=instance,
                    inventory=inventory["inventory"],
                    quantity=inventory["quantity"],
                )

        return instance


class SkuSubmissionSerializer(serializers.ModelSerializer):
    labour = serializers.SerializerMethodField()
    created_at = serializers.DateField(format="%d-%m-%Y", read_only=True)

    class Meta:
        model = SkuSubmission
        fields = [
            "id",
            "created_at",
            "labour",
            "sku_code",
            "quantity",
            "status",
        ]

    def get_labour(self, obj):
        return f"{obj.labour.first_name} {obj.labour.last_name}".strip()

    def create(self, validated_data):
        request = self.context.get("request")
        labour = request.user
        sku_code = validated_data["sku_code"]
        quantity = validated_data["quantity"]

        # Get the SKU
        sku = Sku.objects.filter(code=sku_code).first()
        if not sku:
            raise serializers.ValidationError({"sku_code": "Invalid SKU code."})

        # Fetch required inventory for this SKU
        required_inventories = InventoryNeeded.objects.filter(sku=sku)

        # Check if enough inventory is available
        for item in required_inventories:
            inventory = item.inventory
            required_qty = item.quantity * quantity  # mutliply by sku quantity

            if inventory.stock < required_qty:
                raise serializers.ValidationError(
                    {"inventory": f"Insufficient stock of {inventory.name}."}
                )

        # Reduce inventory stock
        for item in required_inventories:
            inventory = item.inventory
            inventory.stock -= item.quantity * quantity  # mutliply by sku quantity
            inventory.save()

        # Create SKU submission
        return SkuSubmission.objects.create(
            labour=labour, sku_code=sku_code, quantity=quantity
        )
