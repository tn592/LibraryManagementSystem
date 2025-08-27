from django.urls import path, include
from book.views import BookViewSet, CategoryViewSet
from borrow_record.views import BorrowRecordViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("books", BookViewSet, basename="books")
router.register("categories", CategoryViewSet)
router.register("borrow", BorrowRecordViewSet, basename="borrow")

book_router = routers.NestedDefaultRouter(router, "books", lookup="book")

urlpatterns = router.urls

urlpatterns = [
    path("", include(router.urls)),
    path("", include(book_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
