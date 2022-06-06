import random

from django.contrib import auth
from django.db.models import Q, Count
from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.cart import Cart
from store.models import (Product, Collection, News, AboutUs, Help, Client, Order, OrderDetail,
                          PublicOffer, Slider, Advantage, CallBack, FavoriteProduct, Image, FirstFooter, SecondFooter,
                          HelpImage)
from store.serializers import (ProductDetailSerializer, CollectionSerializer, NewsSerializer,
                               AboutUsSerializer, HelpSerializer, PublicOfferSerializer, SliderSerializer,
                               SimilarProductSerializer, MainPageSerializer, SearhcWithHintSerializer, FooterSerializer)
from cart.favorite import Favorite
from cart.views import APIListPagination


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        favorite = Favorite(request)
        serializer_data = ProductDetailSerializer(product, context={'favorite': favorite.favorite}).data
        similar_product = Product.objects.filter(Q(collection__id=product.collection.id) & ~Q(id=product.id))[:5]
        similar_product_data = SimilarProductSerializer(similar_product, many=True, context={'favorite': favorite.favorite}).data
        return Response({'product': serializer_data, 'similar_products': similar_product_data})


class CollectionAPIView(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class SerializerContext(generics.ListAPIView):

    def get_serializer_context(self):
        favorite = Favorite(self.request)
        return {'favorite': favorite.favorite}


class CollectionProductsItem(SerializerContext):

    """View для товаров в коллекции + новинки"""

    queryset = Product.objects.all()
    serializer_class = SimilarProductSerializer
    pagination_class = APIListPagination

    def get_queryset(self):

        """фильтрация товаров по коллекции"""

        return self.queryset.filter(collection__id=self.kwargs['pk'])

    def list(self, request, *args, **kwargs):

        """переопределил list():добавил к отфильтрованным товарам "'Новинки'"""

        queryset = self.filter_queryset(self.get_queryset())
        new_product = Product.objects.filter(new=True)[:5]
        new_product_ser = SimilarProductSerializer(new_product, many=True).data

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response({'collection_product': serializer.data, 'new_product': new_product_ser})


class NewsAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class AboutUsViewSet(generics.ListAPIView):
    serializer_class = AboutUsSerializer

    def get(self, request):
        about_us = AboutUs.objects.all().first()
        about_us_data = AboutUsSerializer(about_us).data
        return Response(about_us_data)


class HelpViewSet(generics.ListAPIView):
    serializer_class = HelpSerializer

    def get(self, request):
        help_obj = HelpImage.objects.all()
        help_ser_data = HelpSerializer(help_obj, many=True).data
        return Response(help_ser_data)


class PublicOfferAPIView(generics.ListAPIView):
    serializer_class = PublicOfferSerializer

    def get(self, request):
        p_offer = PublicOffer.objects.all().first()
        p_offer_serializer = PublicOfferSerializer(p_offer).data
        return Response(p_offer_serializer)


class MainPageTopSalesAPIView(SerializerContext):
    queryset = Product.objects.filter(top_sales=True)
    serializer_class = SimilarProductSerializer


class MainPageNewAPIView(SerializerContext):
    queryset = Product.objects.filter(new=True)
    serializer_class = SimilarProductSerializer


class MainPageAdvantageAPIView(generics.ListAPIView):
    queryset = Advantage.objects.all()
    serializer_class = MainPageSerializer


class FooterAPIView(generics.ListAPIView):
    queryset = FirstFooter.objects.all()
    serializer_class = FooterSerializer


class CallBackAPIView(generics.ListAPIView):

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


class OrderAPIView(APIView):
    def post(self, request):
        name = request.data.get('name')
        surname = request.data.get('surname')
        country = request.data.get('country')
        city = request.data.get('city')
        email = request.data.get('email')
        cart = Cart(request)
        products = cart.get_full_cart()
        price = cart.get_total_price()
        total_price = price['price']
        discount_price = price['discount_price']
        discount_sum = total_price - discount_price
        cart_count = cart.get_product_count(products[0])

        try:
            order = Order(total_quantity=cart_count['total_count'], total_price=total_price,
                          discount_price=discount_price, discount_sum=discount_sum, product_quantity=cart_count['product_quantity'])
            order.save()

            client = Client(name=name, surname=surname, country=country, city=city, email=email, order=order)
            client.save()

            for product_id, product_data in cart.cart.items():
                for color, quantity in product_data['color_quantity'].items():
                    order_detail = OrderDetail(order=order, product_id=int(product_id), quantity=quantity, product_image_id=int(color))
                    order_detail.save()
            return Response({'success': True})
        except Exception as e:
            order.delete()
            return Response({'success': False})

