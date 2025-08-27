from book.models import Book, Category
from book.serializers import BookSerializer, CategorySerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from book.filters import BookFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from book.paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from drf_yasg.utils import swagger_auto_schema


class BookViewSet(ModelViewSet):
    """
    API endpoint for managing books in the Library Management System
     - Allows authenticated admin to create, update, and delete books
     - Allows users to views, borrow and filter book
     - Support searching by title and category
     - Support ordering by updated_at
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    pagination_class = DefaultPagination
    search_fields = ["name"]
    ordering_fields = ["updated_at"]
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(operation_summary="Retrive a list of books")
    def list(self, request, *args, **kwargs):
        """Retrive all the books"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a book by admin",
        operation_description="This allow an admin to create a book",
        request_body=BookSerializer,
        responses={201: BookSerializer, 400: "Bad Request"},
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create book"""
        return super().create(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(book_count=Count("books")).all()
    serializer_class = CategorySerializer
