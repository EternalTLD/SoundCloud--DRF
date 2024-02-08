from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..users.serializers import UserSerializer


class LikeActionMixin:
    @action(detail=True, methods=["post", "get"])
    def like(self, request, pk):
        if request.method == "POST":
            return self._handle_like(request.user)
        elif request.method == "GET":
            return self._get_users_likes()

    def _handle_like(self, user):
        obj = self.get_object()
        if user in obj.likes.all():
            obj.likes.remove(user)
            obj.save()
            return Response({"status": "Like removed"}, status=status.HTTP_200_OK)
        obj.likes.add(user)
        obj.save()
        return Response({"status": "Like added"}, status=status.HTTP_200_OK)

    def _get_users_likes(self):
        obj = self.get_object()
        users = obj.likes.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
