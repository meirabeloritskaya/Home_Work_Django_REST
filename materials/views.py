from rest_framework import generics
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from materials.filters import CourseFilter, LessonFilter
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CourseFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [~IsModer]

        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated & IsOwner]

        elif self.action in ["update", "retrieve", "list"]:

            if self.action == "list":

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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LessonFilter
    # permission_classes = [IsAuthenticated & (IsOwner | IsModer)]
    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if self.request.user.groups.filter(name="moders").exists():
    #         # Модераторы видят все уроки
    #         return queryset
    #     # Обычные пользователи видят только свои уроки
    #     return queryset.filter(course__owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated & (IsOwner | IsModer)]
    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if not self.request.user.groups.filter(name="moders").exists():
    #         # Если это не модератор, показываем только уроки, принадлежащие пользователю
    #         queryset = queryset.filter(course__owner=self.request.user)
    #     return queryset


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated & (IsOwner | IsModer)]
    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if not self.request.user.groups.filter(name="moders").exists():
    #         # Если это не модератор, показываем только уроки, принадлежащие пользователю
    #         queryset = queryset.filter(course__owner=self.request.user)
    #     return queryset


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated & (IsOwner | IsModer)]

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if not self.request.user.groups.filter(name="moders").exists():
    #         # Если это не модератор, показываем только уроки, принадлежащие пользователю
    #         queryset = queryset.filter(course__owner=self.request.user)
    #     return queryset