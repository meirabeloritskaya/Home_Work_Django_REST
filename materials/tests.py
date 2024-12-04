from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from materials.models import Course
from rest_framework.test import APITestCase


class CourseAndLessonAccessTests(APITestCase):

    def setUp(self):
        # Создание группы 'moders', если она не существует
        self.moder_group, created = Group.objects.get_or_create(name="moders")

        # Создание пользователей
        self.manager = get_user_model().objects.create_user(
            email="manager@example.com", password="password123", is_staff=True
        )
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="password123", is_staff=False
        )

        # Добавление пользователя в группу "moders"
        self.manager.groups.add(self.moder_group)

        # Создание курсов
        self.course1 = Course.objects.create(title="Course 1", owner=self.manager)
        self.course2 = Course.objects.create(title="Course 2", owner=self.user)

    def test_manager_can_view_all_courses(self):
        """Тест для проверки доступа менеджера ко всем курсам"""
        self.client.force_authenticate(user=self.manager)

        response = self.client.get("/courses/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Course 1")
        self.assertContains(response, "Course 2")

    def test_user_can_only_view_own_courses(self):
        """Тест для проверки, что пользователь видит только свои курсы"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/courses/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Course 2")  # Ожидаем увидеть только свой курс
        self.assertNotContains(response, "Course 1")  # Не должно быть курсов менеджера
