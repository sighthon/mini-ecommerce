from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def transform_status(self, obj, value):
        status_choices = {
            "in_stock": "In Stock",
            "unavailable": "Unavailable"
        }
        if obj.stock > 0:
            return status_choices.get("in_stock", "")
        else:
            return status_choices.get("unavailable", "")
