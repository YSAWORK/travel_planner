# ./apps/auth/serializers.py
# This module contains serializers for user registration, login, token refresh.


###### IMPORT TOOLS ######
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


###### REGISTRATION ######
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    @staticmethod
    def validate_email(value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create_user(**validated_data)


###### LOGIN #######
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=6)


###### REFRESH TOKEN ######
class RefreshSerializer(serializers.Serializer):
    """Serializer for refreshing JWT tokens."""

    refresh = serializers.CharField()
