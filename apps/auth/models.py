# ./apps/auth/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.auth import validators


###### USER ######
class User(AbstractUser):
    """Custom User model extending AbstractUser with additional validations."""
    email = models.EmailField(validators=[validators.validate_email])
    password = models.CharField(validators=[validators.validate_password])

    class Meta:
        default_related_name = "users"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"User: {self.username}"
