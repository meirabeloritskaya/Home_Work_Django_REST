from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView  # TokenObtainPairView,

from users.apps import UsersConfig

from .views import (
    CreatePaymentView,
    MyTokenObtainPairView,
    PaymentViewSet,
    UserCreateAPIView,
    UserViewSet,
)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("", include(router.urls)),
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
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("create-payment/", CreatePaymentView.as_view(), name="create-payment"),
]
