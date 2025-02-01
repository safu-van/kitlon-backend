from rest_framework import serializers
from django.contrib.auth import get_user_model

from .utils import generate_username, generate_password

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LabourSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "phone_number"]


class LabourCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number"]

    def validate_phone_number(self, value):
        """Ensure phone number is unique"""
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists")
        return value

    def create(self, validated_data):
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        phone_number = validated_data["phone_number"]

        username = generate_username(first_name)
        password = generate_password(first_name, phone_number)

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            username=username,
            password=password,
        )

        return user
    

class LabourUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number"]

    def validate_phone_number(self, value):
        """Ensure phone number is unique"""
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists")
        return value
    
    def update(self, instance, validated_data):
        first_name = validated_data.get("first_name", instance.first_name)
        last_name = validated_data.get("last_name", instance.last_name)
        phone_number = validated_data.get("phone_number", instance.phone_number)

        # handle username change if first name changes
        if first_name != instance.first_name:
            instance.username = generate_username(first_name)
        
        # handle password change if either first name or phone number changes
        if first_name != instance.first_name or phone_number != instance.phone_number:
            instance.set_password(generate_password(first_name, phone_number))

        instance.first_name = first_name
        instance.last_name = last_name
        instance.phone_number = phone_number
        instance.save()

        return instance