from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from fieldsets_with_inlines import FieldsetsInlineMixin


from store.models import (Product, Collection, News, Image, AboutUsImage, AboutUs, Help, PublicOffer, Order, Client,
                          OrderDetail, Advantage, Slider, HelpImage, CallBack, FirstFooter, SecondFooter)
from store.forms import ProductForm, SvgImageForm


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


class AdvantageFormAdmin(admin.ModelAdmin):
    model = Advantage
    form = SvgImageForm
    fields = ('icon','title', 'text')


class HelpInline(admin.StackedInline):
    model = Help
    extra = 0
    fields = ('question', 'answer')


class HelpFormAdmin(admin.ModelAdmin):
    model = HelpImage
    inlines = (HelpInline,)
    fields = ('image',)


class CallBackFormAdmin(admin.ModelAdmin):
    model = CallBack
    fields = ('name', 'phone_number', 'callback_type', 'contacted', 'date')
    readonly_fields = ('date',)


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
    readonly_fields = ('date',)


class OrderFormAdmin(admin.ModelAdmin):
    model = Order
    inlines = (ClientInline, OrderDetailInline)
    extra = 0
    fields = ('product_quantity', 'total_quantity', 'discount_sum', 'discount_price', 'total_price',)


class SecondFooterInline(admin.StackedInline):
    model = SecondFooter
    extra = 0


class FooterFormAdmin(admin.ModelAdmin):
    model = FirstFooter
    inlines = (SecondFooterInline,)


class HasAddPermission(admin.ModelAdmin):
    def has_add_permission(self, request):
        """Лимит на создание обьектов модели"""
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True


class AboutUsImageInline(admin.StackedInline):
    max_num = 3
    extra = 0
    model = AboutUsImage
    fields = ('image',)


class AboutUsFormAdmin(HasAddPermission):
    model = AboutUs
    inlines = (AboutUsImageInline,)
    list_display = ('title', 'text')


class PublicOfferFormAdmin(HasAddPermission):
    model = PublicOffer


admin.site.register(AboutUs, AboutUsFormAdmin)
admin.site.register(Advantage, AdvantageFormAdmin)
admin.site.register(Product, ProductFormAdmin)
admin.site.register(Slider)
admin.site.register(CallBack, CallBackFormAdmin)
admin.site.register(News)
admin.site.register(HelpImage, HelpFormAdmin)
admin.site.register(Collection)
admin.site.register(PublicOffer, PublicOfferFormAdmin)
admin.site.register(FirstFooter, FooterFormAdmin)
admin.site.register(Order, OrderFormAdmin)
