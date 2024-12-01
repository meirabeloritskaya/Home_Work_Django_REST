from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from materials.paginators import CustomPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from materials.models import Course, Lesson, Subscription
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
)
from .serializers import SubscriptionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from materials.filters import CourseFilter, LessonFilter
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CourseFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [~IsModer]

        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated & IsOwner]

        elif self.action in ["update"]:
            self.permission_classes = [IsAuthenticated & (IsOwner | IsModer)]

        elif self.action in ["list"]:
            if not self.request.user.groups.filter(name="moders").exists():
                self.queryset = self.queryset.filter(owner=self.request.user)
            self.permission_classes = [IsAuthenticated & (IsOwner | IsModer)]
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LessonFilter
    permission_classes = [IsAuthenticated & (IsOwner | IsModer)]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if not user.groups.filter(name="moders").exists():
            queryset = queryset.filter(course__owner=user)

        return queryset


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & (IsOwner | IsModer)]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if not user.groups.filter(name="moders").exists():
            queryset = queryset.filter(course__owner=user)

        return queryset


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & (IsOwner | IsModer)]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if not user.groups.filter(name="moders").exists():
            queryset = queryset.filter(course__owner=user)

        return queryset


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & IsOwner]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(course__owner=user)

        return queryset


class SubscriptionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        if not course_id:
            return Response(
                {"detail": "Не указан курс"}, status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)

        # Проверяем, есть ли уже подписка
        subscription, created = Subscription.objects.get_or_create(
            user=user, course=course
        )

        if not created:
            # Если подписка существует, удаляем её
            subscription.delete()
            message = "Подписка удалена"
        else:
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)


class UserSubscriptionsView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем подписки только для текущего пользователя
        return Subscription.objects.filter(user=self.request.user)
