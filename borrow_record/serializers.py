from rest_framework import serializers
from borrow_record.models import BorrowRecord
from book.serializers import BookSerializer
from users.models import User


class BorrowRecordSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    member_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BorrowRecord
        fields = ["id", "book", "borrow_date", "return_date"]

    def validate_book_id(self, value):
        from book.models import Book

        if not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Book with id {value} does not exist.")
        return value

    def validate_member_id(self, value):
        from users.models import User

        if not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Member with id {value} does not exist.")
        return value

    def create(self, validated_data):
        book_id = validated_data.pop("book_id")
        member_id = validated_data.pop("member_id")

        borrow_record = BorrowRecord.objects.create(
            book_id=book_id, member_id=member_id, **validated_data
        )
        return borrow_record
