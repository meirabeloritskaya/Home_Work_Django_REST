from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    course_lesson_count = SerializerMethodField()
    lesson_titles = SerializerMethodField()

    def get_course_lesson_count(self, course):
        return course.lessons.count()

    def get_lesson_titles(self, course):
        return [lesson.title for lesson in course.lessons.all()]

    class Meta:
        model = Course
        fields = ("title", "description", "course_lesson_count", "lesson_titles")


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
