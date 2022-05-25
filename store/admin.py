from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from store.models import Product, Collection, Order, OrderDetail, Image
from store.forms import ProductForm, ImageForm


class ImageTableInline(admin.StackedInline):
    model = Image
    fields = ('image', 'color',)


class ProductFormAdmin(admin.ModelAdmin):
    form = ProductForm
    inlines = (ImageTableInline,)
    fieldsets = (
        (_('Основные'), {'fields': (
            'collection',
            'name',
            'article',
            'price',
            'discount_price',
            'discount_percent',
            'about_text',
            'size',
            'substance',
            'quantity',
            'material',


        )}),
    )
    search_fields = ('name', 'category')


# admin.site.register(Order)
# admin.site.register(OrderDetail)
admin.site.register(Collection)
admin.site.register(Product, ProductFormAdmin)
