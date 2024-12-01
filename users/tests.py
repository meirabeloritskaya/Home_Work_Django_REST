# users/tests.py
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


class UserTests(APITestCase):

    def test_create_user(self):
        """
        Проверяем создание пользователя через API.
        """
        data = {
            "email": "newuser@example.com",
            "password": "password123",
        }
        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            get_user_model().objects.filter(email="newuser@example.com").exists()
        )
