from rest_framework import serializers

from . import models


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'title')


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.License
        fields = ('id', 'text')


class AudioSerializer(serializers.ModelSerializer):
    licenses = LicenseSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = models.Audio
        fields = ('user', 'title', 'album', 'genres', 'file', 'release_date', 'licenses', 'plays_count', 'downloads')


class AlbumSerializer(serializers.ModelSerializer):
    audios = AudioSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        models = models.Album
        fields = ('user', 'title', 'audios', 'descriprion', 'genres', 'release_date', 'private', 'cover')


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         models = models.Comment
#         fields = ('user', 'text', 'audio', 'timestamp')


class PlaylistSerializer(serializers.ModelSerializer):
    audios = AudioSerializer(many=True)
    
    class Meta:
        model = models.Playlist
        fields = ('user', 'title', 'audios', 'cover')