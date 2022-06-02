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


class AboutUsImageInline(admin.StackedInline):
    max_num = 3
    extra = 0
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


class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}">edit</a>'.format(u=url))
        else:
            return ''


class OrderDetailInline(admin.StackedInline):
    model = OrderDetail
    fields = ('product_quantity', 'total_quantity', 'discount_sum', 'discount_price', 'total_price', 'product')


class OrderInline(EditLinkToInlineObject, admin.StackedInline):
    model = Order
    readonly_fields = ('edit_link',)
    extra = 0
    fields = ('product_quantity', 'total_quantity', 'discount_sum', 'discount_price', 'total_price', 'edit_link',)


class ClientFormAdmin(FieldsetsInlineMixin, admin.ModelAdmin):
    # inlines = (OrderInline,)
    # model = Client
    fieldsets_with_inlines = (
        ('Клиент', {'fields': (
                      'name',
                       'surname',
                       'country',
                       'city',
                       'email',
                       'date',
                       'status')}),
        OrderInline,
    )
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
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Client, ClientFormAdmin)

