from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import authenticate, get_user_model

from payout.models import LabourWallet
from .serializers import (
    LoginSerializer,
    LabourSerializer,
    LabourCreateSerializer,
    LabourUpdateSerializer,
)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)
        if user:
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token

            if user.last_name != "sales":
                user_name = f"{user.first_name} {user.last_name}".strip()
                role = "admin" if user.is_superuser else "labour"
            else:
                user_name = user.first_name
                role = "sales"

            return Response(
                {
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token),
                    "name": user_name,
                    "role": role,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


User = get_user_model()


class LabourView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """Retrieve all labours"""
        labours = User.objects.filter(is_superuser=False)
        serializer = LabourSerializer(labours, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create new labour account"""
        serializer = LabourCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        if user.last_name != "sales":
            LabourWallet.objects.create(labour=user)

        return Response(
            {"username": user.username},
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request, pk):
        """update an existing labour account"""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "user not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = LabourUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()

        return Response(
            {"username": updated_user.username},
            status=status.HTTP_200_OK,
        )


class LabourBlockUnblockView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "user not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user.is_active = not user.is_active
        user.save()

        status_message = "Blocked" if not user.is_active else "Unblocked"
        return Response(
            {"message": f"Labour {status_message}"}, status=status.HTTP_200_OK
        )
