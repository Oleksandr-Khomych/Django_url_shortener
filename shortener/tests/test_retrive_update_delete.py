from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from shortener.models import ShortUrl
from shortener.utils import shortit


User = get_user_model()


class RetrieveUpdateDestroyShortUrlTestCase(APITestCase):
    def setUp(self):
        self.password = "testPassword"
        self.super_user = User.objects.create_user("admin", "admin@example.com", self.password, is_superuser=True)
        self.test_user = User.objects.create_user("test", "test@example.com", self.password)
        self.test_full_url = 'https://www.google.com.ua/'
        self.obj1 = ShortUrl.objects.create(full_url='https://www.google.com.ua/', url_hash='qwertyu', creator=self.super_user)
        self.obj2 = ShortUrl.objects.create(full_url='https://www.google.com.ua/2/', url_hash='dsdfdu', creator=self.test_user)

    def test_delete(self):
        self.client.login(username=self.test_user.username, password=self.password)
        response = self.client.delete(
            reverse("retrieve_update_destroy_short_url", kwargs={"pk": self.obj1.id}),
        )
        data = response.json()
        self.assertEqual(data, {'detail': 'You do not have permission to perform this action.'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(
            reverse("retrieve_update_destroy_short_url", kwargs={"pk": self.obj2.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update(self):
        full_url = "http://127.0.0.1:8000/"
        self.client.login(username=self.test_user.username, password=self.password)
        response = self.client.put(
            reverse("retrieve_update_destroy_short_url", kwargs={"pk": self.obj2.id}),
            data={"full_url": full_url}
        )
        self.obj2 = ShortUrl.objects.get(full_url=full_url)
        self.assertEqual(self.obj2.url_hash, shortit(full_url))
        self.assertEqual(self.obj2.full_url, full_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        full_url += 'test/'
        response = self.client.patch(
            reverse("retrieve_update_destroy_short_url", kwargs={"pk": self.obj2.id}),
            data={"full_url": full_url}
        )
        self.obj2 = ShortUrl.objects.get(full_url=full_url)
        self.assertEqual(self.obj2.url_hash, shortit(full_url))
        self.assertEqual(self.obj2.full_url, full_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
