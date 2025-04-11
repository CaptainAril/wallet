import re
from typing import Optional

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_password(password: str, user: Optional[object] = None) -> None:
    """
    Validate that the password meets all validator requirements.

    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
    """
    if len(password) < 8:
        raise ValidationError(
            _("Password must be at least 8 characters long."),
            code="password_too_short",
        )
    if not re.search(r"[A-Z]", password):
        raise ValidationError(
            _("Password must contain at least one uppercase letter."),
            code="password_no_uppercase",
        )
    if not re.search(r"[a-z]", password):
        raise ValidationError(
            _("Password must contain at least one lowercase letter."),
            code="password_no_lowercase",
        )
    if not re.search(r"[0-9]", password):
        raise ValidationError(
            _("Password must contain at least one digit."),
            code="password_no_digit",
        )
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError(
            _("Password must contain at least one special character."),
            code="password_no_special",
        )
    if re.search(r"\s", password):
        raise ValidationError(
            _("Password must not contain any whitespace characters."),
            code="password_contains_whitespace",
        )
    if re.search(r"(.+)\1", password):
        raise ValidationError(
            _("Password must not contain repeated characters."),
            code="password_repeated_characters",
        )
    if user and user.username in password:
        raise ValidationError(
            _("Password must not contain the username."),
            code="password_contains_username",
        )
    if user and user.email in password:
        raise ValidationError(
            _("Password must not contain the email address."),
            code="password_contains_email",
        )
    if user and user.first_name in password:
        raise ValidationError(
            _("Password must not contain the first name."),
            code="password_contains_first_name",
        )
    if user and user.last_name in password:
        raise ValidationError(
            _("Password must not contain the last name."),
            code="password_contains_last_name",
        )
    if user and user.phone in password:
        raise ValidationError(
            _("Password must not contain the phone number."),
            code="password_contains_phone",
        )
