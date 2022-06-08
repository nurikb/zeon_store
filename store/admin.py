from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from store.models import (Product, Collection, Image, Order, Client, OrderDetail)
from store.forms import ProductForm


class ProductImageInline(admin.StackedInline):
    max_num = 8
    extra = 0
    model = Image
    fields = ('image', 'color',)


class ProductFormAdmin(admin.ModelAdmin):
    form = ProductForm
    inlines = (ProductImageInline,)
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
            'top_sales',
            'new'
        )}),
    )
    search_fields = ('name', 'category')
    list_display = ('name', 'collection_id')


class OrderDetailInline(admin.StackedInline):
    model = OrderDetail
    extra = 0
    fieldsets = (
        ('Товар', {'fields': (
            ('product', 'color', 'product_image_tag'),
            ('size', 'quantity', 'price', 'discount_price')),
                }),
    )
    readonly_fields = ('quantity', 'product', 'product_image_tag', 'size', 'price', 'discount_price')

    def product_image_tag(self, obj):
        """Отображение картинки в админ панели"""
        return mark_safe('<img src="%s" width="150" height="150" />' % (obj.product_image.image.url))

    def discount_price(self, obj):
        """Отображение цены со скидкой в админ панели"""
        if obj.product.discount_percent:
            return obj.product.discount_price

    def price(self, obj):
        """Отображение цены в админ панели"""
        return obj.product.price

    def size(self, obj):
        """Отображение размера в админ панели"""
        return obj.product.size

    product_image_tag.short_description = 'Image'
    size.short_description = 'размерный ряд'
    price.short_description = 'цена'
    discount_price.short_description = 'цена со скидкой'

    def has_add_permission(self, request, obj):
        return False


class ClientInline(admin.StackedInline):
    model = Client
    extra = 0
    fieldsets = (
        ('Клиент', {'fields': (
                        ('surname', 'name',),
                        ('country', 'city',),
                        'email',
                        'date',
                        'status')}),
    )
    readonly_fields = ('date', 'surname', 'name', 'country', 'city', 'email')

    def has_add_permission(self, request, obj):
        return False


class OrderFormAdmin(admin.ModelAdmin):
    model = Order
    inlines = (ClientInline, OrderDetailInline)
    extra = 0
    fields = ('product_quantity', 'total_quantity', 'discount_sum', 'discount_price', 'total_price',)


admin.site.register(Product, ProductFormAdmin)
admin.site.register(Collection)
admin.site.register(Order, OrderFormAdmin)
