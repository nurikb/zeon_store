from django.core.paginator import InvalidPage
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response

from about_store.models import (News, AboutUs, HelpImage, PublicOffer, Advantage, FirstFooter, CallBack)
from cart.favorite import Favorite
from store.models import Product
from about_store.serializers import (NewsSerializer, AboutUsSerializer, HelpSerializer, PublicOfferSerializer,
                                     MainPageSerializer, FooterSerializer)
from store.serializers import SimilarProductSerializer


class NewsAPIView(generics.ListAPIView):
    """API для раздела "Новости" """
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class AboutUsViewSet(generics.ListAPIView):
    """API для раздела "О нас" """
    serializer_class = AboutUsSerializer

    def get(self, request):
        about_us = AboutUs.objects.all().first()
        about_us_data = AboutUsSerializer(about_us).data
        return Response(about_us_data)


class HelpViewSet(generics.ListAPIView):
    """API для раздела "Помощь/Вопросы и ответы" """
    serializer_class = HelpSerializer

    def get(self, request):
        help_obj = HelpImage.objects.all()
        help_ser_data = HelpSerializer(help_obj, many=True).data
        return Response(help_ser_data)


class PublicOfferAPIView(generics.ListAPIView):
    """API для раздела "Публичный оффер" """
    serializer_class = PublicOfferSerializer

    def get(self, request):
        p_offer = PublicOffer.objects.all().first()
        p_offer_serializer = PublicOfferSerializer(p_offer).data
        return Response(p_offer_serializer)


class CursorSetPagination(CursorPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    ordering = 'id' # '-created' is default


class SerializerContext(generics.ListAPIView):

    def get_serializer_context(self):
        favorite = Favorite(self.request)
        return {'favorite': favorite.favorite}


class MainPageTopSalesAPIView(SerializerContext):
    queryset = Product.objects.filter(top_sales=True)
    serializer_class = SimilarProductSerializer


class MainPageNewAPIView(SerializerContext):
    """API для раздела "Новинки" главной страницы"""
    pagination_class = CursorSetPagination
    queryset = Product.objects.filter(new=True)
    serializer_class = SimilarProductSerializer


class MainPageAdvantageAPIView(generics.ListAPIView):
    """API для раздела "Наши преимущества" главной страницы"""
    queryset = Advantage.objects.all()
    serializer_class = MainPageSerializer


class FooterAPIView(generics.ListAPIView):
    """API для раздела "Футер" """
    queryset = FirstFooter.objects.all()
    serializer_class = FooterSerializer


class CallBackAPIView(generics.ListAPIView):

    """API для 'Обратного звонка'"""

    def post(self, request):

        name = request.data.get('name')
        phone = request.data.get('phone')
        type = request.data.get('callback_type')
        callback = CallBack(name=name, phone_number=phone, callback_type=type)
        try:
            callback.save()
            return Response({'success': True})
        except:
            return Response({'success': False})

