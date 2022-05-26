from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.views import ProductViewSet, CollectionViewSet, NewsViewSet, AboutUsViewSet, HelpViewSet, PublicOfferViewSet, MainPageAPIView

router = DefaultRouter()

router.register('product', ProductViewSet)
router.register('category', CollectionViewSet)
router.register('news', NewsViewSet)
router.register('about-us', AboutUsViewSet)
router.register('help', HelpViewSet)
router.register('public-offer', PublicOfferViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('main', MainPageAPIView.as_view(), name='main')
]
