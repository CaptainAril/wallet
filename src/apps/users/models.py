from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _

from utilities.enums import Currency, DocumentTypes, NextOfKinRelationship


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a new user"""
        if not email:
            raise ValueError('User must have email address')
        email = self.normalize_email(email.lower())
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a new superuser"""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
    


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), max_length=255, unique=True)
    first_name = models.CharField(_('First Name'), max_length=255)
    last_name = models.CharField(_('Last Name'), max_length=255)
    username = models.CharField(_('Username'), max_length=255, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.CharField(max_length=255, null=True, blank=True)
    state_LGA = models.IntegerField(_("StateLGACode"), null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    dob = models.DateField(_('Date of Birth'), null=True, blank=True)
    pin = models.CharField(max_length=6, null=True, blank=True)
    tier = models.IntegerField(null=True, blank=True)

    is_active = models.BooleanField(_('Active'), default=True)
    is_enabled = models.BooleanField(_('Enabled'), default=True)
    is_deleted = models.BooleanField(_('Deleted'), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username or self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_short_name(self):
        return self.first_name
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
        ]


class UserNextOfKin:
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='next_of_kin')
    first_name = models.CharField(_('First Name'), max_length=255)
    last_name = models.CharField(_('Last Name'), max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    relationship = models.CharField(max_length=50, choices=NextOfKinRelationship.choices)
    address = models.TextField(null=True, blank=True)
    state_LGA = models.IntegerField(_("StateLGACode"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = _('User Next of Kin')
        verbose_name_plural = _('User Next of Kin')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
        ]


class UserKYCInformation:
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kyc_information')
    document_type = models.CharField(max_length=50, choices=DocumentTypes.choices)
    document_number = models.CharField(max_length=50)
    document_image = models.CharField(max_length=255)
    document_verified = models.BooleanField(default=False)

    bvn = models.CharField(max_length=11, null=True, blank=True)
    bvn_verified = models.BooleanField(default=False)
    

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.document_type}'
    
    class Meta:
        verbose_name = _('User KYC Information')
        verbose_name_plural = _('User KYC Information')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
        ]
    
