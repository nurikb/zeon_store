from django.contrib import admin

from about_store.forms import SvgImageForm
from about_store.models import (Advantage, Help, HelpImage, CallBack, SecondFooter, FirstFooter, AboutUs, AboutUsImage,
                                PublicOffer, Slider, News)


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
admin.site.register(Slider)
admin.site.register(CallBack, CallBackFormAdmin)
admin.site.register(News)
admin.site.register(HelpImage, HelpFormAdmin)
admin.site.register(PublicOffer, PublicOfferFormAdmin)
admin.site.register(FirstFooter, FooterFormAdmin)
