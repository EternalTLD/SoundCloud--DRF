# Generated by Django 4.2.6 on 2024-02-08 16:07

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import src.base.services
import src.base.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Album",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=30)),
                ("description", models.TextField(max_length=1000)),
                ("release_date", models.DateTimeField(auto_now_add=True)),
                ("private", models.BooleanField(default=False)),
                (
                    "cover",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=src.base.services.get_upload_album_cover_path,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg"]
                            ),
                            src.base.validators.validate_image_size,
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Audio",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=30)),
                ("release_date", models.DateTimeField(auto_now_add=True)),
                (
                    "file",
                    models.FileField(
                        upload_to=src.base.services.get_upload_audio_path,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["mp3", "wav"]
                            )
                        ],
                    ),
                ),
                ("plays_count", models.PositiveIntegerField(default=0)),
                ("downloads", models.PositiveIntegerField(default=0)),
                ("private", models.BooleanField(default=False)),
                (
                    "album",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="audios",
                        to="audio_library.album",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Playlist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                (
                    "cover",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=src.base.services.get_upload_playlist_cover_path,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg"]
                            ),
                            src.base.validators.validate_image_size,
                        ],
                    ),
                ),
                (
                    "audios",
                    models.ManyToManyField(
                        related_name="audio_playlists", to="audio_library.audio"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="playlists",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(max_length=200)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "audio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="audio_comments",
                        to="audio_library.audio",
                    ),
                ),
                (
                    "likes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="comment_likes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="audio",
            name="genre",
            field=models.ManyToManyField(
                related_name="audio_genres", to="audio_library.genre"
            ),
        ),
        migrations.AddField(
            model_name="audio",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="audio_likes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="audio",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="audios",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="album",
            name="genre",
            field=models.ManyToManyField(
                related_name="album_genres", to="audio_library.genre"
            ),
        ),
        migrations.AddField(
            model_name="album",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="album_likes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="album",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="albums",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
