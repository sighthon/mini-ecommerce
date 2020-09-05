from django.db import models


class Product(models.Model):
    """Model for a Product"""

    class Meta:
        db_table = "product"

    STATUS_CHOICES = [
        ("In Stock", "In Stock"),
        ("Unavailable", "Unavailable")
    ]

    name = models.CharField(null=False, max_length=100)
    description = models.CharField(null=True, max_length=100)
    price = models.FloatField(null=False)
    stock = models.IntegerField(null=False)
    status = models.CharField(null=False, blank=True, choices=STATUS_CHOICES, max_length=20)
    details = models.CharField(null=True, max_length=1000)  # SQLLite doesn't support JSON, so storing as a json string
