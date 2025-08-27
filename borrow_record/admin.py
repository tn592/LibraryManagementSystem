from django.contrib import admin
from borrow_record.models import BorrowRecord

# Register your models here.


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
