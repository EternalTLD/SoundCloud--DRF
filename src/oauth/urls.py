from django.urls import path, include

from .endpoint import views, auth_views


app_name = 'oauth'

urlpatterns = [
    path('authors/', views.AuthorView.as_view({'get': 'list'})),
    path('authors/<int:pk>/', views.AuthorView.as_view({'get': 'retrieve'})),

    path('social/', views.SocialLinksView.as_view(
        {
            'get': 'list', 
            'post': 'create', 
            'put': 'update', 
            'delete': 'destroy'
        }
    )),

    path('me/', views.UserView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('google/', auth_views.google_login_view),
]

