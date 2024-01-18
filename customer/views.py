# Create your views here.
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from .models import Customer
from .serializers import CustomerSerializer


# Create your views here.


class CustomerCreateAPIView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
