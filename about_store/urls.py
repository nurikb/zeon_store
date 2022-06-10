from django.urls import path, include
from rest_framework.routers import DefaultRouter
from about_store.views import (NewsAPIView, AboutUsViewSet, HelpViewSet, PublicOfferAPIView, MainPageTopSalesAPIView,
                               MainPageNewAPIView, CallBackAPIView, MainPageAdvantageAPIView, FooterAPIView)
from store.views import CollectionAPIView

router = DefaultRouter()

urlpatterns = [
    path('main/top-sales', MainPageTopSalesAPIView.as_view(), name='main_top_sales'),
    path('main/new', MainPageNewAPIView.as_view(), name='main_new'),
    path('main/collection', CollectionAPIView.as_view(), name='main_collection'),
    path('main/advantage', MainPageAdvantageAPIView.as_view(), name='main_advantage'),
    path('main/footer', FooterAPIView.as_view(), name='footer'),
    path('about-store/news', NewsAPIView.as_view(), name='news'),
    path('about-store/public-offer', PublicOfferAPIView.as_view(), name='public_offer'),
    path('about-store/about-us', AboutUsViewSet.as_view(), name='about_us'),
    path('about-store/help', HelpViewSet.as_view(), name='help'),
    path('callback', CallBackAPIView.as_view(), name='callback'),
]
