from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import Customer, CustomerProfile

User = get_user_model()


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ["id", "full_name", "mobile_number", "shipping_address"]


class CustomerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    profile = CustomerProfileSerializer()

    class Meta:
        model = Customer
        fields = ["id", "user", "profile"]

    def validate(self, attrs):
        user_data = attrs.get("user")
        user_data["is_customer"] = True
        user = User(**user_data)
        user.full_clean()

        profile_data = attrs.get("profile")
        profile = CustomerProfile(**profile_data)
        profile.full_clean()
        return attrs

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        profile_data = validated_data.pop("profile")

        user = User.objects.create_user(**user_data)
        profile = CustomerProfile.objects.create(**profile_data)

        customer = Customer.objects.create(user=user, profile=profile)
        return customer
