from django.db import models
from users.models import Author

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"
    LOST = "Lost"
    STATUS_CHOICES = [
        (AVAILABLE, "Available"),
        (BORROWED, "Borrowed"),
        (LOST, "Lost"),
    ]

    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    isbn = models.CharField(max_length=13, unique=True)
    category = models.ForeignKey(
        Category, max_length=100, on_delete=models.CASCADE, related_name="books"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
