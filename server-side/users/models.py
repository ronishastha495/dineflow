# models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, username=None, password=None, **extra_fields):
        if not email and not username:
            raise ValueError("Users must have either an email or username.")

        if email:
            email = self.normalize_email(email)
            extra_fields['email'] = email
        if username:
            extra_fields['username'] = username

        user = self.model(**extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not username:
            raise ValueError('Superuser must have a username.')

        return self.create_user(username=username, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('restaurant_owner', 'Restaurant Owner'),
    )

    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    
    # Additional fields for restaurant owners
    restaurant_name = models.CharField(max_length=255, blank=True, null=True)
    restaurant_address = models.TextField(blank=True, null=True)
    restaurant_phone = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email or self.username or "Unknown User"

    def is_restaurant_owner(self):
        return self.user_type == 'restaurant_owner'

    def is_customer(self):
        return self.user_type == 'customer'