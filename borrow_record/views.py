from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from borrow_record.models import BorrowRecord
from borrow_record import serializers as brSz
from datetime import date


class BorrowRecordViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        borrow_record = self.get_object()

        if borrow_record.user != request.user and not request.user.is_staff:
            raise PermissionDenied(
                {"detail": "you can only return your own borrowed books."}
            )
        if borrow_record.return_date:
            raise ValidationError({"detail": "Book already returned"})
        borrow_record.return_date = date.today()
        borrow_record.save()
        borrow_record.book.status = "available"
        borrow_record.book.save()

        return Response({"status": "Book returned."})

    def get_permissions(self):
        if self.action in ["destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return brSz.CreateBorrowRecordSerializer
        elif self.action == "return_book":
            return brSz.EmptySerializer
        elif self.action == "partial_update":
            return brSz.UpdateBorrowRecordSerializer
        return brSz.BorrowRecordSerializer

    def get_serializer_context(self):
        if getattr(self, "swagger_fake_view", False):
            return super().get_serializer_context()
        return {"user_id": self.request.user.id, "user": self.request.user}

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return BorrowRecord.objects.none()
        if self.request.user.is_staff:
            return BorrowRecord.objects.select_related("book", "user").all()
        return BorrowRecord.objects.select_related("book", "user").filter(
            user=self.request.user
        )
