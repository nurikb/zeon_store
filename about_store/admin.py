from functools import update_wrapper

from django.contrib import admin
from django.views.generic import RedirectView

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


class HasAddPermission(admin.ModelAdmin):
    def has_add_permission(self, request):
        """Лимит на создание обьектов модели"""
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True

    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        try:
            id = self.model.objects.all().first().id
        except AttributeError:
            return self.changeform_view(request, None, form_url, extra_context)

        object_id = str(id)
        return self.changeform_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        return [
            path('', wrap(self.change_view), name='%s_%s_changelist' % info),
            path('add/', wrap(self.add_view), name='%s_%s_add' % info),
            path('<path:object_id>/history/', wrap(self.history_view), name='%s_%s_history' % info),
            path('<path:object_id>/delete/', wrap(self.delete_view), name='%s_%s_delete' % info),
            path('<path:object_id>/change/', wrap(self.change_view), name='%s_%s_change' % info),
            # For backwards compatibility (was the change url before 1.9)
            path('<path:object_id>/', wrap(RedirectView.as_view(
                pattern_name='%s:%s_%s_change' % ((self.admin_site.name,) + info)
            ))),
        ]


class HelpFormAdmin(HasAddPermission):
    model = HelpImage
    inlines = (HelpInline,)
    fields = ('image',)


class CallBackFormAdmin(admin.ModelAdmin):
    model = CallBack
    fields = ('name', 'phone_number', 'callback_type', 'contacted', 'date')
    readonly_fields = ('date',)
    list_display = ('name', 'phone_number', 'contacted')
    search_fields = ('name', 'phone_number')
    list_filter = ('contacted',)


class SecondFooterInline(admin.StackedInline):
    model = SecondFooter
    extra = 0


class FooterFormAdmin(HasAddPermission):
    model = FirstFooter
    inlines = (SecondFooterInline,)


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
