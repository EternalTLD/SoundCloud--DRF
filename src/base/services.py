import os


def get_upload_album_cover_path(instance, file):
    """
    Returns file path to albums cover.
    Format: media/covers/album_title/photo.jpg
    """
    return f"covers/albums/{instance.title}/{file}"


def get_upload_audio_path(instance, file):
    """
    Returns file path to audio file.
    Format: media/audios/audio_title/audio.mp3
    """
    return f"audios/{instance.title}/{file}"


def get_upload_playlist_cover_path(instance, file):
    """
    Returns file path to playlist cover.
    Format: media/covers/playlist_title/photo.jpg
    """
    return f"covers/playlists/{instance.title}/{file}"


def delete_old_file(file_path):
    """Remove path if exist"""
    if os.path.exists(file_path):
        os.remove(file_path)
