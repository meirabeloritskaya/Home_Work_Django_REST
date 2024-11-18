from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet
from users.apps import UsersConfig

app_name = UsersConfig.name
router = SimpleRouter()
router.register("", UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
