from decimal import Decimal
from django.db import models
from django.utils.crypto import get_random_string
from cart.models import Cart
from customer.models import Customer
from shared.models import BaseModel


class Order(BaseModel):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=False, null=False
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=False, null=False)
    ref_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING",
    )
    quantity = models.PositiveIntegerField(blank=False, null=False, default=1)
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, default=0.00
    )
    shipping = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, default=0.00
    )
    tax = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, default=0.00
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, default=0.00
    )

    def save(self, *args, **kwargs):
        if not self.ref_id:
            self.ref_id = get_random_string(length=6).upper()

        if not self.subtotal:
            self.subtotal = self.cart.subtotal
            self.quantity = self.cart.quantity

        # Set a flat rate for shipping
        self.shipping = Decimal("5.00")

        # Calculate tax as a percentage of the subtotal
        tax_rate = Decimal("0.10")  # 10%
        self.tax = self.subtotal * tax_rate

        if not self.total:
            self.total = self.subtotal + self.shipping + self.tax
            super().save(*args, **kwargs)
