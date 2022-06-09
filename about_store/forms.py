from django.forms import ModelForm
from django_svg_image_form_field import SvgAndImageFormField

from about_store.models import Advantage


class SvgImageForm(ModelForm):
    class Meta:
        model = Advantage
        exclude = []
        field_classes = {
            'icon': SvgAndImageFormField,
        }
