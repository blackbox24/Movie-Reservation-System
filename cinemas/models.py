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
