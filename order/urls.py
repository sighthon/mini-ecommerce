from .views import OrderViewSet
from rest_framework.routers import SimpleRouter

app_name = "product"

router = SimpleRouter()
router.register("order", OrderViewSet, basename="order")
urlpatterns = router.urls