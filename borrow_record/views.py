from rest_framework.viewsets import ModelViewSet
from borrow_record.models import BorrowRecord
from borrow_record.serializers import (
    BorrowRecordSerializer,
    AddBorrowRecordSerializer,
    UpdateBorrowRecordSerializer,
)


class BorrowRecordViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddBorrowRecordSerializer
        elif self.request.method == "PATCH":
            return UpdateBorrowRecordSerializer
        return BorrowRecordSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def get_queryset(self):
        return BorrowRecord.objects.select_related("book", "user").all()
