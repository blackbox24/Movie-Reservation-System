import datetime
from decimal import Decimal

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from bookings.models import Booking, Ticket
from cinemas.models import Cinema, Screen
from movies.models import Movie
from showtimes.models import Showtime
from users.models import User


class BookingTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin", password="password123", role="admin"
        )
        self.normal_user = User.objects.create_user(
            username="user", password="password123", role="user"
        )
        self.other_user = User.objects.create_user(
            username="other", password="password123", role="user"
        )
        self.movie = Movie.objects.create(
            title="The Matrix", description="Red pill or blue pill", duration=136
        )
        self.cinema = Cinema.objects.create(
            name="Cinema Central", city="San Francisco", country="USA", total_screen=1
        )
        # Small screen to test capacity easily
        self.screen = Screen.objects.create(cinema_id=self.cinema, screen_number="1", total_seats=2)

        self.start_time = timezone.now() + datetime.timedelta(days=1)
        self.showtime = Showtime.objects.create(
            movie_id=self.movie,
            screen_id=self.screen,
            start_time=self.start_time,
            base_price=Decimal("12.50"),
        )

    def test_create_booking_success(self):
        url = reverse("booking-list-create")
        self.client.force_authenticate(user=self.normal_user)

        data = {
            "showtime": self.showtime.id,
            "tickets": [{"seat_row": "A", "seat_number": 1}, {"seat_row": "A", "seat_number": 2}],
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(float(response.data["total_amount"]), 25.00)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 2)

    def test_double_booking_prevention(self):
        # First booking
        self.test_create_booking_success()

        # Try to book the same seat with another user
        url = reverse("booking-list-create")
        self.client.force_authenticate(user=self.other_user)

        data = {"showtime": self.showtime.id, "tickets": [{"seat_row": "A", "seat_number": 1}]}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        # Either capacity or specific seat error is acceptable as both prevent the double book
        error_msg = str(response.data)
        self.assertTrue("already booked" in error_msg or "Not enough seats" in error_msg)

    def test_capacity_prevention(self):
        url = reverse("booking-list-create")
        self.client.force_authenticate(user=self.normal_user)

        # Screen only has 2 seats. Try to book 3.
        data = {
            "showtime": self.showtime.id,
            "tickets": [
                {"seat_row": "A", "seat_number": 1},
                {"seat_row": "A", "seat_number": 2},
                {"seat_row": "A", "seat_number": 3},
            ],
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Not enough seats", str(response.data))

    def test_list_bookings_isolation(self):
        # Create booking for normal_user
        self.test_create_booking_success()

        # List as other_user (should see 0)
        url = reverse("booking-list-create")
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(url)
        # Account for pagination
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 0)

        # List as admin (should see 1)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 1)

    def test_cancel_booking(self):
        # Create booking
        self.client.force_authenticate(user=self.normal_user)
        booking = Booking.objects.create(
            user=self.normal_user, showtime=self.showtime, total_amount=Decimal("12.50")
        )

        url = reverse("booking-cancel", args=[booking.id])
        response = self.client.patch(url)

        self.assertEqual(response.status_code, 200)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "cancelled")

    def test_cancel_past_booking_fail(self):
        # Create past showtime and booking
        past_time = timezone.now() - datetime.timedelta(days=1)
        past_showtime = Showtime.objects.create(
            movie_id=self.movie,
            screen_id=self.screen,
            start_time=past_time,
            base_price=Decimal("10.00"),
        )
        booking = Booking.objects.create(
            user=self.normal_user, showtime=past_showtime, total_amount=Decimal("10.00")
        )

        self.client.force_authenticate(user=self.normal_user)
        url = reverse("booking-cancel", args=[booking.id])
        response = self.client.patch(url)

        self.assertEqual(response.status_code, 400)
        self.assertIn("past or ongoing", str(response.data))
