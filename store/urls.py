from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.views import (CollectionAPIView, NewsAPIView, AboutUsViewSet, HelpViewSet, PublicOfferAPIView,
                         MainPageTopSalesAPIView, ProductDetailAPIView, CollectionProductsItem, MainPageNewAPIView,
                         CallBackAPIView, MainPageAdvantageAPIView, OrderAPIView, FooterAPIView)
from store.search_views import SearchAPIView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('main-top-sales', MainPageTopSalesAPIView.as_view(), name='main_top_sales'),
    path('main-new', MainPageNewAPIView.as_view(), name='main_new'),
    path('main-collection', CollectionAPIView.as_view(), name='main_collection'),
    path('main-advantage', MainPageAdvantageAPIView.as_view(), name='main_advantage'),
    path('footer', FooterAPIView.as_view(), name='footer'),
    path('collection/', CollectionAPIView.as_view(), name='collection'),
    path('collection/<int:pk>', CollectionProductsItem.as_view(), name='collection_detail'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view()),
    path('news/', NewsAPIView.as_view(), name='news'),
    path('public-offer/', PublicOfferAPIView.as_view(), name='public_offer'),
    path('about-us/', AboutUsViewSet.as_view(), name='about_us'),
    path('help/', HelpViewSet.as_view(), name='help'),
    path('callback/', CallBackAPIView.as_view(), name='callback'),
    path('search/', SearchAPIView.as_view(), name='search'),
    path('order/', OrderAPIView.as_view(), name='order'),
]
