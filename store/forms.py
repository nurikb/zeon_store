from django.forms import ModelForm
from django.forms.widgets import TextInput
from django_svg_image_form_field import SvgAndImageFormField

from store.models import Product, Image, Advantage


class SvgImageForm(ModelForm):
    class Meta:
        model = Advantage
        exclude = []
        field_classes = {
            'icon': SvgAndImageFormField,
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
                    'color': TextInput(attrs={'type': 'color'}),
                }


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
