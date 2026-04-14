# ./apps/auth/views.py
# This module contains API views for user registration, login, and logout.


###### IMPORT TOOLS #######
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth import serializers, models


###### REGISTRATION ######
@method_decorator(csrf_exempt, name="dispatch")
class RegistrationView(APIView):
    """ API view for user registration."""
    permission_classes = [AllowAny]

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
@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    """ API view for user login."""
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        """ Authenticate user and return JWT tokens."""
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
def logout_view(request):
    """ Log out the user """
    logout(request)
    return Response("User logged out", status=status.HTTP_204_NO_CONTENT)
