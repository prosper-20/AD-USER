from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from PIL import Image
from .managers import CustomUserManager
from datetime import timedelta
import random
import secrets
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator, MaxValueValidator

import string


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        related_name="custom_users",  # Unique related_name for CustomUser model
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        related_name="custom_users",  # Change or add related_name here
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Users"



class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default="user.jpg", upload_to="profile_pictures")
    address = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profile"

    class Meta:
        verbose_name_plural = "User Profiles"