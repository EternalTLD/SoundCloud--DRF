from django.urls import path

from . import views


app_name = 'audio'

urlpatterns = [
    path('genre/', views.GenreListView.as_view()),

    path('license/', views.LicenseView.as_view({'get': 'list', 'post': 'create'})),
    path('license/<int:pk>/', views.LicenseView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('audio/', views.AllAudioListView.as_view()),
    path('my_audio/', views.AudioView.as_view({'get': 'list', 'post': 'create'})),
    path('my_audio/<int:pk>/', views.AudioView.as_view({'put': 'update', 'delete': 'destroy'})),
]
