import os
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import Token, User


def send_email_verification(user: User):
    """
    Send email verification to the user.
    """
    token, uid = generate_user_token(user)
    verification_link = f"{settings.BASE_URL}/auth/verify-email/{uid}/{token}/"

    # TODO: send email with verification link
    
    return verification_link

def verify_email(token: str, uid: str):
    user = verify_token(token=token, uid=uid)
    user.is_verified = True
    user.save()
    
    # TODO: send verification success email

def send_password_reset():
    pass


def generate_user_token(user: User):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))

    TTL = int(settings.TOKEN_TTL)
    expires_at = timezone.now() + timedelta(minutes=TTL)

    T, created = Token.objects.update_or_create(
        user=user,
        defaults={'token': token, 'expires_at': expires_at})

    return T.token, uid

def verify_token(token: str, uid: str):
    """
    Verify the token and uid.
    """
    try:
        user_id = urlsafe_base64_decode(uid).decode('utf-8')
        token_object = Token.objects.get(token=token)

        if timezone.now() > token_object.expires_at:
            raise ValueError("Token has expired")
    
        if token_object.user != User.objects.get(pk=user_id):
            raise ValueError("Invalid uid")
        
        return token_object.user
    
    except Exception as e:
        raise ValueError("Invalid verification link!")
