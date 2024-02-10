from rest_framework import serializers

from . import models
from .fields import GenreField
from ..base.services import delete_old_file


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ("id", "title")


class AlbumSerializer(serializers.ModelSerializer):
    genre = GenreField(many=True, queryset=models.Genre.objects.all())

    class Meta:
        model = models.Album
        fields = (
            "id",
            "user",
            "title",
            "description",
            "genre",
            "release_date",
            "cover",
            "count_audios",
            "count_likes",
        )

    def update(self, instance, validated_data):
        if instance.cover:
            delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class AudioSerializer(serializers.ModelSerializer):
    plays_count = serializers.IntegerField(read_only=True)
    downloads = serializers.IntegerField(read_only=True)
    genre = GenreField(many=True, queryset=models.Genre.objects.all())

    class Meta:
        model = models.Audio
        fields = (
            "id",
            "user",
            "title",
            "album",
            "genre",
            "file",
            "release_date",
            "plays_count",
            "downloads",
        )


class AudioWithAlbumSerializer(AudioSerializer):
    album = AlbumSerializer()


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Playlist
        fields = ("id", "title", "user", "audios", "cover")

    def update(self, instance, validated_data):
        if instance.cover:
            delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class PlaylistWithAudiosSerializer(PlaylistSerializer):
    audios = AudioSerializer(many=True, read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ("id", "user", "text", "timestamp", "audio")
