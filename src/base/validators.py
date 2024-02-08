from django.core.exceptions import ValidationError
from django.conf import settings


def validate_image_size(file_object):
    """File size validator"""
    if file_object.size > settings.PROFILE_IMAGE_SIZE_MB_LIMIT * 1024 * 1024:
        raise ValidationError(
            f"Max size of image is {settings.PROFILE_IMAGE_SIZE_MB_LIMIT} MB"
        )
