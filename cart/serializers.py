from rest_framework.serializers import ModelSerializer
from product.serializers import ProductSerializer
from .models import CartItem, Cart


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["product"] = ProductSerializer(instance.product).data
        return representation


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"
