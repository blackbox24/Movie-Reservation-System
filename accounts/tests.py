from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED
from rest_framework.test import APITestCase

from users.models import User


class AuthTestCase(APITestCase):
    def test_signup_successful(self, *args, **kwargs):
        url = reverse("signup_view")
        response = self.client.post(url, data={
            "first_name":"test_firstname",
            "last_name":"test_lastname",
            "username":"test_username",
            "password":"test_firstname",
        })
        is_ava = User.objects.filter(username="test_username").exists()
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertTrue(is_ava)
