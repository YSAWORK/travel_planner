# ./apps/auth/views.py
# This module contains API views for user registration, login, and logout.


###### IMPORT TOOLS #######
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    OpenApiExample,
    extend_schema_view,
)

from apps.auth import serializers


###### REGISTRATION ######
@extend_schema_view(
    post=extend_schema(
        tags=["Auth"],
        summary="Реєстрація користувача",
        description="Створити нового користувача та повернути JWT access/refresh токени.",
        request=serializers.RegisterSerializer,
        responses={
            201: OpenApiResponse(
                description="Користувача успішно зареєстровано.",
            ),
            400: OpenApiResponse(
                description="Помилка валідації даних.",
            ),
        },
        examples=[
            OpenApiExample(
                "Registration Example",
                value={
                    "username": "john_doe",
                    "password": "StrongPassword123!",
                    "password2": "StrongPassword123!",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Registration Success Response",
                value={
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.access_token",
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh_token",
                    "user_id": 1,
                    "username": "john_doe",
                },
                response_only=True,
                status_codes=["201"],
            ),
        ],
    )
)
@method_decorator(csrf_exempt, name="dispatch")
class RegistrationView(APIView):
    """API view for user registration."""

    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        # Create a new user
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user_id": user.id,
                    "username": user.username,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###### LOG IN ######
@extend_schema_view(
    post=extend_schema(
        tags=["Auth"],
        summary="Вхід користувача",
        description="Автентифікувати користувача за username/password та повернути JWT access/refresh токени.",
        request=serializers.LoginSerializer,
        responses={
            200: OpenApiResponse(
                description="Вхід успішний.",
            ),
            400: OpenApiResponse(
                description="Помилка валідації даних.",
            ),
            401: OpenApiResponse(
                description="Невірні облікові дані.",
            ),
        },
        examples=[
            OpenApiExample(
                "Login Example",
                value={
                    "username": "john_doe",
                    "password": "StrongPassword123!",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Login Success Response",
                value={
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.access_token",
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh_token",
                    "user_id": 1,
                    "username": "john_doe",
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Invalid Credentials Response",
                value={"error": "Invalid credentials."},
                response_only=True,
                status_codes=["401"],
            ),
        ],
    )
)
@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    """API view for user login."""

    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        """Authenticate user and return JWT tokens."""
        serializer = serializers.LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
            )
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user_id": user.id,
                "username": user.username,
            },
            status=status.HTTP_200_OK,
        )


###### LOG OUT ######
@extend_schema(
    tags=["Auth"],
    summary="Вихід користувача",
    description="Завершити сесію поточного користувача.",
    responses={
        204: OpenApiResponse(description="Користувача успішно розлогінено."),
    },
    examples=[
        OpenApiExample(
            "Logout Success Response",
            value="User logged out",
            response_only=True,
            status_codes=["204"],
        ),
    ],
)
@api_view(["POST"])
def logout_view(request):
    """Log out the user"""
    permission_classes = [permissions.IsAuthenticated]
    logout(request)
    return Response("User logged out", status=status.HTTP_204_NO_CONTENT)
