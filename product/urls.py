from django.urls import include, path
from rest_framework.routers import DefaultRouter
from product.views import (
    DeleteAllProductOptionsView,
    ProductCategoryViewSet,
    ProductOptionViewSet,
    ProductViewSet,
    DeleteAllProductsView,
)

app_name = "product"

router = DefaultRouter()
router.register(r"category", ProductCategoryViewSet, basename="category")
router.register(r"option", ProductOptionViewSet, basename="option")
router.register(r"", ProductViewSet, basename="product")

urlpatterns = [
    path(
        "delete-all/",
        DeleteAllProductsView.as_view(),
        name="product_delete_all",
    ),
    path(
        "option/delete-all/",
        DeleteAllProductOptionsView.as_view(),
        name="product_option_delete_all",
    ),
    path("", include(router.urls)),
]
