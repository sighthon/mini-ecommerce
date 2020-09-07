from rest_framework import serializers, exceptions

from product.models import Product
from product.serializers import ProductSerializer
from user.models import Customer
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for Order Item"""

    class Meta:
        model = OrderItem
        fields = ["item", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["order_items", "customer"]

    def create(self, validated_data):
        """Override create to add custom field values not passed in the request"""
        try:
            validated_data["customer"] = Customer.objects.get(id=self.context['request'].user.id)
        except Customer.DoesNotExist:
            exc_msg = "Customer doesn't exist"
            raise exceptions.ValidationError(exc_msg)

        # get order items data
        items_data = validated_data.pop('order_items')
        if not items_data:
            exc_msg = "Need atleast one order item to place the Order"
            raise exceptions.ValidationError(exc_msg)

        # check if order quantities are valid and get those quantities booked
        products_modified = {}
        try:
            for idx, item_data in enumerate(items_data):
                product = item_data['item']

                if product.status != Product.StatusChoices.IN_STOCK:
                    exc_msg = f"The product {product.name} is unavailable."
                    raise exceptions.ValidationError(exc_msg)

                if product.stock < item_data["quantity"]:
                    exc_msg = f"Not enough stock available for product {product.name}"
                    raise exceptions.ValidationError(exc_msg)

                product.stock -= item_data["quantity"]
                product.save()
                products_modified[product.id] = (product, item_data["quantity"])

                item_data["item_price"] = product.price
        except Exception as e:
            # give back the quantity to product stocks
            for product_id, data in products_modified:
                data[0].stock += data[1]
                data[0].save()
            raise e

        # Create the order
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
