# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import User


class MovieTest(APITestCase):
    def setUp(self) -> None:
        self.admin_user = User.objects.create_user(
            username="testadmin",
            password="testpass123",
            role="admin"
        )
        self.normal_user = User.objects.create_user(
            username="test1admin",
            password="testpass123"
        )

    def test_create_movie_successful(self):
        self.client.force_authenticate(user=self.admin_user) # type: ignore

        url = reverse("list_create_movie_view")
        response = self.client.get(url)

        movies = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(movies), 0)
