# materials/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson
from django.urls import reverse


class CourseAndLessonAccessTests(TestCase):

    def setUp(self):
        # Создание пользователей
        self.manager = get_user_model().objects.create_user(
            email="manager@example.com", password="password123", is_staff=True
        )
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="password123", is_staff=False
        )

        # Создание курсов и уроков
        self.course1 = Course.objects.create(title="Course 1", owner=self.manager)
        self.course2 = Course.objects.create(title="Course 2", owner=self.user)
        self.lesson1 = Lesson.objects.create(
            course=self.course1,
            title="Lesson 1",
            description="Content 1",
            owner=self.manager,
        )
        self.lesson2 = Lesson.objects.create(
            course=self.course2,
            title="Lesson 2",
            description="Content 2",
            owner=self.user,
        )

    def test_manager_can_view_all_courses_and_lessons(self):
        # Логиним менеджера
        self.client.force_login(self.manager)

        # Проверка доступа к курсам
        response = self.client.get(reverse("materials:course-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")

        # Проверка доступа к урокам
        response = self.client.get(reverse("materials:lessons_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lesson 1")
        self.assertContains(response, "Lesson 2")

    def test_user_can_only_view_own_courses_and_lessons(self):
        # Логиним обычного пользователя
        self.client.force_login(self.user)

        # Проверка доступа к курсам
        response = self.client.get(reverse("materials:course-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Course 2")
        self.assertNotContains(response, "Course 1")

        # Проверка доступа к урокам
        response = self.client.get(reverse("materials:lessons_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lesson 2")
        self.assertNotContains(response, "Lesson 1")
