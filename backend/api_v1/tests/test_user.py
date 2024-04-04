from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class JWTAuthenticationTest(APITestCase):

    def setUp(self):
        self.email = 'testemail@mail.com'
        self.password = 'testpassword'
        self.url_registration = reverse('users')
        self.url_jwt = reverse('create_jwt')
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password
        )

    def test_registration_success(self):
        """Проверка успешной регистрации"""
        payload = {
            'email': 'testemail2@mail.com',
            'password': 'testpassword2'
        }
        response = self.client.post(self.url_registration, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_jwt_authentication_success(self):
        """Проверка успешной аутентификации"""
        payload = {
            'email': self.email,
            'password': self.password
        }
        response = self.client.post(self.url_jwt, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_authentication_failure(self):
        """Проверка неудачной аутентификации"""
        payload = {
            'email': self.email,
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url_jwt, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
