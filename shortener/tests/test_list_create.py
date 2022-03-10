from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from shortener.models import ShortUrl
from shortener.utils import shortit


User = get_user_model()


class ListCreateShortUrlTestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('auth-login')
        self.password = "testPassword"
        self.super_user = User.objects.create_user("admin", "admin@example.com", self.password, is_superuser=True)
        self.test_user = User.objects.create_user("test", "test@example.com", self.password)
        self.test_full_url = 'https://www.google.com.ua/'
        self.create_url = reverse("list_create_short_url")

    def test_create_short_url(self):
        response = self.client.post(self.login_url, {'username': self.super_user.username, 'password': self.password}, format='json').json()
        response = self.client.post(
            self.create_url,
            data={
                "full_url": self.test_full_url
            },
            HTTP_AUTHORIZATION=f'Bearer {response["access"]}',
            format="json")
        data = response.json()
        short_urls_count = ShortUrl.objects.count()
        self.assertEqual(data["full_url"], self.test_full_url)
        self.assertEqual(data["url_hash"], shortit(self.test_full_url))
        self.assertEqual(data["redirect_count"], 0)
        self.assertEqual(data["creator"], self.super_user.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(short_urls_count, 1)

    def test_create_short_url_not_authorized(self):
        response = self.client.post(
            self.create_url,
            data={
                "full_url": self.test_full_url
            },
            format="json")
        short_urls_count = ShortUrl.objects.count()
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(short_urls_count, 0)

    def test_create_existing_short_url(self):
        response = self.client.post(self.login_url, {'username': self.super_user.username, 'password': self.password}, format='json').json()
        self.client.post(
            self.create_url,
            data={"full_url": self.test_full_url},
            HTTP_AUTHORIZATION=f'Bearer {response["access"]}',
            format="json"
        )

        response = self.client.post(
            self.create_url,
            data={"full_url": self.test_full_url},
            HTTP_AUTHORIZATION=f'Bearer {response["access"]}',
            format="json"
        )
        data = response.json()
        short_urls_count = ShortUrl.objects.count()
        self.assertEqual(data, {'full_url': ['short url with this full url already exists.']})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(short_urls_count, 1)

    def test_show_list_urls(self):
        ShortUrl.objects.create(full_url='https://www.google.com.ua/', url_hash='qwertyu', creator=self.super_user)
        ShortUrl.objects.create(full_url='https://www.google.com.ua/2/', url_hash='dsdfdu', creator=self.test_user)
        response = self.client.post(self.login_url,
                                    {'username': self.super_user.username, 'password': self.password},
                                    format='json').json()
        response = self.client.get(
            self.create_url,
            HTTP_AUTHORIZATION=f'Bearer {response["access"]}',
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 2)

        response = self.client.post(self.login_url,
                                    {'username': self.test_user.username, 'password': self.password},
                                    format='json').json()
        response = self.client.get(
            self.create_url,
            HTTP_AUTHORIZATION=f'Bearer {response["access"]}',
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["creator"], self.test_user.id)


