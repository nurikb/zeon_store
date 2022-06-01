from django.contrib import auth
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import viewsets, generics, status
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from store.models import Product, Collection, News, AboutUs, Help, PublicOffer, Slider, Advantage, CallBack, FavoriteProduct
from store.serializers import ProductSerializer, CollectionSerializer, NewsSerializer, AboutUsSerializer, HelpSerializer,\
    PublicOfferSerializer, SliderSerializer, SimilarProductSerializer, MainPageSerializer
from cart.favorite import Favorite


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        favorite = Favorite(request)
        serializer_data = ProductSerializer(product, context={'favorite': favorite.favorite}).data
        similar_product = Product.objects.filter(Q(collection__id=product.collection.id) & ~Q(id=product.id))[:5]
        similar_product_data = SimilarProductSerializer(similar_product, many=True, context={'favorite': favorite.favorite}).data
        return Response({'product': serializer_data, 'similar_products': similar_product_data})


class CollectionAPIView(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CollectionProductsItem(generics.ListAPIView):

    """View для товаров в коллекции + новинки"""
    queryset = Product.objects.all()
    serializer_class = SimilarProductSerializer

    def get_queryset(self):
        """фильтрация товаров по коллекции"""
        return self.queryset.filter(collection__id=self.kwargs['pk'])

    def list(self, request, *args, **kwargs):
        # добавил к отфильтрованным товарам "Новинки"
        queryset = self.filter_queryset(self.get_queryset())
        favorite = Favorite(request)
        new_product = Product.objects.filter(new=True)[:5]
        new_product_ser = SimilarProductSerializer(new_product, many=True, context={'favorite': favorite.favorite}).data

        page = self.paginate_queryset(queryset)
        test = self.paginate_queryset(new_product_ser)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'collection_product': serializer.data, 'new_product': test})

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NewsAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class AboutUsViewSet(APIView):
    def get(self, request):
        about_us = AboutUs.objects.all().first()
        about_us_data = AboutUsSerializer(about_us).data
        return Response(about_us_data)


class HelpViewSet(APIView):
    def get(self, request):
        help_obj = Help.objects.all()
        help_ser_data = HelpSerializer(help_obj, many=True).data
        return Response(help_ser_data)


class PublicOfferAPIView(APIView):
    def get(self, request):
        p_offer = PublicOffer.objects.all().first()
        p_offer_serializer = PublicOfferSerializer(p_offer).data
        return Response(p_offer_serializer)


class MainPageTopSalesAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(top_sales=True)
    serializer_class = SimilarProductSerializer


class MainPageNewAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(new=True)
    serializer_class = SimilarProductSerializer


class MainPageAdvantageAPIView(generics.ListAPIView):
    queryset = Advantage.objects.all()
    serializer_class = MainPageSerializer


class CallBackAPIView(APIView):
    """View для 'Обратного звонка'"""
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


class FavoriteProductAPIView(APIView):
    model = FavoriteProduct
    def get(self, request):
        user = auth.get_user(request)
        print(user, '**************************************')

    # def post(self, request, pk):
    #     user = auth.get_user(request)
    #     print(user, '**************************************')
    #     if user:
    #         print('--------------------------------------')
    #         bookmark, created = self.model.objects.get_or_create(user=user, obj_id=pk)
    #         if not created:
    #             bookmark.delete()
