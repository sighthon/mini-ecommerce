from .views import ProductViewSet
from rest_framework.routers import SimpleRouter

app_name = "product"

router = SimpleRouter()
router.register("product", ProductViewSet, basename="shipment")
urlpatterns = router.urls