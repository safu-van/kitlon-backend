from rest_framework import serializers

from .models import LabourWallet, WalletTransaction


class LabourWalletSerializer(serializers.ModelSerializer):
    labour = serializers.SerializerMethodField()

    class Meta:
        model = LabourWallet
        fields = ["id", "labour", "amount"]

    def get_labour(self, obj):
        return f"{obj.labour.first_name} {obj.labour.last_name}".strip()


class WalletDeductionSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=False)

    class Meta:
        model = LabourWallet
        fields = ["amount", "message"]

    def update(self, instance, validated_data):
        if "amount" not in validated_data:
            raise serializers.ValidationError({"amount": "This field is required."})

        amount = validated_data["amount"]
        message = validated_data.get("message", "-")

        instance.amount -= amount
        instance.save()

        # Record the transaction
        WalletTransaction.objects.create(
            labour=instance.labour,
            amount_payed=amount,
            balance_amount=instance.amount,
            message=message,
        )

        return instance
