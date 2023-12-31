from rest_framework import serializers

from . import models
from ..base.services import delete_old_file


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'title')


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.License
        fields = ('id', 'text')


class AlbumSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = models.Album
        fields = ('user', 'title', 'description', 'genres', 'release_date', 'private', 'cover')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class CreateAudioSerializer(serializers.BaseSerializer):
    plays_count = serializers.IntegerField(read_only=True)
    downloads = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Audio
        fields = (
            'user', 
            'title', 
            'album', 
            'genre', 
            'file', 
            'release_date', 
            'license', 
            'plays_count', 
            'downloads'
        )

    def update(self, instance, validated_data):
        delete_old_file(instance.file.path)
        return super().update(instance, validated_data)


class AudioSerializer(CreateAudioSerializer):
    license = LicenseSerializer(many=True)
    genre = GenreSerializer(many=True)
    album = AlbumSerializer()


class CreatePlaylistSerializer(serializers.BaseSerializer):
    class Meta:
        model = models.Playlist
        fields = ('title', 'user', 'audios', 'cover')
    
    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)
    

class PlaylistSerializer(CreatePlaylistSerializer):
    audios = AudioSerializer(many=True, read_only=True)
    