
from .models import (User, )
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
import django.contrib.auth.password_validation as validators

class SignUpUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    id = serializers.CharField( read_only=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        max_length=128,
        label="Password",
        style={"input_type": "password"},
        write_only=True,
        required=True
    )
    confirm_password = serializers.CharField(
        max_length=128,
        label="Confirm Password",
        style={"input_type": "password"},
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ("id", "username","password", "confirm_password", )

    def validate_email(self, value):
        """
        Check if the email is already registered.
        """
        if User.objects.filter(username=value.lower()).exists():
            raise serializers.ValidationError("Username already exists.")
        return value.lower()

    def validate(self, attrs):
        """
        Additional validations for the serializer.
        """
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        """
        Create and return a new user.
        """
        validated_data.pop("confirm_password", None)
        user = User.objects.create(
            username=validated_data["username"],
            password=make_password(validated_data["password"])
        )
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name')



class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login using username instead of email.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        max_length=128,
        label='Password',
        style={'input_type': 'password'},
        write_only=True,
        required=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'error': 'Username does not exist.'})

        # Authenticate user (checks password)
        if not user.check_password(password):
            raise serializers.ValidationError({'error': 'Incorrect password.'})

        # Return validated attributes
        return attrs
