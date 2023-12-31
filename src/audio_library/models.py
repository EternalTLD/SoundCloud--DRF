from django.db import models
from django.core.validators import FileExtensionValidator

from ..oauth.models import AuthUser
from ..base.services import (
    validate_image_size, 
    get_upload_album_cover_path, 
    get_upload_audio_path,
    get_upload_playlist_cover_path
)


class License(models.Model):
    """Audio license model"""
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name='licenses'
    )
    text = models.TextField(max_length=1000)
    

class Genre(models.Model):
    """Genre model"""
    title = models.CharField(max_length=20, unique=True)
    
    def __str__(self) -> str:
        return self.title


class Album(models.Model):
    """Album model"""
    title = models.CharField(max_length=30)
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name='albums'
    )
    description = models.TextField(max_length=1000)
    release_date = models.DateTimeField(auto_now_add=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='album_genres'
    )
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_upload_album_cover_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg']),
            validate_image_size
        ]
    )
    likes = models.ManyToManyField(
        AuthUser,
        related_name='album_likes'
    )

    @property
    def total_audios(self):
        return Audio.objects.filter(album=self).count()

    def __str__(self) -> str:
        return f'{self.user} - {self.title}'
    

class Audio(models.Model):
    """Audio model"""
    title = models.CharField(max_length=30)
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name='audios'
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='audios',
        null=True,
        blank=True
    )
    license = models.ForeignKey(
        License,
        on_delete=models.PROTECT,
        related_name='audio_license'
    )
    release_date = models.DateTimeField(auto_now_add=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='audio_genres'
    )
    file = models.FileField(
        upload_to=get_upload_audio_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
        ]
    )
    plays_count = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(
        AuthUser,
        related_name='audio_likes'
    )

    def __str__(self) -> str:
        return f'{self.user} - {self.title}'


class Comment(models.Model):
    """Comment model"""
    text = models.TextField(max_length=200)
    audio = models.ForeignKey(
        Audio,
        on_delete=models.CASCADE,
        related_name='audio_comments'
    )
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return super().__str__()


class Playlist(models.Model):
    """Playlist model"""
    title = models.CharField(max_length=50)
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name='playlists'
    )
    audios = models.ManyToManyField(
        Audio,
        related_name='audio_playlists'
    )
    cover = models.ImageField(
        upload_to=get_upload_playlist_cover_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg']),
            validate_image_size
        ]
    )

    def __str__(self) -> str:
        return f'Playlist - {self.title}'