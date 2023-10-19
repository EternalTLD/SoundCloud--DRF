from rest_framework import generics, viewsets

from . import models, serializers
from ..base.permissions import IsAuthor


class GenreListView(generics.ListAPIView):
    """Genre list view"""
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class LicenseView(viewsets.ModelViewSet):
    """CRUD license"""
    serializer_class = serializers.LicenseSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return self.request.user.licenses.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AudioView(viewsets.ModelViewSet):
    """CRUD audio"""
    serializer_class = serializers.AudioSerializer

    def get_queryset(self):
        return self.request.user.audios.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AllAudioListView(generics.ListAPIView):
    """All audio list view"""
    serializer_class = serializers.AudioSerializer
    queryset = models.Audio.objects.all()