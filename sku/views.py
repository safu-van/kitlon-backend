import io
import xlsxwriter

from django.http import HttpResponse
from rest_framework import status as http_status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Sku, SkuSubmission
from .serializers import SkuSerailizer, SkuSubmissionSerializer, SkuSalesSerializer
from .utils import on_approval, on_decline


class SkuView(APIView):
    def get_permissions(self):
        """Apply different permissions for different requests"""
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get(self, request):
        """Retrieve all SKUs"""
        skus = Sku.objects.all()
        serializer = SkuSerailizer(skus, many=True)
        return Response(serializer.data, status=http_status.HTTP_200_OK)

    def post(self, request):
        """Create new SKU"""
        serializer = SkuSerailizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=http_status.HTTP_201_CREATED)

    def patch(self, request, pk):
        """update an existing SKU"""
        try:
            sku = Sku.objects.get(pk=pk)
        except Sku.DoesNotExist:
            return Response(
                {"error": "sku not found"}, status=http_status.HTTP_404_NOT_FOUND
            )

        serializer = SkuSerailizer(sku, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=http_status.HTTP_200_OK)


class SkuSalesView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        """Reduce SKU stock on sale"""
        serializer = SkuSalesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sku_code = serializer.validated_data["sku_code"]
        quantity = serializer.validated_data["quantity"]

        try:
            sku = Sku.objects.get(code=sku_code)
        except Sku.DoesNotExist:
            return Response(
                {"error": "sku not found"}, status=http_status.HTTP_404_NOT_FOUND
            )

        if sku.stock < quantity:
            return Response(
                {"error": "Insufficient stock"}, status=http_status.HTTP_400_BAD_REQUEST
            )

        sku.stock -= quantity
        sku.save()

        return Response(
            {"message": "Updated Sucessfully"}, status=http_status.HTTP_200_OK
        )


class SkuSubmissionView(APIView):
    def get_permissions(self):
        """Apply different permissions for different requests"""
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get(self, request):
        """Retrieve all SKU Submissions"""
        sku_submissions = SkuSubmission.objects.filter(status="Pending")
        serializer = SkuSubmissionSerializer(sku_submissions, many=True)
        return Response(serializer.data, status=http_status.HTTP_200_OK)

    def post(self, request):
        """Create a new record of SKU Submission"""
        serializer = SkuSubmissionSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=http_status.HTTP_201_CREATED)

    def patch(self, request, pk, status):
        """Update status (Approved/Declined)"""
        try:
            sku_data = SkuSubmission.objects.get(pk=pk)
        except SkuSubmission.DoesNotExist:
            return Response(
                {"error": "sku data not found"}, status=http_status.HTTP_404_NOT_FOUND
            )

        status = "Apporved" if status == "approve" else "Declined"
        sku_data.status = status
        sku_data.save()

        if status == "Apporved":
            on_approval(sku_data.sku_code, sku_data.quantity, sku_data.labour)
        else:
            on_decline(sku_data.sku_code, sku_data.quantity)

        return Response({"message": "Status updated successfully"})


class SkuSubmissionExcelView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, reqeust):
        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Sku_Submission_Data")

        headers = ["Date", "Labour Name", "SKU Code", "Quantity", "Status"]
        worksheet.write_row(0, 0, headers)

        sku_data = SkuSubmission.objects.all()

        row = 1
        for data in sku_data:
            labour_name = f"{data.labour.first_name} {data.labour.last_name}".strip()
            formatted_date = data.created_at.strftime("%d/%m/%Y")

            worksheet.write_row(
                row,
                0,
                [
                    formatted_date,
                    labour_name,
                    data.sku_code,
                    data.quantity,
                    data.status,
                ],
            )
            row += 1

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = (
            'attachment; filename="Sku_Submission_Data.xlsx"'
        )

        return response
