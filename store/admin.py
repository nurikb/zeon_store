from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from store.models import Product, Collection, Order
from store.forms import ProductForm


class ProductFormAdmin(admin.ModelAdmin):
    form = ProductForm
    fieldsets = (
        (_('Основные'), {'fields': (
            'name',
            'price',
            'collection',
        )}),
    )
    readonly_fields = ('created_at', 'modified_at',)
    search_fields = ('name', 'category')


admin.site.register(Order)
admin.site.register(Collection)
admin.site.register(Product, ProductFormAdmin)
