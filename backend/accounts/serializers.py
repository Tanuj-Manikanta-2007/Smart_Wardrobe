from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email__iexact=value).exists() or User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    def create(self, validated_data: dict):
        email = validated_data["email"].strip().lower()
        password = validated_data["password"]
        # Use email as username to keep things simple
        return User.objects.create_user(username=email, email=email, password=password)


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT login using email + password (maps to username under the hood)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Replace default username field with email
        self.fields.pop(self.username_field, None)
        self.fields["email"] = serializers.EmailField()

    def validate(self, attrs: dict):
        email = attrs.get("email")
        password = attrs.get("password")
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = User.objects.filter(email__iexact=email).first() or User.objects.filter(username__iexact=email).first()
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")

        # Call parent validation with mapped username
        data = super().validate({self.username_field: user.get_username(), "password": password})
        data["user"] = {"id": user.id, "email": user.email}
        return data
