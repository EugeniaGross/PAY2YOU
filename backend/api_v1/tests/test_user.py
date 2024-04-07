from datetime import datetime as dt
from calendar import monthrange
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient, APITestCase

from services.models import (CategoryService, Service, TariffTrialPeriod, TariffSpecialCondition,
                             Tariff, TariffCondition)

from users.models import UserService, UserTrialPeriod, UserSpecialCondition

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


class AnaliticsTest(APITestCase):

    def setUp(self):
        self.url_future_expenses = reverse('future-expenses-list')
        self.category = CategoryService.objects.create(
            name='Текст'
        )
        self.services = Service.objects.bulk_create(
            Service(
                name=f'Текст {i}',
                full_name=f'Текст {i}',
                short_description=f'Текст {i}',
                description=f'Текст {i}',
                image_logo=f'Текст {i}',
                image_logo_popular=f'Текст {i}',
                image_logo_poster=f'Текст {i}',
                cashback=i,
                category=self.category,
                url=f'Текст {i}'
            )
            for i in range(3)
        )
        self.tariff = Tariff.objects.bulk_create(
            Tariff(
                service=self.services[i],
                name=f'Текст {i}',
                description='Текст'
            )
            for i in range(3)
        )
        self.tariff_condition = TariffCondition.objects.bulk_create(
            TariffCondition(
                tariff=self.tariff[i],
                count=1,
                period='M',
                price=200
            )
            for i in range(3)
        )
        self.tariff_trial = TariffTrialPeriod.objects.bulk_create(
            TariffTrialPeriod(
                tariff=self.tariff[i],
                count=1,
                period='M',
                price=10
            )
            for i in range(2)
        )
        self.tariff_spec_cond = TariffSpecialCondition.objects.create(
            tariff=self.tariff[1],
            count=1,
            period='M',
            price=45
        )
        self.user = User.objects.create_user(
            email='testuser@ya.ru',
            password='testpass'
        )
        current_month = dt.today().month
        current_day = dt.today().day
        if current_month > 1:
            self.start_date = date(
                year=dt.today().year, month=dt.today().month - 1, day=current_day + 1)
        else:
            self.start_date = date(
                year=dt.today().year - 1, month=12, day=current_day + 1)
        self.end_date = (dt.today() + timedelta(days=5)).date()
        self.userservice = UserService.objects.bulk_create(
            UserService(
                user=self.user,
                service=self.services[i],
                tariff=self.tariff[i],
                start_date=self.start_date,
                end_date=self.end_date,
                cashback=1,
                status_cashback=True,
                expense=(
                    self.tariff_condition[i].price if i == 2 else self.tariff_trial[i].price
                ),
                is_active=1,
                auto_pay=True,
                phone_number='+79998887766'
            )
            for i in range(3)
        )
        self.user_trial_period = UserTrialPeriod.objects.bulk_create(
            UserTrialPeriod(
                user=self.user,
                service=self.services[i],
                start_date=self.start_date,
                end_date=self.end_date,
            )
            for i in range(2)
        )
        self.user_special_condition = UserSpecialCondition.objects.create(
            user=self.user,
            tariff=self.tariff[1],
            start_date=self.start_date,
            end_date=self.end_date,
        )
        self.auth_client = APIClient()
        self.token = RefreshToken.for_user(self.user).access_token
        self.auth_client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.anon_client = APIClient()

    def test_future_expenses(self):
        """Проверка будущих затрат"""
        response = self.auth_client.get(self.url_future_expenses).json()
        self.assertIn('future_expenses', response)
        test_expenses = (
            self.tariff_condition[0].price * 2
        ) + (self.tariff_spec_cond.price)
        self.assertEqual(response['future_expenses'], test_expenses)
