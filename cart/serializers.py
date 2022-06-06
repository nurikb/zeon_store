from rest_framework import serializers

from store.models import Product, Image


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'quantity', 'price', 'discount_price', 'discount_percent', 'size',)


class ColorProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField('get_product')
    count = serializers.SerializerMethodField('get_count')

    class Meta:
        model = Image
        fields = ('color', 'image', 'count', 'product')

    def get_product(self, obj):
        p_data = CartSerializer(instance=obj.product, context=self.context).data
        return p_data

    def get_count(self, obj):
        return self.context['quantity'][str(obj.product_id)]['color_quantity'][obj.color]
