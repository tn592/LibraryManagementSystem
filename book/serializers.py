from rest_framework import serializers
from book.models import Category, Book
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "book_count"]

    book_count = serializers.IntegerField(read_only=True)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "status", "category"]  # other


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name="get_current_user_name")

    class Meta:
        model = get_user_model()
        fields = ["id", "name"]

    def get_current_user_name(self, obj):
        return obj.get_full_name()
