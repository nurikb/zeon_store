from django.forms import ModelForm
from django.forms.widgets import TextInput

from store.models import Product, Image


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
