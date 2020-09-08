from django.db.models import Sum
from rest_framework import serializers, exceptions

from invoice.models import FinancialLedger
from invoice.serializers import InvoiceSerializer, FinancialLedgerSerializer
from product.models import Product
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
        fields = ["order_items", "customer", "status", "description"]
        extra_kwargs = {
            'customer': {'read_only': True}
        }

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

    def update(self, instance, validated_data):
        # update the sales sales agent
        validated_data['sales_agent'] = self.context['request'].user

        order_hierarchy = {
            "ordered": 0,
            "accepted": 1,
            "delivered": 2,
            "cancelled": 2
        }

        status = validated_data['status']

        if instance.status not in order_hierarchy or status not in order_hierarchy:
            exc_msg = f"Cannot update the order status to {status}"
            raise exceptions.ValidationError(exc_msg)

        if order_hierarchy[status] - order_hierarchy[instance.status] != 1:
            exc_msg = f"Cannot update the order status from {instance.status} to {status}"
            raise exceptions.ValidationError(exc_msg)

        # If changing an order status to accepted, add an invoice and a financial ledger
        if status in ["accepted"]:
            # create an invoice
            invoice_data = {
                "order": instance.id,
                "customer": instance.customer.id,
                "sales_agent": self.context['request'].user.id,
                "invoice_total": sum([a.total_cost for a in instance.order_items.all()])
            }
            invoice_ser = InvoiceSerializer(data=invoice_data)
            invoice_ser.is_valid(raise_exception=True)
            inv = invoice_ser.save()

            # create a financial ledger
            # get previous balance for the customer
            ledgers = FinancialLedger.objects.filter(customer=instance.customer).order_by('-id')
            if not ledgers:
                previous_balance = 0
            else:
                previous_balance = ledgers[0].balance

            ledger_data = {
                "order": instance.id,
                "customer": instance.customer.id,
                "amount": inv.invoice_total,
                "balance": previous_balance + inv.invoice_total
            }
            fl_ser = FinancialLedgerSerializer(data=ledger_data)
            fl_ser.is_valid(raise_exception=True)
            fl_ser.save()

            # TODO: send an SMS to the customer asynchronously
            print("SMS sent")

        # if updating an order status to cancelled from accepted,
        # add a reverse financial ledger entry
        if instance.status == "accepted" and status == "cancelled":
            # create a reverse financial ledger
            # get previous balance for the customer
            ledgers = FinancialLedger.objects.filter(customer=instance.customer).order_by('-id')
            if not ledgers:
                previous_balance = 0
            else:
                previous_balance = ledgers[0].balance

            amount = -1 * sum([a.total_cost for a in instance.order_items.all()])
            ledger_data = {
                "order": instance.id,
                "customer": instance.customer.id,
                "amount": amount,
                "balance": previous_balance + amount
            }
            fl_ser = FinancialLedgerSerializer(data=ledger_data)
            fl_ser.is_valid(raise_exception=True)
            fl_ser.save()

        return super(OrderSerializer, self).update(instance, validated_data)
