# ./apps/auth/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.auth import validators


class User(AbstractUser):
    """Custom User model extending AbstractUser with additional validations."""

    email = models.EmailField(
        unique=True,
        validators=[validators.validate_email],
    )

    class Meta:
        default_related_name = "users"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"User: {self.username}"
