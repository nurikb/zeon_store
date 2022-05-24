from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from store.models import Product, Collection, Order, OrderDetail, Image
from store.forms import ProductForm, ImageForm


class ProductFormAdmin(admin.ModelAdmin):
    form = ProductForm
    fieldsets = (
        (_('Основные'), {'fields': (
            'name',
            'price',
            'color',
            'image',
            'collection',
            'size',
            'quantity',
            'about_text'
        )}),
    )
    search_fields = ('name', 'category')


class ImageFormAdmin(admin.ModelAdmin):
    form = ImageForm
    fields = ('image', 'color')


admin.site.register(Order)
admin.site.register(Image, ImageFormAdmin)
admin.site.register(OrderDetail)
admin.site.register(Collection)
admin.site.register(Product, ProductFormAdmin)
