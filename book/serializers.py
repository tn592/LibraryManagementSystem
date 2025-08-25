from rest_framework import serializers
from book.models import Category, Book


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "book_count"]

    book_count = serializers.IntegerField(read_only=True)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "status", "category"]  # other
