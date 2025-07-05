from rest_framework import serializers
from .models import CustomUser

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        user = CustomUser(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
            phone_number=self.validated_data["phone_number"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"Error": "Both passwords must match"})

        user.set_password(password)
        user.save()
        return user
    


