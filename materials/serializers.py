from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .validators import VideoURLValidator
from materials.models import Course, Lesson, Subscription
from rest_framework import serializers


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    course_lesson_count = SerializerMethodField()
    lesson_titles = SerializerMethodField()
    is_paid = SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_course_lesson_count(self, course):
        return course.lessons.count()

    def get_lesson_titles(self, course):
        return [lesson.title for lesson in course.lessons.all()]

    def get_is_paid(self, course):
        return course.is_paid()

    def get_is_subscribed(self, obj):
        user = self.context.get(
            "request"
        ).user  # получаем текущего пользователя из запроса
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "course_lesson_count",
            "lesson_titles",
            "is_paid",
            "is_subscribed",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title")

    class Meta:
        model = Subscription
        fields = ["user", "course", "course_title"]


class LessonSerializer(serializers.ModelSerializer):

    video_url = serializers.URLField(
        validators=[VideoURLValidator()], required=False, allow_null=True
    )

    class Meta:
        model = Lesson
        fields = "__all__"
