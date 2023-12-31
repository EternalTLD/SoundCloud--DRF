from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.urls import path, include


schema_view = get_schema_view(
    openapi.Info(
        title='SoundCloud',
        default_version='v1',
        description='Sound cloud like web-app',
        contact=openapi.Contact(url='https://vk.com/id323228018'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth/', include('src.oauth.urls')),
    path('', include('src.audio_library.urls'))
]