from typing import Any, Dict

from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator

from .models import User, Admin


class AdminSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(required=True)

    class Meta:
        model = Admin
        fields = ["username", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AdminLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = Admin
        fields = ["username", "password"]
        extra_kwargs = {
            'password': {'read_only': True}
        }

    def validate(self, data: Dict) -> Dict:
        username = data.get('username')
        password = data.get('password')

        try:
            user = Admin.objects.get(username=username, password=password)
        except Admin.DoesNotExist:
            exc_msg = "Incorrect username or password"
            raise exceptions.ValidationError(exc_msg)

        if user:
            data["user"] = user

        return data
