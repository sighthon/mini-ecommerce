from typing import Dict, List

from django.db.models import Q
from rest_framework import viewsets, request, response
from rest_framework.decorators import action

from user.models import Customer, User, SalesAgent
from .permissions import OrderPermission

from .models import Order, OrderItem
from .serializers import OrderSerializer


# A model view set provide CRUD implementation and other APIs
class OrderViewSet(viewsets.ModelViewSet):
    """A View set for viewing and editing orders."""
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [OrderPermission]

    def get_queryset(self):
        query_set = self.queryset

        # If the request is from a customer, filter the queryset
        # to show fetch only orders from that customer
        if self.request.user.type == User.Types.CUSTOMER:
            try:
                user = Customer.objects.get(id=self.request.user.id)
                query_set = query_set.filter(customer=user.id)
            except Customer.DoesNotExist:
                pass
        # If the request is from a sales agent, filter the queryset
        # to show fetch only orders handled by that sales agent or
        # orders to which no sales agent has been assigned yet
        elif self.request.user.type == User.Types.SALES_AGENT:
            try:
                user = SalesAgent.objects.get(id=self.request.user.id)
                query_set = query_set.filter(Q(sales_agent__isnull=True) | Q(sales_agent=user.id))
            except SalesAgent.DoesNotExist:
                pass

        # filter on query params
        if self.request.GET.get('customer'):
            query_set = query_set.filter(customer=self.request.GET.get('customer'))
        if self.request.GET.get('status'):
            query_set = query_set.filter(status=self.request.GET.get('status'))

        return query_set

    @action(methods=["get"], detail=False)
    def past_order_product_details(self, req: request.Request, *args: List, **kwargs: Dict) -> response.Response:
        """List all the details for the past products ordered"""
        queryset = self.get_queryset()
        if not len(queryset):
            return response.Response({})

        # get unique products
        unique_prod_set = set()
        past_order_items = [
            order_item for order_item in OrderItem.objects.filter(order__in=queryset).order_by('-id')
            if order_item.item not in unique_prod_set and not unique_prod_set.add(order_item.item)
        ]
        response_data = {"past_ordered_products": []}
        for past_order_item in past_order_items:
            response_data["past_ordered_products"].append({
                "name": past_order_item.item.name,
                "current_price": past_order_item.item.price,
                "past_order_price": past_order_item.item_price
            })
        return response.Response(response_data)
