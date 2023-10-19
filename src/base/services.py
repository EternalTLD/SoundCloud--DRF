from django.core.exceptions import ValidationError
from django.conf import settings


def get_upload_profile_image_path(instance, file):
    """
    Returns file path to profile image.
    Format: media/profile_images/user_id/photo.jpg
    """
    return f"profile_images/user_{instance.user.id}/{file}"


def get_upload_album_cover_path(instance, file):
    """
    Returns file path to albums cover.
    Format: media/album_covers/album_id/photo.jpg
    """
    return f"albums/album_{instance.id}/cover/{file}"


def get_upload_audio_path(instance, file):
    """
    Returns file path to audio file.
    Format: media/audios/user_id/audio.mp3
    """
    return f"albums/album_{instance.album.id}/audios/{file}"


def get_upload_playlist_cover_path(instance, file):
    """
    Returns file path to playlist cover.
    Format: media/playlist_covers/user_id/photo.jpg
    """
    return f"playlist_covers/user_{instance.user.id}/{file}"


def validate_image_size(file_object):
    """File size validator"""
    if file_object.size > settings.PROFILE_IMAGE_SIZE_MB_LIMIT * 1024 * 1024:
        raise ValidationError(f"Max size of image is {settings.PROFILE_IMAGE_SIZE_MB_LIMIT} MB")