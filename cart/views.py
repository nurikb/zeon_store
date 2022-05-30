from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from cart.cart import Cart
from store.models import Product
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from store.serializers import SimilarProductSerializer, CartSerializer


class AddToCart(APIView):

    def post(self, request, pk):
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
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
        quantity_list = [product['quantity'] for product in list(cart.cart.values())]

        product = cart.get_full_cart()
        print(type(product), product)
        for obj, quantity in zip(product, quantity_list):
            product._quantity = quantity
        cart_data = CartSerializer(product, many=True, context={'quantity': quantity_list}).data
        price = cart.get_total_price()
        total_price = price['price']
        discount_price = price['discount_price']
        discount_sum = total_price - discount_price
        return Response({'product': cart_data, 'total_price': total_price, 'discount_price': discount_price,
                         'discount_sum': discount_sum})
