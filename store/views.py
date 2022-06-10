from django.contrib import auth
from django.db.models import Q
from rest_framework import  generics
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.cart import Cart
from store.models import (Product, Collection, Client, Order, OrderDetail, FavoriteProduct)
from store.serializers import ProductDetailSerializer, CollectionSerializer, SimilarProductSerializer
from cart.favorite import Favorite
from cart.views import APIListPagination


class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer

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

    def get_serializer_context(self):
        favorite = Favorite(self.request)
        return {'favorite': favorite.favorite}

    def list(self, request, *args, **kwargs):

        """переопределил list():добавил к отфильтрованным товарам "'Новинки'"""

        queryset = self.filter_queryset(self.get_queryset())
        new_product = Product.objects.filter(new=True)[:5]
        new_product_ser = SimilarProductSerializer(new_product, many=True).data

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response({'collection_product': serializer.data, 'new_product': new_product_ser})


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
            client = Client(name=name, surname=surname, country=country, city=city, email=email)
            client.save()

            order = Order(total_quantity=cart_count['total_count'], total_price=total_price,
                          discount_price=discount_price, discount_sum=discount_sum,
                          product_quantity=cart_count['product_quantity'], client=client)
            order.save()

            for product_id, product_data in cart.cart.items():
                for color, quantity in product_data['color_quantity'].items():
                    order_detail = OrderDetail(order=order, product_id=int(product_id),
                                               quantity=quantity, product_image_id=int(color))
                    order_detail.save()
                    print(order_detail)
            # cart.clear()
            return Response({'success': True})
        except Exception as e:
            order.delete()
            return Response({'success': False})

