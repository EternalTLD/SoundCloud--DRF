from django.urls import path

from . import views


app_name = 'audio'

urlpatterns = [
    path('genre/', views.GenreView.as_view())
]
