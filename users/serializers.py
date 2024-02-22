from datetime import datetime, timedelta, timezone
import jwt
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from EmailService.settings import SECRET_KEY
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message='This email is already in use.')]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=120, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        return {"email": email, "password": password}

    @staticmethod
    def get_token(user):
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.now(timezone.utc) + timedelta(days=7),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')
