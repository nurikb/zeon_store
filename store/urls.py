from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.views import (CollectionAPIView, NewsAPIView, AboutUsViewSet, HelpViewSet, PublicOfferAPIView,
                         MainPageTopSalesAPIView, ProductDetailAPIView, CollectionProductsItem, MainPageNewAPIView)

router = DefaultRouter()

router.register('about-us', AboutUsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('main-top-sales', MainPageTopSalesAPIView.as_view(), name='main_top_sales'),
    path('main-new', MainPageNewAPIView.as_view(), name='main_new'),
    path('collection/', CollectionAPIView.as_view(), name='collection'),
    path('collection/<int:pk>', CollectionProductsItem.as_view(), name='collection_detail'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view()),
    path('news/', NewsAPIView.as_view(), name='news'),
    path('public-offer/', PublicOfferAPIView.as_view(), name='public_offer'),
]
