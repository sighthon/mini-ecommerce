from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer


# A model view set provide basic CRUD implementation
class ProductViewSet(viewsets.ModelViewSet):
    """A View set for viewing and editing products."""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
