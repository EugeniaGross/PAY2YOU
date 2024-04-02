from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from services.models import Service, CategoryService, CategoryImage, ServiceCategoryImage, Tariff, TariffCondition

User = get_user_model()


class ServiceTest(APITestCase):

    def setUp(self):
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
            for i in range(12)
        )
        self.category_image = CategoryImage.objects.create(
            service=self.services[0],
            name='Текст'
        )
        self.service_category_image = ServiceCategoryImage.objects.create(
            category=self.category_image,
            title='Текст',
            image='Текст'
        )
        self.tariff = Tariff.objects.create(
            service=self.services[0],
            name='Текст',
            description='Текст'
        )
        self.tariff_condition = TariffCondition.objects.create(
            tariff=self.tariff,
            count=1,
            period='M',
            price=200
        )
        self.user = User.objects.create_user(
            email='testemail@mail.com',
            password='testpassword'
        )
        self.auth_client = APIClient()
        self.token = RefreshToken.for_user(self.user).access_token
        self.auth_client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.anon_client = APIClient()

    def test_availability_services(self):
        users_statuses = (
            (self.auth_client, HTTP_200_OK),
            (self.anon_client, HTTP_401_UNAUTHORIZED),
        )
        urls = (
            ('services-list', None),
            ('popular-services-list', None),
            ('image-categories-list', (self.services[0].pk,)),
            ('services-detail', (self.services[0].pk,)),
            ('tariffs-list', (self.services[0].pk,)),
            ('tariffs-detail', (self.services[0].pk, self.tariff.pk)),
            ('images-list', (self.services[0].pk, self.category_image.pk))
        )
        for user, status in users_statuses:
            for name, args in urls:
                url = reverse(name, args=args)
                response = user.get(url)
                self.assertEqual(response.status_code, status)

    def test_services_list(self):
        url = reverse('services-list')
        response = self.auth_client.get(url).json()
        self.assertIn('data', response)
        self.assertIn('next', response)
        self.assertIn('previous', response)
        self.assertIn('id', response['data'][0])
        self.assertIn('logo', response['data'][0])
        self.assertIn('name', response['data'][0])
        self.assertIn('cashback', response['data'][0])
        self.assertEqual(len(response['data']), 10)

    def test_services_detail(self):
        service = self.services[0]
        url = reverse('services-detail', args=(service.pk,))
        response = self.auth_client.get(url).json()
        self.assertEqual(response['id'], str(service.id))
        self.assertEqual(response['name'], service.name)
        self.assertEqual(response['full_name'], service.full_name)
        self.assertEqual(response['cashback'], service.cashback)
        self.assertIn(service.image_logo.url, response['logo'])
        self.assertEqual(response['description'], service.description)
        self.assertEqual(response['url'], service.url)

    def test_popular_services(self):
        url = reverse('popular-services-list')
        response = self.auth_client.get(url).json()
        self.assertIn('data', response)
        self.assertIn('next', response)
        self.assertIn('previous', response)
        self.assertIn('id', response['data'][0])
        self.assertIn('logo', response['data'][0])
        self.assertIn('cashback', response['data'][0])
        self.assertEqual(len(response['data']), 10)

    def test_category_images(self):
        url = reverse('image-categories-list', args=(self.services[0].pk,))
        response = self.auth_client.get(url).json()
        self.assertIn('data', response)
        self.assertIn('next', response)
        self.assertIn('previous', response)
        self.assertIn('id', response['data'][0])
        self.assertIn('name', response['data'][0])

    def test_service_category_images(self):
        url = reverse(
            'images-list', args=(self.services[0].pk, self.category_image.pk))
        response = self.auth_client.get(url).json()
        self.assertIn('data', response)
        self.assertIn('next', response)
        self.assertIn('previous', response)
        self.assertIn('id', response['data'][0])
        self.assertIn('title', response['data'][0])
        self.assertIn('image', response['data'][0])

    def test_tariffs_list(self):
        url = reverse('tariffs-list', args=(self.services[0].pk,))
        response = self.auth_client.get(url).json()
        self.assertIn('data', response)
        self.assertIn('next', response)
        self.assertIn('previous', response)
        self.assertIn('id', response['data'][0])
        self.assertIn('name', response['data'][0])
        self.assertIn('description', response['data'][0])

    def test_tariffs_detail(self):
        url = reverse('tariffs-detail',
                      args=(self.services[0].pk, self.tariff.pk))
        response = self.auth_client.get(url).json()
        self.assertIn('trial_period', response)
        self.assertIn('special_condition', response)
        self.assertIn('condition', response)
        self.assertEqual(response['id'], str(self.tariff.id))
        self.assertEqual(response['name'], self.tariff.name)
        self.assertEqual(response['description'], self.tariff.description)
        self.assertEqual(response['condition']['count'],
                         self.tariff.tariff_condition.count)
        self.assertEqual(response['condition']['period'], 'Месяц')
        self.assertEqual(response['condition']['price'],
                         self.tariff.tariff_condition.price)
