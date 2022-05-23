from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.views import ProductViewSet, CategoryViewSet

router = DefaultRouter()

router.register('product', ProductViewSet)
router.register('category', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]