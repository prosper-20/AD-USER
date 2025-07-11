# from django.shortcuts import render, get_object_or_404
# from rest_framework.views import APIView
# from rest_framework import status
# from .serializers import CustomUserRegistrationSerializer, PasswordChangeSerializer, InitiatePasswordResetSerializer, PasswordResetSerializer
# from rest_framework.response import Response
# from django.core.mail import send_mail
# from decouple import config
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import smart_str
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from .models import CustomUser
# from decouple import config
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.utils.http import urlsafe_base64_decode
# from django.contrib.auth import get_user_model
# from django.utils.encoding import force_str

# User = get_user_model()

# class RegistrationAPIView(APIView):
#     def post(self, reuqest, fomrat=None):
#         serializer = CustomUserRegistrationSerializer(data=reuqest.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 "Success": "Account creation successful, check your email for verification link!",
#             },
#             status=status.HTTP_201_CREATED,
#         )
    

# class ConfirmEmailView(APIView):
#     def get(self, request, uidb64, token):
#         try:
#             uid = smart_str(urlsafe_base64_decode(uidb64))
#             user = get_user_model().objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
#             return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)

#         if default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             return Response({"message": "Email confirmation successful"})
#         else:
#             return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


# class PasswordChangeView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request, format=None, **kwargs):
#         serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         current_user = CustomUser.objects.get(email=request.user)
#         # if not current_user.check_password(serializer.validated_data['old_password']):
#         #     return Response({"Error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
#         serializer.is_valid(raise_exception=True)
#         current_user.set_password(serializer.validated_data['new_password'])
#         current_user.save()
#         return Response({"Success": "Password successfully changed"}, status=status.HTTP_202_ACCEPTED)



# class InitiatePasswordResetView(APIView):
#     permission_classes = [AllowAny]
    
#     def post(self, request, format=None):
#         serializer = InitiatePasswordResetSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data["email"]
#         user = get_object_or_404(CustomUser, email=email)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         token = default_token_generator.make_token(user)
#         reset_link = f"https://127.0.0.1:8000/reset-password/{uid}/{token}/"
        
#         subject = 'Password Reset!'
#         html_message = render_to_string('accounts/password_reset_email.html', {'uid': uid, 'token': token, 'reset_link': reset_link})
#         plain_message = strip_tags(html_message)
#         from_email = config('DEFAULT_FROM_EMAIL_2')  # Replace with your email
#         to = email
#         send_mail(subject, plain_message, from_email, [to], html_message=html_message)
#         return Response({"Success": "Password Reset email sent!"}, status=status.HTTP_200_OK)
    


# class PasswordResetConfirmView(APIView):
#     def post(self, request, uidb64, token, format=None):
#         serializer = PasswordResetSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = get_user_model().objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
#             user = None

#         if user is not None and default_token_generator.check_token(user, token):
#             new_password = serializer.validated_data.get('new_password')
#             user.set_password(new_password)
#             user.save()
#             return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)




# from django.urls import path
# from .views import RegistrationAPIView, ConfirmEmailView, PasswordChangeView, InitiatePasswordResetView, PasswordResetConfirmView
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,

# )


# urlpatterns = [
#     path('confirm-email/<str:uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm-email'),
#     path("register/", RegistrationAPIView.as_view(), name="register"),
#     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path("password/reset/", InitiatePasswordResetView.as_view(), name="password-reset"),
#     path("password/change/", PasswordChangeView.as_view(), name='password-change'),
#     path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
# ]



# @receiver(post_save, sender=User)
# def send_confirmation_email(sender, instance, created, **kwargs):
#     if created:
#         try:
#             user = get_object_or_404(CustomUser, email=instance)
#             subject = "Confirm Your Email Address"
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             message = render_to_string(
#                 "accounts/email_confirmation.html",
#                 {
#                     "user": instance,
#                     "domain": "localhost:8000",
#                     "uid": uid,
#                     "token": token,
#                 },
#             )

#             plain_message = strip_tags(message)
#             from_email = config("EMAIL_HOST_USER")
#             to = user.email
#             send_mail(subject, plain_message, from_email, [to], html_message=message)
#             # return Response({"Success": "Account verification email sent!"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             raise e
        


# class PasswordChangeSerializer(serializers.Serializer):
#     new_password = serializers.CharField(max_length=100, required=True)
#     confirm_new_password = serializers.CharField(max_length=100, required=True)

#     def validate(self, data):
#         new_password = data.get("new_password")
#         confirm_new_password = data.get("confirm_new_password")

#         if new_password != confirm_new_password:
#             raise serializers.ValidationError(
#                 "The new password and its confirmation do not match."
#             )

#         return data
    


# class InitiatePasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         if CustomUser.objects.filter(email=value).exists():
#             return value
#         raise serializers.ValidationError("Email address does not exist.")


# class PasswordResetSerializer(serializers.Serializer):
#     new_password = serializers.CharField(max_length=20, style= {'input_type': 'password'}, write_only=True)
#     confirm_new_password = serializers.CharField(max_length=20, style= {'input_type': 'password'}, write_only=True)

#     def validate_passwords(self, value):
#         if self.new_password != self.confirm_new_password:
#             raise serializers.ValidationError({"Response": "Both passwords must match"})