from django.db import models
from book.models import Book
from users.models import User
from uuid import uuid4


# Create your models here.
class BorrowRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrow_records"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrow_records"
    )
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} borrowed {self.book}"
