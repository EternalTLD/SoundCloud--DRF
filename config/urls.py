from django.contrib import admin
from django.urls import path, include

from src.audio_library.views import auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('src.routes')),
    path('', include('social_django.urls', namespace='social')),
    path('git_auth/', auth)
]
