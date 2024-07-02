import imghdr
import os
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_image(value):
    # Get the file content type
    image_type = imghdr.what(value)

    # Define allowed common image types
    valid_image_types = ["jpeg", "png", "gif", "bmp", "webp"]

    if image_type not in valid_image_types:
        raise ValidationError(
            "Unsupported image format. Allowed types are: JPG, JPEG, PNG, GIF, BMP, and WebP."
        )

    # Check file extension matches content type
    ext = os.path.splitext(value.name)[1][
        1:
    ].lower()  # Get extension without the dot and lowercase it

    if image_type == "jpeg" and ext not in ["jpg", "jpeg"]:
        raise ValidationError(
            "File extension does not match the image content. Expected .jpg or .jpeg"
        )
    elif image_type != ext and image_type != "jpeg":
        raise ValidationError(
            f"File extension does not match the image content. Expected .{image_type}"
        )


def validate_date(value):
    if value < timezone.now().date():
        raise ValidationError("Date cannot be in the past")
