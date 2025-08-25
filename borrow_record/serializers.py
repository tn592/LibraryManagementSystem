from rest_framework import serializers
from borrow_record.models import BorrowRecord
from book.models import Book


class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "status"]


class AddBorrowRecordSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()

    class Meta:
        model = BorrowRecord
        fields = ["id", "book_id", "borrow_date", "return_date"]

    def save(self, **kwargs):
        user_id = self.context["user_id"]
        book_id = self.validated_data["book_id"]

        try:
            borrow_record = BorrowRecord.objects.get(user_id=user_id, book_id=book_id)
        except BorrowRecord.DoesNotExist:
            self.instance = BorrowRecord.objects.create(
                user_id=user_id, book_id=book_id, **self.validated_data
            )
            book = Book.objects.get(pk=book_id)
            book.status = "borrowed"
            book.save()

        return self.instance

    def validate_book_id(self, value):
        if not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Book with id {value} does not exist")
        return value


class UpdateBorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ["return_date"]

    def save(self, **kwargs):
        borrow_record = super().save(**kwargs)
        if borrow_record.return_date:
            borrow_record.book.status = "available"
            borrow_record.book.save()
        return borrow_record


class BorrowRecordSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer()

    class Meta:
        model = BorrowRecord
        fields = ["id", "book", "borrow_date", "return_date"]
