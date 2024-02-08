from django.urls import path, include

from rest_framework.routers import SimpleRouter

from . import views


app_name = "users"

router = SimpleRouter()
router.register(r"user", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
