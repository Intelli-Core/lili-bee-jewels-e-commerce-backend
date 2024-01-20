from collections import Counter
from django.db.models import Count, F
from django.db.models.functions import Lower
from rest_framework import generics
from rest_framework.response import Response
from django_filters import rest_framework as filters, OrderingFilter
from django_filters.constants import EMPTY_VALUES
from product.models import Product, ProductAttributes, ProductCategory, ProductMaterial


class ArrayFilter(filters.Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        return qs.filter(**{f"{self.field_name}__contains": [float(value)]})


class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__name", lookup_expr="iexact")
    material = filters.CharFilter(field_name="attributes__material__name", lookup_expr="iexact")
    size = ArrayFilter(field_name="attributes__sizes")
    sort = OrderingFilter(
        # tuple-mapping retains the order
        fields=(
            ('-created_at', 'newest'),
            ('price', 'price_asc'),
            ('-price', 'price_desc'),
        ),
    )


class Meta:
    model = Product
    fields = ["category", "material", "size", "sort"]

    class Meta:
        model = Product
        fields = ["category", "material", "size"]


class FilterOptionsListView(generics.ListAPIView):
    def get(self, request):
        categories = (
            ProductCategory.objects.annotate(category_name=Lower("name"))
            .values("id", "category_name")
            .annotate(count=Count("product"))
            .order_by("category_name")
        )
        materials = (
            ProductMaterial.objects.annotate(material_name=Lower("name"))
            .values("id", "material_name")
            .annotate(count=Count("attributes"))
            .order_by("material_name")
        )
        sizes = ProductAttributes.objects.values_list("sizes", flat=True)
        all_sizes = [size for sublist in sizes for size in sublist]
        size_counts = dict(Counter(all_sizes))
        # Sort sizes
        size_counts = {k: size_counts[k] for k in sorted(size_counts)}

        # Capitalize the first letter of each word in category_name and material_name
        categories = [{**category, 'category_name': category['category_name'].title(), 'id': category['id']} for
                      category in categories]
        materials = [{**material, 'material_name': material['material_name'].title(), 'id': material['id']} for material
                     in materials]

        return Response(
            {
                "categories": list(categories),
                "materials": list(materials),
                "sizes": size_counts,
            }
        )
