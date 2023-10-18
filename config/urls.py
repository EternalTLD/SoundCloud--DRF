from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('src.routes')),
    path('auth/', include('src.oauth.urls', namespace='oauth')),
]
