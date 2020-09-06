from typing import Any, Dict

from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator

from .models import User, Admin, Customer, SalesAgent


class AdminSignupSerializer(serializers.ModelSerializer):
    """Serializer for admin signup"""
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
    """Serializer for admin login"""
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
            exc_msg = "Incorrect username or password for an Admin."
            raise exceptions.ValidationError(exc_msg)

        if user:
            data["user"] = user

        return data


class CustomerSignupSerializer(AdminSignupSerializer, serializers.ModelSerializer):
    """Serializer for customer signup"""
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    mobile_number = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = Customer
        fields = ["username", "mobile_number"]


class CustomerLoginSerializer(serializers.ModelSerializer):
    """Serializer for customer signup"""
    mobile_number = serializers.CharField(required=True)
    otp = serializers.IntegerField(required=True)

    class Meta:
        model = Customer
        fields = ["mobile_number", "otp"]

    def validate(self, data: Dict) -> Dict:
        mobile_number = data.get('mobile_number')

        try:
            user = Customer.objects.get(mobile_number=mobile_number)
        except Customer.DoesNotExist:
            exc_msg = "Invalid mobile number provided for a customer."
            raise exceptions.ValidationError(exc_msg)

        if user:
            data["user"] = user

        return data


class SalesAgentSignupSerializer(AdminSignupSerializer, serializers.ModelSerializer):
    """Serializer for customer signup"""

    class Meta:
        model = SalesAgent
        fields = ["username", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }


class SalesAgentLoginSerializer(serializers.ModelSerializer):
    """Serializer for admin login"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = SalesAgent
        fields = ["username", "password"]
        extra_kwargs = {
            'password': {'read_only': True}
        }

    def validate(self, data: Dict) -> Dict:
        username = data.get('username')
        password = data.get('password')

        try:
            user = SalesAgent.objects.get(username=username, password=password)
        except SalesAgent.DoesNotExist:
            exc_msg = "Incorrect username or password for a sales agent."
            raise exceptions.ValidationError(exc_msg)

        if user:
            data["user"] = user

        return data
