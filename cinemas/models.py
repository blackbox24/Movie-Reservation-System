from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Cinema(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    total_screen = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

# Create your models here.
class Screen(models.Model):
    cinema_id = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    screen_number = models.CharField(max_length=20, null=False, blank=False)
    total_seats = models.IntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    def __str__(self):
        return f"Screen: #{self.screen_number}, cinema: #{self.cinema_id}"

    class Meta:
        indexes = [
            models.Index(
                fields=("cinema_id",),
            ),
        ]

        unique_together = ["cinema_id", "screen_number"]
