from django.db.models import Q
from rest_framework import serializers
from store.models import (Product, Collection, Image, News, AboutUs, AboutUsImage, Help,
                          PublicOffer, Slider, HelpImage, Advantage, FirstFooter, SecondFooter)


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


class HelpImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Help
        fields = '__all__'


class HelpSerializer(serializers.ModelSerializer):
    answers_questions = serializers.SerializerMethodField('get_help')

    class Meta:
        model = HelpImage
        fields = '__all__'

    def get_help(self, image):
        help = Help.objects.filter(image=image)
        serializer = HelpImageSerializer(instance=help.image, many=True)
        return serializer.data


class PublicOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicOffer
        fields = ('title', 'text')


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'


class MainPageSerializer(serializers.ModelSerializer):
    slider = serializers.SerializerMethodField('get_slider')

    class Meta:
        model = Advantage
        fields = '__all__'

    def get_slider(self, obf):
        slider = Slider.objects.filter(active=True)
        slider_ser = SliderSerializer(instance=slider, many=True).data
        return slider_ser


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondFooter
        fields = ('link',)


class FooterSerializer(serializers.ModelSerializer):
    numbers = serializers.SerializerMethodField('get_number')

    class Meta:
        model = FirstFooter
        fields = '__all__'

    def get_number(self, obj):
        number = SecondFooter.objects.filter(footer=obj)
        number_data = NumberSerializer(instance=number, many=True)
        return number_data.data


class SearhcWithHintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name',)