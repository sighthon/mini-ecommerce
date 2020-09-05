from django.db import models
from rest_framework import fields


class Product(models.Model):
    """Model for a Product"""
    name = models.CharField(null=False)
    description = models.CharField(null=True)
    price = models.FloatField(null=False)
    stock = models.IntegerField(null=False)
    details = fields.JSONField(null=True)
