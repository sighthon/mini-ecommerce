from django.db import models


class Product(models.Model):
    """Model for a Product"""

    class Meta:
        db_table = "product"

    class StatusChoices(models.TextChoices):
        IN_STOCK = "In Stock", "In Stock"
        UNAVAILABLE = "Unavailable", "Unavailable"

    name = models.CharField(null=False, max_length=100)
    description = models.CharField(null=True, max_length=100)
    price = models.FloatField(null=False)
    stock = models.IntegerField(null=False)
    status = models.CharField(null=False, blank=True, choices=StatusChoices.choices, max_length=20)
    details = models.CharField(null=True, max_length=1000)  # SQLLite doesn't support JSON, so storing as a json string

    def save(self, *args, **kwargs):
        self.status = Product.StatusChoices.IN_STOCK if self.stock > 0 else Product.StatusChoices.UNAVAILABLE
        return super(Product, self).save(*args, **kwargs)
