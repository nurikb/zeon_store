from django.db.models import Q
from rest_framework import serializers
from store.models import Product, Collection, Image


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'color',)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class SimilarProductMixin(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, product):
        image = Image.objects.filter(product=product)
        serializer = ProductImageSerializer(instance=image, many=True)
        return serializer.data

    def get_similar(self, product):
        similar_product = Product.objects.filter(Q(collection__id=product.collection.id) & ~Q(id=product.id))[:5]
        serializer = SimilarProductSerializer(instance=similar_product, many=True)
        return serializer.data


class SimilarProductSerializer(SimilarProductMixin):
    product_image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_image', 'price', 'discount_price', 'discount_percent', 'size',)


class ProductSerializer(SimilarProductMixin):
    product_image = serializers.SerializerMethodField('get_image')
    similar_product = serializers.SerializerMethodField('get_similar')






