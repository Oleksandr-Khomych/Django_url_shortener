from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from shortener.models import ShortUrl
from shortener.utils import shortit


User = get_user_model()


class RedirectHandlerTestCase(APITestCase):
    def setUp(self):
        self.full_url = 'https://www.google.com.ua/'
        self.url_hash = shortit(self.full_url)
        self.super_user = User.objects.create_user("admin", "admin@example.com", "test_pass", is_superuser=True)
        self.obj1 = ShortUrl.objects.create(full_url=self.full_url, url_hash=self.url_hash, creator=self.super_user)

    def test_redirect(self):
        response = self.client.get(reverse("redirect", kwargs={"url_hash": self.url_hash}))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, self.full_url)
        self.obj1 = ShortUrl.objects.get(full_url=self.full_url)
        self.assertEqual(self.obj1.redirect_count, 1)

    def hash_not_found(self):
        response = self.client.get(reverse("redirect", kwargs={"url_hash": "not-exist_hash"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
