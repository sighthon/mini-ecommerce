from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Model for a Base User"""

    class Meta:
        db_table = "user"

    class Types(models.TextChoices):
        ADMIN = "admin", "admin"
        CUSTOMER = "customer", "customer"
        SALES_AGENT = "sales_agent", "sales_agent"

    base_type = Types.CUSTOMER

    type = models.CharField(null=False, max_length=50, choices=Types.choices, default=base_type)
    username = models.CharField(null=False, max_length=30, unique=True)
    password = models.CharField(null=True, max_length=30)
    mobile_number = models.CharField(null=True, max_length=13)

    USERNAME_FIELD = "username"

    def save(self, *args, **kwargs):
        self.type = self.base_type
        return super().save(*args, **kwargs)


class AdminManager(models.Manager):
    """Manager class for admin"""

    def get_queryset(self, *args, **kwargs):
        return super(AdminManager, self).get_queryset(*args, **kwargs).filter(type=User.Types.ADMIN)


class Admin(User):
    """Model for Admin users"""
    base_type = User.Types.ADMIN
    objects = AdminManager()

    class Meta:
        proxy = True


class CustomerManager(models.Manager):
    """Manager class for Customer"""

    def get_queryset(self, *args, **kwargs):
        return super(CustomerManager, self).get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)


class Customer(User):
    """Model for Customers"""
    base_type = User.Types.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True


class SalesAgentManager(models.Manager):
    """Manager class for SalesAgent"""

    def get_queryset(self, *args, **kwargs):
        return super(SalesAgentManager, self).get_queryset(*args, **kwargs).filter(type=User.Types.SALES_AGENT)


class SalesAgent(User):
    """Model for Sales Agents"""
    base_type = User.Types.CUSTOMER
    objects = SalesAgentManager()

    class Meta:
        proxy = True
