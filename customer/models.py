import uuid
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


# Create your models here.
class CustomerProfile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    full_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    mobile_number = models.CharField(
        max_length=13,
        validators=[RegexValidator(r"^\+63\d{10}$")],
        unique=True,
        null=False,
        blank=False,
    )
    shipping_address = models.CharField(max_length=255)


class Customer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer",
    )
    profile = models.OneToOneField(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="customer",
        null=False,
        blank=False,
    )
