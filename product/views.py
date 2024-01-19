from django.db.models.signals import pre_delete
from django.dispatch import receiver
from rest_framework import generics, status
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from product.filters import ProductFilter
from shared.generic_viewset import GenericViewSet
from shared.permissions import IsAdminOrReadOnly
from shared.utils.s3_functions import remove_file_from_s3
from .models import Product, ProductCategory, ProductImage, ProductOption, ProductMaterial
from .serializers import (
    ProductCategorySerializer,
    ProductOptionSerializer,
    ProductSerializer, ProductMaterialSerializer,
)


@receiver(pre_delete, sender=Product)
def product_pre_delete(sender, instance, **kwargs):
    remove_file_from_s3(sender, instance, "thumbnail", **kwargs)


@receiver(pre_delete, sender=ProductImage)
def product_image_pre_delete(sender, instance, **kwargs):
    remove_file_from_s3(sender, instance, "image", **kwargs)


class ProductCategoryViewSet(GenericViewSet):
    protected_views = ["create", "update", "partial_update", "destroy"]
    permissions = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductMaterialViewSet(GenericViewSet):
    protected_views = ["create", "update", "partial_update", "destroy"]
    permissions = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = ProductMaterial.objects.all()
    serializer_class = ProductMaterialSerializer


class ProductViewSet(GenericViewSet):
    protected_views = ["create", "update", "partial_update", "destroy"]
    permissions = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter


class ProductOptionViewSet(GenericViewSet):
    protected_views = ["create", "update", "partial_update", "destroy"]
    permissions = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = ProductOption.objects.all()
    serializer_class = ProductOptionSerializer


class DeleteAllProductsView(generics.GenericAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def delete(self, request, *args, **kwargs):
        confirmation = request.data.get("confirmation")

        if str(confirmation).lower() == "delete all products":
            self.get_queryset().delete()
            return Response(
                {"detail": "All products has been deleted"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"confirmation": "Please type 'delete all products' to confirm."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteAllProductOptionsView(generics.GenericAPIView):
    queryset = ProductOption.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def delete(self, request, *args, **kwargs):
        self.get_queryset().delete()

        return Response(
            {"detail": "All product options has been deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


class DeleteAllProductMaterialsView(generics.GenericAPIView):
    queryset = ProductMaterial.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def delete(self, request, *args, **kwargs):
        self.get_queryset().delete()

        return Response(
            {"detail": "All product materials has been deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
