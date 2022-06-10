from django.contrib.admin import TabularInline, StackedInline
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

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


class OrderDetailInline(SuperInlineModelAdmin, TabularInline):
    def discount_price_tag(self, obj):
        if obj.discount_price:
            return True
        return False
    model = OrderDetail
    extra = 0
    max_num = 0
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

    def has_delete_permission(self, request, obj):
        return False

    product_image_tag.short_description = 'Image'
    size.short_description = 'размерный ряд'
    price.short_description = 'цена'
    discount_price.short_description = 'цена со скидкой'


class OrderFormAdmin(SuperInlineModelAdmin, StackedInline):
    model = Order
    inlines = (OrderDetailInline,)
    extra = 0
    max_num = 0
    fields = ('product_quantity', 'total_quantity', 'discount_sum', 'discount_price', 'total_price',)
    readonly_fields = ('product_quantity', 'total_quantity', 'discount_sum', 'discount_price', 'total_price',)

    def has_delete_permission(self, request, obj):
        return False


class ClientFormAdmin(SuperModelAdmin):
    model = Client
    inlines = (OrderFormAdmin,)
    extra = 0
    search_fields = ('name', 'email', 'status')
    fieldsets = (
        ('Клиент', {'fields': (
                        ('surname', 'name',),
                        ('country', 'city',),
                        'email',
                        'date',
                        'status')}),
    )
    readonly_fields = ('date', 'surname', 'name', 'country', 'city', 'email')


admin.site.register(Product, ProductFormAdmin)
admin.site.register(Collection)
admin.site.register(Client, ClientFormAdmin)
