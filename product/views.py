from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """A View set for viewing and editing products."""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
