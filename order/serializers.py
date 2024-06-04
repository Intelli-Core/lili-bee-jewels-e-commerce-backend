from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from cart.serializers import CartSerializer
from customer.serializers import CustomerSerializer
from order.models import Order
from cart.models import Cart
from customer.models import Customer


class OrderSerializer(ModelSerializer):
    customer = PrimaryKeyRelatedField(queryset=Customer.objects.all())
    cart = PrimaryKeyRelatedField(queryset=Cart.objects.all())

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        customer_id = validated_data.pop("customer")
        cart_id = validated_data.pop("cart")

        # Get the Customer and Cart instances
        customer = Customer.objects.get(id=customer_id.id)
        cart = Cart.objects.get(id=cart_id.id)

        # Create the Order instance
        order = Order.objects.create(customer=customer, cart=cart, **validated_data)
        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["customer"] = CustomerSerializer(instance.customer).data
        representation["cart"] = CartSerializer(instance.cart).data
        return representation
