# A model view set provide CRUD implementation and other APIs
from rest_framework import viewsets

from .models import FinancialLedger
from .permissions import FinancialLedgerPermission
from .serializers import FinancialLedgerSerializer


class FinancialLedgerViewSet(viewsets.ModelViewSet):
    """A View set for viewing and editing orders."""
    serializer_class = FinancialLedgerSerializer
    queryset = FinancialLedger.objects.all()
    permission_classes = [FinancialLedgerPermission]
    http_method_names = ['get']  # limiting the APIs to only GET

    def get_queryset(self):
        query_set = self.queryset

        # filter on query params
        if self.request.GET.get('customer'):
            query_set = query_set.filter(invoice__customer=self.request.GET.get('customer'))

        return query_set
