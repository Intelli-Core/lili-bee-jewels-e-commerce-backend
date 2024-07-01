import os
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_image(value):
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png"]
    if ext.lower() not in valid_extensions:
        raise ValidationError("Unsupported file extension.")


def validate_date(value):
    if value < timezone.now().date():
        raise ValidationError("Date cannot be in the past")
