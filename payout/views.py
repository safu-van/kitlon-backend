import io
import xlsxwriter

from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import LabourWallet, WalletTransaction
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


class WalletTransactionExcelView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Kitlon_transactions_history")

        headers = ["Date", "Labour Name", "Amount Payed", "Balance Amount"]
        worksheet.write_row(0, 0, headers)

        transactions = WalletTransaction.objects.all()

        row = 1
        for transaction in transactions:
            labour_name = f"{transaction.labour.first_name} {transaction.labour.last_name}".strip()
            formatted_date = transaction.created_at.strftime("%d/%m/%Y")

            worksheet.write_row(
                row, 0, [formatted_date, labour_name, transaction.amount_payed, transaction.balance_amount]
            )
            row += 1

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = (
            'attachment; filename="Kitlon_transactions_history.xlsx"'
        )

        return response
