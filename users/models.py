from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    membership_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    USERNAME_FIELD = "email"  # Use email instead of username
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
