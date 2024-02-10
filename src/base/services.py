import os


def get_upload_album_cover_path(instance, file):
    """
    Returns file path to albums cover.
    Format: media/covers/album_title/photo.jpg
    """
    title = instance.title.replace(" ", "_")
    filename = file.replace(" ", "_")
    return f"covers/albums/{title}/{filename}"


def get_upload_audio_path(instance, file):
    """
    Returns file path to audio file.
    Format: media/audios/audio_title/audio.mp3
    """
    title = instance.title.replace(" ", "_")
    filename = file.replace(" ", "_")
    return f"audios/{title}/{filename}"


def get_upload_playlist_cover_path(instance, file):
    """
    Returns file path to playlist cover.
    Format: media/covers/playlist_title/photo.jpg
    """
    title = instance.title.replace(" ", "_")
    filename = file.replace(" ", "_")
    return f"covers/playlists/{title}/{filename}"


def delete_old_file(file_path):
    """Remove path if exist"""
    if os.path.exists(file_path):
        os.remove(file_path)
