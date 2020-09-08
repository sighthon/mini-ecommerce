from django.db import models

from product.models import Product
from user.models import Customer, SalesAgent


class Order(models.Model):
    """Model for  Order"""

    class Meta:
        db_table = "order"

    class StatusChoices(models.TextChoices):
        ORDERED = "ordered, ordered"
        ACCEPTED = "accepted", "accepted"
        DELIVERED = "delivered", "delivered"
        CANCELLED = "cancelled", "cancelled"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, related_name="customer_orders")
    sales_agent = models.ForeignKey(SalesAgent, on_delete=models.CASCADE, null=True, related_name="sales_agent_orders")
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

    @property
    def total_cost(self) -> int:
        """
        Property to calculate loss of sale of a product.

        Returns:
            None.
        """
        return int(int(self.item_price) * int(self.quantity))
