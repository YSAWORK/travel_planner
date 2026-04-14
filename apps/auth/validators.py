# ./apps/auth/validators.py
# Purpose: This module contains custom validators for email, password.

import re
from django.core.exceptions import ValidationError


###### EMAIL VALIDATOR ######
def validate_email(mail: str):
    """
    Validate email address format.
    The email must not start or end with a dot, must not contain consecutive dots,
    and must include only letters (A-Z, a-z), digits (0-9), or the following symbols: ., _, -, +.
    """
    pattern = re.compile(
        r"^(?![.])" r"[A-Za-z0-9._+-]+" r"(?<![.])" r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )
    if ".." in mail.split("@")[0] or bool(pattern.match(mail.strip())) == False:
        raise ValidationError(
            "Email can`t start or end with a dot, contain a double dot, and must include only letters (A-Z, a-z), digits (0-9) or the following symbols: ., _, -, +."
        )


###### PASSWORD VALIDATOR #######
def validate_password(password: str):
    """
    Validate password strength.
    Password must be at least 8 characters long and contain:
    - at least one uppercase letter
    - at least one lowercase letter
    - at least one digit
    - at least one special character
    """
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:"\'<>,.?/~`]).{8,}$'
    if not bool(re.match(pattern, password)):
        raise ValidationError(
            "Password must be at least 8 characters long and contain: 1 uppercase and 1 lowercase letters, 1 digit, and 1 special character"
        )
