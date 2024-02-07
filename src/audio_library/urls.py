from django.urls import path, include

from rest_framework.routers import SimpleRouter

from . import views


app_name = "audio"

router = SimpleRouter()
router.register(r"album", views.AlbumViewSet)
router.register(r"audio", views.AudioViewSet)
router.register(r"playlist", views.PlaylistViewSet)
router.register(r"comment", views.CommentViewSet)

urlpatterns = [
    path("genre/", views.GenreListAPIView.as_view()),
    path("", include(router.urls)),
]
