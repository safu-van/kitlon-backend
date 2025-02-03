from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import LabourWallet
from .serializers import LabourWalletSerializer, WalletDeductionSerializer


class WalletView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """Retrieve all labour wallet"""
        wallets = LabourWallet.objects.all()
        serializer = LabourWalletSerializer(wallets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """Subtract the paid amount from the labour wallet"""
        try:
            wallet = LabourWallet.objects.get(pk=pk)
        except LabourWallet.DoesNotExist:
            return Response(
                {"error": "wallet not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = WalletDeductionSerializer(wallet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Amount deducted successfully"}, status=status.HTTP_200_OK
        )
