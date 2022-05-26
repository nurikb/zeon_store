from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from store.models import Product, Collection, News, AboutUs, Help, PublicOffer, Slider
from store.serializers import ProductSerializer, CollectionSerializer, NewsSerializer, AboutUsSerializer, HelpSerializer,\
    PublicOfferSerializer, SliderSerializer


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


class MainPageAPIView(APIView):
    def get(self, request):
        top_sales = Product.objects.filter(top_sales=False)[:5]

        return Response({'top_sales': ProductSerializer(top_sales, many=True).data})



