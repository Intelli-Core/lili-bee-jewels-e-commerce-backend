"""
URL configuration for lbjec_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

api_prefix = "api/v1/"

schema_view = get_schema_view(
    openapi.Info(
        title="Lili Bee Jewels E-Commerce API",
        default_version="v1",
        description="API for Lili Bee Jewels E-Commerce",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path(f"{api_prefix}auth/", include("shared.auth.urls")),
    path(f"{api_prefix}customer/", include("customer.urls")),
    path(f"{api_prefix}product/", include("product.urls")),
    path(f"{api_prefix}cart/", include("cart.urls")),
]
