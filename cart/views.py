from django.shortcuts import render

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
from shared.generic_viewset import GenericViewSet

# Create your views here.


class CartItemViewset(GenericViewSet):
    include_list_view = False
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartViewset(GenericViewSet):
    include_list_view = False
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
 
