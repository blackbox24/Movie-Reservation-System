from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APITestCase

from users.models import User


class AuthTestCase(APITestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username="test_user", password="test_password")

    def test_signup_successful(self, *args, **kwargs):
        url = reverse("signup_view")
        response = self.client.post(
            url,
            data={
                "first_name": "test_firstname",
                "last_name": "test_lastname",
                "username": "test_username",
                "password": "test_firstname",
            },
        )
        is_ava = User.objects.filter(username="test_username").exists()
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertTrue(is_ava)

    def test_login_successful(self):
        url = reverse("login_view")
        response = self.client.post(
            url, data={"username": self.test_user.username, "password": "test_password"}
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
