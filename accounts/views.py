from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CustomUserRegistrationSerializer
from rest_framework.response import Response
from django.core.mail import send_mail
from decouple import config
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_str
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser
from decouple import config
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str

User = get_user_model()

class RegistrationAPIView(APIView):
    def post(self, reuqest, fomrat=None):
        serializer = CustomUserRegistrationSerializer(data=reuqest.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "Success": "Account creation successful, check your email for verification link!",
            },
            status=status.HTTP_201_CREATED,
        )
    

