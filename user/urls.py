from django.urls import path
from .views import admin_signup, admin_login, customer_signup, customer_login

app_name = "user"

urlpatterns = [
    path("admin/signup", admin_signup, name="admin-signup"),
    path("admin/login", admin_login, name="admin-login"),
    path("customer/signup", customer_signup, name="customer-signup"),
    path("customer/login", customer_login, name="customer-login")
]
