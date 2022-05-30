from django.db.models import Q
from rest_framework import serializers
from store.models import Product, Collection, Image, News, AboutUs, AboutUsImage, Help, PublicOffer, Slider


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'color',)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'image', 'name')


class SimilarProduct(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, product):
        image = Image.objects.filter(product=product)
        serializer = ProductImageSerializer(instance=image, many=True)
        return serializer.data


class SimilarProductSerializer(SimilarProduct):
    product_image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_image', 'price', 'discount_price', 'discount_percent', 'size',)


class CartSerializer(SimilarProduct):
    product_image = serializers.SerializerMethodField('get_image')
    # quantity = serializers.SerializerMethodField('_get_quantity')

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_image', 'price', 'discount_price', 'discount_percent', 'size',)

    def _get_quantity(self, obj):
        return self.context.get('quantity')


class ProductSerializer(SimilarProduct):
    product_image = serializers.SerializerMethodField('get_image')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('image', 'title', 'text')


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
        fields = ('title', 'text')


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'

