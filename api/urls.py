from django.urls import path, include

from book.views import BookViewSet, CategoryViewSet

# from order.views import CartViewSet, CartItemViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("books", BookViewSet, basename="books")
router.register("categories", CategoryViewSet)
# router.register('carts', CartViewSet, basename='carts')

book_router = routers.NestedDefaultRouter(router, "books", lookup="book")
# product_router.register('reviews', ReviewViewSet, basename='product-review')

# cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
# cart_router.register('items', CartItemViewSet, basename='cart-item')

urlpatterns = router.urls

urlpatterns = [
    path("", include(router.urls)),
    path("", include(book_router.urls)),
    # path('', include(cart_router.urls))
]
