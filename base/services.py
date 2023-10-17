from django.core.exceptions import ValidationError
from django.conf import settings


def get_path_upload_profile_image(instance, file):
    """
    Returns file path to profile image.
    Format: media/profile_images/user_id/photo.jpg
    """
    return f"profile_images/{instance.id}/{file}"


def validate_image_size(file_object):
    """File size validator"""
    if file_object.size > settings.PROFILE_IMAGE_SIZE_MB_LIMIT * 1024 * 1024:
        raise ValidationError(f"Max size of image is {settings.PROFILE_IMAGE_SIZE_MB_LIMIT} MB")