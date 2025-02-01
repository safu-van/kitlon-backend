from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import Inventory
from .serializers import InventorySerializer, StockIncreaseSerializer


class InventoryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """Retrieve all inventories"""
        items = Inventory.objects.all()
        serializer = InventorySerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create new inventory"""
        serializer = InventorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        """update an existing inventory"""
        try:
            item = Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            return Response(
                {"error": "item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = InventorySerializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class StockIncreaseView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            item = Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            return Response(
                {"error": "item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = StockIncreaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        stock = serializer.validated_data["stock"]
        item.stock += stock
        item.save()

        return Response(
            {"message": "Stock updated successfully"}, status=status.HTTP_200_OK
        )
