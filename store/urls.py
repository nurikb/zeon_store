from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.views import ProductViewSet, CollectionViewSet

router = DefaultRouter()

router.register('product', ProductViewSet)
router.register('category', CollectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]