from django.db.models import Q
from rest_framework import serializers
from store.models import Product, Collection, Image, News, AboutUs, AboutUsImage, Help, PublicOffer


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


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model =News
        fields = '__all__'


class AboutUsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsImage
        fields = '__all__'


class AboutUsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = AboutUs
        fields = '__all__'

    def get_image(self, about):
        image = AboutUsImage.objects.filter(about_us=about)
        serializer = AboutUsImageSerializer(instance=image, many=True)
        return serializer.data


class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = '__all__'


class PublicOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicOffer
        fields = '__all__'





