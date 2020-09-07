from rest_framework import viewsets

from user.models import Customer, User
from .permissions import OrderPermission

from .models import Order
from .serializers import OrderSerializer


# A model view set provide basic CRUD implementation
class OrderViewSet(viewsets.ModelViewSet):
    """A View set for viewing and editing orders."""
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [OrderPermission]

    def get_queryset(self):
        queryset = self.queryset

        # If the request is from a customer, filter the queryset
        # to show fetch only orders from that customer
        if self.request.user.type == User.Types.CUSTOMER:
            try:
                user = Customer.objects.get(id=self.request.user.id)
                query_set = queryset.filter(customer=user.id)
            except Customer.DoesNotExist:
                pass

        return query_set
