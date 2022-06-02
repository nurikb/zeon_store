from django.contrib import auth
from django.db.models import Q, Count
from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from store.models import (Product, Collection, News, AboutUs, Help, Client, Order, OrderDetail,
                          PublicOffer, Slider, Advantage, CallBack, FavoriteProduct, Image)
from store.serializers import (ProductDetailSerializer, CollectionSerializer, NewsSerializer,
                               AboutUsSerializer, HelpSerializer, PublicOfferSerializer, SliderSerializer,
                               SimilarProductSerializer, MainPageSerializer, SearhcWithHintSerializer)
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


class CollectionProductsItem(generics.ListAPIView):

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
        favorite = Favorite(request)
        new_product = Product.objects.filter(new=True)[:5]
        new_product_ser = SimilarProductSerializer(new_product, many=True, context={'favorite': favorite.favorite}).data

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response({'collection_product': serializer.data, 'new_product': new_product_ser})


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


class SearchAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = SimilarProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ('name', 'collection__name')

    def list(self, request, *args, **kwargs):

        """
        переопределил list(): если нет результата функции self.filter_queryset()
        добавил 5 обьектов класса(модели) Product
        """

        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        filtered_queryset_status = True
        hints = SearhcWithHintSerializer(filtered_queryset, many=True).data

        if not filtered_queryset:
            filtered_queryset_status = False
            collection_id_list = queryset.values('collection').annotate(dcount=Count('collection', )).order_by()[:5]
            product_id_list = [queryset.filter(collection__id=c_product['collection']).first().id for c_product in
                               collection_id_list]
            filtered_queryset = queryset.filter(id__in=product_id_list)

        page = self.paginate_queryset(filtered_queryset)
        favorite = Favorite(request)
        search_param = self.request.GET.get('search')

        serializer = self.get_serializer(page, many=True, context={'favorite': favorite.favorite})
        return self.get_paginated_response({'search_result': serializer.data, 'hints': hints,
                                            'search_param': search_param, 'search_status': filtered_queryset_status})


class OrderAPIView(APIView):
    def post(self, request):
        name = request.data.get('name')
        surname = request.data.get('surname')
        country = request.data.get('country')
        city = request.data.get('city')
        email = request.data.get('email')
        total_price = request.data.get('total_price')
        discount_price = request.data.get('discount_price')
        discount_sum = request.data.get('discount_sum')
        total_quantity = request.data.get('total_quantity')
        product_quantity = request.data.get('product_quantity')
        products = request.data.get('products')

        try:
            client = Client(name=name, surname=surname, country=country, city=city, email=email)
            client.save()
            order = Order(client=client, total_quantity=total_quantity, total_price=total_price,
                          discount_price=discount_price, discount_sum=discount_sum, product_quantity=product_quantity)
            order.save()
            for product in products:
                product_obj = Product.objects.get(id=product['id'])
                image_obj = Image.objects.get(product__id=product['id'], color=product['color'])
                order_detail = OrderDetail(order=order, product=product_obj,
                                           product_image=image_obj, quantity=product['quantity'])
                order_detail.save()
            return Response({'success': True})
        except Exception as e:
            order.delete()
            client.delete()
            print(e)
            return Response({'success': False})

