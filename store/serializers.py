from rest_framework import serializers
from store.models import Product, Collection, Image


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'color',)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'image', 'name')


class BaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, product):
        image = Image.objects.filter(product=product)
        serializer = ProductImageSerializer(instance=image, many=True)
        return serializer.data

    def get_favorite(self, obj):
        if self.context.get('favorite'):
            if obj.id in self.context.get('favorite'):
                return True
        return False


class ProductDetailSerializer(BaseProductSerializer):
    product_image = serializers.SerializerMethodField('get_image')
    favorite = serializers.SerializerMethodField('get_favorite')


class SimilarProductSerializer(BaseProductSerializer):
    product_image = serializers.SerializerMethodField('get_image')
    favorite = serializers.SerializerMethodField('get_favorite')

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_image', 'price', 'discount_price', 'discount_percent', 'favorite', 'size',)


class FavoriteSerializer(BaseProductSerializer):
    favorite = serializers.SerializerMethodField('get_favorite')

    class Meta:
        model = Product
        fields = ('id', 'name', 'count', 'quantity', 'product_image', 'price', 'discount_price', 'discount_percent', 'size', 'favorite',)


class SearhcWithHintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name',)