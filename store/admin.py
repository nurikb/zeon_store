from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from store.models import (Product, Collection, News, Image, AboutUsImage, AboutUs, Help, PublicOffer,
                          Advantage, Slider, HelpImage, CallBack, FirstFooter, SecondFooter)
from store.forms import ProductForm, SvgImageForm


class ProductImageInline(admin.StackedInline):
    max_num = 8
    model = Image
    fields = ('image', 'color',)


class AboutUsImageInline(admin.StackedInline):
    max_num = 3
    model = AboutUsImage
    fields = ('image',)


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


        )}),
    )
    search_fields = ('name', 'category')


class AboutUsFormAdmin(admin.ModelAdmin):
    model = AboutUs
    inlines = (AboutUsImageInline,)
    list_display = ('title', 'text')


class AdvantageFormAdmin(admin.ModelAdmin):
    model = Advantage
    form = SvgImageForm
    fields = ('icon','title', 'text')


class HelpInline(admin.StackedInline):
    model = Help
    fields = ('question', 'answer')


class HelpFormAdmin(admin.ModelAdmin):
    model = HelpImage
    inlines = (HelpInline,)
    fields = ('image',)


class CallBackFormAdmin(admin.ModelAdmin):
    model = CallBack
    fields = ('name', 'phone_number', 'callback_type', 'contacted', 'date')
    readonly_fields = ('date',)


admin.site.register(AboutUs, AboutUsFormAdmin)
admin.site.register(Advantage, AdvantageFormAdmin)
admin.site.register(Product, ProductFormAdmin)
admin.site.register(Slider)
admin.site.register(CallBack, CallBackFormAdmin)
admin.site.register(News)
admin.site.register(HelpImage, HelpFormAdmin)
admin.site.register(Collection)
admin.site.register(PublicOffer)
admin.site.register(FirstFooter)
admin.site.register(Image)
admin.site.register(SecondFooter)

