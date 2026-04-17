# Create your tests here.
import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase

from movies.models import Movie
from users.models import User


class MovieTest(APITestCase):
    def setUp(self) -> None:
        self.admin_user = User.objects.create_user(
            username="testadmin", password="testpass123", role="admin"
        )
        self.normal_user = User.objects.create_user(username="test1admin", password="testpass123")
        self.test_movie = Movie.objects.create(
            title="spiderman", description="spiderman", duration="16:37:18.154Z"
        )

    def test_create_movie_successful(self):
        self.client.force_authenticate(user=self.admin_user)  # type: ignore

        url = reverse("list_create_movie_view")
        response = self.client.get(url)

        movies = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(movies) > 0)

    def test_create_movie_post_fail(self):
        self.client.force_authenticate(user=self.normal_user)  # type: ignore

        url = reverse("list_create_movie_view")
        data = {"title": "test movie", "description": "", "duration": "16:37:18.154Z", "poster": ""}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 403)

    def test_create_movie_post_success(self):
        self.client.force_authenticate(user=self.admin_user)  # type: ignore
        file_response = requests.get(
            "https://images.unsplash.com/photo-1661495896705-dce1b43030b0?ixid=M3w4MjcwNjd8MHwxfHNlYXJjaHwxODF8fGFuaW1lJTIwd2FsbHBhcGVyfGVufDB8fHx8MTc3NjQzNzc3Mnww&ixlib=rb-4.1.0&fit=max&q=80"
        )

        if file_response.status_code != 200:
            self.fail("Could not download file")

        image = SimpleUploadedFile(
            name="testfile.jpg", content=file_response.content, content_type="image/jpeg"
        )
        url = reverse("list_create_movie_view")
        data = {
            "title": "test movie",
            "description": "test movie",
            "duration": "16:37:18.154Z",
            "poster": image,
        }
        response = self.client.post(url, data=data)

        is_ava = Movie.objects.filter(title="test movie").exists()
        print(response.json())

        self.assertEqual(response.status_code, 201)
        self.assertTrue(is_ava)

    def test_retrieve_movie_successful(self):
        self.client.force_authenticate(user=self.admin_user)  # type: ignore

        url = reverse("get_update_delete_movie_view", args=[self.test_movie.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_update_movie_successful(self):
        self.client.force_authenticate(user=self.admin_user)  # type: ignore
        data = {"title": "Man of steel"}
        url = reverse("get_update_delete_movie_view", args=[self.test_movie.pk])
        response = self.client.patch(url, data=data)

        is_ava = Movie.objects.filter(title="Man of steel").exists()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_ava)

    def test_delete_movie_successful(self):
        self.client.force_authenticate(user=self.admin_user)  # type: ignore

        url = reverse("get_update_delete_movie_view", args=[self.test_movie.pk])
        response = self.client.delete(url)

        is_ava = Movie.objects.filter(title="Man of steel").exists()

        self.assertEqual(response.status_code, 204)
        self.assertFalse(is_ava)
