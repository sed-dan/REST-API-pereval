from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Coords, Level, Pereval, Images
from django.urls import reverse


class PerevalAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@test.com',
            'fam': 'Иванов',
            'name': 'Иван',
            'otc': 'Иванович',
            'phone': '+71234567890'
        }
        self.user = User.objects.create(**self.user_data)

        self.coords_data = {
            'latitude': '12.3456',
            'longitude': '1.2345',
            'height': '1234'
        }
        self.coords = Coords.objects.create(**self.coords_data)

        self.level_data = {
            'winter': '1A',
            'summer': '1A',
            'autumn': '1A',
            'spring': '1A'
        }
        self.level = Level.objects.create(**self.level_data)

        self.pereval_data = {
            'beauty_title': 'Тестовый перевал',
            'title': 'Тестовый перевал',
            'other_titles': 'Тестовый перевал',
            'connect': 'Тестовый перевал',
            'add_time': '2021-09-22 13:18:13',
            'status': 'new',
            'user': self.user,
            'coords': self.coords,
            'level': self.level
        }
        self.pereval = Pereval.objects.create(**self.pereval_data)

        self.image_data = {
            'pereval': self.pereval,
            'data': None,
            'title': 'Тестовое изображение'
        }
        self.images = Images.objects.create(**self.image_data)

    def test_pereval_create(self):
        url = reverse('submit_data')
        data = {
            'beauty_title': 'Новый перевал',
            'title': 'Новый перевал',
            'other_titles': 'Новый перевал',
            'connect': 'Новый перевал',
            'add_time': '2021-09-22 13:18:13',
            'user': self.user_data,
            'coords': self.coords_data,
            'level': self.level_data,
            'images': []
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Запись успешно создана.')
        self.assertTrue(response.data['id'] > 0)

    def test_get_detail(self):
        url = reverse('submit_data_detail', kwargs={'id': self.pereval.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.pereval.title)

    def test_get_with_email(self):
        url = reverse('submit_data') + '?user__email=' + self.user.email
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.pereval.title)

    def test_pereval_update(self):
        url = reverse('submit_data_detail', kwargs={'id': self.pereval.id})
        data = {
            'title': 'Обновленный перевал'
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Запись успешно обновлена.')
        updated_pereval = Pereval.objects.get(id=self.pereval.id)
        self.assertEqual(updated_pereval.title, 'Обновленный перевал')

    def test_user_data_update(self):
        url = reverse('submit_data_detail', kwargs={'id': self.pereval.id})
        data = {
            'user': {
                'fam': 'Петров'
            }
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Нельзя редактировать данные пользователя.')

    def test_status_update(self):
        self.pereval.status = 'accepted'
        self.pereval.save()

        url = reverse('submit_data_detail', kwargs={'id': self.pereval.id})
        data = {
            'title': 'Попытка обновления'
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Запись нельзя редактировать в данном статусе.')

