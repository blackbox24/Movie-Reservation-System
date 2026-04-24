from django.db import models
from django.conf import settings
from showtimes.models import Showtime

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    # In a real app, this might be a URL or a path to a generated QR code
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username} for {self.showtime}"

class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='tickets')
    seat_row = models.CharField(max_length=2)
    seat_number = models.PositiveIntegerField()

    class Meta:
        # Prevent the same seat from being booked twice for the same showtime
        # We need to reach showtime through booking
        # Since unique_together doesn't support spanning relationships directly for database-level constraints,
        # we'll handle this validation in the serializer/clean method.
        unique_together = ('booking', 'seat_row', 'seat_number')

    def __str__(self):
        return f"Ticket for {self.booking.showtime.movie_id.title} - Seat {self.seat_row}{self.seat_number}"
