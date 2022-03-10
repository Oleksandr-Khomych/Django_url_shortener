from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


class JWTAuthenticationTestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('auth-login')
        self.refresh_token = reverse('auth-refresh-token')
        self.password = "testPassword"
        self.test_user = User.objects.create_user("test", "test@example.com", self.password)
        self.test_url = reverse("list_create_short_url")

    def test_access(self):
        # Test Unauthorized Access
        response = self.client.get(
            self.test_url,
        )
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test auth with incorrect credentials
        auth_response = self.client.post(self.login_url,
                                         {'username': 'invalid_username', 'password': self.password},
                                         format='json')
        self.assertEqual(auth_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(auth_response.json(), {'detail': 'No active account found with the given credentials'})

        # Successfully auth
        auth_response = self.client.post(self.login_url,
                                    {'username': self.test_user.username, 'password': self.password},
                                    format='json').json()
        response = self.client.get(
            self.test_url,
            HTTP_AUTHORIZATION=f'Bearer {auth_response["access"]}',
        )

        self.assertEqual(response.json(), {'count': 0, 'next': None, 'previous': None, 'results': []})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh token
        response = self.client.post(
            self.refresh_token,
            data={"refresh": auth_response["refresh"]}
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", data)

        # Get data with new token
        response = self.client.get(
            self.test_url,
            HTTP_AUTHORIZATION=f'Bearer {data["access"]}',
        )
        self.assertEqual(response.json(), {'count': 0, 'next': None, 'previous': None, 'results': []})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
