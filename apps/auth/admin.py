# ./apps/auth/admin.py
# This module customizes the Django admin interface for user-related models.

from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass