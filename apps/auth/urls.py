# ./apps/auth/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.auth import views

app_name = "app_auth"

###### URLs #######
urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register-api"),
    path("login/", views.LoginView.as_view(), name="login-api"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", views.logout_view, name="logout"),
]
