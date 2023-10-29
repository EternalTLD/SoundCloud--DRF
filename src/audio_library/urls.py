from django.urls import path

from . import views


app_name = 'audio'

urlpatterns = [
    path('genre/', views.GenreListView.as_view()),

    path('license/', views.LicenseView.as_view({'get': 'list', 'post': 'create'})),
    path('license/<int:pk>/', views.LicenseView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('album/', views.AlbumView.as_view({'get': 'list', 'post': 'create'})),
    path('album/<int:pk>/', views.AlbumView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('author_album/<int:pk>/', views.PublicAlbumListView.as_view()),

    path('audio/', views.AudioView.as_view({'get': 'list', 'post': 'create'})),
    path('audio/<int:pk>/', views.AudioView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('stream_audio/<int:pk>/', views.StreamAudioView.as_view()),
    path('download_audio/<int:pk>/', views.DownloadAudioView.as_view()),

    path('audio_list/', views.AllAudioView.as_view()),
    path('author_audio_list/<int:pk>/', views.AuthorAudioView.as_view()),

    path('playlist/', views.PlaylistView.as_view({'get': 'list', 'post': 'create'})),
    path('playlist/<int:pk>/', views.PlaylistView.as_view({'put': 'update', 'delete': 'destroy'})),

]
