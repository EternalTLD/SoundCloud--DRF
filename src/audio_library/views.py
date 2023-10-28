from rest_framework import generics, viewsets, parsers

from . import models, serializers
from ..base.permissions import IsAuthor
from ..base.services import delete_old_file


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


class AlbumView(viewsets.ModelViewSet):
    """CRUD album"""
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.AlbumSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return self.request.user.albums.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class PublicAlbumListView(generics.ListAPIView):
    """List of all public albums"""
    serializer_class = serializers.AlbumSerializer

    def get_queryset(self):
        return models.Album.objects.filter(user__id=self.kwargs.get('pk'), private=False)
