from rest_framework.response import Response
from rest_framework import status
from book.models import Book, Category
from book.serializers import BookSerializer, CategorySerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from book.filters import BookFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from book.paginations import DefaultPagination


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    pagination_class = DefaultPagination
    search_fields = ["name"]
    ordering_fields = ["updated_at"]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(book_count=Count("books")).all()
    serializer_class = CategorySerializer
