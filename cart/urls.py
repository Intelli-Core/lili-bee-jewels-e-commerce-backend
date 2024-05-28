from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CartItemViewset, CartViewset

app_name = "cart"

router = DefaultRouter()
router.register(r"item", CartItemViewset, basename="item")
router.register(r"", CartViewset, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
]
