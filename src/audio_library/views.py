import os

from django.http import FileResponse
from rest_framework import generics, viewsets, parsers, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..base.permissions import IsAuthorOrReadOnly
from ..base.services import delete_old_file
from ..base.classes import MixedSerializer
from . import models, serializers
from .mixins import LikeActionMixin


class GenreListAPIView(generics.ListAPIView):
    """Genre list view"""

    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class AlbumViewSet(LikeActionMixin, viewsets.ModelViewSet):
    """CRUD album"""

    queryset = models.Album.objects.filter(private=False)
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.AlbumSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.cover:
            delete_old_file(instance.cover.path)
        instance.delete()

    @action(detail=True, methods=["get"], serializer_class=serializers.AudioSerializer)
    def audios(self, request, pk):
        album = self.get_object()
        audios = models.Audio.objects.filter(album=album)
        serializer = self.get_serializer(audios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AudioViewSet(LikeActionMixin, MixedSerializer, viewsets.ModelViewSet):
    """CRUD audio"""

    queryset = models.Audio.objects.filter(private=False)
    serializer_class = serializers.AudioSerializer
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthorOrReadOnly]
    serializer_classes_by_action = {
        "list": serializers.AudioWithAlbumSerializer,
        "retrieve": serializers.AudioWithAlbumSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=True, methods=["get"], serializer_class=serializers.CommentSerializer
    )
    def comments(self, request, pk):
        audio = self.get_object()
        comments = models.Comment.objects.filter(audio=audio)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True, methods=["post"], serializer_class=serializers.CommentSerializer
    )
    def add_comment(self, request, pk):
        audio = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(audio=audio, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def play(self, request, pk):
        audio = self.get_object()
        if not os.path.exists(audio.file.path):
            return Response(
                {"error": "File doesn't exists"}, status=status.HTTP_404_NOT_FOUND
            )
        audio.plays_count += 1
        audio.save()
        return FileResponse(open(audio.file.path, "rb"), filename=audio.file.name)

    @action(detail=True, methods=["get"])
    def download(self, request, pk):
        audio = self.get_object()
        if not os.path.exists(audio.file.path):
            return Response(
                {"error": "File doesn't exists"}, status=status.HTTP_404_NOT_FOUND
            )
        audio.downloads += 1
        audio.save()
        return FileResponse(
            open(audio.file.path, "rb"),
            filename=audio.file.name,
            as_attachment=True,
        )


class PlaylistViewSet(MixedSerializer, viewsets.ModelViewSet):
    """CRUD playlist"""

    queryset = models.Playlist.objects.all()
    serializer_class = serializers.PlaylistSerializer
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthorOrReadOnly]
    serializer_classes_by_action = {
        "list": serializers.PlaylistWithAudiosSerializer,
        "retrieve": serializers.PlaylistWithAudiosSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.cover:
            delete_old_file(instance.cover.path)
        instance.delete()


class CommentViewSet(LikeActionMixin, viewsets.ModelViewSet):
    """CRUD comments"""

    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
