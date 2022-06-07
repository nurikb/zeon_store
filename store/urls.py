from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.views import (CollectionAPIView, ProductDetailAPIView, CollectionProductsItem, OrderAPIView)
from store.search_views import SearchAPIView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('collection', CollectionAPIView.as_view(), name='collection'),
    path('collection/<int:pk>', CollectionProductsItem.as_view(), name='collection_detail'),
    path('product/<int:pk>', ProductDetailAPIView.as_view()),
    path('search/', SearchAPIView.as_view(), name='search'),
    path('order', OrderAPIView.as_view(), name='order'),
]
