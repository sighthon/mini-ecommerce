from rest_framework.authentication import SessionAuthentication

from .serializers import AdminSignupSerializer, AdminLoginSerializer
from rest_framework import decorators, permissions, response, request, status
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login


# API for Admin Signup
@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def admin_signup(req: request.Request) -> response.Response:
    """Signup for admins"""
    admin_signup_ser = AdminSignupSerializer(data=req.data)

    # If the request data is valid, save the data
    if admin_signup_ser.is_valid():
        admin_signup_ser.save()
        return response.Response(
            {"Message": f"Successfully registered {admin_signup_ser.validated_data.get('username')}"},
            status=status.HTTP_200_OK
        )

    return response.Response(admin_signup_ser.errors, status=status.HTTP_400_BAD_REQUEST)


# API for Admin Login
@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def admin_login(req: request.Request) -> response.Response:
    """Login for admins"""
    admin_login_ser = AdminLoginSerializer(data=req.data)

    # If the request data is valid, save the data
    if admin_login_ser.is_valid():
        user = admin_login_ser.validated_data.get('user')
        # django_login(request, user)

        try:
            token = Token.objects.get_or_create(user=user)
        except Exception:
            return response.Response({"Message": "Login failed."}, status=status.HTTP_400_BAD_REQUEST)

        return response.Response(
            {"auth_token": token[0].key},
            status=status.HTTP_200_OK
        )

    return response.Response(admin_login_ser.errors, status=status.HTTP_400_BAD_REQUEST)
