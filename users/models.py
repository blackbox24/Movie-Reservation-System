from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    ROLES = (("user", "USER"), ("admin", "ADMIN"))
    role = models.CharField(max_length=6, choices=ROLES, default="user")
