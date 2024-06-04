from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import OrderViewset

app_name = "order"

router = DefaultRouter()
router.register(r"", OrderViewset, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
