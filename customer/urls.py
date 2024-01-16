from django.urls import path

from customer.views import (
    CustomerCreateAPIView,
    CustomerDeleteAPIView,
    CustomerDetailAPIView,
    CustomerListAPIView,
)


app_name = "customer"

urlpatterns = [
    path("create/", CustomerCreateAPIView.as_view(), name="customer_create"),
    path("list/", CustomerListAPIView.as_view(), name="customer_list"),
    path("detail/<uuid:pk>/", CustomerDetailAPIView.as_view(), name="customer_detail"),
    path("delete/<uuid:pk>/", CustomerDeleteAPIView.as_view(), name="customer_delete"),
]
