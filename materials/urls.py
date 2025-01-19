from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)

from .views import SubscriptionAPIView, UserSubscriptionsView

app_name = MaterialsConfig.name
router = SimpleRouter()
router.register("courses", CourseViewSet, basename="course")

urlpatterns = [
    path("", views.home, name="home"),
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyAPIView.as_view(),
        name="lessons_delete",
    ),
    path(
        "lessons/<int:pk>/edit/", LessonUpdateAPIView.as_view(), name="lessons_update"
    ),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),
    path("subscriptions/", UserSubscriptionsView.as_view(), name="user_subscriptions"),
]

urlpatterns += router.urls
