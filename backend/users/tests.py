from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class JWTAuthenticationTest(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)

    def test_jwt_authentication_success(self):
        """Проверка успешной аутентификации"""
        payload = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/api/v1/login/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_authentication_failure(self):
        """Проверка неудачной аутентификации"""
        payload = {
            'username': self.username,
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/v1/login/', payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
