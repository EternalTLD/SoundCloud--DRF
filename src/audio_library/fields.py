from rest_framework import serializers

from . import models


class GenreField(serializers.RelatedField):
    def to_representation(self, value):
        return value.title
    
    def to_internal_value(self, data):
        if isinstance(data, list):
            genre_ids = []
            for genre_title in data:
                try:
                    genre = models.Genre.objects.get(title=genre_title)
                    genre_ids.append(genre.id)
                except models.Genre.DoesNotExist:
                    raise serializers.ValidationError(f"Genre {genre_title} doesn't exists")
            return genre_ids
        else:
            try:
                genre = models.Genre.objects.get(title=data)
                return genre.id
            except models.Genre.DoesNotExist:
                raise serializers.ValidationError(f"Genre {genre_title} doesn't exists")
                