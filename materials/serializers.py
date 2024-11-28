from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .validators import VideoURLValidator
from materials.models import Course, Lesson
from rest_framework import serializers


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    course_lesson_count = SerializerMethodField()
    lesson_titles = SerializerMethodField()
    is_paid = SerializerMethodField()

    def get_course_lesson_count(self, course):
        return course.lessons.count()

    def get_lesson_titles(self, course):
        return [lesson.title for lesson in course.lessons.all()]

    def get_is_paid(self, course):
        return course.is_paid()

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "course_lesson_count",
            "lesson_titles",
            "is_paid",
        )


class LessonSerializer(serializers.ModelSerializer):

    video_url = serializers.URLField(
        validators=[VideoURLValidator()], required=False, allow_null=True
    )

    class Meta:
        model = Lesson
        fields = "__all__"
