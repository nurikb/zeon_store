from rest_framework import viewsets
from rest_framework import permissions
from store.models import Product, Collection, News, AboutUs, Help, PublicOffer
from store.serializers import ProductSerializer, CollectionSerializer, NewsSerializer, AboutUsSerializer, HelpSerializer, PublicOfferSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    """
    API
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer


class HelpViewSet(viewsets.ModelViewSet):
    queryset = Help.objects.all()
    serializer_class = HelpSerializer


class PublicOfferViewSet(viewsets.ModelViewSet):
    queryset = PublicOffer.objects.all()
    serializer_class = PublicOfferSerializer



