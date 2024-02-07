from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class LikeActionMixin:
    @action(detail=True, methods=["get"])
    def like(self, request, pk):
        obj = self.get_object()
        if request.user in obj.likes.all():
            obj.likes.remove(request.user)
            obj.save()
            return Response({"status": "Like removed"}, status=status.HTTP_200_OK)
        obj.likes.add(request.user)
        obj.save()
        return Response({"status": "Like added"}, status=status.HTTP_200_OK)