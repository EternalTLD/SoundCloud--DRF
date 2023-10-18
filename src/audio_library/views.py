from rest_framework import generics

from . import models, serializers


class GenreView(generics.ListAPIView):
    """Genre list view"""
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
