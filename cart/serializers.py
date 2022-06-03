from rest_framework import serializers

from store.models import Product, Image


class CartSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('_get_quantity')

    class Meta:
        model = Product
        fields = ('id', 'name', 'count', 'quantity', 'price', 'discount_price', 'discount_percent', 'size',)

    def _get_quantity(self, obj):
        quantity = self.context.get('quantity')[str(obj.id)]['color_quantity']
        return quantity


class ColorProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField('get_product')

    class Meta:
        model = Image
        fields = ('color', 'image')

    def get_product(self, obj):
        p_data = CartSerializer(instance=obj.produt).data
        return p_data
