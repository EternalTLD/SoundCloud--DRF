from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..base.permissions import IsUserOrReadOnly
from ..audio_library.serializers import (
    AudioWithAlbumSerializer,
    CommentSerializer,
    AlbumSerializer,
    PlaylistWithAudiosSerializer,
)
from .serializers import UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrReadOnly]

    @action(detail=True, methods=["get"], serializer_class=AudioWithAlbumSerializer)
    def audios(self, request, pk):
        user = self.get_object()
        audios = user.audios.all()
        serializer = self.get_serializer(audios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], serializer_class=CommentSerializer)
    def comments(self, request, pk):
        user = self.get_object()
        comments = user.comments.all()
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], serializer_class=AlbumSerializer)
    def albums(self, request, pk):
        user = self.get_object()
        albums = user.albums.all()
        serializer = self.get_serializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], serializer_class=PlaylistWithAudiosSerializer)
    def playlists(self, request, pk):
        user = self.get_object()
        playlists = user.playlists.all()
        serializer = self.get_serializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
