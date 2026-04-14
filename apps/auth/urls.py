# ./apps/auth/urls.py
# This module defines the URL patterns for the user management application.

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.auth import views

app_name = "app_auth"

###### URLs #######
urlpatterns = [
    path("api/register/", views.RegistrationView.as_view(), name="register-api"),
    path("api/login/", views.LoginView.as_view(), name="login-api"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/logout/", views.logout_view, name="logout"),
]
