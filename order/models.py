from django.db import models

from product.models import Product
from user.models import Customer


class Order(models.Model):
    """Model for  Order"""

    class Meta:
        db_table = "order"

    class StatusChoices(models.TextChoices):
        ORDERED = "ordered, ordered"
        ACCEPTED = "accepted", "accepted"
        DELIVERED = "delivered", "delivered"
        CANCELLED = "cancelled", "cancelled"

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    description = models.CharField(null=True, max_length=100)
    status = models.CharField(null=False, blank=True, choices=StatusChoices.choices, max_length=20,
                              default="ordered")


class OrderItem(models.Model):
    """Model for Item Detail"""

    class Meta:
        db_table = "order_item"

    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE, null=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    item_price = models.FloatField(null=False)
    quantity = models.IntegerField()
