from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import viewsets, generics, status
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from store.models import Product, Collection, News, AboutUs, Help, PublicOffer, Slider
from store.serializers import ProductSerializer, CollectionSerializer, NewsSerializer, AboutUsSerializer, HelpSerializer,\
    PublicOfferSerializer, SliderSerializer, SimilarProductSerializer


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer_data = ProductSerializer(product).data
        similar_product = Product.objects.filter(Q(collection__id=product.collection.id) & ~Q(id=product.id))[:5]
        similar_product_data = SimilarProductSerializer(similar_product, many=True).data
        return Response({'product': serializer_data, 'similar_products': similar_product_data})


class CollectionAPIView(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class APIListPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 10


class CollectionProductsItem(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = SimilarProductSerializer
    pagination_class = APIListPagination

    def get_queryset(self):
        return self.queryset.filter(collection__id=self.kwargs['pk'])

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        new_product = Product.objects.filter(new=True)[:5]
        new_product_ser = SimilarProductSerializer(new_product, many=True).data

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'collection_product': serializer.data, 'new_product': new_product_ser})

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NewsAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer


class HelpViewSet(APIView):
    def get(self, request, pk):
        help_obj = Help


class PublicOfferAPIView(APIView):
    def get(self, request):
        p_offer = PublicOffer.objects.all().first()
        p_offer_serializer = PublicOfferSerializer(p_offer).data
        return Response(p_offer_serializer)


class MainPageAPIView(APIView):
    def get(self, request):
        top_sales = Product.objects.filter(top_sales=False)[:5]

        return Response({'top_sales': ProductSerializer(top_sales, many=True).data})



