from django.contrib import admin
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson

User = get_user_model()


class CourseInline(admin.TabularInline):
    model = Course
    fields = ("title", "description", "owner")
    extra = 0
    can_delete = True
    show_change_link = True


class LessonInline(admin.TabularInline):
    model = Lesson
    fields = ("title", "course", "owner")
    extra = 0
    can_delete = True
    show_change_link = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "groups")
    search_fields = ("email", "first_name", "last_name")
    ordering = ["email"]
    inlines = [CourseInline, LessonInline]
