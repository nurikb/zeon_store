from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.views import (CollectionAPIView, NewsAPIView, AboutUsViewSet, HelpViewSet, PublicOfferAPIView,
    MainPageAPIView, ProductDetailAPIView, CollectionProductsItem)

router = DefaultRouter()

router.register('about-us', AboutUsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('main', MainPageAPIView.as_view(), name='main'),
    path('collection/', CollectionAPIView.as_view(), name='main'),
    path('collection/<int:pk>', CollectionProductsItem.as_view(), name='main'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view()),
    path('news/', NewsAPIView.as_view(), name='main'),
    path('public-offer/', PublicOfferAPIView.as_view(), name='public_offer'),
]
