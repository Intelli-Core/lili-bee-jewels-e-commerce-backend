# Generated by Django 5.0.1 on 2024-07-02 16:10

import django.core.validators
import shared.validators
import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3.S3Storage(), upload_to='product_images', validators=[shared.validators.validate_image, django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3.S3Storage(), upload_to='product_images', validators=[shared.validators.validate_image, django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='productoption',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, storage=storages.backends.s3.S3Storage(), upload_to='product_images', validators=[shared.validators.validate_image, django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])]),
        ),
    ]
