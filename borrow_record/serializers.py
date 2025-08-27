from rest_framework import serializers
from borrow_record.models import BorrowRecord
from book.models import Book
from users.models import User


class EmptySerializer(serializers.Serializer):
    pass


class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "isbn", "status"]


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]


class CreateBorrowRecordSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found.")

        if book.status != "available":
            raise serializers.ValidationError("Book is not available for borrowing.")
        user = self.context["user"]
        if BorrowRecord.objects.filter(user=user, book=book).exists():
            raise serializers.ValidationError(
                "already borrowed this book and not returned yet"
            )

        return book_id

    def create(self, validated_data):
        user = self.context["user"]
        book = Book.objects.get(pk=validated_data["book_id"])
        book.status = "borrowed"
        book.save()

        borrow_record = BorrowRecord.objects.create(user=user, book=book)
        return borrow_record

    def to_representation(self, instance):
        return BorrowRecordSerializer(instance).data


class UpdateBorrowRecordSerializer(serializers.ModelSerializer):
    return_date = serializers.DateField(read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ["return_date"]


class BorrowRecordSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    book = SimpleBookSerializer()

    class Meta:
        model = BorrowRecord
        fields = ["id", "user", "book", "borrow_date", "return_date"]
