import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from shared.validators import validate_image
from storages.backends.s3boto3 import S3Boto3Storage


class ProductCategory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)


class ProductMaterial(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)


class ProductAttributes(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    material = models.ForeignKey(ProductMaterial, on_delete=models.CASCADE, blank=False, null=False,
                                 related_name="attributes")
    weight = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False
    )
    sizes = ArrayField(
        models.CharField(max_length=255, blank=True),
        blank=True,
        null=True,
        default=list,
    )


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, default=0.00
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="product",
    )
    attributes = models.OneToOneField(
        ProductAttributes,
        on_delete=models.CASCADE,
        related_name="product",
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to="product_images",
        validators=[validate_image],
        storage=S3Boto3Storage(),
        blank=True,
        null=True,
    )
    stock = models.PositiveIntegerField(default=0)


class ProductOption(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, default=0.00
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="options",
    )
    attributes = models.ForeignKey(
        ProductAttributes,
        on_delete=models.CASCADE,
        related_name="options",
        blank=False,
        null=False,
    )
    thumbnail = models.ImageField(
        upload_to="product_images",
        validators=[validate_image],
        storage=S3Boto3Storage(),
        blank=True,
        null=True,
    )
    stock = models.PositiveIntegerField(default=0)


class ProductImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to="product_images",
        validators=[validate_image],
        storage=S3Boto3Storage(),
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="media",
    )

    product_option = models.ForeignKey(
        ProductOption,
        on_delete=models.CASCADE,
        related_name="media",
        blank=True,
        null=True,
    )
