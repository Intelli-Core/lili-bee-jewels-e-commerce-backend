from django.shortcuts import render
from shared.generic_viewset import GenericViewSet
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated


class OrderViewset(GenericViewSet):
    include_list_view = True
    protected_views = ["create", "update", "partial_update", "destroy"]
    # permissions = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
