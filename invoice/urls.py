from .views import FinancialLedgerViewSet
from rest_framework.routers import SimpleRouter

app_name = "invoice"

router = SimpleRouter()
router.register("financial_ledger", FinancialLedgerViewSet, basename="financial_ledger")
urlpatterns = router.urls