from django.urls import path
from .views import admin_signup, admin_login

app_name = "user"

urlpatterns = [
    path("admin/signup", admin_signup, name="admin-signup"),
    path("admin/login", admin_login, name="admin-login")
]
