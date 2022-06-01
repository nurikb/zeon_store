from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from rest_framework.pagination import PageNumberPagination

from cart.cart import Cart
from cart.favorite import Favorite
from store.models import Product
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from store.serializers import SimilarProductSerializer, CartSerializer


class APIListPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 10


class AddToCart(APIView):

    def post(self, request, pk):
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        quantity = request.data.get('quantity')
        update = request.data.get('update')
        if update:
            cart.add(product, quantity=quantity, update_quantity=True)
        else:
            cart.add(product)
        return Response({'success': True})


class CartRemove(APIView):

    def post(self, request, pk):
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        cart.remove(product)
        return Response({'success': True})


class CartInfo(APIView):
    def get(self, request):
        cart = Cart(request)
        product = cart.get_full_cart()
        cart_data = CartSerializer(product, many=True, context={'quantity': cart.cart}).data
        price = cart.get_total_price()
        total_price = price['price']
        discount_price = price['discount_price']
        discount_sum = total_price - discount_price
        count = cart.get_product_count(product)
        return Response({'product': cart_data, 'total_price': total_price, 'discount_price': discount_price,
                         'discount_sum': discount_sum, 'product_count': count['total_count'],
                         'product_quantity': count['product_quantity']})


class AddToFavorite(APIView):

    def post(self, request, pk):
        fav = Favorite(request)
        product = get_object_or_404(Product, id=pk)
        fav.add(product)
        return Response({'success': True})


class FavoriteRemove(APIView):

    def post(self, request, pk):
        fav = Favorite(request)
        product = get_object_or_404(Product, id=pk)
        fav.remove(product)
        return Response({'success': True})


class FavoriteInfo(generics.ListAPIView):
    queryset = Product.objects.all()
    pagination_class = APIListPagination
    serializer_class = SimilarProductSerializer

    def get_serializer(self, *args, **kwargs):
        favorite = Favorite(self.request)
        return super(FavoriteInfo, self).get_serializer(*args, **kwargs, context={'favorite': favorite.favorite})

    def get_queryset(self):
        fav = Favorite(self.request)
        return self.queryset.filter(id__in=fav.favorite)
