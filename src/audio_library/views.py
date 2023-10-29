import os
from django.http import FileResponse, Http404
from rest_framework import generics, viewsets, parsers, views
from django.shortcuts import get_object_or_404

from . import models, serializers
from ..base.permissions import IsAuthor
from ..base.services import delete_old_file
from ..base.classes import MixedSerializer, Pagination


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
    

class AudioView(MixedSerializer, viewsets.ModelViewSet):
    """CRUD audio"""
    serializer_class = serializers.CreateAudioSerializer
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_classes_by_action = {
        'list': serializers.AudioSerializer
    }

    def get_queryset(self):
        return self.request.user.audios.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.file.path)
        instance.delete()


class AuthorAudioView(generics.ListAPIView):
    """Author audio list"""
    serializer_class = serializers.AudioSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return models.Audio.objects.filter(user__id=self.kwargs.get('pk'))


class AllAudioView(generics.ListAPIView):
    """All audio list"""
    queryset = models.Audio.objects.all()
    serializer_class = serializers.AudioSerializer
    pagination_class = Pagination


class StreamAudioView(views.APIView):
    """Listen audio view"""

    def get(self, request, pk):
        audio = get_object_or_404(models.Audio, id=pk)
        if os.path.exists(audio.file.path):
            audio.plays_count += 1
            audio.save()
            return FileResponse(open(audio.file.path, 'rb'), filename=audio.file.name)
        else:
            return Http404()
        

class DownloadAudioView(views.APIView):
    """Download audio view"""
    
    def get(self, request, pk):
        audio = get_object_or_404(models.Audio, id=pk)
        if os.path.exists(audio.file.path):
            audio.downloads += 1
            audio.save()
            return FileResponse(
                open(audio.file.path, 'rb'), filename=audio.file.name, as_attachment=True
            )
        else:
            return Http404()


class PlaylistView(MixedSerializer, viewsets.ModelViewSet):
    """CRUD playlist"""
    serializer_class = serializers.CreateAudioSerializer
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_classes_by_action = {
        'list': serializers.PlaylistSerializer
    }

    def get_queryset(self):
        return self.request.user.playlists.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()
