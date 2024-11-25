from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentViewSet
from users.apps import UsersConfig
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import AllowAny

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("", include(router.urls)),
    # path('login/', TokenObtainPairView.as_view(), name='login'),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "login/",
        MyTokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path("register/", UserViewSet.as_view({"post": "create"}), name="register"),
]
