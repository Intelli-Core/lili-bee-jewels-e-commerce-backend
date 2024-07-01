from django.urls import include, path
from rest_framework.routers import DefaultRouter
from product.filters import FilterOptionsListView
from product.views import (
    DeleteAllProductOptionsView,
    ProductAttributesViewSet,
    ProductCategoryViewSet,
    ProductOptionViewSet,
    ProductViewSet,
    DeleteAllProductsView,
    ProductMaterialViewSet,
    DeleteAllProductMaterialsView,
    DeleteProductMediaView,
)

app_name = "product"

router = DefaultRouter()
router.register(r"category", ProductCategoryViewSet, basename="category")
router.register(r"material", ProductMaterialViewSet, basename="material")
router.register(r"attributes", ProductAttributesViewSet, basename="attributes")
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
    path(
        "material/delete-all/",
        DeleteAllProductMaterialsView.as_view(),
        name="product_material_delete_all",
    ),
    path(
        "media/<uuid:product_id>/",
        DeleteProductMediaView.as_view(),
        name="delete_product_media",
    ),
    path("filters/", FilterOptionsListView.as_view(), name="product_filters"),
    # Base route
    path("", include(router.urls)),
]
