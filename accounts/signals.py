from django.db.models.signals import post_save, pre_delete
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from .models import CustomUser
from decouple import config
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.encoding import smart_bytes
from django.urls import reverse
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from .models import UserProfile


User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()




