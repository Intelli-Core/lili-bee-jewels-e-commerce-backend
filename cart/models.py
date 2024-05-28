from django.db import models

from product.models import Product
from shared.models import BaseModel


class Cart(BaseModel):
    quantity = models.PositiveIntegerField(default=0)
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, default=0.00
    )


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, blank=False, null=False, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="item")
    quantity = models.PositiveIntegerField(blank=False, null=False, default=1)
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, default=0.00
    )
    selectedSize = models.CharField(max_length=255, blank=False, null=False)
    selectedMaterial = models.CharField(max_length=255, blank=False, null=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)  # Save the CartItem first

        # Update the associated Cart
        self.cart.quantity = self.cart.items.count()
        self.cart.subtotal = sum(item.subtotal for item in self.cart.items.all())
        self.cart.save()
